import json
import os
import webbrowser
from datetime import *

import mplfinance as mpf
import pyttsx3
import speech_recognition as sr
import yfinance as yf
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from num2words import num2words as n2w

import sqlite3
from sqlite3 import Error

Builder.load_file('elvis_design.kv')

##########################################################################################
voiceEngine = None
companyData = None
intentsData = None
conn = None


##########################################################################################
class MainWidget(Widget):
    def runElvis(self):
        self.ids.img.source = ''
        self.ids.img.opacity = 0
        programInit()
        greet()
        userVoiceCommand = getUserVoiceCommand()
        toDisplay = processCommand(userVoiceCommand)

        try:
            if toDisplay.endswith('.png'):
                self.ids.img.source = toDisplay
                self.ids.img.opacity = 1

            else:
                toDisplay = addNewLine(toDisplay)
                self.ids.output_screen.text = toDisplay

        except:
            pass

        if conn:
            print("Closing elvis_db connection...")
            conn.close()


##########################################################################################
class ElvisApplication(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainWidget()


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

    connectToDatabase()
    createInitialTables()


##########################################################################################
def connectToDatabase():
    global conn
    try:
        conn = sqlite3.connect("elvis_data.db")
        print("Connected to elvis db...")
    except Error as e:
        print(e)


##########################################################################################
def createInitialTables():
    global conn
    sql_create_watchlist_table = """ CREATE TABLE IF NOT EXISTS watchlist (
                                            id INTEGER PRIMARY KEY,
                                            stock_name TEXT NOT NULL UNIQUE,
                                            stock_ticker TEXT NOT NULL UNIQUE
                                        ); """

    sql_create_portfolio_table = """ CREATE TABLE IF NOT EXISTS portfolio (
                                                id INTEGER PRIMARY KEY,
                                                stock_name TEXT NOT NULL UNIQUE,
                                                stock_ticker TEXT NOT NULL UNIQUE,
                                                number_of_shares FLOAT
                                            ); """

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_watchlist_table)
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_portfolio_table)
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")


##########################################################################################################################
def addStockToWatchlist(query):
    global conn

    companyNameAndTicker = getCompanyNameAndTicker(query)
    if companyNameAndTicker is not None:
        sql = '''INSERT INTO watchlist(stock_name, stock_ticker)
                      VALUES(?, ?);'''
        data_tuple = (companyNameAndTicker[0], companyNameAndTicker[1])
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(sql, data_tuple)
                conn.commit()
            except Error as e:
                print("Cannot insert into table. Failed.")
        else:
            print("Error! cannot create the database connection.")
    else:
        print("Could not fetch company name from list.")


##########################################################################################
def removeStockFromWatchlist(query):
    global conn

    companyNameAndTicker = getCompanyNameAndTicker(query)
    if companyNameAndTicker is not None:
        sql = """DELETE from watchlist where id = (SELECT id FROM watchlist WHERE stock_name = ?);"""
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(sql, (companyNameAndTicker[0],))
                conn.commit()
            except Error as e:
                print("No such stock found in watchlist.")
        else:
            print("Error! cannot create the database connection.")
    else:
        print("Could not fetch company name from list.")


##########################################################################################
def removeAllStocksFromWatchlist():
    global conn
    sql = """DELETE from watchlist;"""
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")


##########################################################################################
def getWatchlistFromDatabase():
    global conn
    rows = None
    sql = """SELECT * FROM watchlist;"""
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")

    return rows


##########################################################################################
def addNumberOfSharesToPortfolio(query):
    numberOfShares = [int(i) for i in query.split() if i.isdigit()]
    if len(numberOfShares) == 1:
        companyNameAndTicker = getCompanyNameAndTicker(query)
        # if companyNameAndTicker:

        # work here
        #     sql = ''' INSERT INTO watchlist(stock_name, stock_ticker, current_price)
        #                   VALUES(?, ?, ?); '''
        #     data_tuple = (companyNameAndTicker[0], companyNameAndTicker[1], 0)
        #     if conn is not None:
        #         try:
        #             cur = conn.cursor()
        #             cur.execute(sql, data_tuple)
        #             conn.commit()
        #         except Error as e:
        #             print("Already exists in watchlist.")
        #     else:
        #         print("Error! cannot create the database connection.")
        # else:
        #     print("Could not fetch company name from list.")

    else:
        print("Multiple numbers found in query. Failed to update portfolio.")
        return


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

    return query.lower().strip()


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

    company_name = ""

    if "of" in query:
        start_index = query.split().index('of')
        company_name = " ".join(query.split()[start_index + 1:])
    elif "to watchlist" in query or "to watch list" in query:
        start_index = query.split().index('add')
        end_index = query.split().index('to')
        company_name = " ".join(query.split()[start_index + 1:end_index])
    elif "from watchlist" in query or "from watch list" in query:
        start_index = query.split().index('remove')
        end_index = query.split().index('from')
        company_name = " ".join(query.split()[start_index + 1:end_index])

    company_name = company_name.title()
    try:
        ticker = companyData[company_name]['company_ticker']
        return [company_name, ticker]

    except Exception as e:
        print(e)
        # results = f"It seems you have said an invalid company name, please say a valid name and try again"
        # speak(results)


##########################################################################################
def exceptions(query):
    vocal_results = f"Sorry, the data is not available"
    speak(vocal_results)

    results = f"Sorry, the data is not available"
    return results


##########################################################################################
def getStockPrice(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)

    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        price = round(stock_data.info['currentPrice'], 2)
        vocal_results = f"The last trading price of {company_name}, is {n2w(price)}{companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The last trading price of {company_name}, is {getSymbol(companyData[company_name]['currency'])}{price}"
        return results

    except:
        exceptions(query)


##########################################################################################
def addNewLine(str):
    if (len(str) > 38):
        chunks = [str[i:i + 38] for i in range(0, len(str), 38)]
        # print(chunks)
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
    try:
        revenue = round(stock_data.info['totalRevenue'], 2)

        vocal_results = f"The total revenue of {company_name} is  {n2w(revenue)} dollars"
        speak(vocal_results)

        results = f"The total revenue of {company_name} is  ${revenue}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getMarketCap(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        marketcap = round(stock_data.info['marketCap'], 2)

        vocal_results = f"The market capitalisation of {company_name} is {n2w(marketcap)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The market capitalisation of {company_name} is {getSymbol({companyData[company_name]['currency']})}{(marketcap)}"
        return results

    except:
        exceptions(query)


##########################################################################################
def get52WeekLow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:

        ftwl = round(stock_data.info['fiftyTwoWeekLow'], 2)

        vocal_results = f"The fifty two week low of {company_name} is {n2w(ftwl)} {getSymbol(companyData[company_name]['currency'])}"
        speak(vocal_results)

        results = f"The fifty two week low of {company_name} is {getSymbol(companyData[company_name]['currency'])}{ftwl}"
        return results

    except:
        exceptions(query)


##########################################################################################
def get52WeekHigh(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        ftwh = round(stock_data.info['fiftyTwoWeekHigh'], 2)

        vocal_results = f"The fifty two week high of {company_name} is  {n2w(ftwh)} {getSymbol(companyData[company_name]['currency'])}"
        speak(vocal_results)

        results = f"The fifty two week high of {company_name} is {getSymbol(companyData[company_name]['currency'])}{ftwh}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getFreeCashFlow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        fcf = round(stock_data.info['freeCashflow'], 2)

        speak_results = f"The free cash flow of {company_name} is {n2w(fcf)} {companyData[company_name]['currency']}"
        speak(speak_results)

        results = f"The free cash flow of {company_name} is {getSymbol(companyData[company_name]['currency'])}{fcf}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getOperatingCashFlow(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        ocf = round(stock_data.info['operatingCashflow'], 2)

        vocal_results = f"The operating cash flow of {company_name} is {n2w(ocf)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The operating cash flow of {company_name} is {getSymbol({companyData[company_name]['currency']})}{ocf}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getEps(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        eps = round(stock_data.info['trailingEps'], 2)

        vocal_results = f"The earnings per share of {company_name} is {n2w(eps)}{companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The earnings per share of {company_name} is {getSymbol(companyData[company_name]['currency'])}{eps}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getPeRatio(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        pe_ratio = round(stock_data.info['trailingPE'], 2)

        vocal_results = f"The price to earnings ratio of {company_name} is {n2w(pe_ratio)}"
        speak(vocal_results)
        # print(pe_ratio)
        if pe_ratio < 10:
            speak(
                "Elvis thinks right now it is not good for investment but still you can keep it on watch")
        elif 10 <= pe_ratio <= 15:
            speak(
                "Elvis thinks it can be considered for long term profits, still you can keep it on watch")
        elif 20 < pe_ratio <= 30:
            speak("Elvis thinks you can consider to invest")
        else:
            speak("Elvis thinks its high right now and should hold")

        # speak(
        #     "All such information is for assistance only and shall not be taken as the sole basis for making any investment decision.")

        results = f"The price to earnings ratio  of {company_name} is {pe_ratio}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getEbitda(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        ebitda = round(stock_data.info['ebitda'], 2)

        vocal_results = f"The EBITDA of {company_name} is {n2w(ebitda)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The EBITDA of {company_name} is {getSymbol(companyData[company_name]['currency'])}{ebitda}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getPriceToBook(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        price_to_book = round(stock_data.info['priceToBook'], 2)

        vocal_results = f"Price to book ratio of {company_name} is {n2w(price_to_book)}"
        speak(vocal_results)

        results = f"Price to book ratio of {(company_name)} is {price_to_book}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getDebtToEquity(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        d2e = round(stock_data.info['debtToEquity'], 2)

        vocal_results = f"The debt to equity ratio of {company_name} is {n2w(d2e)}"
        speak(vocal_results)

        results = f"The debt to equity ratio of {company_name} is {d2e}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getTargetHighPrice(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        tp = round(stock_data.info['targetHighPrice'], 2)

        vocal_results = f"The target high price of {company_name} is {n2w(tp)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The target high price of {company_name} is {getSymbol(companyData[company_name]['currency'])}{tp}"
        return results

    except:
        exceptions(query)


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

    try:
        feps = round(stock_data.info['forwardPE'], 2)

        vocal_results = f"The forward price to earning ratio of {company_name} is {n2w(feps)}"
        speak(vocal_results)

        results = f"The forward price to earning ratio of {company_name} is {feps}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getFiftyDma(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        fiftyDma = round(stock_data.info['fiftyDayAverage'], 2)

        vocal_results = f"The fifty day moving average of {company_name} is {n2w(fiftyDma)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The fifty day moving average of {company_name} is {getSymbol(companyData[company_name]['currency'])}{fiftyDma}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getPegRatio(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        peg = round(stock_data.info['trailingPegRatio'], 2)

        vocal_results = f"The price earnings to growth ratio of {company_name} is {n2w(peg)}"
        speak(vocal_results)

        results = f"The price earnings to growth ratio of {company_name} is {peg}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getDividendRate(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        divRate = round(stock_data.info['dividendRate'], 2)

        vocal_results = f"The dividend rate of {company_name} is {n2w(divRate)}"
        speak(vocal_results)

        results = f"The dividend rate of {company_name} is {divRate}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getLastDividendValue(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        ldiv = round(stock_data.info['lastDividendValue'], 2)
        vocal_results = f"The last dividend value of {company_name} is {n2w(ldiv)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The last dividend value of {company_name} is {getSymbol(companyData[company_name]['currency'])}{ldiv}"
        return results

    except:
        exceptions(query)


##########################################################################################
def get52WeekChange(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)
    try:
        weekchng = round(stock_data.info['52WeekChange'], 2)

        vocal_results = f"The fifty two week change of {company_name} is {n2w(weekchng)} percent"
        speak(vocal_results)

        results = f"The fifty two week change of {company_name} is %{weekchng}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getPreviousClose(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        prevclose = round(stock_data.info['previousClose'], 2)

        vocal_results = f"The previous close of {company_name} is {n2w(prevclose)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The previous close of {company_name} is {getSymbol(companyData[company_name]['currency'])}{prevclose}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getRegularMarketOpen(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        openprice = round(stock_data.info['regularMarketOpen'], 2)

        vocal_results = f"The opening price of {company_name}, is {n2w(openprice)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The opening price of {company_name}, is {getSymbol(companyData[company_name]['currency'])}{openprice}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getRegularMarketDayLow(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        daylow = round(stock_data.info['regularMarketDayLow'], 2)

        vocal_results = f"The day low price of {company_name} is {n2w(daylow)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The day low price of {company_name} is {daylow}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getRegularMarketDayHigh(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        dayhigh = round(stock_data.info['regularMarketDayHigh'], 2)

        vocal_results = f"The day high price of {company_name} is {n2w(dayhigh)} {companyData[company_name]['currency']}"
        speak(vocal_results)

        results = f"The day high price of {company_name} is {getSymbol(companyData[company_name]['currency'])}{dayhigh}"
        return results

    except:
        exceptions(query)


##########################################################################################
def getSector(query):
    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    stock_data = yf.Ticker(ticker)

    try:
        sec = stock_data.info['sector']

        vocal_results = f"The {company_name} belongs to {sec} sector"
        speak(vocal_results)
        return vocal_results

    except:
        exceptions(query)


##########################################################################################
def displayFiveDaysCandleSticks(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    # print(ticker)
    comp = yf.Ticker(ticker)
    history = comp.history(period='5d', actions=False)

    file = 'images/' + company_name.lower() + '.png'

    if os.path.exists(file):
        os.remove(file)

    mpf.plot(history, type='candle', style='yahoo',
             volume=True, savefig=file)

    speak(f"here is the five days candle stick chart of {company_name}")

    return file


##########################################################################################
def displayFifteenDaysCandleSticks(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    comp = yf.Ticker(ticker)
    history = comp.history(period='15d', actions=False)

    file = 'images/' + company_name.lower() + '.png'

    if os.path.exists(file):
        os.remove(file)
    mpf.plot(history, type='candle', style='yahoo',
             volume=True, savefig=file)

    speak(f"here is the fifteen days candle stick chart of {company_name}")

    return file


##########################################################################################################################
def displayOneMonthCandleSticks(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    comp = yf.Ticker(ticker)
    history = comp.history(period='30d', actions=False)

    file = 'images/' + company_name.lower() + '.png'

    if os.path.exists(file):
        os.remove(file)

    mpf.plot(history, type='candle', style='yahoo',
             volume=True, savefig=file)

    speak(f"here is the one month candle stick chart of {company_name}")

    return file


##########################################################################################################################
def displayFortyFiveDaysCandleSticks(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    comp = yf.Ticker(ticker)
    history = comp.history(period='45d', actions=False)

    file = 'images/' + company_name.lower() + '.png'

    if os.path.exists(file):
        os.remove(file)

    mpf.plot(history, type='candle', style='yahoo', volume=True, savefig=file)
    speak(f"here is the forty five days candle stick chart of {company_name}")

    return file


##########################################################################################################################
def displayThreeMonthCandleSticks(query):
    global companyData

    compNameAndTicker = getCompanyNameAndTicker(query)
    company_name, ticker = compNameAndTicker[0], compNameAndTicker[1]
    comp = yf.Ticker(ticker)
    history = comp.history(period='90d', actions=False)

    file = 'images/' + company_name.lower() + '.png'

    if os.path.exists(file):
        os.remove(file)

    mpf.plot(history, type='candle', style='yahoo', volume=True, savefig=file)

    speak(f"here is the three months candle stick chart of {company_name}")
    return file


##########################################################################################################################
def googleSearch(query):
    search_term = query.split("for")[-1]
    url = f"https://google.com/search?q={search_term}"
    webbrowser.get().open(url)
    speak(f'Here is what I found for {search_term} on google')


##########################################################################################################################
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

    if intent == 'addStockToWatchlist':
        return addStockToWatchlist(query)

    elif intent == 'removeStockFromWatchlist':
        return removeStockFromWatchlist(query)

    elif intent == 'removeAllStocksFromWatchlist':
        return removeAllStocksFromWatchlist()

    elif intent == 'getStockPrice':
        return getStockPrice(query)

    elif intent == 'displayFiveDaysCandleSticks':
        return displayFiveDaysCandleSticks(query)

    elif intent == 'displayFifteenDaysCandleSticks':
        return displayFifteenDaysCandleSticks(query)

    elif intent == 'displayOneMonthCandleSticks':
        return displayOneMonthCandleSticks(query)

    elif intent == 'displayFortyFiveDaysCandleSticks':
        return displayFortyFiveDaysCandleSticks(query)

    elif intent == 'displayThreeMonthCandleSticks':
        return displayThreeMonthCandleSticks(query)

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
