#!/usr/bin/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DynamicalSystemsModule.py
#
# Project Webpage:
# http://geovis.cis.rit.edu
#
# Multidisciplinary Vision Research Laboratory (MVRL)
# Chester F. Carlson Center for Imaging Science (CIS)
# Rochester Institute of Technology (RIT)
#
# Tommy P. Keane
# tommy@tommypkeane.com
# http://www.tommypkeane.com
#
# Published in:
# "Eye-Movement Sequence Statistics and Hypothesis-Testing with Classical Recurrence Analysis"
# Tommy P. Keane, Nathan D. Cahill, Jeff B. Pelz
# tpk4100@rit.edu, ndcsma@rit.edu, pelz@cis.rit.edu
#
# Presented at:
# Eye-Tracking Research and Applications Symposium 2014
# Safety Harbor, FL
# March 26 - 28, 2014
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## STANDARD PYTHON MODULE IMPORTS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import os;
import sys;
import math;
import cmath;
import random;
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE EUCLIDEAN DISTANCE (p = 2, Norm) BETWEEN TWO POINTS OF ANY DIMENSIONALITY
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getEuclideanDistance( dataPoint1, dataPoint2 ):
	
	dataDistance = 0.0;

	for i in range( 0, len( dataPoint1 ), 1 ):

		dataDistance += ( math.pow( dataPoint2[i] - dataPoint1[i], 2.0 ) );

	#rof

	dataDistance = math.sqrt( dataDistance );

	return dataDistance;
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## FOLLOW THE TIME-DELAY EMBEDDING ALGORITHM TO CREATE A LIST OF PHASE-SPACE DATA FROM A LIST OF TIME-SERIES OBSERVATIONS
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def TimeDelayEmbedding( timeSeriesObservations, delayStep= 1, delaySamples= 3 ):

	# INTIALIZE EMPTY LIST
	phaseSpaceData = [];

	minValues = [];
	maxValues = [];

	for i in range( int((delaySamples - 1) * delayStep), len(timeSeriesObservations), 1 ):

		phaseSpaceData.append( [] );

		for j in range( 0, delaySamples, 1 ):

			if (i == ((delaySamples - 1) * delayStep)):

				for k in range( 0, len( timeSeriesObservations[0] ), 1 ):
					
					minValues.append( float( 'inf' ) );
					maxValues.append( -float( 'inf' ) );

				#rof

			#fi

			( phaseSpaceData[-1] ).extend( timeSeriesObservations[ i - (j * delayStep) ] );

		#rof

	#rof


	#NORMALIZATION
	for i in range( 0, len( phaseSpaceData ), 1 ):

		for j in range( 0, len( phaseSpaceData[0] ), 1 ):

			currentPhasePoint = ( phaseSpaceData[i] )[j];

			if ( currentPhasePoint > maxValues[j] ):

				maxValues[j] = currentPhasePoint;

			#fi

			if ( currentPhasePoint < minValues[j] ):

				minValues[j] = currentPhasePoint;

			#fi

		#rof

	#rof

	for i in range( 0, len( phaseSpaceData ), 1 ):

		for j in range( 0, len( phaseSpaceData[0] ), 1 ):

			( phaseSpaceData[i] )[j] -= minValues[j];

			scalingValue = ( maxValues[j] - minValues[j] );

			if (scalingValue == 0 ):

				scalingValue = 1;

			#fi

			( phaseSpaceData[i] )[j] /= scalingValue;

		#rof

	#rof

	return phaseSpaceData;
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CREATE THE (UPPER TRIANGLE) RECURRENCE ARRAY (MATRIX) AS A PYTHON LIST
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateRecurrenceMatrix( phaseSpaceData, clusteringDistanceThreshold= 0.01 ):

	recurrenceIndices = [];

	for i in range( 0, len( phaseSpaceData ), 1 ):

		recurrenceIndices.append( [] );

		for j in range( i, len( phaseSpaceData ), 1 ):

			currentDistance = getEuclideanDistance( phaseSpaceData[i], phaseSpaceData[j] );

			if ( currentDistance <= clusteringDistanceThreshold ):

				(recurrenceIndices[-1]).append( j );

			#fi

		#rof

	#rof


	return recurrenceIndices;
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE RECURRENCE COUNT FROM A RECURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getRecurrence( recurrenceIndices, numSamples ):
	
	R = 0;

	N = len( recurrenceIndices ) - numSamples + 1;

	for i in range( 0, N, 1 ):

		R += ( len( recurrenceIndices[i] ) - 1 );

	#rof

	return ( float( R ) );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	

## CALCULATE THE UPPER TRIANGLE RECURRENCE RATE FROM A RECURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getRecurrenceRate( recurrenceIndices, numSamples ):

	R = getRecurrence( recurrenceIndices, numSamples );

	N = len( recurrenceIndices ) - numSamples + 1;

	RR = ( float(R) / (float(N) * float(N - 1.0) * 0.5) );

	return ( RR );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE UPPER TRIANGLE MEAN(S) FROM A RECURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getRecurrenceMean( recurrenceIndices, numSamples ):

	R = getRecurrence( recurrenceIndices, numSamples );

	R = float( R );

	N = len( recurrenceIndices );

	meanX = 0.0;
	meanY = 0.0;

	for i in range( 0, N, 1 ):

		meanX += ( float( len( recurrenceIndices[i] ) - 1 ) * float(i + numSamples - 1) );

	#rof

	for i in range( 0, N, 1 ):

		meanY += ( float( sum(recurrenceIndices[i]) - i ) + float( (len(recurrenceIndices[i]) - 1) * (numSamples - 1) ) );

	#rof

	meanX /= R;
	meanY /= R;

	return ( (meanX, meanY) );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE UPPER TRIANGLE STANDARD DEVIATION(S) FROM A RECURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getRecurrenceStandardDeviation( recurrenceIndices, numSamples ):

	R = getRecurrence( recurrenceIndices, numSamples );

	R = float( R );

	N = len( recurrenceIndices );

	( meanX, meanY ) = getRecurrenceMean( recurrenceIndices, numSamples )

	stdDevX = 0.0;
	stdDevY = 0.0;

	for i in range( 0, N, 1 ):

		t = ( float( len( recurrenceIndices[i] ) - 1 ) * float(i + numSamples - 1) );

		if (t > 0):

			stdDevX += ( float( t - meanX ) ** 2.0 );

		#fi

	#rof

	for i in range( 0, N, 1 ):

		t = ( float( sum(recurrenceIndices[i]) - i ) + float( (len(recurrenceIndices[i]) - 1) * (numSamples - 1) ) );

		if ( t > 0 ):
			
			stdDevY += ( float( t - meanY ) ** 2.0 );

		#fi

	#rof

	stdDevX /= R;
	stdDevY /= R;

	stdDevX **= 0.5;
	stdDevY **= 0.5;

	return ( (stdDevX, stdDevY) );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
