Monte Carlo Scheduler
=====================

Project to use Monte Carlo Simulations from historical data to estimate project completion dates.

#Usage
To run simulations based on historical and future data, use the **runSimulationFromFiles()** method as follows:
```
runSimulationFromFiles(historicalFileName,futureFileName,[verbose=False],[trials=10000])
```
The *verbose* and *trials* parameters are optional and have sensible defaults (non-verbose, and 10000 trials).

#Input File Formats


#Function Breakdown 

##loadData(historicalFileName, futureFileName)
	Loads historical and future data from a file.
	Input:	historicalFileName	= filename containing historical task data
			futureFileName		= filename containing future task data
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
	Runs a sample data set.

## runSimulationFromFiles(historicalFileName,futureFileName,verbose=False,trials=10000):
	Runs a simulation based on historical and future data sets.