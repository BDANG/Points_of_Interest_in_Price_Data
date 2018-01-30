import pandas as pd
import sys

def main(gdaxPath, selector):
    data = pd.read_csv(gdaxPath, index_col=0)
    if selector in ["price", "average", "avg"]:
        selector = "price"

    # save to csv
    data.to_csv(selector+"_"+gdaxPath.split("/")[-1],
                columns=["minute_timestamp", selector],
                index=False)



def valid_args(args):
    if len(args) == 3:
        if args[2].lower() in ["open", "high", "low", "close", "price", "average", "avg"]:
            return True
        else:
            return False
    else:
        return False

if __name__ == "__main__":
    if not valid_args(sys.argv):
        print("\nARGUMENTS:")
        print("<gdax.csv> - a gdax OHLC csv created by get_gdax_historical.py")
        print("<selector> - MUST BE:")
        print("\topen - use the open of the candlestick")
        print("\thigh - use the high of the candlestick")
        print("\tlow - use the low of the candlestick")
        print("\tclose - use the close of the candlestick")
        print("\taverage - use the average of OHLC (price column)")

        print("\nRun as python "+sys.argv[0]+" <gdax.csv> <selector>")
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2].lower())
