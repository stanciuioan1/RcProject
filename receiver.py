import socket
import time


class Receiver:
    def __init__(self, UDP_IP: str, UDP_PORT: int):
        self.UDP_IP = UDP_IP
        self.UDP_PORT = UDP_PORT

    def connect(self, family, protocol):
        self.sock = socket.socket(family, protocol)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

    def receive(self, chunk_size: int):
        while True:
            data, addr = self.sock.recvfrom(chunk_size)
            print(f'receiver message: {data} from {addr}')
            time.sleep(0.1)


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

receiver = Receiver(UDP_IP, UDP_PORT)
receiver.connect(socket.AF_INET, socket.SOCK_DGRAM)
receiver.receive(1024)