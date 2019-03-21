import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib import dates as mdates
from matplotlib import ticker
import matplotlib as mpl
from mpl_finance import candlestick_ohlc
from urllib import request
import urllib

stock = input("Enter Symbol for NSE Listed Stock : ")



def scrapedata(stock):          #Fetches data from alphavantage site into a csv file

    print("Fetching data for " + stock + " from the internet. Please wait....")
    key = 'K68R430Z51RZTGJG'

    link = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock + '.NS&outputsize=full&apikey=' + key + '&datatype=csv'

    fname = stock + '.csv'
    source = urllib.request.urlopen(link).read()

    open(fname, "wb").write(source)

    with open(fname, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for line in data:
            if (line[0] == '{'):
                print("Could not download the required data as a csv file.")
                break
            else :
                print("Successfully downloaded data for " + stock + " in a csv file.")
                break


def ProcessData(stock):

    print("Processing data from csv file for plotting..")

    date_data = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume_data = []

    fname = stock + '.csv'
    with open (fname, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter =',')
        for line in data:
            if line[0]!= 'timestamp':
                date_data.append(line[0])
                open_data.append(line[1])
                high_data.append(line[2])
                low_data.append(line[3])
                close_data.append(line[4])
                volume_data.append(line[5])


        open_val = np.array(open_data[1:], dtype=np.float)
        high_val = np.array(high_data[1:], dtype=np.float)
        low_val = np.array(low_data[1:], dtype=np.float)
        close_val = np.array(close_data[1:], dtype=np.float)
        volume_val = np.array(volume_data[1:], dtype=np.float)


        data_dates = []
        for date in date_data[1:]:
            new_Date = mdates.datestr2num(date)
            data_dates.append(new_Date)

        i = 0
        ohlc_data  = []
        while i < len(data_dates):

            stats_1_day = data_dates[i], open_val[i], high_val[i], low_val[i], close_val[i]
            ohlc_data.append(stats_1_day)
            i += 1




    print("Calculating Simple Moving Average..")
    MAL1 = input("Enter duration for first moving average : ")
    MAL2 = input("Enter duration for second moving average : ")


    n= len(close_data)
    sma1 = [None] *(n-1)
    sma2 = [None] *(n-1)

    def smafnc(arr, MAL, n=len(close_data)):   #Function to calculate Simple Moving Average
        sum = 0
        for i in range(MAL-1, n - 2):
            if (i == MAL - 1):
                for j in range(0, i):
                    sum = sum + float(close_data[j])
                arr[i] = sum / MAL
            else:
                sum = sum - float(close_data[i - MAL]) + float(close_data[i + 1])
                arr[i] = sum / MAL
        # print(arr)

    smafnc(sma1, int(MAL1))
    smafnc(sma2, int(MAL2))


    print("Plotting data for " + stock)

    dayFormatter = mdates.DateFormatter('%d-%b-%y')
    # dayFormatter2 = mdates.DateFormatter('%y%m%d')



    fig = plt.figure()
    ax1 = plt.axes()


    candlestick_ohlc(ax1, ohlc_data, width=0.5, colorup='g', colordown='r', alpha=0.8)


    ax1.xaxis.set_major_formatter(dayFormatter)


    ax1.xaxis_date()

    plt.xticks(rotation=30)
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))

    ax1.set_xlim()

    plt.xlabel("Date")
    plt.ylabel(" Stock Price")
    plt.title("Historical Data for " + stock)

    plt.grid(True)

    label1 = MAL1 + ' day Simple Moving Average'
    label2 = MAL2 + ' day Simple Moving Average'

    plt.plot(data_dates[(int(MAL1)-1):], sma1[(int(MAL1)-1):], color = '#39FF14', label = label1)
    plt.plot(data_dates[(int(MAL2)-1):], sma2[(int(MAL2)-1):], color = 'b', label = label2)
    plt.legend()
    plt.show()

    print("Plotted required chart successfully.")

scrapedata(stock)
ProcessData(stock)












































    #
    # ax2 = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4, sharex = ax1)
    # ax2.plot(date_data, volume_data, color = 'b')
    # ax2.xaxis.set_major_formatter(dayFormatter)
    # ax2.xaxis.set_major_locator(ticker.MaxNLocator(5))
    # ax2.yaxis.set_major_locator(ticker.MaxNLocator(6))
    # plt.ylabel("Volume")
    # plt.xticks(rotation=45)

