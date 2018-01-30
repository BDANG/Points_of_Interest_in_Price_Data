import requests
import csv
import sys
import datetime
import time
from datetime import timezone
from datetime import timedelta
import pandas as pd
GDAX_BASE_URL = "https://api.gdax.com"

def parse_timestamps(args):
    startdateSplits = args[1].split("/")
    starttimeSplits = args[2].split(":")
    enddateSplits = args[3].split("/")
    endtimeSplits = args[4].split(":")

    # MM/DD/YYYY and HH:MM:SS to YYYY, MM, DD and HH, MM, SS
    startday = datetime.datetime(
                                int(startdateSplits[2]),
                                int(startdateSplits[0]),
                                int(startdateSplits[1]),
                                int(starttimeSplits[0]),
                                int(starttimeSplits[1]),
                                int(starttimeSplits[2]), tzinfo=timezone.utc)
    endday = datetime.datetime(
                                int(enddateSplits[2]),
                                int(enddateSplits[0]),
                                int(enddateSplits[1]),
                                int(endtimeSplits[0]),
                                int(endtimeSplits[1]),
                                int(endtimeSplits[2]), tzinfo=timezone.utc)

    return startday, endday

def request_data(startDatetime, endDatetime, granularity):
    payload = {'start': startDatetime.isoformat(), 'end': endDatetime.isoformat(), 'granularity': granularity}

    data = requests.get(GDAX_BASE_URL+"/products/BTC-USD/candles", params=payload).json()
    df = pd.DataFrame(data, columns=["minute_timestamp", "low", "high", "open", "close", "amount"])
    #df = df.sort_values("minute_timestamp").drop("index", axis=1)
    df["price"] = df.apply(lambda row: (row["low"]+row["high"]+row["open"]+row["close"])/4,axis=1)
    return df

def main(startTimestamp, endTimestamp, granularity, outputDir):
    # list of DataFrames that are OHLC data
    dataframeList = []

    # counter for number of requests
    count = 0
    currentTimestamp = startTimestamp
    complete = False
    while not complete:
        print(currentTimestamp)
        count+=1

        # request_data() will return 300 candles since the currentTimestamp
        tdelta = timedelta(seconds=300*granularity)
        df = request_data(currentTimestamp, currentTimestamp+tdelta, granularity)
        dataframeList.append(df)
        currentTimestamp = currentTimestamp+tdelta
        time.sleep(0.5)
        if currentTimestamp > endTimestamp:
            complete = True


    print("Number of requests: "+str(count))

    # combine all of the request data
    df = pd.concat(dataframeList)
    df = df.sort_values("minute_timestamp").reset_index().drop("index", axis=1)

    print("Number of data rows: "+str(df.count()))

    # save to csv
    df.to_csv(outputDir+"gdax_"+startTimestamp.isoformat()+"_"+endTimestamp.isoformat()+".csv")

    # save to pickle -- deprecated
    # df.to_pickle(outputDir+"gdax_"+startTimestamp.isoformat()+"_"+endTimestamp.isoformat()+".pickle")



# WIP: Could use better input validation
def valid_args(args):
    if len(args) == 7:
        try:
            granularity = int(args[5])
            if granularity not in [60, 300, 900, 3600, 21600, 86400]:
                print("\n---!!!--- "+args[5]+" is not 60, 300, 900, 3600, 21600, OR 86400 ---!!!---\n")
                return False
            else:
                return True
        except:
            print("\n---!!!--- COULD NOT PARSE "+args[5]+" INTO AN INTEGER ---!!!---\n")
            return False
    else:
        return False

if __name__ == "__main__":
    if not valid_args(sys.argv):
        print("\nThe script retrieves the trade nearest to each second from specified to start and end dates.")
        print("The data is saved in a csv at a specified directory with the filename gdax_startdate_enddate.csv")
        print("\n1. the start date (MM/DD/YYYY)")
        print("2. the start time (HH:MM:SS) using 24-hour time")
        print("3. the end date (MM/DD/YYYY)")
        print("4. the end time (HH:MM:SS) using 24-hour time")
        print("5. <granularity> - the granularity of data in seconds (MUST BE 60, 300, 900, 3600, 21600, OR 86400)")
        print("6. <output_dir> - the DIRECTORY of the output")
        print("\n-----DATE/TIME FORMAT SPECIFIC-----\nRun as python "+sys.argv[0]+" MM/DD/YYYY HH:MM:SS MM/DD/YYYY HH:MM:SS <granularity> <output_dir>\n-----DATE/TIME FORMAT SPECIFIC-----")
        sys.exit(-1)

    startTimestamp, endTimestamp = parse_timestamps(sys.argv)
    main(startTimestamp, endTimestamp, int(sys.argv[5]), sys.argv[6])
