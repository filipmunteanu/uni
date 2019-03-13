from pywinauto.application import Application
import subprocess
import speech_recognition as sr
from playsound import playsound

class Paint:
	def __init__(self):
		self.instances = []

	def Start_Paint_App(self):
		pid = subprocess.Popen(["C:\\Windows\\System32\\mspaint.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		self.instances.append(pid)


	def Close_Paint_App(self):
		if not self.instances:
			return
		pid = self.instances[0]
		self.instances = self.instances[1 : ]
		pid.kill()