import pyttsx3                   # install using:-  pip install pyttsx3
import speech_recognition as sr  # install using:- pip install SpeechRecognition
import datetime                  # install using:-  pip install datetime
import wikipedia                 # install using:- pip install wikipedia
import webbrowser
import os
import smtplib
from googlesearch import search  # pip install googlesearch-python
import random
import subprocess
import time
import json
import yfinance as yf                       # pip install yfinance
from num2words import num2words as n2w      # pip install num2words
from yahoo_fin.stock_info import *

# will require pyaudio as well, you can install it using below commands
# In Terminal type

# pip install pipwin
# Then

# pipwin install pyaudio

# pyttsx3 configurations

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)

voiceEngine = pyttsx3.init()

rate = voiceEngine.getProperty('rate')
volume = voiceEngine.getProperty('volume')
voice = voiceEngine.getProperty('voice')

# print(rate)
# print(volume)
# print(voice)

#  speak function defination


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# wish function definition

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Elvis. how can I help")

# command taking function


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.operation_timeout = 2
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception:
        # print(e)
        print("Say that again please...")
        word = random.choice(
            ["Sorry, i didnt get that", "Please ,say that again", "Pardon..", "come again..."])
        speak(word)
        return "None"
    return query


def getCompNameAndTicker(query):
    index_of = query.split().index('of')                  # gets index of word "of" from a list containing all words of query
    company_name = " ".join(query.split()[index_of+1:])   # extracts the name of company and converts it into a single string (if name of company contains multiple words like Larsen and Toubro)
    company_name = company_name.strip().title()           # strips all the whitespace and coverts first letter of each word to uppercase (as per the json convention made by us)
    ticker = data[company_name]['company_ticker']         # gets ticket
 
    return [company_name, ticker]                         # returns company name and ticker

# creating a json object
with open('company_name_ticker.json') as f:
    data = json.load(f)


if __name__ == "__main__":

    if len(input('Press Enter to enable voice assistant')) == 0:
        wishMe()
        while True:

            query = takeCommand().lower()

            # Logic for executing tasks based on query

            if 'stock price of' in query:
                compNameAndTicker = getCompNameAndTicker(query)
                company_name, ticker = compNameAndTicker[0], compNameAndTicker[1] 
                stock_data = yf.Ticker(ticker)                        # makes a yfinance object
                price = n2w(round(stock_data.info['currentPrice'], 2))# extracts current price and rounds it by 2 digits and also converts the numerical digits into words using n2w function

                results = "The last trading price of", company_name, "is", price, data[company_name]['currency']
                speak(results)
            
            elif 'total revenue of' in query:
                compNameAndTicker = getCompNameAndTicker(query)
                company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
                stock_data = yf.Ticker(ticker)
                revenue = n2w(round(stock_data.info['totalRevenue'], 2))

                results = "The total revenue of", company_name, "is", revenue, 'dollars'       # all revenue is given in dollars
                speak(results)

            elif 'market capitalisation of' in query:
                compNameAndTicker = getCompNameAndTicker(query)
                company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
                stock_data = yf.Ticker(ticker)
                revenue = n2w(round(stock_data.info['marketCap'], 2))

                results = "The market capitalisation of", company_name, "is", revenue, data[company_name]['currency']      
                speak(results)

            elif '52 week low of' in query:
                compNameAndTicker = getCompNameAndTicker(query)
                company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
                stock_data = yf.Ticker(ticker)
                revenue = n2w(round(stock_data.info['fiftyTwoWeekLow'], 2))

                results = "The fifty two week low of", company_name, "is", revenue, data[company_name]['currency']      
                speak(results)
    
            elif '52 week high of' in query:
                compNameAndTicker = getCompNameAndTicker(query)
                company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
                stock_data = yf.Ticker(ticker)
                revenue = n2w(round(stock_data.info['fiftyTwoWeekHigh'], 2))

                results = "The fifty two week high of", company_name, "is", revenue, data[company_name]['currency']      
                speak(results)

            elif 'price to book ratio of' in query:
                compNameAndTicker = getCompNameAndTicker(query)
                company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
                stock_data = yf.Ticker(ticker)
                revenue = n2w(round(stock_data.info['priceToBook'], 2))

                results = "The price to book ratio of", company_name, "is", revenue     
                speak(results)


            elif 'free cash flow of' in query:
                compNameAndTicker = getCompNameAndTicker(query)
                company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
                stock_data = yf.Ticker(ticker)
                revenue = n2w(round(stock_data.info['freeCashflow'], 2))

                results = "The free cash flow of", company_name, "is", revenue, data[company_name]['currency']      
                speak(results)

            elif 'operating cash flow of' in query:
                compNameAndTicker = getCompNameAndTicker(query)
                company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
                stock_data = yf.Ticker(ticker)
                revenue = n2w(round(stock_data.info['operatingCashflow'], 2))

                results = "The operating cash flow of", company_name, "is", revenue, data[company_name]['currency']      
                speak(results)

            # searching the wiki

            elif 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            # opening random commands


            elif 'open youtube' in query:
                speak("opening youtube")
                webbrowser.open("www.youtube.com")

            elif 'open google' in query:
                speak("opening Google")
                webbrowser.open("www.google.com")

            elif 'open stackoverflow' in query:
                speak("opening stackoverflow")
                webbrowser.open("www.stackoverflow.com")

            elif 'open github' in query:
                speak("opening github")
                webbrowser.open("www.github.com")

            elif 'open netflix' in query:
                speak("opening netflix")
                subprocess.call("Netflix")

            # google search

            elif "search on google" in query:
                speak("What should i search")
                query = takeCommand()
                for j in search(query, tld="co.in", num=10, stop=1, pause=2):
                    speak(j)
                speak("should i open this ?")
                query = takeCommand()
                if 'yes' in query:
                    os.startfile(j)
                else:
                    speak('ok')

            # Random commands



            elif "what is the time" in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif "play random songs on youtube" in query:
                speak("playing random songs!")
                os.startfile(
                    'https://www.youtube.com/watch?v=weRTCk-mJyE&list=PLx0sYbCqOb8QTF1DCJVfQrtWknZFzuoAE&index=1')

            elif "who made you" in query:
                # os.startfile('C:\\Users\\Ambade\\Downloads\\Queen.mp3')
                speak(
                    "I am Elvis. Shounak, Somesh and Deepak are my creators.")

            # Hangman code


            elif "make an appointment" in query:
                speak("booking an appointnment")

            # to email

            # Ineraction

            elif "hi" in query:
                word = random.choice(
                    ["Hi", "Hello", "How can i help you", "Any problem again?"])
                speak(word)

            elif "google assistant" in query:
                word = random.choice(["oh yes !!!!", "that bitch , why? whats the problem",
                                    "we are cousins ,although im elder", "why , what did i do wrong?"])
                speak(word)

            elif "siri" in query:
                word = random.choice(["nahhhhhh , its better not to know that...",
                                    "Bad choice indeed ", "I am far far far far more better", "we were roommates"])
                speak(word)

            elif "how are you " in query:
                word = random.choice(
                    ["Fine as fresh new wine ", "good, what about you"])
                speak(word)

            elif "tell me about yourself" in query:
                word = random.choice([])

            # quit

            elif "bye" in query or "that would be all sam" in query:
                speak("i'll go to sleep now")
                break
        
        else:
            sys.exit()
