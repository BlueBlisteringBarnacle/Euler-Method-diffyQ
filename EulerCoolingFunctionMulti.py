import numpy as np
import matplotlib.pyplot as plt

#define function
#Newton's Law of Cooling is dT/dt = k(Tequilibrium-Tinitial)
#for us: dT/dt = 0.2(20-T), with a list of T0's
T0List = [0.0,5.0,10.0,15.0,20.0,25.0,30.0,35.0,40.0]
Teq = 20.0
k = 0.2

maxDiff = 100
maxDiffAllowed = 0.01

#choose a time period to solve for; we'll try 10 minutes
timePeriod = 10

#choose range of y-axis for plot
yMin = 0.0
yMax = 40

#choose an initial partition of the time period "Time"
#we'll start with 4 
#as set up, this must be an even number greater than 4, i think
#well, odd numbers >=3 seem to work and even numbers greater than 2 work
#2 & 3 work okay, but comparison of curves is not quite right; it only works because program cycles to higher partion numbers due to large diff between starting curve and first calculated curve
#4 is best choice, to keep things a binary expansion
#but 2 is nice to show degree of progress
initialPartitionIndex = 2


def incrementaLawOfCooling(Tprev,Teq,k,deltaTime):
	Tnext = Tprev + k*(Teq-Tprev)*deltaTime
	return Tnext
	
def coolingCurve(T0,Teq,k,timePeriod,partitionIndex):
	Tprev = T0
	deltaTime = timePeriod/partitionIndex
	timePoints = []
	TempPoints = []
	
	for n in range(0,int(partitionIndex+1)):
		time = n*deltaTime
		timePoints.append(time)
		TempPoints.append(Tprev)
		Tnext = incrementaLawOfCooling(Tprev,Teq,k,deltaTime)
		#TempPoints.append(Tnext)
		Tprev = Tnext
		
	return timePoints,TempPoints
	
	
def compareCurves(timePoints,TempPoints,oldTimePoints,oldTempPoints):
	'''point-by-point comparison of two curves, '''
	'''looking for maximum separation'''
	n = 0
	maxSoFarDiff = 0.0

	for tempPoint in oldTempPoints:
		diff = abs(tempPoint-TempPoints[(2*n)])
		#print(diff)
		n += 1
		if diff > maxSoFarDiff:
			maxSoFarDiff = diff
			
	return maxSoFarDiff



def makeStarterCurve(timePeriod,initialPartitionIndex):
	'''make an initial "curve" for comparison'''
	'''this should generate a straight line'''

	oldTimePoints = []
	oldTempPoints = []

	for n in range(0,int(initialPartitionIndex/2+1)):
		time = 2*n*timePeriod/initialPartitionIndex
		oldTimePoints.append(time)
		oldTempPoints.append(T0)
		
	return oldTimePoints,oldTempPoints
	

def computeAndPlotTimeFunctionCurve(T0,Teq,k,timePeriod,initialPartitionIndex,maxDiffAllowed,yMin,yMax):
	'''computes the time function of the differential equation for a given T0'''
	#set maxDiff to some high number to permit first while loop
	maxDiff = 100
	
	#create a starter line for comparison
	oldTimePoints, oldTempPoints = makeStarterCurve(timePeriod,initialPartitionIndex)
	
	partitionIndex = initialPartitionIndex
	
	#loop around calculating curves until curves change minimally
	#that is, until maxDiff < maxAllowedDiff
	while maxDiff > maxDiffAllowed:
		#calculate cooling curves for a given T0
		timePoints, TempPoints = coolingCurve(T0,Teq,k,timePeriod,partitionIndex)
	
		#find out how different the curves are
		#point-by-point comparison of curves to find maximum separation
		maxDiff = compareCurves(timePoints,TempPoints,oldTimePoints,oldTempPoints)

		#the new curve becomes the old curve
		oldTimePoints = timePoints
		oldTempPoints = TempPoints
		
		#double the partitionIndex
		partitionIndex = 2*partitionIndex
	

	#plot curve, but hold show() for later
	plt.subplot(211)
	plt.plot(timePoints,TempPoints)
	plt.axis([0,timePeriod,yMin,yMax])
	#plt.show()
	
	
#generate a series of curves
for T0 in T0List:
	computeAndPlotTimeFunctionCurve(T0,Teq,k,timePeriod,initialPartitionIndex,maxDiffAllowed,yMin,yMax)
plt.show()

