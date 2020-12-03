import numpy as np


file = 'text.txt'
data = 0

with open(file, 'r') as stream:
    data = stream.read()


ptr = -1

def next(size):
    global ptr
    ptr += 1
    return bytes(data[ptr*size:(ptr+1)*size], 'utf-8')


class Packet:
    def __init__(self, d_port: int, s_port: int):
        self.d_port = np.astype(d_port, np.uint16)
        self.s_port = np.astype(s_port, np.uint16)
    