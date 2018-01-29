from plotly.offline import plot
import plotly.graph_objs as go
import sys
import pandas as pd

MIN_ARGS = 4

def main(dataCsvPath, poiCsvPath, padding, outputDir=None):
    # load the entire data set into a dataframe
    data = pd.read_csv(dataCsvPath, header=0)
    xCol = data.columns[0]
    yCol = data.columns[1]

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
                x = dataSlice[xCol],
                y = dataSlice[yCol],
                name = "Data")

        startPoint = go.Scatter(
                x = [row[xCol+"_start"]],
                y = [dataSlice.loc[row["index_start"]][yCol]],
                mode = 'markers',
                name = "Start",
                line = {"color": "red"}
                )

        endPoint = go.Scatter(
                x = [row[xCol+"_end"]],
                y = [dataSlice.loc[row["index_end"]][yCol]],
                mode = 'markers',
                name = "End",
                line = {"color": "red"}
                )

        plotdata = [lineplot, startPoint, endPoint]
        plotlayout = go.Layout(
            title="Breakout between "+str(row[xCol+"_start"])+" and "+str(row[xCol+"_end"]),
            xaxis={
                "title": xCol
                },
            yaxis={
                "title": yCol
                }
        )

        figure = go.Figure(data=plotdata, layout=plotlayout)


        # outputDir != None --> save the plots
        if outputDir:
            plot(figure, filename=
                                outputDir
                                +dataCsvPath.split("/")[-1].rstrip(".csv")
                                +"_"+row[xCol+"_start"]
                                +"_"+row[xCol+"_end"])
        else: # no need to save the plots
            plot(figure)
            input("Enter to continue.")



# WIP: could use more robust validation
def valid_args(args):
    return len(args) == MIN_ARGS or len(args) == MIN_ARGS+1

if __name__ == "__main__":
    if not valid_args(sys.argv):
        print ("\nARGUMENTS:")
        print("<input_file.csv> - the original two column csv used in find_poi.py")
        print("<poi.csv> - the csv of points of interest created by find_poi.py")
        print("<padding> - an integer specifying the number of x-values to pad the left and right side of the breakout")
        print("[output_directory/] - an OPTIONAL directory for saving the plots.")
        sys.exit(-1)

    if len(sys.argv) == MIN_ARGS:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) == MIN_ARGS+1:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
