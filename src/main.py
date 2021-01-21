from tkinter import filedialog
from tkinter import *
import sender
import receiver
import configparser


cfgParser = configparser.RawConfigParser()
cfgParser.read('com.cfg')

s_ip = cfgParser.get('com-cfg', 's_ip')
s_port = int(cfgParser.get('com-cfg', 's_port'))
d_ip = cfgParser.get('com-cfg', 'd_ip')
d_port = int(cfgParser.get('com-cfg', 'd_port'))

input_path = "a"

class UIObjects:
	def updateObj(self):
		pass

	def onStart(self):
		pass

	def onStop(self):
		pass

	def startCongestion(self):
		pass

	def stopCongestion(self):
		pass


	def file_opener(self):
		input_path = filedialog.askopenfile(initialdir="D")
		input_path = input_path.name
		print(input_path)
	


	def __init__(self):

		
		self.principal = Tk()

		self.startButton = Button(self.principal, text="Start connection", command=self.onStart, padx=40, pady=20, fg="blue", bg="white")
		self.stopButton = Button(self.principal, text="Stop connection", command=self.onStop, padx=40, pady=20, fg="blue", bg="white")
		self.congestionButton = Button(self.principal, text="Pierde pachete", command=self.startCongestion, padx=100, pady=10, fg="blue", bg="white")
		self.sendButton = Button(self.principal, text="Stop pierdere pachete", command=self.stopCongestion, padx=100, pady=10, fg="blue", bg="white")
		self.server = Label(self.principal, text="Server")
		self.client = Label(self.principal, text="Client")
		self.rasfoire = Button(self.principal, text="Alege fisier", command=self.file_opener, padx=100, pady=10, fg="blue", bg="white")
		#self.messageToSend = Entry(self.principal, width=30, borderwidth=3)
		#self.messageToReceive = Entry(self.principal, width=30, borderwidth=3)
		self.SliderProbability = Scale(self.principal, from_ = 0, to = 100, orient = HORIZONTAL)
		self.SliderPortSource = Scale(self.principal, from_ = 5000, to = 5010, orient = HORIZONTAL)
		self.SliderPortDest = Scale(self.principal, from_ = 5000, to = 5010, orient = HORIZONTAL)
		self.updateProbabilityButton = Button(self.principal, text="Seteaza probabilitate", command=self.updateProbabilitate, padx=100, pady=10, fg="blue", bg="white")
		self.updatePortButton = Button(self.principal, text="Seteaza Port", command=self.setPort, padx=100, pady=10, fg="blue", bg="white")
		self.PortSource = Label(self.principal, text="Port sursa")
		self.PortDest = Label(self.principal, text="Port destinatie")

		self.startButton.grid(row=1, column=0)
		self.stopButton.grid(row=1, column=2)
		self.server.grid(row=0, column=0)
		self.client.grid(row=0, column=2)
		#self.messageToSend.grid(row=2, column=0)
		#self.messageToReceive.grid(row=2, column=2)
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


		self.port_is_set = 0

	def updateProbabilitate(self):
		
		self.receiver.update_probability(self.SliderProbability.get())
		print(self.SliderProbability.get())

	def setPort(self):
		if self.port_is_set == 0:
			port_source = self.SliderPortSource.get()
			port_dest = self.SliderPortDest.get()
			self.sender = sender.Sender(s_ip, port_source, d_ip, port_dest)
			self.receiver = receiver.Receiver(d_ip, port_dest, s_ip, port_source, input_path)
			self.port_is_set = 1

	def startInterface(self):
		self.principal.mainloop()
		self.sender.stop()
		self.receiver.stop()

	def onStart(self):
		print("onStart")
		self.sender.start()
		self.receiver.start()

	def onStop(self):
		print("stop")
		self.receiver.stop()
		self.sender.stop()

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


main()