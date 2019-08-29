def favorable_increment(previous_y, current_y, end_y, threshold):
    # current value breaks the threshold
    # with respect to the best max checkpoint
    # thus, it is infavorable increment
    if (end_y-current_y)/float(current_y) < threshold:
        return False

    # favorable; WIP: should current exceed some threshold less than previous?
    # incrementing the min index decreased the value
    if current_y <= previous_y:
        return True
    else:
        return False

def favorable_decrement(previous_y, current_y, start_y, threshold):
    # current value breaks the threshold
    # with respect to the best max checkpoint
    # thus, it is infavorable increment
    if (current_y - start_y)/float(current_y) < threshold:
        return False

    # favorable; WIP: should current exceed some threshold less than previous?
    # incrementing the min index decreased the value
    if current_y <= previous_y:
        return True
    else:
        return False

def search_window(data, threshold):
    """
    Args:
        data - a list of (x, y) points
        threshold - minimum percent difference for values to be returned
    Returns:
        start
        end
    """
    if threshold == 0: return None, None
    
    start = best_start = 1
    end = best_end = len(data) - 2
    
    while start <= end:
        if favorable_increment(data[start-1][1], data[start][1], data[best_end][1], threshold):
            best_start = start
        if favorable_decrement(data[end+1][1], data[end][1], data[best_start][1], threshold):
            best_end = end

        start += 1
        end -= 1
    
    if best_end <= best_start: return None, None

    diff = float(data[best_end][1])/data[best_start][1]
    if threshold < 0 and (diff - 1) <= threshold:
        return best_start, best_end
    elif threshold <= diff:
        return best_start, best_end
    else:
        return None, None

def merge(l, y):
    """
    Interval merginging function
    Args:
        l - a list of intervals [[1,2], [2, 3]...]
    Returns:
        a list of a merged intervals [[1, 3]]
    """
    if not l: return []
    result = [l[0]]
    for i in range(1, len(l)):
        if result[-1][0] == result[-1][1]:
            result = result[:-1]
        interval = l[i]
        if interval[0] <= result[-1][1]:
            result[-1][0] = interval[0] if y[interval[0]] <= y[result[-1][0]] else result[-1][0]
            result[-1][1] = interval[1] if y[result[-1][1]] <= y[interval[1]] else result[-1][1]
        else:
            result.append(interval)

    return result

def find(data, threshold, window_size=None, merge_intervals=True):
    """
    Args:
        data - a list (x, y) points
        threshold - percentage threshold for defining a breakout
        window_size - int representing the sliding search window (number of points)
        mrege_intervals - boolean flag whether or not to merge overlapping breakouts
    Returns:
        a list of [(start, end),...] that indicate a % change of p. start and end are indices of data
    """
    if not window_size:
        window_size = int(len(data)/10)

    result = []
    # iterate each row on a sliding (slicing) window
    i = 0
    while i < len(data):
        subset = data[i:i+window_size].copy()
        
        # search for points of interest
        # start and ends are the indexes of subset that indicate a breakout
        start, end = search_window(subset, threshold)
        
        # adjust the indexes so that they're global indexes
        
        if start is not None and end is not None:
            start += i
            end += i
            i = start+1
            result.append([start, end])
        else:
            i += 1
    y = [p[1] for p in data]
    return result if not merge_intervals else merge(sorted(result), y)