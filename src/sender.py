import socket
import time
import sys
import select
import threading


class Sender:
    def __init__(self, s_ip, s_port, d_ip, d_port):    
        self.d_ip = d_ip
        self.d_port = d_port
        self.s_ip = s_ip
        self.s_port = s_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.bind((self.s_ip, self.s_port))
        self.running = False
        self.recv_package = False

    def start(self):
        self.send_thread = threading.Thread(target=self.send)
        self.recv_thread = threading.Thread(target=self.receive)
        self.running = True
        self.send_thread.start()
        self.recv_thread.start()

    def stop(self):
        self.running = False
        self.send_thread.join()
        self.recv_thread.join()

    def send(self):
        while self.running:
            try:
                self.socket.sendto(b'data', (self.d_ip, self.d_port))
                time.sleep(1)
            except:
                print('Client closed the connection')

    def receive(self):
        while self.running:
            r, _, _ = select.select([self.socket], [], [], 1)
            if r:
                try:
                    data, address = self.socket.recvfrom(1024)
                    print("[SERVER]: S-a receptionat ", str(data), " de la ", address)
                except:
                    print('Client closed the connection')
