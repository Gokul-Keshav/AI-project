#!/usr/bin/env python3
 
import speech_recognition as sr
import pyttsx
from subprocess import call
 
r = sr.Recognizer()
     

while(1):     
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
         
        engine = pyttsx.init()
        print("1")

        ai = "sublime"
        try:
            print("2")
            speech = r.recognize_google(audio)
            print("You said: " + speech)
            engine.say("processing"+speech)
            engine.runAndWait()
            if ai in speech:
                call(["subl"])
        except sr.UnknownValueError:
            print("Goki could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Goki service; {0}".format(e))
else:
        print "Goodbye :), Have a nice day"