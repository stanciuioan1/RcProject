import numpy as np
import matplotlib.pyplot as plt

# plt.axis([x[0], x[-1], -1, 1])      # disable autoscaling
cnt = 0

def plot_point(x, y):
    global cnt
    cnt += 1
    if cnt == 2:
        plt.plot(x, y, '.-', color='b')
        plt.draw()
        # plt.pause(1)
        cnt = 0
# plt.clf()                           # clear the current figure