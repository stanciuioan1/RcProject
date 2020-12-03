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

def onStart():
	print("onStart")
	sender.start()
	receiver.start()

def onStop():
	print("stop")
	receiver.stop()
	sender.stop()

def onCongestion():
	receiver.is_congested(True)
	print("congestion")

def sendData():
	print("send data")



class UIObjects:

	def __init__(self):
		self.principal = Tk()

		self.startButton = Button(self.principal, text="Start connection", command=onStart, padx=40, pady=20, fg="blue", bg="white")
		self.stopButton = Button(self.principal, text="Stop connection", command=onStop, padx=40, pady=20, fg="blue", bg="white")
		self.congestionButton = Button(self.principal, text="Pierde pachete", command=onCongestion, padx=50, pady=10, fg="blue", bg="white")
		self.sendButton = Button(self.principal, text="Trimite text", command=sendData, padx=50, pady=10, fg="blue", bg="white")
		self.server = Label(self.principal, text="Server")
		self.client = Label(self.principal, text="Client")
		self.messageToSend = Entry(self.principal, width=30, borderwidth=3)
		self.messageToReceive = Entry(self.principal, width=30, borderwidth=3)
	
		self.startButton.grid(row=0, column=0)
		self.stopButton.grid(row=0, column=1)
		self.server.grid(row=1, column=0)
		self.client.grid(row=1, column=1)
		self.messageToSend.grid(row=2, column=0)
		self.messageToReceive.grid(row=2, column=1)
		self.sendButton.grid(row=3, column=0)
		self.congestionButton.grid(row=3, column=1)


	def startInterface(self):
		self.principal.mainloop()
		sender.stop()
		receiver.stop()


def main():
	window = UIObjects()
	window.startInterface()	


main()