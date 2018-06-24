import os.path
import sys
import json
import pyttsx
from pprint import PrettyPrinter
p = PrettyPrinter(indent=4)


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

    request.query = "convert 26 degrees Celsius to Fahrenheit"
    response = request.getresponse()

    answer = json.loads(response.read())#["result"]["fulfillment"]["speech"]
    p.pprint(answer)
    '''
    #print (response.read())
    engine = pyttsx.init()

    engine.say(answer)
    engine.runAndWait()
    '''

if __name__ == '__main__':
    main()
