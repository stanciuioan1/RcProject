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
        self.beta = beta
        self.last = 0

        self.low_window = 2
        self.min_win = 128
        self.max_win = 512
        self.prev_max = 0
        self.target_win = 256
        self.is_BITCP_ss = False
        self.ss_cwnd = 0
        self.ss_target = 0

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

            # st.plot_point(self.last, self.cwnd)
            self.last += 1

        # if packets_dropped:
        #     if self.cwnd < self.w_max:
        #         self.w_max = self.cwnd * (2 - self.beta) / 2
        #     else:
        #         self.w_max = self.cwnd
        #     self.cwnd = self.cwnd * (1 - self.beta)
        # else:
        #     bic_inc = 0
        #     if self.cwnd < self.w_max:
        #         bic_inc = (self.w_max - self.cwnd) / 2
        #     else:
        #         self.cwnd += self.s_max / self.cwnd
        #         self.last += 1
        #         return
        
        #     if bic_inc > self.s_max:
        #         bic_inc = self.s_max 
        #     elif bic_inc < self.s_min:
        #         bic_inc = self.s_min

        #     self.cwnd = max(1, self.cwnd + bic_inc)

        #     # st.plot_point(self.last, self.cwnd)
        #     self.last += 1

        # if packets_dropped:
        #     if self.low_window <= self.cwnd:
        #         self.prev_max = self.max_win
        #         self.max_win = self.cwnd
        #         self.cwnd = self.cwnd * (1 - self.beta)
        #         self.min_win = self.cwnd
        #         if self.prev_max > self.max_win:
        #             self.max_win = (self.max_win + self.min_win) / 2
        #         self.target_win = (self.max_win + self.min_win) / 2
        #     else:
        #         self.cwnd = self.cwnd * 0.5
        # else:
        #     if self.low_window > self.cwnd:
        #         self.cwnd += 1 / self.cwnd
        #     if self.is_BITCP_ss is False:
        #         if self.target_win - self.cwnd < self.s_max:
        #             self.cwnd = (self.target_win - self.cwnd) / self.cwnd
        #         else:
        #             self.cwnd += self.s_max / self.cwnd
                
        #         if self.max_win > self.cwnd:
        #             self.min_win = self.cwnd
        #             self.target_win = (self.max_win + self.min_win) / 2
        #         else:
        #             self.is_BITCP_ss = True
        #             self.ss_cwnd = 1
        #             self.ss_target = self.cwnd + 1
        #             self.max_win = self.w_max
        #     else:
        #         self.cwnd += self.ss_cwnd / self.cwnd
        #         if self.cwnd >= self.ss_target:
        #             self.ss_cwnd = 2 * self.ss_cwnd
        #             self.ss_target += self.ss_cwnd

        #     if self.ss_cwnd >= self.s_max:
        #         self.is_BITCP_ss = False

        self.last += 1

        if self.is_BITCP_ss:
            return self.ss_cwnd
        else:
            return self.cwnd

    def get_cwnd(self):
        return self.cwnd

    def __str__(self):
        return f'Current window size: {self.cwnd}\nMax window size: {self.w_max}'
