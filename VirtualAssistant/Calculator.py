from pywinauto import Desktop, Application
import time
import speech_recognition as sr
from playsound import playsound

class Calculator:
	def __init__(self):
		self.instances = []

	def Calculate(self):
		app = Application(backend="uia").start('calc.exe')

		dlg = Desktop(backend="uia").Calculator

		r = sr.Recognizer()
		while True:
			try:
				playsound("what_to_calculate.mp3")
				with sr.Microphone() as source:
					audio = r.listen(source)
				text = r.recognize_google(audio)
				break
			except:
				#assistant couldn't understand well
				playsound("please_repeat_parameter.mp3")
		print text
		text = text.replace(" ", "")
		text = text.replace("x", "*")
		print text
		dlg.type_keys(text+'=')
		time.sleep(3)
		app = Application().Connect(title = 'Calculator')
		app.Kill_()

	# Example "gittwo multiplied by four"