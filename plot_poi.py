from plotly.offline import plot
import sys
import pandas as pd

MIN_ARGS = 4

def main(dataCsvPath, poiCsvPath, padding, outputDir=None):
    # load the entire data set into a dataframe
    data = pd.read_csv(dataCsvPath, names=["x", "y"])

    # load the points of interest into a dataframe
    # columns: index_start, index_end, x_start, x_end
    # former two columns are indices (row) into data
    # latter two columns are the "x" column of data
    poi = pd.read_csv(poiCsvPath)

    for index, row in poi.iterrows():
        graphStart = row["index_start"] - padding
        graphEnd = row["index_end"] + padding

        dataSlice = data.iloc[graphStart:graphEnd+1]


        # outputDir != None --> save the plots
        if outputDir:
            None
        else: # no need to save the plots
            None



# WIP: could use more robust validation
def valid_args(args):
    return len(args) == MIN_ARGS or len(args) == MIN_ARGS+1

if __name__ == "__main__":
    if not valid_args(sys.argv):
        print ("\nARGUMENTS:")
        sys.exit(-1)

    if len(sys.argv) == MIN_ARGS:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) == MIN_ARGS+1:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
