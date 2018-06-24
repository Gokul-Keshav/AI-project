import requests
from subprocess import call
from urllib import quote_plus
from pprint import PrettyPrinter
import speech_recognition as sr


p = PrettyPrinter(indent=4)

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say the name of a song!")
    audio = r.listen(source)
    video = r.recognize_google(audio)
#video = "gucci"
video = quote_plus(video)
URL = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&order=relevance&q=" + video + "&type=video&key=AIzaSyDHA5AKa4A-RjqdYPxBJnNe4zsJzecetX4"
print(URL)
r = requests.get(url=URL)

data = r.json()
try:
	p.pprint(data["items"][0]["id"]["videoId"])

	video_key = data["items"][0]["id"]["videoId"]
	print("launching")
	call(["xdg-open","https://www.youtube.com/watch?v="+video_key])
	print("launched")

except Exception as e:
	print("video not found")

