	
from __future__ import print_function
import httplib2
import os

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



def main():
        # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    '''
    event = {
      'summary': 'A test event from agent',
      'location': 'chennai, pallavaram',
      'description': 'This is a great moment. When you face a problem, keep calm and think. You will get the solution',
      'start': {
        'dateTime': '2018-03-28T06:00:00+05:30',
      },
      'end': {
        'dateTime': '2018-03-28T7:00:00+05:30',
      },
      
      'attendees': [
        {'email': 'gokulkeshav7@gmail.com'},
        {'email': 'boomilaxyz@gmail.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    '''

    event = {
      'summary': 'Afternoon we have TIP',
      'location': 'chennai, pallavaram',
      'description': 'Today afternoon we will relax',
      'start': {
        'dateTime': '2018-03-23T18:00:00+05:30',
      },
      'end': {
        'dateTime': '2018-03-23T18:00:00+05:30',
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
    #print 'Event created: %s' % (event.get('htmlLink'))
    print("Event created")


if __name__ == '__main__':
    main()