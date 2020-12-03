import socket
import time
import sys
import select
import threading
import random


class Receiver:
    def __init__(self, s_ip, s_port, d_ip, d_port):
        self.d_ip = d_ip
        self.d_port = d_port
        self.s_ip = s_ip
        self.s_port = s_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.bind((self.s_ip, self.s_port))
        self.running = False
        self.recv_packet = False
        self.data = b''

        self.drop_packets = False

    def start(self):
        self.send_thread = threading.Thread(target=self.send_ack)
        self.recv_thread = threading.Thread(target=self.receive)
        self.running = True
        self.send_thread.start()
        self.recv_thread.start()

    def stop(self):
        self.running = False
        self.send_thread.join()
        self.recv_thread.join()

    def is_congested(self, value):
        self.drop_packets = value

    def send_ack(self):
        while self.running:
            if self.recv_packet and self.drop_packets and random.randint(0, 100) < 50:
                self.recv_packet = False
            elif self.recv_packet:
                self.socket.sendto(bytes(f'{self.data.decode()}[ACK]', 'utf-8'), (self.d_ip, self.d_port))
                self.recv_packet = False

    def receive(self):
        while self.running:
            r, _, _ = select.select([self.socket], [], [], 1)
            if r:
                self.data, address = self.socket.recvfrom(1024)
                print("[CLIENT]: S-a receptionat ", str(self.data), " de la ", address)
                self.recv_packet = True
