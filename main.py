import pyttsx3
import datetime
import speech_recognition as sr
import os
import wikipedia
import webbrowser
import random
import smtplib
import socket
from pytube import YouTube
import pyshorteners
import pywhatkit

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# print(voices[2].id)
rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                      #printing current voice rate
engine.setProperty('rate', 190)     # setting up new voice rate
chat = True                         #Toggle between chat and speechRecognition
        

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")
    
    else:
        speak("Good Evening Sir!")

   

def takeCommand():
    # it takes microphone input  from user

    if chat == True:

        print("How may I help you?\n")
        speak("How may I help you?\n")
        query = input("=>")
        try:
            print("Please wait for a while...")
            print(f"User said: {query}\n")
        
        except Exception as e:
            print(e)
            print("Say that again please...")
            return "None"
            
        return query
    else:

        r = sr.Recognizer()
        with sr.Microphone() as source:


            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in').lower()
            print(f"User said: {query}\n")
        
        except Exception as e:
        # print(e)
            print("Say that again please...")
            return "None"
        return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('kharey211@gmail.com','')          #Type your gmail id and password here to send email
    server.sendmail('kharey211@gmail.com',to,content)
    server.close()

#To find your system Ip Address
def ipFiender():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Hostname: {hostname}")
    print(f"Your IP Address is: {ip_address}")
    speak(f"Your IP Address is {ip_address}")

def wpMsgSender():
    strTimeH = datetime.datetime.now().strftime("%H")
    strTimeM = datetime.datetime.now().strftime("%M")
    speak("to whome you want me to send message?")
    name = input("Please enter name: ")
    number = str(input("Please enter number with country code: "))
    speak("Ok, what's the message?")
    message = input("Please type a message")
    pywhatkit.sendwhatmsg(number,message,int(strTimeH),int(strTimeM) + 2)
    speak(f"message has been send to {name}")


#YouTube video downloader
def YTVdownloader():
    while True:
        speak("Please Enter a link of video which you want me to download")
        link = input("waiting for your link:)")
        YouTube(link).streams.first().download()
        speak("Your video has been downloaded")
        speak("Is there any other video you want me to download?")
        userInput = input("Please type yes or no: ").lower()
        if userInput ==  "yes":
            YTVdownloader()

            break
        elif userInput ==  "no":
            speak("OK")
            
            break

#Play music
def playMusic():
    speak("Ok, sir i will play random songs from your favriot songs play list...")
    music_dir = 'F:\\songs\\Fav'  #Enter your song directory here
    songs = os.listdir(music_dir)  
    print(int(len(songs))-10)
    os.startfile(os.path.join(music_dir,songs[random.randint(0,len(songs)-10)]))

#Link shortner
def linkShortner():
    while True:
        speak("Please enter the url which you want me to shortener it.")
        url = input("Enter the url:")
        print("shorten url is: ",pyshorteners.Shortener().tinyurl.short(url))
        speak("Is there any other url which you want me to shortener it.?")
        userInput = input("Please type yes or no: ").lower()
        if userInput ==  "yes":
            linkShortner()
            break
        elif userInput ==  "no":
            speak("OK")
          
            break
    


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open chrome" in query:
            os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")

        elif 'play music' in query:
            playMusic()
            
        elif "stop songs" in query:
            os.system("TASKKILL /F /IM Music.UI.exe")
            
        elif 'send message from whatsapp' in query:
            wpMsgSender()
            

        elif 'go to sleep' in query:
            speak("ok, sir bye i am going in sleep mode")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            
            break

        elif 'restart my pc' in query:
            speak("ok, sir i am restarting the pc")
            os.system("shutdown /r /t 1")

        elif 'shutdown' in query:
            speak("ok, sir bye")
            os.system("shutdown /s /t 1")
            

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H  O clock %M minutes")
            speak(f"Sir, the time is {strTime}")

        elif 'shortener the url for me' in query:
            linkShortner()
            
        elif "open code" in query:
            codePath = "C:\\Users\\khare\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to yash' in query:
            try:
                speak("what should I say?")
                content = takeCommand()
                to = "yashkhare383@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry I am not abel to send email this time...")

        elif "ip address" in query:
            ipFiender()
            
        elif "download a youtube video" in query:
            YTVdownloader()
            
        elif 'voice' in query:
            chat = False
           
        elif 'i want to type a command for you' in query:
            chat = True
           
        elif "exit" or "stop" in query:
            speak("Bye")
            break
    # pass
  
    