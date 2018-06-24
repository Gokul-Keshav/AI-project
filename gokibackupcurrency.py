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
def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = speech
    response = request.getresponse()
    c = CurrencyConverter()
    answer = json.loads(response.read())["result"]["parameters"]#["currency-to"]["fulfillment"]["speech"]
    #print(answer["amount"])
    currency = c.convert(answer["amount"],answer["currency-from"],answer["currency-to"],date=datetime(2018,2, 16))
    print(currency)
    tts = gTTS(text=str(currency) + answer["currency-to"], lang="en")
    tts.save("hello.mp3")
    ppath = os.path.abspath("hello.mp3")
    #print(ppath)
    #call(["xdg-open", ppath])
    
    print(answer["currency-to"])
    
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

if __name__ == '__main__':
    main()
