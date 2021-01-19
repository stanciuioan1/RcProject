import numpy as np


file = 'text.txt'
data = 0

with open(file, 'r') as stream:
    data = stream.read()


ptr = -1

def next(size: int, amount: int):
    global ptr
    packets = []
    packet_ids = set()
    while amount:
        ptr += 1
        packet_ids.add(ptr)
        packets.append(Packet(data[ptr*size:(ptr+1)*size], ptr))
        amount -= 1

    return packets, packet_ids


def bundle(packets: list):
    return bytes('#'.join([str(x) for x in packets]), 'utf-8')


def parse(byte_arr: bytes):
    string = byte_arr.decode('utf-8')
    packets = [tuple(x.split('*')) for x in string.split('#')]
    packets = map(lambda x: Packet(x[0], x[1]), packets)
    return packets


def decode(byte_arr: bytes):
    string = byte_arr.decode('utf-8')
    data, p_id = string.split('*')
    return Packet(data, p_id)


class Packet:
    def __init__(self, data: str, id: int):
        self.data = data
        self.id = int(id)

    def __bytes__(self):
        self.bytes = self.data + '*' + str(self.id)
        return bytes(self.bytes, 'utf-8')

    def __str__(self):
        return f'{self.data}*{self.id}'

    def update_data(self, data: str):
        self.data = data
    
    def get_id(self):
        return self.id