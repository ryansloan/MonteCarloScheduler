from random import *
from matplotlib.pyplot import *
import csv

def loadData(historicalFilename, futureFilename,verbose=False):
	'''
	Input: historicalFilename, futureFilename
	Output: historical, future
	'''
	historical 	= []
	future 		= []
	hasHeaders=False
	with open(historicalFilename) as csvfile:
		sample = csvfile.read(1024)
		hasHeaders = csv.Sniffer().has_header(sample)
		dialect = csv.Sniffer().sniff(sample)
		csvfile.seek(0)
		reader = csv.reader(csvfile,dialect)
		firstLine=True
		for row in reader:
			if (hasHeaders and firstLine):
				firstLine=False
			else:
				historical.append([row[0],int(row[1]),int(row[2])])
		if (verbose):
			print("Loaded {0} historical entries.".format(len(historical)))
	with open(futureFilename,newline=None) as csvfile:
		sample = csvfile.read(1024)
		hasHeaders = csv.Sniffer().has_header(sample)
		dialect = csv.Sniffer().sniff(sample)
		csvfile.seek(0)
		reader = csv.reader(csvfile,dialect)
		firstLine=True
		for row in reader:
			if (hasHeaders and firstLine):
				firstLine=False
			else:
	 			future.append([row[0],int(row[1])])
		if (verbose):
	 		print("Loaded {0} future entries.".format(len(future)))
	return(historical, future)


def runSimulations(historical,future,n=1,verbose=False):
	'''
	Runs n simulations of future data based on historical data.
	Input: 	historical 	= list of lists in the format: [[TaskName, estimated, actual], ...]
			future 		= list of lists in the format: [[TaskName, estimated], ...]
			n 			= number of simulations to run
	'''
	estTotal=0
	predictions=[]
	for task in future:
		estTotal+=task[1]
	print("Estimated Total: "+str(estTotal))
	for i in range(0,n):
		predictedTotal = runSimulation(historical,future)
		predictions.append(predictedTotal)
		if (verbose):
			print ("Trial {0:2} prediction: {1:.2f} ({2:.2f}% of estimated)".format(i,predictedTotal,100*predictedTotal/estTotal))
	print("Min:{0:.2f} ({1:.2f}% of estimated)\nMax:{2:.2f} ({3:.2f}% of estimated)".format(min(predictions),100*min(predictions)/estTotal,max(predictions),100*max(predictions)/estTotal))
	return(sorted(predictions))

def runSimulation(historical,future):
	'''
	Runs a single simulation of future data based on historical data.
	Input: 	historical 	= list of lists in the format: [[TaskName, estimated, actual], ...]
			future 		= list of lists in the format: [[TaskName, estimated], ...]
	'''
	predictedTotal=0
	for task in future:
		selectedEvent = historical[randint(0,len(historical)-1)]
		velocity = selectedEvent[2]/selectedEvent[1]
		predicted = velocity*task[1]
		predictedTotal+=predicted
		task.append(predicted)
	return (predictedTotal)

def summarize(data,verbose=False):
	'''
	Input: List of predictions
	Output: List of lists, predictions and their counts: [[prediction, count], [prediction, count]...]
	'''
	points = []
	output=[]
	for p in data:
		if (p not in points):
			points.append(p)
	for p in points:
		c = data.count(p)
		output.append([p,c])
	return(output)

def computeConfidence(data,verbose=False):
	'''
	Input: Prediction counts, a list of lists in format: [[prediction, count], [prediction,count]...]
	Output: Predictions with confidence percentages in format: [[prediction, percent], [prediction, percent]...]
	'''
	trialsSoFar=0
	totalTrials = sum([pred[1] for pred in data])
	confidenceRatings=[]
	for prediction in data:
		trialsSoFar+=prediction[1]
		if (verbose):
			print("Prediction: {0} (Confidence: {1:.2f}%)".format(prediction[0],trialsSoFar/totalTrials*100))
		confidenceRatings.append([prediction[0],trialsSoFar/totalTrials*100])
	return(confidenceRatings)

def runSampleModel():
	print("Running for sample files.")
	return(runModelFromFiles("testData_historical.csv","testData_future.csv"))
	

def runModelFromFiles(historicalFilename,futureFilename,verbose=False,trials=10000,plot=True):
	historical, future 	= loadData(historicalFilename,futureFilename,verbose)
	return runModelFromData(historical,future,verbose,trials,plot)

def runModelFromData(historical,future,verbose=False,trials=10000,plot=True):
	'''
	Input: Historical and Future data
	Output: Predictions with confidence in the format: [[predicted, confidence percent], [predicted, confidence percent],...]
			(List is sorted low to high based on predictions. Interpretation: "C% chance of completion by P")
	'''
	if (not verbose):
		print("Running in quiet mode. For full output, supply verbose=True as a parameter. (Warning: it's noisy!)")
	print("Running {0} trials. Set parameter trials to customize, default is 10000".format(trials))
	if (trials<10000):
		print("Tip: Fewer trials = faster runs, but less accuracy!")
	matplotlib.pyplot.clf()
	simulationData 		= runSimulations(historical, future,trials,verbose)
	summaryData 		= summarize(simulationData,verbose)
	confidenceData 		= computeConfidence(summaryData,verbose)
	perfectEstimate = sum([item[1] for item in future])
	if (plot):
		plotPredictions(confidenceData,perfectEstimate)
	return(confidenceData,perfectEstimate)

def plotPredictions(confidenceData,estimated=None):
	x = [item[0] for item in confidenceData]
	y = [item[1] for item in confidenceData]
	matplotlib.pyplot.plot(x,y,'o')
	if (estimated is not None):
		matplotlib.pyplot.vlines(estimated,0,100,linestyles='dotted')
	matplotlib.pyplot.xlabel("Hours")
	matplotlib.pyplot.ylabel("Confidence")
	matplotlib.pyplot.title('Hours to completion and confidence')
	matplotlib.pyplot.show()
