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

sender = sender.Sender(s_ip, s_port, d_ip, d_port)
receiver = receiver.Receiver(d_ip, d_port, s_ip, s_port)



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

	def __init__(self):
		self.principal = Tk()

		self.startButton = Button(self.principal, text="Start connection", command=self.onStart, padx=40, pady=20, fg="blue", bg="white")
		self.stopButton = Button(self.principal, text="Stop connection", command=self.onStop, padx=40, pady=20, fg="blue", bg="white")
		self.congestionButton = Button(self.principal, text="Pierde pachete", command=self.startCongestion, padx=100, pady=10, fg="blue", bg="white")
		self.sendButton = Button(self.principal, text="Stop pierdere pachete", command=self.stopCongestion, padx=100, pady=10, fg="blue", bg="white")
		self.server = Label(self.principal, text="Server")
		self.client = Label(self.principal, text="Client")
		self.messageToSend = Entry(self.principal, width=30, borderwidth=3)
		self.messageToReceive = Entry(self.principal, width=30, borderwidth=3)
		self.SliderProbability = Scale(self.principal, from_ = 0, to = 100, orient = HORIZONTAL)
		self.updateButton = Button(self.principal, text="Seteaza parametri", command=self.updateObj, padx=100, pady=10, fg="blue", bg="white")


		self.startButton.grid(row=0, column=0)
		self.stopButton.grid(row=0, column=2)
		self.server.grid(row=1, column=0)
		self.client.grid(row=1, column=2)
		self.messageToSend.grid(row=2, column=0)
		self.messageToReceive.grid(row=2, column=2)
		self.sendButton.grid(row=3, column=0)
		self.SliderProbability.grid(row=3, column=1)
		self.updateButton.grid(row=2, column=1)
		self.congestionButton.grid(row=3, column=2)


	def updateObj(self):
		receiver.update_probability(self.SliderProbability.get())
		print(self.SliderProbability.get())


	def startInterface(self):
		self.principal.mainloop()
		sender.stop()
		receiver.stop()

	def onStart(self):
		print("onStart")
		sender.start()
		receiver.start()

	def onStop(self):
		print("stop")
		receiver.stop()
		sender.stop()

	def startCongestion(self):
		receiver.is_congested(True)
		print("congestion")

	def stopCongestion(self):
		receiver.is_congested(False)
		print("send data")




def main():
	window = UIObjects()
	window.startInterface()	


main()