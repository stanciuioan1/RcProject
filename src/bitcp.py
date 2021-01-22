import socket
import time
import sys
import select
import threading
import packet

from matplotlib.lines import Line2D
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation



class BITCPStrategy:
    def __init__(self, cwnd: int, s_max: int, s_min: int, w_max: int, beta: float):
        self.cwnd = cwnd
        self.s_max = s_max
        self.s_min = s_min
        self.w_max = w_max
        self.beta = beta / 100
        self.last = 0


    def update_strategy(self, packets_dropped: bool):
        if packets_dropped:
            if self.cwnd < self.w_max:
                self.w_max = self.cwnd * (2 - self.beta) / 2
            else:
                self.w_max = self.cwnd
            self.cwnd = self.cwnd * (1 - self.beta)
        else:
            bic_inc = 0
            if self.cwnd < self.w_max:
                bic_inc = (self.w_max - self.cwnd) / 2
            else:
                bic_inc = self.cwnd - self.w_max

            if bic_inc > self.s_max:
                bic_inc = self.s_max 
            elif bic_inc < self.s_min:
                bic_inc = self.s_min

            self.cwnd = max(1, self.cwnd + (bic_inc / self.cwnd))

            self.last += 1

    def get_cwnd(self):
        return self.cwnd

    def __str__(self):
        return f'Current window size: {self.cwnd}\nMax window size: {self.w_max}'
