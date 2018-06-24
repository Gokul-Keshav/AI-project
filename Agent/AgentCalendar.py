from __future__ import print_function
import os.path
import sys
import json
import pyttsx
import speech_recognition as sr
import pyglet
import httplib2
import os
from gtts import gTTS
from pprint import PrettyPrinter
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.contrib import gce

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API'

def get_credentials():
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'cal-credential.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


p = PrettyPrinter(indent=4)

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something")
    audio = r.listen(source)
    speech = r.recognize_google(audio)


#speech = "remind me for a movie this sunday at 6pm"
print("You said: "+ speech)

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
#CLIENT_ACCESS_TOKEN = 'f0959e6d76ae45eeb2d796d317ac4370'
CLIENT_ACCESS_TOKEN = 'c118e7572df94b9da10d399f29c4ee36' #the integrated one


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = speech

    #request.query = speech
    response = request.getresponse()

    answer = json.loads(response.read())["result"]
    daate = answer["parameters"]["date-time"]
    daate = daate[:-1]
    daate = daate + "+05:30"

    p.pprint(daate)
    p.pprint(answer["parameters"]["name"]);
    p.pprint(answer["fulfillment"]["speech"])


    #inserting into calendar
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = {
      'summary':answer["parameters"]["name"] ,
      'location': 'chennai',
      'description': speech,
      'start': {
        'dateTime': daate,
      },
      'end': {
        'dateTime': daate,
      },
      
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }


    event = service.events().insert(calendarId='primary', body=event).execute()


    tts = gTTS(text=str(answer["fulfillment"]["speech"]), lang="en")
    tts.save("hello.mp3")
    ppath = os.path.abspath("hello.mp3")
    music = pyglet.resource.media("hello.mp3")
    music.play()
    pyglet.app.run()
    os.remove("hello.mp3") #remove temperory file

if __name__ == '__main__':
    main()
