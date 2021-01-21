import socket
import time
import sys
import select
import threading
import packet
import bitcp
from tkinter import *

class Sender:
    def __init__(self, s_ip, s_port, d_ip, d_port, file_path):    
        self.d_ip = d_ip
        self.d_port = d_port
        self.s_ip = s_ip
        self.s_port = s_port
        self.file_path = file_path

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.bind((self.s_ip, self.s_port))
        self.running = False
        self.recv_package = False
        self.packet_queue = []
        self.input = input
        self.text_in_box = ""

    def start(self, textbox):
        self.cong_strategy = bitcp.BITCPStrategy(8, 1024, 512, 4096, 0.6)
        tr_file = packet.File(self.file_path)
        self.packets = tr_file.packets
        self.packet_ptr = 0
        self.last_packet_flag = False
        self.send_thread = threading.Thread(target=self.send)
        self.recv_thread = threading.Thread(target=self.receive, args = (textbox,))
        self.running = True
        self.send_thread.start()
        self.recv_thread.start()

    def stop(self):
        self.running = False
        self.send_thread.join()
        self.recv_thread.join()

    def set_file_path(self, path):
        self.file_path = path

    def send(self):
        while self.running:
            try:
                while self.last_packet_flag is False and len(self.packet_queue) < int(self.cong_strategy.cwnd):
                    if self.packets[self.packet_ptr].data == '$EOF$':
                        self.last_packet_flag = True
                    else:
                        self.packet_queue.append(self.packets[self.packet_ptr])
                        self.packet_ptr += 1

                if self.packet_queue:
                    byte_array, self.packet_ids = packet.bundle(self.packet_queue)
                    self.packet_queue.clear()
                    # print(byte_array)
                    self.socket.sendto(byte_array, (self.d_ip, self.d_port))
                elif self.last_packet_flag:
                    self.running = False
                time.sleep(1)
            except Exception as e:
                print(e.with_traceback())

    def receive(self, textbox):
        while self.running:
            r, _, _ = select.select([self.socket], [], [], 1)
            if r:
                try:
                    data, address = self.socket.recvfrom(65536 * 1024)
                    packets = packet.parse(data)
                    self.text_in_box = f'S-au receptionat {len(packets)} pachete de la client\n'
                    textbox.insert(END, self.text_in_box) 
                    for pack in packets:
                        self.packet_ids.remove(int(pack.id))
                    self.cong_strategy.update_strategy(self.packet_ids)

                    if self.packet_ids:
                        self.text_in_box = f'Lipsesc {len(self.packet_ids)} pachete!\n'
                        textbox.insert(END, self.text_in_box)
                    textbox.see('end')
                    for i in self.packet_ids:
                        self.packet_queue.append(self.packets[i])
                except Exception as e:
                    print(e.with_traceback())
            time.sleep(0.1)
