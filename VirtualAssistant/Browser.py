from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from playsound import playsound
from Play import Play
from requests import get
from const import *
import speech_recognition as sr
import urllib2 as urlr
import time
import json

class Browser:

	player = Play()

	def Facebook_Notifications(self):
		options = Options()
		options.add_argument("--disable-notifications")
		options.add_argument("--start-maximized")
		browser = webdriver.Chrome(chrome_options=options)
		browser.get('https://www.facebook.com')
		ok = False
		for i in range(retries):
			try:
				time.sleep(2)
				input_email = browser.find_element_by_id('email')
				input_passwd = browser.find_element_by_id('pass')
				login_btn = browser.find_element_by_id('loginbutton')
				input_email.send_keys(facebook_email)
				input_passwd.send_keys(facebook_passwd)
				login_btn.click()
				ok = True
				break
			except:
				browser.refresh()

		if (ok):
			ok2 = False
			for i in range(num_retries):
				try:
					WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.ID, "fbNotificationsJewel")))
					notification_count = browser.find_element_by_id("notificationsCountValue").get_attribute('innerHTML')
					self.player.play_this(notification_count + " new notification")
					ok2 = True
					break
				except:
					browser.refresh()
			if (ok2):
				time.sleep(2)
			else:
				playsound("browser_inconvenience.mp3")
				browser.close()
		else:
			playsound("browser_inconvenience.mp3")
			browser.close()
		
		browser.close()


	def Play_Youtube_Video(self):
		time.sleep(2)
		r = sr.Recognizer()
		while True:
			try:
				playsound("what_video.mp3")
				with sr.Microphone() as source:
					audio = r.listen(source)
				command = r.recognize_google(audio)
				command = command.lower()
				break
			except:
				#assistant couldn't understand well
				playsound("please_repeat_parameter.mp3")
		try:
			options = Options()
			options.add_argument("--disable-notifications")
			options.add_argument("--start-maximized")
			browser = webdriver.Chrome(chrome_options=options)
			ok = False
			for i in range(retries):
				try:
					browser.get('https://www.youtube.com')
					time.sleep(2)
					input_search = browser.find_element_by_id('search')
					input_search.send_keys(command)
					search = browser.find_element_by_id('search-icon-legacy')
					search.click()
					ok = True
					break
				except:
					pass

			if (ok):
				ok2 = False
				for i in range(retries):
					try:
						time.sleep(1)
						results = browser.find_element_by_id('contents')
						first_result = results.find_element_by_id('dismissable')
						first_result.click()
						ok2 = True
						break
					except:
						browser.refresh()
				if (ok2):
					time.sleep(15)
				else:
					playsound("browser_inconvenience.mp3")
					browser.close()
			else:
				playsound("browser_inconvenience.mp3")
				browser.close()

			browser.close()
		except Exception:
			playsound("response_fail.mp3")

	def get_number_emails(self):
		options = Options()
		options.add_argument("--disable-notifications")
		options.add_argument("--start-maximized")
		browser = webdriver.Chrome(chrome_options=options)
		browser.get('https://www.gmail.com')
		ok = False
		for i in range(retries):
			try:
				WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, "identifierNext")))
				input_email = browser.find_element_by_id('identifierId')
				input_email.send_keys(gmail_email)
				browser.find_element_by_id('identifierNext').click()
				ok = True
				break
			except:
				browser.refresh()

		if (ok):
			time.sleep(1)
			ok2  = False
			for i in range(retries):
				try:
					WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, "passwordNext")))
					input_passwd = browser.find_element_by_name('password')
					input_passwd.send_keys(gmail_passwd)
					browser.find_element_by_id('passwordNext').click()
					ok2 = True
					break
				except:
					browser.refresh()

			if (ok2):
				time.sleep(1)
				ok3 = False
				for i in range(retries):
					try:
						WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, 'gb')))
						time.sleep(2)
						inbox = browser.find_element_by_xpath("//a[contains(@title, 'Inbox')]")
						unread_emails = inbox.get_attribute("aria-label")
						tokens = unread_emails.split()
						msg = "You have " + tokens[1] + " unread emails"
						self.player.play_this(msg)
						ok3 = True
						break
					except:
						browser.refresh()

				if (ok3):
					time.sleep(1)
				else:
					playsound("browser_inconvenience.mp3")
					browser.close()
			else:
				playsound("browser_inconvenience.mp3")
				browser.close()
		else:
			playsound("browser_inconvenience.mp3")
			browser.close()

		browser.close()

	def get_weather_info(self):
		time.sleep(2)
		r = sr.Recognizer()
		while True:
			try:
				playsound("what_city.mp3")
				with sr.Microphone() as source:
					audio = r.listen(source)
				command = r.recognize_google(audio)
				command = command.lower()
				break
			except:
				#assistant couldn't understand well
				playsound("please_repeat_parameter.mp3")
		try:
			#print command
			url = weather_url_1 + command + weather_url_2
			json_text = get(url)
			json_data = json.loads(json_text.text)
			temp = int(float(json_data["main"]["temp_min"]) - 273.15)
			pressure = int(json_data["main"]["pressure"])
			humidity = int(json_data["main"]["humidity"])
			s = "Temperature: " + str(temp) + " degrees Celsius\nPressure: "
			s += str(pressure * 100) + " Pascals\nHumidity: " 
			s += str(humidity) + "%"
			self.player.play_this(s)
		except Exception:
			playsound("response_fail.mp3")

	def get_CNN_news_headlines(self):
		raw = urlr.urlopen(news_BBCSport_url)
		json_text = raw.read()
		data = json.loads(json_text.decode())
		self.player.play_this("The main headlines for today are:")
		for i in range(0, 3):
			self.player.play_this(data['articles'][i]['title'])

