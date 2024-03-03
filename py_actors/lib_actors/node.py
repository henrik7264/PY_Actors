import time
import socket
import pickle
from threading import Thread, Lock
from lib_actors.actor import Actor


def _send_str(sock: socket.socket, v: str):
    s = '#' + str(len(v)) + ':' + v
    sock.sendall(s.encode())


def _send_int(sock: socket.socket, v: int):
    _send_str(sock, str(v))


def _send_msg(sock: socket.socket, msg):
    pickled = pickle.dumps(msg)
    pickled_size = len(pickled)
    pickled_header = "#" + str(pickled_size) + ":"
    sock.sendall(pickled_header.encode())
    sock.sendall(pickled)


def _recv_bytes(sock: socket.socket):
    s: str = ''
    c: str = ''
    while c != ':' or s == '':  # look for string with format '#<digits>:'
        while c != '#':  # find start of string
            c = sock.recv(1).decode()
        c = sock.recv(1).decode()
        s = ''
        while c.isdigit():  # read digits
            s += c
            c = sock.recv(1).decode()
    expt_size: int = int(s)
    recv_size: int = 0
    chunks: [bytes] = []
    while recv_size < expt_size:
        chunk: bytes = sock.recv(min(expt_size - recv_size, 2048))
        if chunk is None:
            raise socket.error()
        chunks.append(chunk)
        recv_size += len(chunk)
    return bytes().join(chunks)


def _recv_str(sock: socket.socket) -> str:
    return _recv_bytes(sock).decode()


def _recv_int(sock: socket.socket) -> int:
    return int(_recv_bytes(sock).decode())


def _recv_msg(sock: socket.socket) -> bytes:
    return pickle.loads(_recv_bytes(sock))


class PeerNode(Thread):
    def __init__(self, node, sock, name: str, addr: str, port: int, send_msgs, recv_msgs):
        super().__init__(daemon=True)
        self.node = node
        self.sock = sock
        self.do_reconnect = (sock is None)
        self.is_connected = (sock is not None)
        self.name = name
        self.addr = addr
        self.port = port
        self.send_msgs = send_msgs
        self.recv_msgs = recv_msgs
        self.subs = []
        for msg_type in send_msgs:
            self.subs.append((self.node.message.subscribe(self.send_to_peer, msg_type), msg_type))
        self.start()

    def send_to_peer(self, msg):
        try:
            if self.is_connected:
                _send_msg(self.sock, msg)
        except socket.error:
            self.sock.close()
            self.is_connected = False

    def run(self):
        do_loop = True
        while do_loop:
            try:
                if not self.is_connected:
                    if self.do_reconnect:
                        self.reconnect()
                    else:
                        for sub, msg_type in self.subs:
                            self.node.message.unsubscribe(sub, msg_type)
                        do_loop = False
                else:
                    msg = _recv_msg(self.sock)
                    if type(msg) in self.recv_msgs:
                        self.node.message.publish(msg)
            except pickle.UnpicklingError as err:
                print(f"Pickle error: {err}.")
            except socket.error:
                self.node.conns.pop(self.name)
                self.sock.close()
                self.is_connected = False

    def reconnect(self):
        while not self.is_connected:
            while self.name in self.node.conns:
                time.sleep(5.0)

            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.addr, self.port))
                _send_str(self.sock, "PY_Actors")
                _send_str(self.sock, "v1.0.0")
                _send_str(self.sock, self.node.name)
                _send_str(self.sock, self.node.addr)
                _send_int(self.sock, self.node.port)
                with self.node.lock:
                    if self.name in self.node.conns:
                        self.sock.close()
                    else:
                        self.node.conns[self.name] = self
                        self.is_connected = True
            except socket.error:
                self.sock.close()
                time.sleep(1.0)


class Node(Thread, Actor):
    def __init__(self, name: str, addr: str, port: int, send_msgs=None, recv_msgs=None):
        assert send_msgs is not None or recv_msgs is not None
        Thread.__init__(self, daemon=True)
        Actor.__init__(self, name=name)
        self.node = self
        self.name = name
        self.addr = addr
        if self.addr == 'localhost':
            self.addr = '127.0.0.1'
        self.port = port
        self.send_msgs = send_msgs
        if self.send_msgs is None:
            self.send_msgs = []
        self.recv_msgs = recv_msgs
        if self.recv_msgs is None:
            self.recv_msgs = []
        self.peers: {PeerNode} = {}
        self.conns: {PeerNode} = {}
        self.lock = Lock()
        self.start()

    def run(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.addr, self.port))
        server_sock.listen(8)
        while True:
            client_sock, client_addr = server_sock.accept()
            with self.lock:
                assert _recv_str(client_sock) == "PY_Actors"
                assert _recv_str(client_sock) == "v1.0.0"
                name = _recv_str(client_sock)
                addr = _recv_str(client_sock)
                port = _recv_int(client_sock)
                if name in self.conns:
                    client_sock.close()
                else:
                    self.conns[name] = PeerNode(self, client_sock, name, addr, port, self.send_msgs, self.recv_msgs)

    def add_peer(self, name: str, addr: str, port: int):
        if addr == 'localhost':
            addr = '127.0.0.1'
        self.peers[name] = PeerNode(self, None, name, addr, port, self.send_msgs, self.recv_msgs)
