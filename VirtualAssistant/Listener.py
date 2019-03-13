import speech_recognition as sr
import time
from Music import Music
from TextEditor import TextEditor
from Browser import Browser
from Calculator import Calculator
from Paint import Paint
from system_commands import SystemCommands
from Play import Play
from Other import Other
import sys

class Listener:

    words      = {}
    music      = {}
    textEditor = {}
    song       = {}
    facebook   = {}
    youtube    = {}
    calculate  = {}
    paint  = {}

    music_handler = Music()
    print "Music handler initialized"
    textEditor_handler = TextEditor()
    print "TextEditor handler initialized"
    calculator_handler = Calculator()
    print "Calculator handler initialized"
    paint_handler = Paint()
    print "Paint handler initialized"
    browser_handler = Browser()
    print "Browser handler initialized"
    system_handler = SystemCommands()
    print "System handler initialized"
    player = Play()
    print "Play handler initialized"
    other_handler = Other()
    print "Other commands handler initialized"

    music["start"] = music_handler.Start_Player_Music
    music["play"] = music_handler.Play_Pause_Music
    music["pause"] = music_handler.Play_Pause_Music
    music["next"] = music_handler.Next_Song_Music
    music["previous"] = music_handler.Prev_Song_Music
    music["stop"] = music_handler.Close_Player_Music

    textEditor["start"] = textEditor_handler.Start_Editor_App
    textEditor["stop"]  = textEditor_handler.Close_Editor_App
    textEditor["edit"]  = textEditor_handler.Write_Document
    textEditor["save"]  = textEditor_handler.Save_Document

    song["next"] = music_handler.Next_Song_Music  
    song["previous"] = music_handler.Prev_Song_Music

    facebook["notifications"] = browser_handler.Facebook_Notifications
    youtube["video"] = browser_handler.Play_Youtube_Video

    words["music"] = music
    words["notepad"] = textEditor
    words["song"] = song
    words["facebook"] = facebook
    words["youtube"] = youtube
    words["date"] = system_handler.getDateAndTime
    words["battery"] = system_handler.batteryLevel
    words["accounts"] = system_handler.computerAccounts
    words["users"] = system_handler.computerAccounts
    words["internet"] = system_handler.checkInternetConnection
    words["email"] = browser_handler.get_number_emails 
    words["weather"] = browser_handler.get_weather_info
    words["sports"] = browser_handler.get_CNN_news_headlines
    words["stop talking"] = other_handler.stop_talking
    words["your iq"] = other_handler.tell_iq
    words["are you"] = other_handler.tell_about_today
    words["best assistant"] = other_handler.thank_you
    words["wikipedia definition"] = other_handler.wikipedia_search

    words["calculate"] = calculate
    words["paint"] = paint
    paint["open"] = paint_handler.Start_Paint_App
    paint["close"] = paint_handler.Close_Paint_App
    calculate["calculate"]  = calculator_handler.Calculate

    def execute(self):

        # time.sleep(2)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.player.respond("ready.mp3")
            audio = r.listen(source)

        try:
            print "Trying to understand command"
            command = r.recognize_google(audio)
            command = command.lower()
            print command
            command_found = False

            if command.find("exit") >= 0 or command.find("eggs") >= 0:
                self.player.respond("thank_you.mp3")
                sys.exit(0)
                #break

            for key in self.words:
                if command.find(key) >= 0:
                    node = self.words[key]
                    
                    while type(node) is dict:
                        node_found = False
                        for sub_key in node:
                            if command.find(sub_key) >= 0:
                                node_found = True
                                node = node[sub_key]
                        if node_found == False:
                            break

                    if callable(node):
                        command_found = True
                        if key != "stop talking":
                            self.player.respond("response_success.mp3")
                        if key == 'wikipedia definition':
                            pos = command.find('for')
                            if pos >= 0:
                                search_term = command[pos + 4:]
                                node(search_term)
                            else:
                                self.player.respond("wikipedia_fail.mp3")
                        else:
                            node()

            if command_found == False:
                self.player.respond("response_not_found.mp3")

        except Exception:
            self.player.respond("response_fail.mp3")
            

