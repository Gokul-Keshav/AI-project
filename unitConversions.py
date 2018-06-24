import os.path
import sys
import json
import pyglet
from gtts import gTTS
from pint import UnitRegistry 
from pprint import PrettyPrinter
import speech_recognition as sr

p = PrettyPrinter(indent=4)
ureg = UnitRegistry()
Q = ureg.Quantity

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = 'c118e7572df94b9da10d399f29c4ee36' #the integrated one

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    speech = r.recognize_google(audio)
    
print("You said :"+ speech)



def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = speech
    response = request.getresponse()

    answer = json.loads(response.read())["result"]["contexts"][0]["parameters"]
    number = float(answer["amount"])
    '''
    p.pprint(answer)
    print(type(number))
    print(type(answer["amount"]))
    print(answer["unit-from.original"])
    print(answer["unit-to.original"])
    '''
    #a = Q(10,'kilogram')
    #print(a.to('lb'))

    a = Q(number,answer["unit-from.original"])
    result = a.to(answer["unit-to.original"])
    print(result)


    tts = gTTS(text=str(result), lang="en")
    tts.save("hello.mp3")
    ppath = os.path.abspath("hello.mp3")
    music = pyglet.resource.media("hello.mp3")
    music.play()
    pyglet.app.run()
    os.remove("hello.mp3") #remove temperory file





if __name__ == '__main__':
    main()
