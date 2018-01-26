# Points of Interest in Price Data
## by Brian Dang

# Use case
The project's purpose is to indicate the start and end points whenever a variable changes a specified percent. In the realm of prices over time (stocks, cryptocurrencies), the project will be able to identify new "breakouts".

The tool will allow analyst, researchers, tinkerers to locate specific points of interest. These may be important for arbitrage, NLP on news, meta-market analysis, and general technical analysis.

## Usage
#### Finding the Points of Interest:

`$ python find_poi.py <input_file.csv> <threshold> <window_size> <output_file.csv>`
* `<input_file.csv>` - a two column/header csv. i.e. timestamp, price
* `<threshold>` - a percent unit threshold that specifies what is considered a significant breakout. `<threshold>=10` represents a 10% jump.
* `<window_size>` - the size of a sliding window. The number of x-values (timestamp) per window. A single pair of start/end are located for a given window.
* `<output_file.csv>` - an output csv with 2 columns/headers: `start,end`
* Example:
    * `$ python find_poi.py gdax.csv 10 7 gdax_poi.csv`
    * Find's the start and end points of breakouts in `gdax.csv` where x-values are average of daily OHLC (open, high, low, close). Breakouts are defined as a 10% swing upward. The program will find a single pair of points in a 7-day window.

#### Plotting the Points of Interest:

`$ python plot_poi.py <input_file.csv> <poi.csv> <padding> [output_directory/]`
* `<input_file.csv>` - the original two column csv used in find_poi.py the two columns represent x,y like timestamp, price
* `<poi.csv>` - the csv of points of interest created by find_poi.py
* `<padding>` - an integer specifying the number of x-values to pad the left and right side of the breakout
* `[output_directory/]` - an OPTIONAL directory for saving the plots.
* Example:
    * `$ python plot_poi.py gdax.csv gdax_poi.csv 5`
    * This plots the points of interest (10% swings) from the example with `find_poi.py` above. Each pair of POIs are padded with 5 x-values, which are a single day each. Specifiying an output directory at the end will save the plots there.

## Algorithm Details
###### Overview
A sliding window passes over the dataset and attempts to find a breakout within a given window. To find a breakout, the minimum and maximum y-values are determined -- the breakout is found between the respective x and y values. If the minimum and maximum y-values to not exceed the percent difference specified by the `threshold`, the window is short-circuited and the next sliding window is attempted. If the threshold is exceeded, a breakout exists. To narrow the breakout, the minimum (x, y) pair is incremented and the maximum (x, y) pair is decremented. With each iteration, the algorithm checks if the increment and/or decrement was "favorable" (more on this later). If it meets favorable criteria, the x-value ("checkpoint") is pushed to a LIFO stack. The narrowing process ends when the incremented and decremented x-values cross or become equivalent. At the end, the most recent favorable "checkpoint" is popped off the stack and saved.

###### Favorable Increment/Decrement:

### Dependencies
* Python 3.6.3
    - Numpy
    - Pandas
    - Plot.ly (works with virtualenv more friendly than matplotlib)
