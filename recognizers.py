#recognize_bing(): Microsoft Bing Speech 
#recognize_google(): Google Web Speech API 
#recognize_google_cloud(): Google Cloud Speech - requires  
#installation of the google-cloud-speech package 
#recognize_houndify(): Houndify by SoundHound 
#recognize_ibm(): IBM Speech to Text 
#recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx 
#recognize_wit(): Wit.ai 
#Источник: https://pythonpip.ru/examples/raspoznavanie-rechi-i-golosa-na-python-podrobno

import speech_recognition as sr 
r=sr.Recognizer() 
astro = sr.AudioFile('/home/user/Музыка/astro.wav') 
with astro as source: 
    Audio = r.record(source) 
type(Audio)
r.recognize_google_cloud(Audio)
