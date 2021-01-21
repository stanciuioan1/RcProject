import socket
import time
import sys
import select
import threading
import packet


class BITCPStrategy:
    def __init__(self, cwnd: int, s_max: int, s_min: int, w_max: int, beta: float):
        self.cwnd = cwnd
        self.s_max = s_max
        self.s_min = s_min
        self.w_max = w_max
        self.beta = beta

    def update_strategy(self, packets_dropped: bool):
        if packets_dropped:
            if self.cwnd < self.w_max:          # fast convergence
                self.w_max = self.cwnd * (2 - self.beta) / 2
            else:
                self.w_max = self.cwnd
            self.cwnd = self.cwnd * (1 - self.beta)
            
            print('DECREASE')
        else:
            bic_inc = 0
            if self.cwnd < self.w_max:          # binary search
                bic_inc = (self.w_max - self.cwnd) / 2
            else:
                bic_inc = self.cwnd - self.w_max

            if bic_inc > self.s_max:
                bic_inc = self.s_max 
            elif bic_inc < self.s_min:
                bic_inc = self.s_min
            self.cwnd = self.cwnd + (bic_inc / self.cwnd)
            print('INCREASE')

    def get_cwnd(self):
        return self.cwnd

    def __str__(self):
        return f'Current window size: {self.cwnd}\nMax window size: {self.w_max}'