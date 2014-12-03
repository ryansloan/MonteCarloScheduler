Monte Carlo Scheduler
=====================

Project to use Monte Carlo Simulations from historical data to estimate project completion dates.

#Usage
To run the model based on historical and future data, you have two options.
##To load files containing historical or future data:
Use the **runModelFromFiles()** method as follows:
```
runModelFromFiles(historicalFileName,futureFileName[,verbose=False,trials=10000,plot=True])
```
The **verbose**, **trials**, and **plot** parameters are optional and have sensible defaults (not verbose, and 10000 trials, True - draw plot).

##To supply your own data as lists:
Use the **runModelFromData()** method as follos:
```
runModelFromData(historicalData,FutureData[verbose=False,trials=10000,plot=True])
```
Same optional parameters apply from above. Input data must be in format:
```
historical: [[name,est,actual],[name,est,actual],...]
future: 	[[name,est],[name,est],...]
```
##Output

Running runModelFromFiles will yield something like this:
```
>>> MCSched.runModelFromFiles("historical.txt","future.txt")
Running in quiet mode. For full output, supply verbose=True as a parameter. (Warning: it's noisy!)
Running 10000 trials. Set parameter trials to customize, default is 10000
Estimated Total: 48
Min:38.40 (80.00% of estimated)
Max:138.00 (287.50% of estimated)
```
If plot=True, it will also display a PyPlot graph like this one:
![Graph of Hours Remaining and Confidence](http://ryanjsloan.com/ConfidenceGraph.png)
*The vertical dotted line indicates the sum of the original estimated hours*

#Input File Formats
CSV or TAB delimited should work, but I haven't tested extensively. Header row is optional.
```
"Task 1",8,10
"Task 2",8,6
"Task 3",15,17
```
The file for future work doesn't require the third column, obviously. For more info, check out sample files testData_historical.csv and testData_future.csv.

#Function Breakdown 

##loadData(historicalFileName, futureFileName)
	Loads historical and future data from a file.
	Input:	historicalFileName	= filename of file containing historical task data
			futureFileName		= filename of file containing future task data
	Output: historical 			= list of historical data in the format: [[TaskName, estimated, actual], ...]
			future 				= list of future data in the format: [[TaskName, estimated], ...]

## runSimulations(historical,future,n=1,verbose=False):
	Runs n simulations of future data based on historical data.
	Input: 	historical 	= list of lists in the format: [[TaskName, estimated, actual], ...]
			future 		= list of lists in the format: [[TaskName, estimated], ...]
			n 			= number of simulations to run
    Output: 

## runSimulation(historical,future):
	Runs a single simulation of future data based on historical data.
	Input: 	historical 		= list of lists in the format: [[TaskName, estimated, actual], ...]
			future 			= list of lists in the format: [[TaskName, estimated], ...]
	Output: predictedTotal 	= total cost of simulated tasks 

## summarize(data,verbose=False):
	Summarizes a list of values with duplicates to a list of values and their counts.
	Input: List of predictions
	Output: List of lists; Predictions and their counts: [[prediction, count], [prediction, count]...]


## computeConfidence(data,verbose=False):
	Comp
	Input: Prediction counts, a list of lists in format: [[prediction, count], [prediction,count]...]
	Output: Predictions with confidence percentages in format: [[prediction, percent], [prediction, percent]...]

## runSample():
	Runs a simulation for the sample CSV files provided.

## runModelFromFiles(historicalFileName,futureFileName,verbose=False,trials=10000):
	Runs a simulation based on historical and future data sets.