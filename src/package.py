import numpy as np


class Package:
    def __init__(self, d_port: int, s_port: int, message: str):
        self.d_port = np.astype(d_port, np.uint16)
        self.s_port = np.astype(s_port, np.uint16)
        