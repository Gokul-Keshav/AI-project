import os.path
from subprocess import call
import sys
import json
import pyglet
from gtts import gTTS
from time import sleep
import pyttsx
from currency_converter import CurrencyConverter
from datetime import datetime
import speech_recognition as sr


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = speech
    response = request.getresponse()
    answer = json.loads(response.read())["result"]["fulfillment"]["speech"]

    print(answer)



    tts = gTTS(text=answer, lang="en")
    tts.save("hello.mp3")
    ppath = os.path.abspath("hello.mp3")
    #print(ppath)
    #call(["xdg-open", ppath])
    
    #print (response.read())
#    engine = pyttsx.init();
#    engine.say(currency)
#    engine.say(answer["currency-to"])
#    engine.runAndWait()

    #speech = gTTS(text='hey how you doing', lang='en', slow=False)
    #speech.save("hello.mp3")

    music = pyglet.resource.media("hello.mp3")
    music.play()
    pyglet.app.run()

    #sleep(music.duration) #prevent from killing
    os.remove("hello.mp3") #remove temperory file

    '''
    #f = TemporaryFile()
    #speech.write_to_fp(f)
    # <do something="" with="" f="">
    #f.close()





    #engine = pyttsx.init()
    #engine.say(answer)
    #engine.runAndWait()
    '''


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
#CLIENT_ACCESS_TOKEN = 'f0959e6d76ae45eeb2d796d317ac4370'
CLIENT_ACCESS_TOKEN = 'c118e7572df94b9da10d399f29c4ee36' #the integrated one

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    speech = r.recognize_google(audio)

print("You said: " + speech)

if __name__ == '__main__':
    main()
