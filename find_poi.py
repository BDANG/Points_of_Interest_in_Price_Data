import sys
import pandas as pd

def narrow_start_end(indexMin, indexMax, window):
    while True:
        #increment indexMin

        #decrement indexMax

        # check for good checkpoint

        # adjust



def search_window(window):
    print(window)
    indexMin = window["y"].idxmin()
    indexMax = window["y"].idxmax()

    indexStart, indexEnd, xStart, xEnd = narrow_start_end(indexMin, indexMax, window)
    return True, 0, 0

def main(inputFilePath, threshold, windowSize):
    # load the csv data into a dataframe
    data = pd.read_csv(inputFilePath, names=["x", "y"])

    # iterate each row on a sliding (slicing) window
    for i in range(data.shape[0]):
        window = data.iloc[i:i+windowSize]

        # preemptive exit, because window is small
        # at the tail end of the data
        if window.shape[0] != windowSize:
            break

        # search for points of interest
        found, xstart, xend = search_window(window)
        if found:
            break

    # save the poi

# WIP: could use more robust validation
def valid_args(args):
    return len(args) == 4

# initial handling
if __name__ == "__main__":
    if not valid_args(sys.argv):
        sys.exit(-1)
    main(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]))
