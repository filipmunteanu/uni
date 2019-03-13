from subprocess import check_output
from Play import Play
import time

class SystemCommands:

	player = Play()

	def getDateAndTime(self):
		self.player.play_this("The current date and time is: " + time.strftime("%c")[:-3])

	def batteryLevel(self):
		output = check_output("WMIC Path Win32_Battery Get EstimatedChargeRemaining", shell=True)
		percentage = [int(s) for s in output.split() if s.isdigit()][0]
		self.player.play_this("Your battery percentage level is at " + str(percentage) + " percent")

	def checkInternetConnection(self):
		output = check_output("ping 8.8.8.8", shell=True)
		if output.find("TTL") > 0:
			out = check_output("ipconfig")
			out = out.split("\r")
			out = [expr for expr in out if 'IPv4' in expr]
			ip = out[0].split(":")[1].strip(" ")
			self.player.play_this("You are connected to the Internet and your IP is: " + ip)
		elif output.find("Destination host unreachable"):
			self.player.play_this("You are connected to the Internet")
		else:
			self.player.play_this("I cannot establish if you are connected to the internet or not")

	def computerAccounts(self):
		output = check_output("WMIC useraccount list brief /Format:List")

		output =  output.split("\r")
		names = [expr.split("=")[1] for expr in output if 'Name' in expr and 'FullName' not in expr]
		text = "The accounts on the current system are: "
		for name in names:
			text += name
			text += ","
		self.player.play_this(text)