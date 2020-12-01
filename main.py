from tkinter import *

def onStart():
	print("onStart")

def onStop():
	print("stop")

def onCongestion():
	print("cong")

def sendData():
	print("send data")



class UIObjects:

	def __init__(self):
		self.principal = Tk()

		self.startButton = Button(self.principal, text="Start connection", command=onStart, padx=40, pady=20, fg="blue", bg="white")
		self.stopButton = Button(self.principal, text="Stop connection", command=onStop, padx=40, pady=20, fg="blue", bg="white")
		self.congestionButton = Button(self.principal, text="Pierde pachete", command=onCongestion, padx=50, pady=10, fg="blue", bg="white")
		self.sendButton = Button(self.principal, text="Trimite text", command=sendData, padx=50, pady=10, fg="blue", bg="white")
		self.text1 = Label(self.principal, text="Mesaj trimis")
		self.text2 = Label(self.principal, text="Mesaj primit")
		self.messageToSend = Entry(self.principal, width=30, borderwidth=3)
		self.messageToReceive = Entry(self.principal, width=30, borderwidth=3)
	
		self.startButton.grid(row=0, column=0)
		self.stopButton.grid(row=0, column=1)
		self.text1.grid(row=1, column=0)
		self.text2.grid(row=1, column=1)
		self.messageToSend.grid(row=2, column=0)
		self.messageToReceive.grid(row=2, column=1)
		self.sendButton.grid(row=3, column=0)
		self.congestionButton.grid(row=3, column=1)


	def startInterface(self):
		self.principal.mainloop()

def main():
	window = UIObjects()
	window.startInterface()	


main()