from tkinter import filedialog
from tkinter import *
import sender as snd
import receiver
import configparser
import bitcp
import threading
import time

#import stripchart as st
import matplotlib.pyplot as plt

cfgParser = configparser.RawConfigParser()
cfgParser.read('com.cfg')

s_ip = cfgParser.get('com-cfg', 's_ip')
s_port = int(cfgParser.get('com-cfg', 's_port'))
d_ip = cfgParser.get('com-cfg', 'd_ip')
d_port = int(cfgParser.get('com-cfg', 'd_port'))

input_path = "a"

sender = 0

class UIObjects:
	def updateObj(self):
		pass


	def file_opener(self):
		global sender
		if sender:
			input_path = filedialog.askopenfile(initialdir="D")
			input_path = input_path.name
			sender.set_file_path(input_path)


	def __init__(self):
		self.principal = Tk()

		self.sender = 0
		self.receiver = 0

		self.startButton = Button(self.principal, text="Start connection", command=self.onStart, padx=40, pady=20, fg="blue", bg="white")
		self.stopButton = Button(self.principal, text="Stop connection", command=self.onStop, padx=40, pady=20, fg="blue", bg="white")
		self.congestionButton = Button(self.principal, text="Pierde pachete", command=self.startCongestion, padx=100, pady=10, fg="blue", bg="white")
		self.sendButton = Button(self.principal, text="Stop pierdere pachete", command=self.stopCongestion, padx=100, pady=10, fg="blue", bg="white")
		self.server = Label(self.principal, text="Server")
		self.client = Label(self.principal, text="Client")
		self.rasfoire = Button(self.principal, text="Alege fisier", command=self.file_opener, padx=100, pady=10, fg="blue", bg="white")
		self.SliderProbability = Scale(self.principal, from_ = 0, to = 100, orient = HORIZONTAL)
		self.SliderPortSource = Scale(self.principal, from_ = 5000, to = 5010, orient = HORIZONTAL)
		self.SliderPortDest = Scale(self.principal, from_ = 5000, to = 5010, orient = HORIZONTAL)
		self.updateProbabilityButton = Button(self.principal, text="Seteaza probabilitate", command=self.updateProbabilitate, padx=100, pady=10, fg="blue", bg="white")
		self.updatePortButton = Button(self.principal, text="Seteaza Port", command=self.setPort, padx=100, pady=10, fg="blue", bg="white")
		self.PortSource = Label(self.principal, text="Port sursa")
		self.PortDest = Label(self.principal, text="Port destinatie")
		self.textClient = Text(self.principal, height = 40, width = 50) 
		self.textServer = Text(self.principal, height = 40, width = 50)


		self.startButton.grid(row=1, column=0)
		self.stopButton.grid(row=1, column=2)
		self.server.grid(row=0, column=0)
		self.client.grid(row=0, column=2)
		self.sendButton.grid(row=3, column=0)
		self.SliderProbability.grid(row=3, column=1)
		self.updateProbabilityButton.grid(row=2, column=1)
		self.congestionButton.grid(row=3, column=2)
		self.SliderPortSource.grid(row = 5, column=0)
		self.SliderPortDest.grid(row = 5, column=2)
		self.PortSource.grid(row = 4, column=0)
		self.PortDest.grid(row = 4, column=2)
		self.updatePortButton.grid(row = 5, column=1)
		self.rasfoire.grid(row = 6, column=0)
		self.textClient.grid(row = 7, column=0)
		self.textServer.grid(row = 7, column=2)



		self.port_is_set = 0

	def updateProbabilitate(self):
		self.receiver.update_probability(self.SliderProbability.get())
		print(self.SliderProbability.get())

	def setPort(self):
		global sender
		if self.port_is_set == 0:
			port_source = self.SliderPortSource.get()
			port_dest = self.SliderPortDest.get()
			sender = snd.Sender(s_ip, port_source, d_ip, port_dest, input_path)
			self.receiver = receiver.Receiver(d_ip, port_dest, s_ip, port_source)
			self.port_is_set = 1

	def startInterface(self):
		global sender
		self.principal.mainloop()
		sender.stop()
		self.receiver.stop()

	def onStart(self):
		global sender
		print("onStart")
		sender.start(self.textServer)
		self.receiver.start(self.textClient)

	def onStop(self):
		global sender
		print("stop")
		self.receiver.stop()
		sender.stop()

	def startCongestion(self):
		self.receiver.is_congested(True)
		print("congestion")

	def stopCongestion(self):
		self.receiver.is_congested(False)
		print("send data")


def return_path():
	return input_path


def main():
	window = UIObjects()
	window.startInterface()	

gui_thread = threading.Thread(target=main)
gui_thread.start()

strategy = 0
while not strategy:
	try:
		strategy = sender.cong_strategy
	except:
		print('Strategy not yet initialized')
	time.sleep(0.5)

x = []
y = []
while True:
	plt.ion()
	x.append(strategy.last)
	y.append(strategy.cwnd)
	plt.show(block=False)
	plt.draw()
	plt.plot(x, y, '-', color='blue')
	plt.pause(0.1)
	plt.ioff()
	time.sleep(0.1)