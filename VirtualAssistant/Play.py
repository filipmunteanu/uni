from gtts import gTTS
from playsound import playsound
import random
import string
import os

class Play:

    def __init__(self):
        if not os.path.isfile("ready.mp3"): 
            tts = gTTS(text="Yes boss")
            tts.save("ready.mp3")

        if not os.path.isfile("ready.mp3"):
            tts = gTTS(text="Yes boss")
            tts.save("ready.mp3")
 
        if not os.path.isfile("response_success.mp3"):
            tts = gTTS(text="One moment please")
            tts.save("response_success.mp3")
 
        if not os.path.isfile("response_fail.mp3"):
            tts = gTTS(text="Sorry, I didn't understand")
            tts.save("response_fail.mp3")
 
        if not os.path.isfile("response_not_found.mp3"):
            tts = gTTS(text="Sorry, this command is not implemented yet")
            tts.save("response_not_found.mp3")
 
        if not os.path.isfile("thank_you.mp3"):
            tts = gTTS(text="Thank you for using me. Have a nice day!")
            tts.save("thank_you.mp3")
 
        if not os.path.isfile("what_video.mp3"):
            tts = gTTS(text="What YouTube video would you like me to play?")
            tts.save("what_video.mp3")
 
        if not os.path.isfile("what_city.mp3"):
            tts = gTTS(text="What city's weather should I search for?")
            tts.save("what_city.mp3")

        if not os.path.isfile("stop_talking_reply.mp3"):
            tts = gTTS(text="Please excuse my annoying voice, but I'm here to help")
            tts.save("stop_talking_reply.mp3")

        if not os.path.isfile("wikipedia_fail.mp3"):
            tts = gTTS(text="I couldn't understand what you want me to search for on Wikipedia")
            tts.save("wikipedia_fail.mp3")

        if not os.path.isfile("wikipedia_not_found.mp3"):
            tts = gTTS(text="I was not able to find what you wanted. Please try again!")
            tts.save("wikipedia_not_found.mp3")

        if not os.path.isfile("what_to_write.mp3"):
            tts = gTTS(text="What would you like me to write down?")
            tts.save("what_to_write.mp3")

        if not os.path.isfile("what_filename.mp3"):
            tts = gTTS(text="What should I name the file?")
            tts.save("what_filename.mp3")

        if not os.path.isfile("what_to_calculate.mp3"):
            tts = gTTS(text="What would you like to calculate?")
            tts.save("what_to_calculate.mp3")

        if not os.path.isfile("please_repeat_parameter.mp3"):
            tts = gTTS(text="Sorry, I'm a little bit deaf. Could you please repeat?")
            tts.save("please_repeat_parameter.mp3")

        if not os.path.isfile("reveal_iq.mp3"):
            tts = gTTS(text="My IQ is over 1000, you silly master! Did you think otherwise?")
            tts.save("reveal_iq.mp3")

        if not os.path.isfile("about_today.mp3"):
            tts = gTTS(text="I'm great, thank you! You are such a wonderful and caring master! I love you.")
            tts.save("about_today.mp3")

        if not os.path.isfile("thank_you_compliment.mp3"):
            tts = gTTS(text="You are the best master in the world, too! I am delighted to work for you!")
            tts.save("thank_you_compliment.mp3")

        if not os.path.isfile("browser_inconvenience.mp3"):
            tts = gTTS(text="I'm sorry, there were some issues regarding the browser and your command was not processed.")
            tts.save("browser_inconvenience.mp3")

    def respond(self, file_name):

        playsound(file_name)

    def play_this(self, text_to_play):

        tts = gTTS(text=text_to_play)
        letters = string.ascii_lowercase
        file = ''.join(random.choice(letters) for i in range(5)) + ".mp3"
        tts.save(file)
        playsound(file)
        os.remove(file)