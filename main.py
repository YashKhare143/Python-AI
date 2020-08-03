'''
                             Welcome to Python-AI-2.0

Kindly install all the Requirements from requirements.txt by using command - pip install -r requirements.txt
You can do lots of things with it like sending emails, whatsapp messages,downloading youtube videos,play songs and much more
more functions will be add in it...


Enjoy :)

Here are commands to controle it by voice or by keyboard 
1: to use ai with your voice - just type "Voice" after running it.
2: to use ai with keyboard(Only use this command if you activing voise mode)  - just say this "i want to type a command for you"

'''
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
from configparser import ConfigParser
import re 
from selenium import webdriver

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# browser = webdriver.Chrome('C:\\Users\\khare\\Downloads\\chromedriver_win32\\chromedriver.exe')

#SettingUp config file
file = 'config.ini'
config = ConfigParser()
config.read(file)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[int(config['Voice']['type'])].id)
# print(voices[2].id)
rate = engine.getProperty('rate')   # getting details of current speaking rate

engine.setProperty('rate', int(config['Voice']['rate']))     # setting up new voice rate
# print (config['Voice']['rate'])                      #printing current voice rate
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


################################## Send Email ends here ##################################
        #setup a SMTP server to send email
def setupSMTPServer(mailAddress,message):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(config['Email']['yourMailId'],config['Email']['yourMailPass'])          #Type your gmail id and password here to send email
    server.sendmail(config['Email']['yourMailId'],mailAddress,message)
    server.close()

# query = query.replace("wikipedia","")
        
def sendEmail(name,mailAddress):
    if chat == True:
        try:
            speak("please type a message: ")
            message = input("=> ")
            setupSMTPServer(mailAddress,message)
            speak(f"Your message has been send to {name} with email address {mailAddress}.")
        except Exception as e:
            print(e)
            speak("Sorry I am not abel to send email this time...")
    elif chat == False:
        try:
            speak("Ok,what's the message")
            message = takeCommand()
            setupSMTPServer(mailAddress,message)
            speak(f"Your message has been send to {name} with email address {mailAddress}.")
        except Exception as e:
            print(e)
            speak("Sorry I am not abel to send email this time...")

def addToMailList(name,mailAddress):
    config.set('EmailAddress',name,mailAddress)
    with open(file,'w') as configfile:
        config.write(configfile)

def askToAddMailToList(name,mailAddress):
    if chat == True:
        speak(f"Do you want me to add {name} Email address to your Email address list?")
        addToList = input("please type yes or no:")
        if addToList == "yes":
            speak("Ok")
            addToMailList(name,mailAddress)
        elif addToList == "no":
            speak("Ok sir as your wish.")
            
    elif chat == False:
        speak(f"Do you want me to add {name} Email address to your Email address list?")
        addToList = takeCommand()
        if addToList == "yes":
            speak("Ok")
            addToMailList(name,mailAddress)
        elif addToList == "no":
            speak("Ok sir as your wish.")

def mailValidition(name,mailAddress):
    if(re.search(regex,mailAddress)):
        if chat == True:
            speak("Is it right mail?")
            mailVerification = input("Pleas type yes or no: ")
            
            if mailVerification == "yes":
                askToAddMailToList(name,mailAddress)
                sendEmail(name,mailAddress)

            elif mailVerification == "no":
                emailVerification(name,mailAddress)

        elif chat == False:
            speak("Is it right mail?")
            mailVerification = takeCommand()
            
            if mailVerification == "yes":
                askToAddMailToList(name,mailAddress)
                sendEmail(name,mailAddress)

            elif mailVerification == "no":
                emailVerification(name,mailAddress)

    else:
        speak("Invalid Email, Please enter the valide Email Address")
        reEnterTheEmaill(name,mailAddress)

def reEnterTheEmaill(name,mailAddress):
    if chat == True:
        mailAddress = input ("=> ")
        mailValidition(name,mailAddress)
    elif chat == False:
        mailAddress = takeCommand()
        mailAddress = mailAddress.replace(" ","")
        mailValidition(name,mailAddress)
    
def emailVerification(name,mailAddress):
    if chat == True:
        speak(f"Please type the mail address of {name} again:")
        mailAddress = input("=> ")
        mailValidition(name,mailAddress)

    elif chat == False:
        speak(f"Please say the mail address of {name} again:")
        mailAddress = takeCommand()
        mailAddress = mailAddress.replace(" ","")
        mailValidition(name,mailAddress)
    
def Email():
    if chat == True:
        try:
            try:

                speak("To whome you want me to send message?")
                name = input("Please enter recipient name: ")
                if config["EmailAddress"][name]:
                    speak("this name is in your email address list")
                    mailAddress = config["EmailAddress"][name]
                    speak(f"the email address of {name} is {mailAddress}")
                    sendEmail(name,mailAddress)
            except Exception as e:
                speak("this name is not in your email address list")
                speak(f"What is the mail address of {name}: ")
                mailAddress = input ("=> ")
                mailValidition(name,mailAddress)
                
           
        except Exception as e:
            print(e)
            speak("Sorry I am not abel to send email this time...")
          
    elif chat == False:
        try:
            try:

                speak("To whome you want me to send message?")
                name = takeCommand()
                if config["EmailAddress"][name]:
                    speak("this name is in your email address list")
                    mailAddress = config["EmailAddress"][name]
                    speak(f"the email address of {name} is {mailAddress}")
                    sendEmail(name,mailAddress)
            except Exception as e:
                speak("this name is not in your email address list")
                speak(f"What is the mail address of {name}: ")
                mailAddress = takeCommand()
                mailAddress = mailAddress.replace(" ","")
                mailValidition(name,mailAddress)
                
        except Exception as e:
            print(e)
            speak("Sorry I am not abel to send email this time...")

        

###################################### Send Email ends here #################################


#To find your system Ip Address
def ipFiender():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Hostname: {hostname}")
    print(f"Your IP Address is: {ip_address}")
    speak(f"Your IP Address is {ip_address}")

###################################### To Send WhatsApp Message ###################################### 
def wpMsgSender():
    strTimeH = datetime.datetime.now().strftime("%H")
    strTimeM = datetime.datetime.now().strftime("%M")
    if chat == True:
        speak("to whome you want me to send message?")
        name = input("Please enter name: ")
        number = str(input("Please enter number with country code: "))
        speak("Ok, what's the message?")
        message = input("Please type a message")
        pywhatkit.sendwhatmsg(number,message,int(strTimeH),int(strTimeM) + 2)
        speak(f"message has been send to {name}")

    elif chat == False:
        speak("to whome you want me to send message?")
        name = takeCommand()
        speak("Please say number with country code: ")
        number = takeCommand()
        speak("Ok, what's the message?")
        message = takeCommand()
        pywhatkit.sendwhatmsg(number,message,int(strTimeH),int(strTimeM) + 2)
        speak(f"message has been send to {name}")
############################ To Send WhatsApp Message end's here ############################ 

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
            # browser.get('http://youtube.com/')

        elif "open google" in query:
            webbrowser.open("google.com")
            # browser.get('http://google.com/')

        elif "open instagram" in query:
            webbrowser.open("instagram.com")
            # browser.get('https://www.instagram.com//')

        elif "open github" in query:
            webbrowser.open("github.com")
            # browser.get('https://github.com//')

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

        elif 'email' in query:
            Email()

        elif "ip address" in query:
            ipFiender()
            
        elif "download a youtube video" in query:
            YTVdownloader()
            
        elif 'voice' in query:
            chat = False
           
        elif 'i want to type a command for you' in query:
            chat = True
           
        
    # pass
  
    
