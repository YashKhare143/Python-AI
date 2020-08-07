import main
from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)


################################## Send Email start here ##################################
def sendEmail(name,mailAddress):
    try:
        main.speak("Ok,what's the message")
        message = takeCommand()
        main.setupSMTPServer(mailAddress,message)
        main.speak(f"Your message has been send to {name} with email address {mailAddress}.")
    except Exception as e:
        print(e)
        main.speak("Sorry I am not abel to send email this time...")

def askToAddMailToList(name,mailAddress):
    while True:
        main.speak(f"Do you want me to add {name} Email address to your Email address list?")
        addToList = takeCommand()
        if addToList == "yes":
            main.speak("Ok")
            main.addToMailList(name,mailAddress)
            break

        elif addToList == "no":
            main.speak("Ok sir as your wish.")
            break
        else:
            enterCorrestOperation()

def enterCorrestOperation():
    main.speak("Please enter yes or no.")

def mailValidition(name,mailAddress):
    while True:
        main.speak("Is it right mail?")
        mailVerification = takeCommand()
        if mailVerification == "yes":
            askToAddMailToList(name,mailAddress)
            sendEmail(name,mailAddress)
            break
        elif mailVerification == "no":
            emailVerification(name,mailAddress)
            break
        else:
            enterCorrestOperation()

def emailVerification(name,mailAddress):
    main.speak(f"Please say the mail address of {name} again:")
    mailAddress = takeCommand()
    mailAddress = mailAddress.replace(" ","")
    main.mailValidition(name,mailAddress)

def enterValidEmaill(name,mailAddress):
    mailAddress = takeCommand()
    mailAddress = mailAddress.replace(" ","")
    main.mailValidition(name,mailAddress)


def Email():
   
    try:

        main.speak("To whome you want me to send message?")
        name = takeCommand()
        if config["EmailAddress"][name]:
            main.speak("this name is in your email address list")
            mailAddress = config["EmailAddress"][name]
            main.speak(f"the email address of {name} is {mailAddress}")
            sendEmail(name,mailAddress)
    except Exception as e:
        main.speak("this name is not in your email address list")
        main.speak(f"What is the mail address of {name}: ")
        mailAddress = takeCommand()
        mailAddress = mailAddress.replace(" ","")
        main.mailValidition(name,mailAddress)
        
 ###################################### Send Email ends here #################################  