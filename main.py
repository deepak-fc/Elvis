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
from kivy.properties import ObjectProperty

Builder.load_file('elvis_design.kv')


##########################################################################################
class MainWidget(Widget):
    def runElvis(self):
        programInit()
        greet()
        userVoiceCommand = getUserVoiceCommand()
        toDisplay = processCommand(userVoiceCommand)

        try:
            toDisplay = addNewLine(toDisplay)
            # print(toDisplay)
            self.ids.output_screen.text = toDisplay

        except:
            pass


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

    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    price = round(stock_data.info['currentPrice'], 2)

    vocal_results = f"The last trading price of {company_name}, is {n2w(price)}, {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The last trading price of {company_name}, is {getSymbol(companyData[company_name]['currency'])}{price}"
    return results
##########################################################################################


def addNewLine(str):

    if(len(str) > 38):
        chunks = [str[i:i+38] for i in range(0, len(str), 38)]
        print(chunks)
        return '\n'.join(chunks)

    return str

##########################################################################################


def getSymbol(str):
    if str == 'rupees':
        return '₹'

    return '$'
##########################################################################################


def getTotalRevenue(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    revenue = round(stock_data.info['totalRevenue'], 2)

    vocal_results = f"The total revenue of {company_name} is  {n2w(revenue)} dollars"
    speak(vocal_results)

    results = f"The total revenue of {company_name} is  ${revenue}"
    return results


##########################################################################################
def getMarketCap(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    revenue = round(stock_data.info['marketCap'], 2)

    vocal_results = f"The market capitalisation of {company_name} is {n2w(revenue)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The market capitalisation of {company_name} is {getSymbol({companyData[company_name]['currency']})}{n2w(revenue)}"
    return results
##########################################################################################


def get52WeekLow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    ftwl = round(stock_data.info['fiftyTwoWeekLow'], 2)

    vocal_results = f"The fifty two week low of {company_name} is {n2w(ftwl)} {getSymbol(companyData[company_name]['currency'])}"
    speak(vocal_results)

    results = f"The fifty two week low of {getSymbol(companyData[company_name]['currency'])}{revenue}{company_name}"
    return results
##########################################################################################


def get52WeekHigh(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    ftwh = round(stock_data.info['fiftyTwoWeekHigh'], 2)

    vocal_results = f"The fifty two week high of {company_name} is  {n2w(ftwh)} {getSymbol(companyData[company_name]['currency'])}"
    speak(vocal_results)

    results = f"The fifty two week high of {getSymbol(companyData[company_name]['currency'])}{ftwh}{company_name}"
    return results


##########################################################################################
def getFreeCashFlow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    fcf = round(stock_data.info['freeCashflow'], 2)

    speak_results = f"The free cash flow of {company_name} is {n2w(fcf)} {companyData[company_name]['currency']}"
    speak(speak_results)

    results = f"The free cash flow of {company_name} is {getSymbol(companyData[company_name]['currency'])}{fcf}"
    return results
##########################################################################################


def getOperatingCashFlow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    ocf = round(stock_data.info['operatingCashflow'], 2)

    vocal_results = f"The operating cash flow of {company_name} is {n2w(ocf)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The operating cash flow of {company_name} is {getSymbol({companyData[company_name]['currency']})}{ocf}"
    return results

##########################################################################################


def getEps(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    eps = round(stock_data.info['trailingEps'], 2)

    vocal_results = f"The earnings per share of {company_name} is {n2w(eps)}{companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The earnings per share of {company_name} is {getSymbol(companyData[company_name]['currency'])}{eps}"
    return results
##########################################################################################


def getPeRatio(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    pe_ratio = round(stock_data.info['trailingPE'], 2)

    vocal_results = f"The price to earnings ratio of {company_name} is {n2w(pe_ratio)}"
    speak(vocal_results)

    # print(pe_ratio)
    if pe_ratio < 10:
        speak("Elvis thinks right now it is not good for investment but still you can keep it on watch")
    elif 10 <= pe_ratio <= 15:
        speak("Elvis thinks it can be considered for long term profits, still you can keep it on watch")
    elif 20 < pe_ratio <= 30:
        speak("Elvis thinks you can consider to invest")
    else:
        speak("Elvis thinks its high right now and should hold")

   # speak(
   #     "All such information is for assistance only and shall not be taken as the sole basis for making any investment decision.")

    results = f"The price to earnings ratio  of {company_name} is {pe_ratio}"
    return results

##########################################################################################


def getEbitda(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    ebitda = round(stock_data.info['ebitda'], 2)

    vocal_results = f"The EBITDA of {company_name} is {n2w(ebitda)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The EBITDA of {company_name} is {getSymbol(companyData[company_name]['currency'])}{ebitda}"
    return results

##########################################################################################


def getPriceToBook(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    price_to_book = round(stock_data.info['priceToBook'], 2)

    vocal_results = f"Price to book ratio of {company_name} is {n2w(price_to_book)}"
    speak(vocal_results)

    results = f"Price to book ratio of {n2w(company_name)} is {price_to_book}"
    return results

##########################################################################################


def getDebtToEquity(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    d2e = round(stock_data.info['debtToEquity'], 2)

    vocal_results = f"The debt to equity ratio of {company_name} is {n2w(d2e)}"
    speak(vocal_results)

    results = f"The debt to equity ratio of {company_name} is {d2e}"
    return results


##########################################################################################

def getTargetHighPrice(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    tp = round(stock_data.info['targetHighPrice'], 2)

    vocal_results = f"The target high price of {company_name} is {n2w(tp)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The target high price of {company_name} is {getSymbol(companyData[company_name]['currency'])}{tp}"
    return results

##########################################################################################


def getForwardEps(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    feps = round(stock_data.info['forwardEps'], 2)

    vocal_results = f"The forward earnings per share of {company_name} is {n2w(feps)}, {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The forward earnings per share of {company_name} is {getSymbol(companyData[company_name]['currency'])}{feps}"
    return results


##########################################################################################

def getForwardPe(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    feps = round(stock_data.info['forwardPE'], 2)

    vocal_results = f"The forward price to earning ratio of {company_name} is {n2w(feps)}"
    speak(vocal_results)

    results = f"The forward price to earning ratio of {company_name} is {feps}"
    return results

##########################################################################################


def getFiftyDma(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    fiftyDma = round(stock_data.info['fiftyDayAverage'], 2)

    vocal_results = f"The fifty day moving average of {company_name} is {n2w(fiftyDma)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The fifty day moving average of {company_name} is {getSymbol(companyData[company_name]['currency'])}{fiftyDma}"
    return results

##########################################################################################


def getPegRatio(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    peg = round(stock_data.info['trailingPegRatio'], 2)

    vocal_results = f"The price earnings to growth ratio of {company_name} is {n2w(peg)}"
    speak(vocal_results)

    results = f"The price earnings to growth ratio of {company_name} is {peg}"
    return results

##########################################################################################


def getDividendRate(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    divRate = round(stock_data.info['dividendRate'], 2)

    vocal_results = f"The dividend rate of {company_name} is {n2w(divRate)}"
    speak(vocal_results)

    results = f"The dividend rate of {company_name} is {divRate}"
    return results
##########################################################################################


def getLastDividendValue(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    ldiv = round(stock_data.info['lastDividendValue'], 2)

    vocal_results = f"The last dividend value of {company_name} is {n2w(ldiv)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The last dividend value of {company_name} is {getSymbol(companyData[company_name]['currency'])}{ldiv}"
    return results

##########################################################################################


def get52WeekChange(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    weekchng = round(stock_data.info['52WeekChange'], 2)

    vocal_results = f"The fifty two week change of {company_name} is {n2w(weekchng)} percent"
    speak(vocal_results)

    results = f"The fifty two week change of {company_name} is %{weekchng}"
    return results
##########################################################################################


def getPreviousClose(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    prevclose = round(stock_data.info['previousClose'], 2)

    vocal_results = f"The previous close of {company_name} is {n2w(prevclose)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The previous close of {company_name} is {getSymbol(companyData[company_name]['currency'])}{prevclose}"
    return results
##########################################################################################


def getRegularMarketOpen(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    openprice = round(stock_data.info['regularMarketOpen'], 2)

    vocal_results = f"The opening price of {company_name}, is {n2w(openprice)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The opening price of {company_name}, is {getSymbol(companyData[company_name]['currency'])}{openprice}"
    return results

##########################################################################################


def getRegularMarketDayLow(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    daylow = round(stock_data.info['regularMarketDayLow'], 2)

    vocal_results = f"The day low price of {company_name} is {n2w(daylow)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The day low price of {company_name} is {daylow}"
    return results

##########################################################################################


def getRegularMarketDayHigh(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    dayhigh = round(stock_data.info['regularMarketDayHigh'], 2)

    vocal_results = f"The day high price of {company_name} is {n2w(dayhigh)} {companyData[company_name]['currency']}"
    speak(vocal_results)

    results = f"The day high price of {company_name} is {getSymbol(companyData[company_name]['currency'])}{dayhigh}"
    return results

##########################################################################################


def getSector(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    sec = stock_data.info['sector']

    vocal_results = f"The {company_name} belongs to {sec} sector"
    speak(vocal_results)
    return vocal_results

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
        return getStockPrice(query)

    elif intent == 'getTotalRevenue':
        return getTotalRevenue(query)

    elif intent == 'getMarketCap':
        return getMarketCap(query)

    elif intent == 'get52WeekLow':
        return get52WeekLow(query)

    elif intent == 'get52WeekHigh':
        return get52WeekHigh(query)

    elif intent == 'getFreeCashFlow':
        return getFreeCashFlow(query)

    elif intent == 'getOperatingCashFlow':
        return getOperatingCashFlow(query)

    elif intent == 'getEps':
        return getEps(query)

    elif intent == 'getPeRatio':
        return getPeRatio(query)

    elif intent == 'getEbitda':
        return getEbitda(query)

    elif intent == 'getPriceToBook':
        return getPriceToBook(query)

    elif intent == 'getDebtToEquity':
        return getDebtToEquity(query)

    elif intent == 'getTargetHighPrice':
        return getTargetHighPrice(query)

    elif intent == 'getForwardEps':
        return getForwardEps(query)

    elif intent == 'getForwardPe':
        return getForwardPe(query)

    elif intent == 'getFiftyDma':
        return getFiftyDma(query)

    elif intent == 'getPegRatio':
        return getPegRatio(query)

    elif intent == 'getDividendRate':
        return getDividendRate(query)

    elif intent == 'getLastDividendValue':
        return getLastDividendValue(query)

    elif intent == 'get52WeekChange':
        return get52WeekChange(query)

    elif intent == 'getPreviousClose':
        return getPreviousClose(query)

    elif intent == 'getRegularMarketOpen':
        return getRegularMarketOpen(query)

    elif intent == 'getRegularMarketDayLow':
        return getRegularMarketDayLow(query)

    elif intent == 'getRegularMarketDayHigh':
        return getRegularMarketDayHigh(query)

    elif intent == 'getSector':
        return getSector(query)

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
