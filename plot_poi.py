from plotly.offline import plot
import plotly.graph_objs as go
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
        if graphStart < 0:
            graphStart = 0
        graphEnd = row["index_end"] + padding
        if data.shape[0]-1 < graphEnd:
            graphEnd = data.shape[0] - 1



        dataSlice = data.iloc[graphStart:graphEnd+1]

        print(graphStart, graphEnd)
        print(dataSlice)
        print(row["index_start"])
        print(row["index_end"])

        lineplot = go.Scatter(
                x = dataSlice["x"],
                y = dataSlice["y"],
                name = "Data")

        startPoint = go.Scatter(
                x = [row["x_start"]],
                y = [dataSlice.loc[row["index_start"]]["y"]],
                mode = 'markers',
                name = "Start",
                line = {"color": "red"}
                )

        endPoint = go.Scatter(
                x = [row["x_end"]],
                y = [dataSlice.loc[row["index_end"]]["y"]],
                mode = 'markers',
                name = "End",
                line = {"color": "red"}
                )

        plotdata = [lineplot, startPoint, endPoint]



        # outputDir != None --> save the plots
        if outputDir:
            plot(plotdata, filename=
                                outputDir
                                +dataCsvPath.split("/")[-1].rstrip(".csv")
                                +"_"+row["x_start"]
                                +"_"+row["x_end"])
        else: # no need to save the plots
            plot(plotdata)
            input("Enter to continue.")



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