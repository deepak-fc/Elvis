from num2words import num2words as n2w
import speech_recognition as sr
from datetime import *
import yfinance as yf
import webbrowser
import pyttsx3
import json


class Elvis:
    voiceEngine = None
    companyData = None
    intentsData = None

    ##########################################################################################
    def __init__(self):
        self.voiceEngine = pyttsx3.init()

        with open('company_name_ticker.json') as f:
            self.companyData = json.load(f)

        with open('intent_function.json') as d:
            self.intentsData = json.load(d)

    ##########################################################################################
    def getUserVoiceCommand(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            recognizer.pause_threshold = 1
            recognizer.operation_timeout = 2
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_sphinx(audio, language='en-in')
            print(f"You said: {query}\n")

        except Exception:
            print("Couldn't process that...")
            reply = "Sorry, I didn't get that. Could you say it again?"
            self.speak(reply)
            return None

        return query.lower()

    ##########################################################################################
    def determineIntent(self, query):
        for i in range(len(self.intentsData['intent_fun_matching'])):
            for pattern in self.intentsData['intent_fun_matching'][i]['patterns']:
                if pattern in query:
                    return self.intentsData['intent_fun_matching'][i]['fun']

    ##########################################################################################
    def getCompanyNameAndTicker(self, query):
        index_of = query.split().index('of')
        company_name = " ".join(query.split()[index_of + 1:])
        company_name = company_name.strip().title()
        ticker = self.companyData[company_name]["company_ticker"]
        return [company_name, ticker]

    ##########################################################################################
    def getStockPrice(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        price = n2w(round(stock_data.info['currentPrice'], 2))

        results = "The last trading price of", company_name, "is", price, self.companyData[company_name]['currency']
        self.speak(results)

    ##########################################################################################
    def getTotalRevenue(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        revenue = n2w(round(stock_data.info['totalRevenue'], 2))

        results = "The total revenue of", company_name, "is", revenue, 'dollars'
        self.speak(results)

    ##########################################################################################
    def getMarketCap(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        revenue = n2w(round(stock_data.info['marketCap'], 2))

        results = "The market capitalisation of", company_name, "is", revenue, self.companyData[company_name][
            'currency']
        self.speak(results)

    ##########################################################################################
    def get52WeekLow(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        revenue = n2w(round(stock_data.info['fiftyTwoWeekLow'], 2))

        results = "The fifty two week low of", company_name, "is", revenue, self.companyData[company_name]['currency']
        self.speak(results)

    ##########################################################################################
    def get52WeekHigh(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        revenue = n2w(round(stock_data.info['fiftyTwoWeekHigh'], 2))

        results = "The fifty two week high of", company_name, "is", revenue, self.companyData[company_name]['currency']
        self.speak(results)

    ##########################################################################################
    def processCommand(self, query):
        if query is None:
            return

        intent = self.determineIntent(query)

        if intent == 'getStockPrice':
            self.getStockPrice(query)

        elif intent == 'getTotalRevenue':
            self.getTotalRevenue(query)

        elif intent == 'getMarketCap':
            self.getMarketCap(query)

        elif intent == 'get52WeekLow':
            self.get52WeekLow(query)

        elif intent == 'get52WeekHigh':
            self.get52WeekHigh(query)

        elif 'free cash flow of' in query:
            compNameAndTicker = self.getCompanyNameAndTicker(query)
            company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
            stock_data = yf.Ticker(ticker)
            revenue = n2w(round(stock_data.info['freeCashflow'], 2))

            results = "The free cash flow of", company_name, "is", revenue, self.companyData[company_name]['currency']
            self.speak(results)

        elif 'operating cash flow of' in query:
            compNameAndTicker = self.getCompanyNameAndTicker(query)
            company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
            stock_data = yf.Ticker(ticker)
            revenue = n2w(round(stock_data.info['operatingCashflow'], 2))

            results = "The operating cash flow of", company_name, "is", revenue, self.companyData[company_name][
                'currency']
            self.speak(results)

        elif "hi" in query:
            reply = "Hey there! How may I help you?"
            self.speak(reply)

        elif "how are you" in query:
            reply = "I'm doing good and how are you?"
            self.speak(reply)

        elif "who made you" in query:
            self.speak("I am Elvis. Shounak, Somesh and Deepak are my creators.")

        elif "what is the time" in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            self.speak(f"The current time is {strTime}")

        elif "open youtube" in query:
            self.speak("opening youtube")
            webbrowser.open("www.youtube.com")

        elif "open google" in query:
            self.speak("opening Google")
            webbrowser.open("www.google.com")

        elif "open stack overflow" in query:
            self.speak("opening stackoverflow")
            webbrowser.open("www.stackoverflow.com")

        elif 'open github' in query:
            self.speak("opening github")
            webbrowser.open("www.github.com")

    ##########################################################################################
    def greet(self):
        currentHourOfTheDay = int(datetime.now().hour)

        if 0 <= currentHourOfTheDay < 12:
            self.speak("Good Morning!")
        elif 12 < currentHourOfTheDay < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")

        self.speak("Hi. I am Elvis. How may I help you?")

    ##########################################################################################
    def speak(self, text):
        self.voiceEngine.say(text)
        self.voiceEngine.runAndWait()

    ##########################################################################################
