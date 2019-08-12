import sys
import pandas as pd
from collections import deque
import csv


def merge(intervals):
    '''
    Args:
        intervals - A sorted list of tuples (i1, i2, x1, y1, x2, y2)
    '''
    merged = []
    '''
    for interval in intervals:
        # if the list of merged intervals is empty or if the current
        # interval does not overlap with the previous, simply append it.
        if not merged or merged[-1][1] < interval[0]:
            merged.append(list(interval))
        else:
        # otherwise, there is overlap, so we merge the current and previous
        # intervals.
            merged[-1][1] = max(merged[-1][1], interval[1])
    '''

    for interval in intervals:
        # if the list of merged intervals is empty or if the current
        # interval does not overlap with the previous, simply append it.
        if not merged or merged[-1][1] < interval[0]:
            merged.append(list(interval))
        else: # merge the interval
            
            # first merge y1, (breakout start y value)
            merged[-1][3] = min(merged[-1][3], interval[3])

            # set x1
            merged[-1][2] = interval[2] if interval[4] == merged[-1][4] else merged[-1][2]

            # set i1
            merged[-1][0] = interval[0] if interval[4] == merged[-1][4] else merged[-1][0]
            
            # then merge y2, (breakout tail y value)
            merged[-1][5] = max(merged[-1][5], interval[5])

            # set x2
            merged[-1][4] = interval[4] if interval[5] == merged[-1][5] else merged[-1][4]

            # set i2
            merged[-1][1] = interval[1] if interval[5] == merged[-1][5] else merged[-1][1]
            
    return merged

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


def narrow_start_end_old(indexMin, indexMax, window, xCol, yCol, threshold):
    # init the min and max values as "previous"
    previousMinValue = window[yCol].loc[indexMin]
    previousMaxValue = window[yCol].loc[indexMax]

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
        currentMinValue = window[yCol].loc[indexMin]
        if favorable_min_increment(previousMinValue, currentMinValue, maxCheckpoints, threshold):
            minCheckpoints.append((indexMin, currentMinValue))

        # decrement indexMax
        indexMax-=1
        currentMaxValue = window[yCol].loc[indexMax]
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
    return True, bestMinIndex, bestMaxIndex, window[xCol].loc[bestMinIndex], window[xCol].loc[bestMaxIndex]

def narrow_start_end(indexMin, indexMax, x, y, threshold):
    # init the min and max values as "previous"
    previousMinValue = y[indexMin]
    previousMaxValue = y[indexMax]

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
        currentMinValue = y[indexMin]
        if favorable_min_increment(previousMinValue, currentMinValue, maxCheckpoints, threshold):
            minCheckpoints.append((indexMin, currentMinValue))

        # decrement indexMax
        indexMax-=1
        currentMaxValue = y[indexMax]
        if favorable_max_decrement(previousMaxValue, currentMaxValue, minCheckpoints, threshold):
            maxCheckpoints.append((indexMax, currentMaxValue))

        previousMinValue = currentMinValue
        previousMaxValue = currentMaxValue


    bestMinPair = minCheckpoints.pop()
    bestMaxPair = maxCheckpoints.pop()

    # validate that it covers spread
    if float(bestMaxPair[1] - bestMinPair[1])/bestMinPair[1] < threshold:
        return False, 0, 0, 0, 0, 0, 0


    bestMinIndex = bestMinPair[0]
    bestMaxIndex = bestMaxPair[0]

    # True -- a valid pair
    # the index of the start
    # the index of the end
    # the x value of the start
    # the x value of the end
    return True, bestMinIndex, bestMaxIndex, x[bestMinIndex], x[bestMaxIndex], y[bestMinIndex], y[bestMaxIndex]


def search_window(x, y, threshold):

    indexMin = 0
    indexMax = len(x)-1

    # WIP: currently force directionality
    # i.e. the program only works for uptrending breakouts, not downtrending
    if indexMax < indexMin:
        return False, 0, 0, 0, 0

    # redundant / also search_window() barely does anything...
    valid, indexStart, indexEnd, xStart, xEnd, yStart, yEnd = narrow_start_end(indexMin, indexMax, x, y, threshold)
    return valid, indexStart, indexEnd, xStart, xEnd, yStart, yEnd

def find_poi_df(x, y, threshold=.05, window_size=None, merge_intervals=True):
    """
    Determine the indexes of x and y where breakouts occur.
    Args:
        x - a list or Series of scalars
        y - a list or Series of scalars
        threshold - a float; the minimum percent difference to be considered a POI (0.1 = 10%)
        window_size - an int specifying the max width of a breakout
    """
    x = x.to_list()
    y = y.to_list()

    if not window_size:
        window_size = int(len(x)/10)

    # WIP: be wary of breakout pairs with the same end index
    breakoutPairs = set()

    # iterate each row on a sliding (slicing) window
    for i in range(len(x)):
        x_subset = x[i:i+window_size].copy()
        y_subset = y[i:i+window_size].copy()

        # preemptive exit, because window is small
        # at the tail end of the data
        if len(x_subset) != window_size:
            break

        # search for points of interest
        found, indexStart, indexEnd, xStart, xEnd, yStart, yEnd = search_window(x_subset, y_subset, threshold)
        if found:
            breakoutPairs.add((indexStart+(i), indexEnd+(i), xStart, yStart, xEnd, yEnd))
    

    if merge_intervals:
        merged_intervals = merge(sorted(list(breakoutPairs)))
        return merged_intervals
    return breakoutPairs

def main(inputFilePath, threshold, windowSize, outputFilePath):
    # load the csv data into a dataframe
    data = pd.read_csv(inputFilePath, header=0)
    xCol = data.columns[0]
    yCol = data.columns[1]


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
        found, indexStart, indexEnd, xStart, xEnd = search_window(window, xCol, yCol, threshold)
        if found:
            breakoutPairs.add((indexStart, indexEnd))

    # save the poi
    outputfile = open(outputFilePath, 'w')
    writer = csv.DictWriter(outputfile, fieldnames=["index_start", "index_end", xCol+"_start", xCol+"_end"], delimiter=',')
    writer.writeheader()
    for poi in breakoutPairs:
        writer.writerow({
                        "index_start": poi[0],
                        "index_end": poi[1],
                        xCol+"_start": data[xCol][poi[0]],
                        xCol+"_end": data[xCol][poi[1]]
                        })




# WIP: could use more robust validation
def valid_args(args):
    return len(args) == 5

# initial handling
if __name__ == "__main__":
    if not valid_args(sys.argv):
        print("\nARGUMENTS:")
        print("<input_file.csv> - a two column csv. THE FIRST ROW IS A HEADER i.e. timestamp,price")
        print("<threshold> - a percent unit threshold that specifies what is considered a significant breakout. `<threshold>=10` represents a 10% jump.")
        print("<window_size> - the size of a sliding window. The number of x-values (timestamp) per window. A single pair of start/end are located for a given window.")
        print("<output_file.csv> - an output csv with 4 columns:")
        print("\tindex_start - the dataframe index for the start of the breakout")
        print("\tindex_end - the dataframe index for the end of the breakout")
        print("\t<x>_start - the x-value for the start of the breakout")
        print("\t<x>_end - the x-value for the end of the breakout")
        sys.exit(-1)
    main(sys.argv[1], float(sys.argv[2])/100.0, int(sys.argv[3]), sys.argv[4])
