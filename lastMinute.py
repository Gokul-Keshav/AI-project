#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
from subprocess import call
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    speeechthing = r.recognize_google(audio)

print("You said: "+speeechthing)

string = "sublime"
if string in speeechthing:
    call(["subl"])

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Goki Speech Recognition thinks you said " + speeechthing )
except sr.UnknownValueError:
    print("Goki Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Goki Speech Recognition service; {0}".format(e))
