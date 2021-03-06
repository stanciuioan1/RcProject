import binascii as bn

class File:
    def __init__(self, path: str):
        with open(path, 'rb') as stream:
            file_name = path.split('/')[-1]
            self.data = bytes(f'{file_name}$FILENAME$', 'latin1') + stream.read()
        self.packets = []
        for i in range((len(self.data) + 7) // 8):
            self.packets.append(Packet(self.data[i*8:(i+1)*8].decode('latin1'), i))

        self.packets.append(Packet('$EOF$', (len(self.data) + 7) // 8 + 1))


def bundle(packets: list):
    return bytes('$PKDATA$'.join([str(x) for x in packets]), 'latin1'), set([x.id for x in packets])


def parse(byte_arr: bytes):
    string = byte_arr.decode('latin1')
    packets = []
    if string:
        packets = [tuple(x.split('$PKID$')) for x in string.split('$PKDATA$')]
        packets = map(lambda x: Packet(str(x[0]), x[1]), packets)
    return list(packets)


class Packet:
    def __init__(self, data: str, id: int):
        self.data = data
        self.id = int(id)

    def __bytes__(self):
        self.bytes = self.data + '$PKID$' + str(self.id)
        return bytes(self.bytes, 'latin1')

    def __str__(self):
        return f'{self.data}$PKID${self.id}'

    def update_data(self, data: str):
        self.data = data