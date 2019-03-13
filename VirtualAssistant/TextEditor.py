from pywinauto.application import Application
import subprocess
import speech_recognition as sr
from playsound import playsound

class TextEditor:
	def __init__(self):
		self.instances = []

	def Start_Editor_App(self):
		pid = subprocess.Popen(["C:\\Windows\\notepad.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		self.instances.append(pid)

	def Write_Document(self):
		app = Application().Connect(title = 'Untitled - Notepad')
		notepadApp = app.notepad
		r = sr.Recognizer()
		while True:
			try:
				playsound("what_to_write.mp3")
				with sr.Microphone() as source:
					audio = r.listen(source)
				text = r.recognize_google(audio)
				break
			except:
				#assistant couldn't understand well
				playsound("please_repeat_parameter.mp3")
		notepadApp.TypeKeys(text)

	def Save_Document(self):
		app = Application().Connect(title = 'Untitled - Notepad')
		notepadApp = app.notepad
		r = sr.Recognizer()
		while True:
			try:
				playsound("what_filename.mp3")
				with sr.Microphone() as source:
					audio = r.listen(source)
				filename = r.recognize_google(audio)
				break
			except:
				#assistant couldn't understand well
				playsound("please_repeat_parameter.mp3")
		filename += ".txt"
		notepadApp.MenuSelect("File -> SaveAs")
		app.SaveAs.edit1.SetText(filename)
		app.SaveAs.Save.Click()
		app.SaveAs.Save.Click()

	def Close_Editor_App(self):
		if not self.instances:
			return
		pid = self.instances[0]
		self.instances = self.instances[1 : ]
		pid.kill()