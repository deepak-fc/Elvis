from num2words import num2words as n2w
import speech_recognition as sr
from datetime import *
import yfinance as yf
import webbrowser
import pyttsx3
import json

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('elvis_design.kv')


##########################################################################################
class MainWidget(Widget):
    def runElvis(self):
        programInit()
        greet()
        userVoiceCommand = getUserVoiceCommand()
        processCommand(userVoiceCommand)


##########################################################################################
class ElvisApplication(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainWidget()


##########################################################################################
voiceEngine = None
companyData = None
intentsData = None


##########################################################################################
def programInit():
    global voiceEngine
    global companyData
    global intentsData

    voiceEngine = pyttsx3.init()
    with open('company_name_ticker.json') as f:
        companyData = json.load(f)

    with open('intent_function.json') as d:
        intentsData = json.load(d)


##########################################################################################
def getUserVoiceCommand():
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
        speak(reply)
        return None

    return query.lower()


##########################################################################################
def determineIntent(query):
    global intentsData

    for i in range(len(intentsData['intent_fun_matching'])):
        for pattern in intentsData['intent_fun_matching'][i]['patterns']:
            if pattern in query:
                return intentsData['intent_fun_matching'][i]['fun']


##########################################################################################
def greet():
    currentHourOfTheDay = int(datetime.now().hour)

    if 0 <= currentHourOfTheDay < 12:
        speak("Good Morning!")
    elif 12 < currentHourOfTheDay < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hi I am Elvis, How may I help you?")


##########################################################################################
def speak(text):
    global voiceEngine

    voiceEngine.say(text)
    voiceEngine.runAndWait()


##########################################################################################
def getCompanyNameAndTicker(query):
    global companyData

    index_of = query.split().index('of')
    company_name = " ".join(query.split()[index_of + 1:])
    company_name = company_name.strip().title()

    try:
        ticker = companyData[company_name]['company_ticker']
        return [company_name, ticker]

    except KeyError:
        results = "It seems you have said an invalid company name, please say a valid name and try again"
        speak(results)


##########################################################################################
def getStockPrice(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)

    try:
        company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
        stock_data = yf.Ticker(ticker)
        price = n2w(round(stock_data.info['currentPrice'], 2))

        results = "The last trading price of", company_name, "is", price, companyData[
            company_name]['currency']
        speak(results)

    except Exception as e:
        print(e)


##########################################################################################

def getTotalRevenue(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    revenue = n2w(round(stock_data.info['totalRevenue'], 2))

    results = "The total revenue of", company_name, "is", revenue, 'dollars'
    speak(results)


##########################################################################################
def getMarketCap(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    revenue = n2w(round(stock_data.info['marketCap'], 2))

    results = "The market capitalisation of", company_name, "is", revenue, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################
def get52WeekLow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    revenue = n2w(round(stock_data.info['fiftyTwoWeekLow'], 2))

    results = "The fifty two week low of", company_name, "is", revenue, companyData[
        company_name]['currency']
    speak(results)


##########################################################################################
def get52WeekHigh(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    revenue = n2w(round(stock_data.info['fiftyTwoWeekHigh'], 2))

    results = "The fifty two week high of", company_name, "is", revenue, companyData[
        company_name]['currency']
    speak(results)


##########################################################################################
def getFreeCashFlow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    revenue = n2w(round(stock_data.info['freeCashflow'], 2))

    results = "The free cash flow of", company_name, "is", revenue, companyData[
        company_name]['currency']
    speak(results)


##########################################################################################
def getOperatingCashFlow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    revenue = n2w(round(stock_data.info['operatingCashflow'], 2))

    results = "The operating cash flow of", company_name, "is", revenue, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getEps(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    eps = n2w(round(stock_data.info['trailingEps'], 2))

    results = "The earnings per share of", company_name, "is", eps, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getPeRatio(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    pe_ratio = n2w(round(stock_data.info['trailingPE'], 2))

    results = "The price to earnings ratio  of", company_name, "is", pe_ratio
    speak(results)

    if pe_ratio < "10":
        speak("Elvis thinks right now it is not good for investment but still you can keep it on watch")
    elif "10" <= pe_ratio <= "15":
        speak("Elvis thinks it can be considered for long term profits, still you can keep it on watch")
    elif "20" < pe_ratio <= "30":
        speak("Elvis thinks you can consider to invest")
    else:
        speak("Elvis thinks its high right now and should hold")

    speak(
        "All such information is for assistance only and shall not be taken as the sole basis for making any investment decision.")


##########################################################################################
def getEbitda(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    ebitda = n2w(round(stock_data.info['ebitda'], 2))

    results = "The EBITDA of", company_name, "is", ebitda, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################
def getPriceToBook(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    price_to_book = n2w(round(stock_data.info['priceToBook'], 2))
    results = "Price to book ratio of", company_name, "is", price_to_book
    speak(results)


##########################################################################################

def getDebtToEquity(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    d2e = n2w(round(stock_data.info['debtToEquity'], 2))

    results = "The debt to equity ratio of", company_name, "is", d2e
    speak(results)


##########################################################################################

def getTargetHighPrice(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    tp = n2w(round(stock_data.info['targetHighPrice'], 2))

    results = "The target high price of", company_name, "is", tp, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getForwardEps(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    feps = n2w(round(stock_data.info['forwardEps'], 2))

    results = "The forward earnings per share of", company_name, "is", feps, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getForwardPe(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    feps = n2w(round(stock_data.info['forwardPE'], 2))

    results = "The forward price to earning ratio of", company_name, "is", feps
    speak(results)


##########################################################################################

def getFiftyDma(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    fiftyDma = n2w(round(stock_data.info['fiftyDayAverage'], 2))
    results = "The fity day moving average of", company_name, "is", fiftyDma, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getPegRatio(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    peg = n2w(round(stock_data.info['trailingPegRatio'], 2))

    results = "The price earnings to growth ratio of", company_name, "is", peg
    speak(results)


##########################################################################################

def getDividendRate(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    divRate = n2w(round(stock_data.info['dividendRate'], 2))

    results = "The dividend rate of", company_name, "is", divRate
    speak(results)


##########################################################################################

def getLastDividendValue(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    ldiv = n2w(round(stock_data.info['lastDividendValue'], 2))

    results = "The last dividend value of", company_name, "is", ldiv, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def get52WeekChange(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    weekchng = n2w(round(stock_data.info['52WeekChange'], 2))

    results = "The fifty two week change of", company_name, "is", weekchng
    speak(results)


##########################################################################################

def getPreviousClose(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    prevclose = n2w(round(stock_data.info['previousClose'], 2))

    results = "The previous close of", company_name, "is", prevclose, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getRegularMarketOpen(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    openprice = n2w(round(stock_data.info['regularMarketOpen'], 2))

    results = "The opening price of", company_name, "is", openprice, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getRegularMarketDayLow(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    daylow = n2w(round(stock_data.info['regularMarketDayLow'], 2))

    results = "The day low price of", company_name, "is", daylow, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getRegularMarketDayHigh(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    dayhigh = n2w(round(stock_data.info['regularMarketDayHigh'], 2))

    results = "The day high price of", company_name, "is", dayhigh, companyData[company_name][
        'currency']
    speak(results)


##########################################################################################

def getSector(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    sec = stock_data.info['sector']

    results = "The", company_name, "belongs to", sec, "sector"
    speak(results)


##########################################################################################


def googleSearch(query):
    search_term = query.split("for")[-1]
    url = f"https://google.com/search?q={search_term}"
    webbrowser.get().open(url)
    speak(f'Here is what I found for {search_term} on google')


##########################################################################################

def youtube(query):
    search_term = query.split("youtube")[-1]
    url = f"https://youtube.com/search?q={search_term}"
    webbrowser.get().open(url)
    speak(f'Here is what I found for {search_term} on youtube')


##########################################################################################

def processCommand(query):
    if query is None:
        return

    intent = determineIntent(query)

    if intent == 'getStockPrice':
        getStockPrice(query)

    elif intent == 'getTotalRevenue':
        getTotalRevenue(query)

    elif intent == 'getMarketCap':
        getMarketCap(query)

    elif intent == 'get52WeekLow':
        get52WeekLow(query)

    elif intent == 'get52WeekHigh':
        get52WeekHigh(query)

    elif intent == 'getFreeCashFlow':
        getFreeCashFlow(query)

    elif intent == 'getOperatingCashFlow':
        getOperatingCashFlow(query)

    elif intent == 'getEps':
        getEps(query)

    elif intent == 'getPeRatio':
        getPeRatio(query)

    elif intent == 'getEbitda':
        getEbitda(query)

    elif intent == 'getPriceToBook':
        getPriceToBook(query)

    elif intent == 'getDebtToEquity':
        getDebtToEquity(query)

    elif intent == 'getTargetHighPrice':
        getTargetHighPrice(query)

    elif intent == 'getForwardEps':
        getForwardEps(query)

    elif intent == 'getForwardPe':
        getForwardPe(query)

    elif intent == 'getFiftyDma':
        getFiftyDma(query)

    elif intent == 'getPegRatio':
        getPegRatio(query)

    elif intent == 'getDividendRate':
        getDividendRate(query)

    elif intent == 'getLastDividendValue':
        getLastDividendValue(query)

    elif intent == 'get52WeekChange':
        get52WeekChange(query)

    elif intent == 'getPreviousClose':
        getPreviousClose(query)

    elif intent == 'getRegularMarketOpen':
        getRegularMarketOpen(query)

    elif intent == 'getRegularMarketDayLow':
        getRegularMarketDayLow(query)

    elif intent == 'getRegularMarketDayHigh':
        getRegularMarketDayHigh(query)

    elif intent == 'getSector':
        getSector(query)

    elif intent == 'googleSearch':
        googleSearch(query)

    elif intent == 'youtube':
        youtube(query)

    elif "how are you" in query:
        reply = "I'm doing good and how are you?"
        speak(reply)

    elif "hi" in query:
        reply = "hi, how can i help you"
        speak(reply)

    elif "who made you" in query:
        speak(
            "I am Elvis. Shounak, Somesh and Deepak are my creators.")

    elif "what is the time" in query:
        strTime = datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {strTime}")


##########################################################################################

if __name__ == '__main__':
    ElvisApplication().run()
##########################################################################################
