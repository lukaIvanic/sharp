import requests
import csv
import time
import config
import os

CRYPTOCURRENCY = 'ETH'
FOLDER_PATH = f'./HistoricalData/{CRYPTOCURRENCY}USD/'

def fileNameFromDate(endDate):
    return f'{FOLDER_PATH}{"_".join(endDate.split("-"))}_{CRYPTOCURRENCY}.csv'


def getNextEndDate(currEndDate):
    filename = fileNameFromDate(currEndDate)
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            last_row = None
            for row in reader:
                last_row = row
            if last_row:
                newEndDate = last_row[0].split(" ")[0]
                return newEndDate
            else:
                print("Something is wrong with " + filename)
                quit()
                return None
    except FileNotFoundError:
        print("Couldn't open file " + filename)
        quit()
        return None


def getData(endDate):
    url = "https://api.twelvedata.com/time_series"
    symbolAndExchange = f'{CRYPTOCURRENCY}/USD:Binance'
    timeInterval = "15min"
    outputSize = 52 * 24 * 4 + 1  # The +1 is so I we can get the previous date without having to calculate it
    apiKey = config.API_KEY
    format = "CSV"
    delimiter = ","

    params = {
        "symbol": symbolAndExchange,
        "interval": timeInterval,
        "outputsize": outputSize,
        "end_date": endDate,
        "apikey": apiKey,
        "format": format,
        "delimiter": delimiter
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Failed to retrieve data. Status code:", response.status_code)
        quit()

    file_name = fileNameFromDate(endDate)
    with open(file_name, 'wb') as f:
        f.write(response.content)

    print("File saved as:", file_name)

    time.sleep(30)

    getData(getNextEndDate(endDate))

getData("2023-06-07")
