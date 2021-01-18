import socket
import time
import sys
import select
import threading
import packet
import bitcp


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

        self.cong_strategy = bitcp.BITCPStrategy(1, 64, 32, 256, 0.6)
        self.ack_set = set()

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
                # extrage cwnd pachete din fisier
                packets, self.packet_ids = packet.next(8, int(self.cong_strategy.cwnd))
                byte_array = packet.bundle(packets)
                self.socket.sendto(byte_array, (self.d_ip, self.d_port))
                time.sleep(1)
            except Exception as e:
                print('Client closed the connection')

    def receive(self):
        while self.running:
            r, _, _ = select.select([self.socket], [], [], 1)
            if r:
                try:
                    data, address = self.socket.recvfrom(1024)
                    print("[SERVER]: S-a receptionat ", str(data), " de la ", address)
                    packets = packet.parse(data)
                    for pack in packets:
                        self.packet_ids.remove(int(pack.get_id()))
                    self.cong_strategy.update_strategy(self.packet_ids)
                    print(self.cong_strategy)
                except:
                    print('Client closed the connection')
