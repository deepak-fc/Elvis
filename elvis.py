from urllib import response
from num2words import num2words as n2w
import speech_recognition as sr
from datetime import *
import yfinance as yf
import webbrowser
import pyttsx3
import json
import sys


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
    def runElvis(self):
        userVoiceCommand = self.getUserVoiceCommand()
        self.processCommand(userVoiceCommand)
    ##########################################################################################

    def getUserVoiceCommand(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            recognizer.pause_threshold = 0.5
            recognizer.operation_timeout = 2
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
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

    def getEbitda(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        ebitda = n2w(round(stock_data.info['ebitda'], 2))

        results = "The EBITDA of", company_name, "is", ebitda, self.companyData[company_name][
            'currency']
        self.speak(results)
    ##########################################################################################

    def getDebtToEquity(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        d2e = n2w(round(stock_data.info['debtToEquity'], 2))

        results = "The debt to equity ratio of", company_name, "is", d2e
        self.speak(results)
    ##########################################################################################

    def getTargetHighPrice(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        tp = n2w(round(stock_data.info['targetHighPrice'], 2))

        results = "The target high price of", company_name, "is", tp, self.companyData[company_name][
            'currency']
        self.speak(results)
    ##########################################################################################

    def getForwardEps(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        feps = n2w(round(stock_data.info['forwardEps'], 2))

        results = "The forward earnings per share of", company_name, "is", feps, self.companyData[company_name][
            'currency']
        self.speak(results)
    ##########################################################################################

    def getForwardPe(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        feps = n2w(round(stock_data.info['forwardPE'], 2))

        results = "The forward price to earning ratio of", company_name, "is", feps
        self.speak(results)
    ##########################################################################################

    def getFiftyDma(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        fiftyDma = n2w(round(stock_data.info['fiftyDayAverage'], 2))
        results = "The fity day moving average of", company_name, "is", fiftyDma, self.companyData[company_name][
            'currency']
        self.speak(results)
    ##########################################################################################

    def getPegRatio(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        peg = n2w(round(stock_data.info['trailingPegRatio'], 2))

        results = "The price earnings to growth ratio of", company_name, "is", peg
        self.speak(results)
    ##########################################################################################

    def getCompanyNameAndTicker(self, query):
        index_of = query.split().index('of')
        company_name = " ".join(query.split()[index_of + 1:])
        company_name = company_name.strip().title()

        try:

            ticker = self.companyData[company_name]['company_ticker']
            return [company_name, ticker]

        except KeyError:
            results = "It seems you have said an invalid company name, please say a valid name and try again"
            self.speak(results)
            self.runElvis()

    ##########################################################################################
    def getStockPrice(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)

        try:

            company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
            stock_data = yf.Ticker(ticker)
            price = n2w(round(stock_data.info['currentPrice'], 2))

            results = "The last trading price of", company_name, "is", price, self.companyData[
                company_name]['currency']
            self.speak(results)

        except Exception as e:
            print(e)

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

        results = "The fifty two week low of", company_name, "is", revenue, self.companyData[
            company_name]['currency']
        self.speak(results)

    ##########################################################################################
    def get52WeekHigh(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        revenue = n2w(round(stock_data.info['fiftyTwoWeekHigh'], 2))

        results = "The fifty two week high of", company_name, "is", revenue, self.companyData[
            company_name]['currency']
        self.speak(results)

    ##########################################################################################
    def getFreeCashFlow(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        revenue = n2w(round(stock_data.info['freeCashflow'], 2))

        results = "The free cash flow of", company_name, "is", revenue, self.companyData[
            company_name]['currency']
        self.speak(results)
    ##########################################################################################

    def getOperatingCashFlow(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        revenue = n2w(round(stock_data.info['operatingCashflow'], 2))

        results = "The operating cash flow of", company_name, "is", revenue, self.companyData[company_name][
            'currency']
        self.speak(results)
    ##########################################################################################

    def getPeRatio(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        pe_ratio = n2w(round(stock_data.info['trailingPE'], 2))
        results = "The price to earnings ratio  of", company_name, "is", pe_ratio
        self.speak(results)

    ##########################################################################################

    def getEps(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        eps = n2w(round(stock_data.info['trailingEps'], 2))

        results = "The earnings per share of", company_name, "is", eps, self.companyData[company_name][
            'currency']
        self.speak(results)
    ##########################################################################################
    
    def getdividendRate(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        divRate = n2w(round(stock_data.info['dividendRate'], 2))

        results = "The dividend rate of", company_name, "is", divRate
        self.speak(results)
    ##########################################################################################

    def getlastDividendValue(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        ldiv = n2w(round(stock_data.info['lastDividendValue'], 2))

        results = "The last dividend value of", company_name, "is", ldiv, self.companyData[company_name][
            'currency']
        self.speak(results)
    ##########################################################################################

    def get52WeekChange(self, query):
        compNameAndTicker = self.getCompanyNameAndTicker(query)
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        weekchng = n2w(round(stock_data.info['52WeekChange'], 2))

        results = "The fifty two week change of", company_name, "is", weekchng
        self.speak(results)
    ##########################################################################################
   
    def googlesearch(self, query):
            search_term = query.split("for")[-1]  
            url = f"https://google.com/search?q={search_term}"  
            webbrowser.get().open(url)  
            self.speak(f'Here is what I found for {search_term} on google') 
    ##########################################################################################

    def youtube(self, query):
            search_term = query.split("youtube")[-1]  
            url = f"https://youtube.com/search?q={search_term}"  
            webbrowser.get().open(url)  
            self.speak(f'Here is what I found for {search_term} on youtube')
    ##########################################################################################

    def processCommand(self, query):
        if query is None:
            return

        print(len(self.intentsData['intent_fun_matching']))
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

        elif intent == 'getFreeCashFlow':
            self.getFreeCashFlow(query)

        elif intent == 'getOperatingCashFlow':
            self.getOperatingCashFlow(query)

        elif intent == 'getEps':
            self.getEps(query)

        elif intent == 'getPeRatio':
            self.getPeRatio(query)

        elif intent == 'getEbitda':
            self.getEbitda(query)

        elif intent == 'getDebtToEquity':
            self.getDebtToEquity(query)

        elif intent == 'getTargetHighPrice':
            self.getTargetHighPrice(query)

        elif intent == 'getForwardEps':
            self.getForwardEps(query)

        elif intent == 'getForwardPe':
            self.getForwardPe(query)

        elif intent == 'getFiftyDma':
            self.getFiftyDma(query)

        elif intent == 'getPegRatio':
            self.getPegRatio(query)

        elif intent == 'getdividendRate':
            self.getdividendRate(query)

        elif intent == 'getlastDividendValue':
            self.getlastDividendValue(query)

        elif intent == 'get52WeekChange':
            self.get52WeekChange(query)

        elif intent == 'googlesearch':
            self.googlesearch(query)

        elif intent == 'youtube':
            self.youtube(query)

        elif "how are you" in query:
            reply = "I'm doing good and how are you?"
            self.speak(reply)

        elif "hi" in query:
            reply = "hi, how can i help you"
            self.speak(reply)

        elif "who made you" in query:
            self.speak(
                "I am Elvis. Shounak, Somesh and Deepak are my creators.")

        elif "what is the time" in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            self.speak(f"The current time is {strTime}")
         
        
    ##########################################################################################
    def greet(self):
        currentHourOfTheDay = int(datetime.now().hour)

        if 0 <= currentHourOfTheDay < 12:
            self.speak("Good Morning!")
        elif 12 < currentHourOfTheDay < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")

        self.speak("Hi I am Elvis, How may I help you?")

    ##########################################################################################
    def speak(self, text):
        self.voiceEngine.say(text)
        self.voiceEngine.runAndWait()

    ##########################################################################################
