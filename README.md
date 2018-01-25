# Points of Interest in Price Data
## by Brian Dang

# Use case
The project's purpose is to indicate the start and end points whenever a variable changes a specified percent. In the realm of prices over time (stocks, cryptocurrencies), the project will be able to identify new "breakouts".

## Usage
`$ python find_poi.py <input_file.csv> <threshold> <window_size> <output_file.csv>`
* `<input_file.csv>` - a two column/header csv. i.e. timestamp, price
* `<threshold>` - a percent unit threshold that specifies what is considered a significant breakout. `<threshold>=10` represents a 10% jump.
* `<window_size>` - the size of a sliding window. The number of x-values (timestamp) per window. A single pair of start/end are located for a given window.
* `<output_file.csv>` - an output csv with 2 columns/headers: `start,end`
* Example:
    * `$ python find_poi.py gdax.csv 10 7`
    * Find's the start and end points of breakouts in `gdax.csv` where x-values are average of daily OHLC (open, high, low, close). Breakouts are defined as a 10% swing upward. The program will find a single pair of points in a 7-day window.

## Algorithm Details

### Dependencies
* Python 3.6.3
* Numpy
* Pandas
* Plot.ly (works with virtualenv more friendly than matplotlib)
