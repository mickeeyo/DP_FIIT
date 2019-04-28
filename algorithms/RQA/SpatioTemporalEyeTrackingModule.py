#!/usr/bin/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SpatioTemporalEyeTrackingModule.py
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



## CREATE A REOCCURRENCE ARRAY (LIST) FROM A LIST OF SPATIAL DATA POINTS (e.g., FIXATIONS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateReoccurrenceMatrix( positionData, clusteringDistanceThreshold= 0.05 ):
	'''
		Inspired By:
		ANDERSON, N.C.; BISCHOF, W.F.; LAIDLAW, K.E.; RISKO, E.F.; AND KINGSTONE, A.; 2013. "Recurrence quantification analysis of eye movements". Behavior research methods, 1–15.
	'''
	
	recurrenceIndices = [];

	for i in range( 0, len( positionData ), 1 ):

		recurrenceIndices.append( [] );

		for j in range( i, len( positionData ), 1 ):

			currentDistance = getEuclideanDistance( positionData[i], positionData[j] );

			if ( currentDistance <= clusteringDistanceThreshold ):

				(recurrenceIndices[-1]).append( j );

			#fi

		#rof

	#rof

	return recurrenceIndices;
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE REOCCURRENCE COUNT FROM THE REOCCURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getReoccurrence( reoccurenceIndices ):
	'''
		Inspired By:
		ANDERSON, N.C.; BISCHOF, W.F.; LAIDLAW, K.E.; RISKO, E.F.; AND KINGSTONE, A.; 2013. "Recurrence quantification analysis of eye movements". Behavior research methods, 1–15.
	'''
	
	R = 0;

	N = len( reoccurenceIndices );

	for i in range( 0, N, 1 ):

		R += ( len( reoccurenceIndices[i] ) - 1 );

	#rof

	return ( R );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE REOCCURRENCE RATE FROM THE REOCCURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getReoccurrenceRate( reoccurenceIndices ):
	'''
		Inspired By:
		ANDERSON, N.C.; BISCHOF, W.F.; LAIDLAW, K.E.; RISKO, E.F.; AND KINGSTONE, A.; 2013. "Recurrence quantification analysis of eye movements". Behavior research methods, 1–15.
	'''
	
	R = getReoccurrence( reoccurenceIndices );

	N = len( reoccurenceIndices );

	REC = 100.0 * ( (2.0 * float(R)) / float( N * (N - 1) ) );

	return ( REC );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE REOCCURRENCE DETERMINISM FROM THE REOCCURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getDeterminism( reoccurenceIndices ):
	'''
		Inspired By:
		ANDERSON, N.C.; BISCHOF, W.F.; LAIDLAW, K.E.; RISKO, E.F.; AND KINGSTONE, A.; 2013. "Recurrence quantification analysis of eye movements". Behavior research methods, 1–15.
	'''
	
	## FIXED ASSUMPTION (PROTOTYPE)
	minLineLength = 2;

	R = getReoccurrence( reoccurenceIndices );

	N = len( reoccurenceIndices );

	DET = 0.0;

	for i in range( 0, N, 1 ):

		for j in range( 0, len( reoccurenceIndices[i] ), 1 ):

			DUR = False;
			DLL = False;
			DUL = False;
			DLR = False;

			if ( j < (len(reoccurenceIndices[i]) - 1) ):

				if ( i < (N - 1) ):
					
					DUR = ( (j + 1) in ( reoccurenceIndices[ i + 1 ] ) );

				#fi
			
				if ( i > 0 ):
				
					DUL = ( (j + 1) in ( reoccurenceIndices[ i - 1 ] ) );

				#fi
			
			#fi

			if ( j > 0 ):
				
				if ( i < (N - 1) ):
					
					DLL = ( (j - 1) in ( reoccurenceIndices[ i - 1 ] ) );
				
				#fi
			
				if ( i > 0 ):
				
					DLR = ( (j - 1) in ( reoccurenceIndices[ i + 1 ] ) );

				#fi

			#fi

			if ( DUR or DLL or DUL or DLR ):

				DET += 1;

			#fi

		#rof

	#rof

	DET *= ( 100.0 / float(R) );

	return ( DET );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE REOCCURRENCE LAMINARITY FROM THE REOCCURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getLaminarity( reoccurenceIndices ):
	'''
		Inspired By:
		ANDERSON, N.C.; BISCHOF, W.F.; LAIDLAW, K.E.; RISKO, E.F.; AND KINGSTONE, A.; 2013. "Recurrence quantification analysis of eye movements". Behavior research methods, 1–15.
	'''
	
	## FIXED ASSUMPTION (PROTOTYPE)
	minLineLength = 2;

	R = getReoccurrence( reoccurenceIndices );

	N = len( reoccurenceIndices );

	LAM = 0.0;

	for i in range( 0, N, 1 ):

		for j in range( 0, len( reoccurenceIndices[i] ), 1 ):

			HR = False;
			HL = False;
			VU = False;
			VR = False;

			if ( i > 0 ):
				
				VU = ( j in ( reoccurenceIndices[ i - 1 ] ) );
			#fi

			
			if ( i < (N - 1) ):
				
				VD = ( j in ( reoccurenceIndices[ i + 1 ] ) );
			#fi

			
			if ( j > 0 ):
				
				HL = ( (j - 1) in ( reoccurenceIndices[ i ] ) );

			#fi


			if ( j < (len(reoccurenceIndices[i]) - 1) ):
					
				HR = ( (j + 1) in ( reoccurenceIndices[ i ] ) );

			#fi


			if ( HR or HL ):

				LAM += 1;

			#fi

			
			if ( VU or VD ):

				LAM += 1;

			#fi

		#rof

	#rof

	LAM *= ( 100.0 / (2.0 * float(R)) );

	return ( LAM );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## CALCULATE THE REOCCURRENCE CORM (CENTER OF REOCCURRENCE MASS) FROM THE REOCCURRENCE ARRAY (LIST)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getCORM( reoccurenceIndices ):
	'''
		Inspired By:
		ANDERSON, N.C.; BISCHOF, W.F.; LAIDLAW, K.E.; RISKO, E.F.; AND KINGSTONE, A.; 2013. "Recurrence quantification analysis of eye movements". Behavior research methods, 1–15.
	'''
	
	R = getReoccurrence( reoccurenceIndices );

	N = len( reoccurenceIndices );

	CORM = 0.0;

	for i in range( 0, N, 1 ):

		for j in reoccurenceIndices[i]:

			CORM += ( (N - i) - j );

		#rof

	#rof

	CORM *= ( 100.0 / ( (float(N) - 1.0) * float(R) ) );

	return ( CORM );
#fed ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
