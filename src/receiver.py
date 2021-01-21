import socket
import time
import sys
import select
import threading
import random
import packet


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
        self.file_data = []

        self.drop_packets = False
        self.probability = 20

    def start(self):
        self.last_pack = 0
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

    def update_probability(self, value):
        self.probability = value

    def send_ack(self):
        while self.running:
            if self.recv_packet:
                recv_packets = packet.parse(self.data)
                ack_packets = []
                for pack in recv_packets:
                    if self.drop_packets and random.randint(0, 100) < self.probability:
                        continue
                    else:
                        ack_packets.append(packet.Packet('ACK', pack.id))
                        self.last_pack = time.time()
                        self.file_data.append(pack)

                byte_array, _ = packet.bundle(ack_packets)
                self.socket.sendto(byte_array, (self.d_ip, self.d_port))
                self.recv_packet = False
            elif time.time() - self.last_pack > 10 and self.last_pack > 0:
                self.running = False
                self.write_data()
            time.sleep(0.1)

    def write_data(self):
        print('Writing data')
        self.file_data.sort(key=lambda x: x.id)
        binary_data = ''
        for data in self.file_data:
            binary_data += data.data
        print(binary_data)
        file_name, binary_data = binary_data.split('$FILENAME$')

        with open(file_name, 'wb') as file:
            file.write(bytes(binary_data, 'latin1'))
        print('Done writing data')

    def receive(self):
        while self.running:
            r, _, _ = select.select([self.socket], [], [], 1)
            if r:
                self.data, address = self.socket.recvfrom(65536 * 1024)
                # print("[CLIENT]: S-a receptionat ", str(self.data), " de la ", address)
                self.recv_packet = True
            time.sleep(0.1)
