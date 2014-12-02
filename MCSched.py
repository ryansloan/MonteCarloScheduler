from random import *
from matplotlib.pyplot import *
'''
Inputs:
	Historical Data: CSV containing:
		Task, Estimated, Actual
	Future Data: CSV containing:
		Task, Estimated
	Start Date?

'''
def loadData(historicalFileName, futureFileName):
	'''
	Input: historicalFileName, futureFileName
	Output: historical, future
	'''
	historical  = [["T1",8,8],["T2",8,6],["T3",15,17],["T4",8,9],["T5",8,8],["T6",8,9],["T7",12,14]]
	#historical  = [["T1",1,1],["T1",1,2]]
	future 		= [["T8",8],["T9",16],["T10",4],["T11",8],["T12",12]]
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
	print("Estimated: "+str(estTotal))
	for i in range(0,n):
		predictedTotal = runSimulation(historical,future)
		#print ("Trial "+str(i)+" prediction: "+str(predictedTotal)+" ("+str(100*predictedTotal/estTotal)+"%)")
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
		#if (verbose):
			#print("Value: {0:.2f}, occurrences: {1}".format(p,c))
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
			print("Total: {0} (Confidence: {1:.2f}%)".format(prediction[0],trialsSoFar/totalTrials*100))
		confidenceRatings.append([prediction[0],trialsSoFar/totalTrials*100])
	return(confidenceRatings)

def runSample():
	matplotlib.pyplot.clf()
	historical, future 	= loadData("","")
	simulationData 		= runSimulations(historical, future,1000)
	summaryData 		= summarize(simulationData)
	confidenceData 		= computeConfidence(summaryData)
	x = [item[0] for item in confidenceData]
	y = [item[1] for item in confidenceData]
	perfectEstimate = sum([item[1] for item in future])
	matplotlib.pyplot.plot(x,y,'o')
	matplotlib.pyplot.vlines(perfectEstimate,0,100,linestyles='dotted')
	matplotlib.pyplot.xlabel("Hours")
	matplotlib.pyplot.ylabel("Confidence")
	matplotlib.pyplot.show()

def runSimulationFromFiles(historicalFileName,futureFileName,verbose=False,trials=10000):
	if (not verbose):
		print("Running in quiet mode. For full output, supply verbose=True as a parameter. (Warning: it's noisy!)")
	print("Running {0} trials. Set parameter trials to customize, default is 10000".format(trials))
	if (trials<10000):
		print("Tip: Fewer trials = faster runs, but less accuracy!")
	matplotlib.pyplot.clf()
	historical, future 	= loadData(historicalFileName,futureFileName)
	simulationData 		= runSimulations(historical, future,trials,verbose)
	summaryData 		= summarize(simulationData,verbose)
	confidenceData 		= computeConfidence(summaryData,verbose)
	x = [item[0] for item in confidenceData]
	y = [item[1] for item in confidenceData]
	perfectEstimate = sum([item[1] for item in future])
	matplotlib.pyplot.plot(x,y,'o')
	matplotlib.pyplot.vlines(perfectEstimate,0,100,linestyles='dotted')
	matplotlib.pyplot.xlabel("Hours")
	matplotlib.pyplot.ylabel("Confidence")
	matplotlib.pyplot.show()
