import sys
import pandas as pd
from collections import deque
import csv

def favorable_min_increment(previous, current, maxCheckpoints, threshold):
    # peek the popping tuple (the best max checkpoint so far)
    maxPair = maxCheckpoints[-1]

    # current value breaks the threshold
    # with respect to the best max checkpoint
    # thus, it is infavorable increment
    if (maxPair[1]-current)/float(current) < threshold:
        return False

    # favorable; WIP: should current exceed some threshold less than previous?
    # incrementing the min index decreased the value
    if current <= previous:
        return True
    else:
        return False



def favorable_max_decrement(previous, current, minCheckpoints, threshold):
    # peek the popping tuple (the best min checkpoint so far)
    minPair = minCheckpoints[-1]


    # current value breaks the threshold
    # with respect to the best min checkpoint
    # thus, it is infavorable decrement
    if float(current)-minPair[1] / float(minPair[1]) < threshold:
        return False

    # WIP: decreasing the max value is favorable?
    # favorable; WIP: exceed some threshold?
    # decrementing the max index decreased the value
    if current <= previous:
        return True
    else:
        return False


def narrow_start_end(indexMin, indexMax, window, threshold):
    # init the min and max values as "previous"
    previousMinValue = window["y"].loc[indexMin]
    previousMaxValue = window["y"].loc[indexMax]

    # verify that threshold is covered



    # deque (LIFO stack) maintain checkpoints (index, value) that are considered good
    # maintains the last favorable (index, value)
    # init them with the bare minimum by pushing
    minCheckpoints = deque()
    minCheckpoints.append((indexMin, previousMinValue))

    maxCheckpoints = deque()
    maxCheckpoints.append((indexMax, previousMaxValue))


    while indexMin <= indexMax:
        # check the next min value
        indexMin+=1
        currentMinValue = window["y"].loc[indexMin]
        if favorable_min_increment(previousMinValue, currentMinValue, maxCheckpoints, threshold):
            minCheckpoints.append((indexMin, currentMinValue))

        # decrement indexMax
        indexMax-=1
        currentMaxValue = window["y"].loc[indexMax]
        if favorable_max_decrement(previousMaxValue, currentMaxValue, minCheckpoints, threshold):
            maxCheckpoints.append((indexMax, currentMaxValue))

        previousMinValue = currentMinValue
        previousMaxValue = currentMaxValue


    bestMinPair = minCheckpoints.pop()
    bestMaxPair = maxCheckpoints.pop()

    # validate that it covers spread
    if float(bestMaxPair[1] - bestMinPair[1])/bestMinPair[1] < threshold:
        return False, 0, 0, 0, 0


    bestMinIndex = bestMinPair[0]
    bestMaxIndex = bestMaxPair[0]

    # True -- a valid pair
    # the index of the start
    # the index of the end
    # the x value of the start
    # the x value of the end
    return True, bestMinIndex, bestMaxIndex, window["x"].loc[bestMinIndex], window["x"].loc[bestMaxIndex]



def search_window(window, threshold):

    indexMin = window["y"].idxmin()
    indexMax = window["y"].idxmax()

    # WIP: currently force directionality
    # i.e. the program only works for uptrending breakouts, not downtrending
    if indexMax < indexMin:
        return False, 0, 0, 0, 0

    # redundant / also search_window() barely does anything...
    valid, indexStart, indexEnd, xStart, xEnd = narrow_start_end(indexMin, indexMax, window, threshold)
    return valid, indexStart, indexEnd, xStart, xEnd

def main(inputFilePath, threshold, windowSize, outputFilePath):
    # load the csv data into a dataframe
    data = pd.read_csv(inputFilePath, names=["x", "y"])

    # WIP: be wary of breakout pairs with the same end index
    breakoutPairs = set()

    # iterate each row on a sliding (slicing) window
    for i in range(data.shape[0]):
        window = data.iloc[i:i+windowSize]

        # preemptive exit, because window is small
        # at the tail end of the data
        if window.shape[0] != windowSize:
            break

        # search for points of interest
        found, indexStart, indexEnd, xStart, xEnd = search_window(window, threshold)
        if found:
            breakoutPairs.add((indexStart, indexEnd))

    # save the poi
    outputfile = open(outputFilePath, 'w')
    writer = csv.DictWriter(outputfile, fieldnames=["index_start", "index_end", "x_start", "x_end"], delimiter=',')
    writer.writeheader()
    for poi in breakoutPairs:
        writer.writerow({
                        "index_start": poi[0],
                        "index_end": poi[1],
                        "x_start": data["x"][poi[0]],
                        "x_end": data["x"][poi[1]]
                        })




# WIP: could use more robust validation
def valid_args(args):
    return len(args) == 5

# initial handling
if __name__ == "__main__":
    if not valid_args(sys.argv):
        sys.exit(-1)
    main(sys.argv[1], float(sys.argv[2])/100.0, int(sys.argv[3]), sys.argv[4])
