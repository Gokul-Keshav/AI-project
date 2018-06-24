import os.path
import sys
import json
import pyttsx
import speech_recognition as sr
engine = pyttsx.init()


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
#CLIENT_ACCESS_TOKEN = 'f0959e6d76ae45eeb2d796d317ac4370' #game
#CLIENT_ACCESS_TOKEN = 'f1515e48e5684c31bbdf03a8bf1676b5' #general chat
CLIENT_ACCESS_TOKEN = '860a215b965e462e8890146f7c435337'
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    speech = r.recognize_google(audio)

    #request.query = speech
    
    request.query = speech

    response = request.getresponse()

    rr = response.read()
    #print(rr)
    answer = json.loads(rr)["result"]["fulfillment"]["speech"]
    print(answer)

    #print (response.read())
    engine.say(answer)
    engine.runAndWait()
    '''
    if(json.loads(rr)["result"]["score"]) == 1.0:
        engine.say(answer)
        engine.runAndWait()
    else:
        reply = "Couldn't process query"
        print(reply)
        engine.say(reply)
        engine.runAndWait()
        '''


if __name__ == '__main__':
    main()