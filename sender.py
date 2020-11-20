import socket


class Sender:
    def __init__(self, UDP_IP: str, UDP_PORT: int):
        self.UDP_IP = UDP_IP
        self.UDP_PORT = UDP_PORT

    def connect(self, family, protocol):
        self.sock = socket.socket(family, protocol)

    def send_message(self, message: str):
        self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sender = Sender(UDP_IP, UDP_PORT)
sender.connect(socket.AF_INET, socket.SOCK_DGRAM)
sender.send_message(b"Hello, World!")