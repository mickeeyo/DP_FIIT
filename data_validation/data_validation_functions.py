#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import string
import math
import csv
from scipy.spatial import distance
from math import atan2, degrees
from IPython.display import clear_output
from shapely.geometry import Point, Polygon


MONITOR_HEIGHT = 32.4 # Monitor height in cm
MONITOR_VERTICAL_RESOLUTION = 1200 # Vertical resolution of the monitor
MONITOR_HORIZONTAL_RESOLUTION = 1900 # # Horizontal resolution of the monitor

#PATH_BEGIN = "../data/calibration_data_begin/"
#PATH_BEGIN = "../MSVN-Data/calibration_data/"
#PATH_BEGIN_END = "data/calibration_data_begin_end/"

TASK_FILE_NAMES = ['V1_190x120.png', 'V2_950x120.png', 'V3_1710x120.png',
	   'V4_190x600.png', 'V5_950x600.png', 'V6_1710x600.png',
	   'V7_190x1080.png', 'V8_950x1080.png', 'V9_1710x1080.png',
	   'VA_950x600.png', 'VB_950x600.png', 'VC_950x600.png',
	   'VD_950x600.png']
	   

TASK_FILE_NAMES_TSV = ['V1_190x120.tsv', 'V2_950x120.tsv', 'V3_1710x120.tsv',
	   'V4_190x600.tsv', 'V5_950x600.tsv', 'V6_1710x600.tsv',
	   'V7_190x1080.tsv', 'V8_950x1080.tsv', 'V9_1710x1080.tsv',
	   'VA_950x600.png', 'VB_950x600.png', 'VC_950x600.png',
	   'VD_950x600.png']
	   
	   
CALIBRATING_POINTS = [
					[190, 120],
					[950,120],
					[1710,120],
					[190, 600],
					[950, 600], 
					[1710, 600],
					[190, 1080],
					[950,1080], 
					[1710, 1080]
					]

					
def get_head_distance(distanceleft, distanceright):
	""" get head distance"""
	if np.isnan(distanceleft) and np.isnan(distanceright):
		return -1
	if np.isnan(distanceleft):
		return distanceright / 10
	if np.isnan(distanceright):
		return distanceleft / 10
	return ((distanceleft + distanceright) / 2.0) /10


def get_distances_accuracy(df, accuracy, point_in_image, participant_name):
	""" 
	   accuracy calculation  
	"""
	for index, row in df.iterrows():
		dist_euc = distance.euclidean(point_in_image, [row["GazePointX (MCSpx)"], row["GazePointY (MCSpx)"]])
		head_distance = get_head_distance(row["DistanceLeft"], row["DistanceRight"])
		if head_distance > 0:
			# Calculate degree per pixel ( tanges of angle ) and then divide it to get degree per pixel from radians
			deg_per_pixel = degrees(atan2(.5 * MONITOR_HEIGHT, head_distance)) / (.5 * MONITOR_VERTICAL_RESOLUTION)
			dist_in_deg = dist_euc * deg_per_pixel

			accuracy[participant_name].append(dist_in_deg)
   
					
def get_distances_precision(df, precision, participant_name):
	""" 
		precision calculation
	"""
	
	last_gaze_point = []
	for index, row in df.iterrows():
		
		if len(last_gaze_point) == 0:
			last_gaze_point = [row["GazePointX (MCSpx)"], row["GazePointY (MCSpx)"]]
			continue
		
		head_distance = get_head_distance(row["DistanceLeft"], row["DistanceRight"])
		if head_distance > 0:
			dist_eu = distance.euclidean(last_gaze_point, [row["GazePointX (MCSpx)"], row["GazePointY (MCSpx)"]])
			deg_per_pixel = degrees(atan2(.5 * MONITOR_HEIGHT, head_distance)) / (.5 * MONITOR_VERTICAL_RESOLUTION)
			size_in_deg = dist_eu * deg_per_pixel

			precision[participant_name].append(size_in_deg)
			
		last_gaze_point = [row["GazePointX (MCSpx)"], row["GazePointY (MCSpx)"]]
	
	
def calculate_accuracy_precision(PATH_CALIB, which = "begin"):
	if(which == "begin"):
		PATH = PATH_CALIB
		#PATH = PATH_BEGIN
	elif(which == "end"):
		PATH = PATH_BEGIN_END
	else:
		return None
		
	accuracy = {}
	precision ={}
	
	# For first 8 calibrating files 
	for i in range(0,9):
		t_ = i + 1
		#recording_by_point = pd.read_csv(PATH + "/V" + str(t_) + "_" + str(CALIBRATING_POINTS[i][0]) + "x" + str(CALIBRATING_POINTS[i][1]) + ".tsv", sep="\t")
		
		recording_by_point = pd.read_csv(PATH + "/" + TASK_FILE_NAMES_TSV[i], sep="\t")
		
		# get participant names from recoring
		participants_names = recording_by_point['ParticipantName'].unique()
		for participant in participants_names:
			can_calculate = False
			
			if participant not in accuracy.keys():
				accuracy[participant] = []
				precision[participant] = []

			# select data for particular participants and delete first 10 fixations
			if(which == "begin"):
				df = recording_by_point[recording_by_point['ParticipantName'] == participant]
				df = df.iloc[150:]
				can_calculate = True
			elif(which == "end"):
				# calculating values from the end 
				df_t = recording_by_point[recording_by_point['ParticipantName'] == participant] 
				g = df_t['StudioEvent'].dropna()
				# [imagebeginstart, imagebeginend, imageendstart, imageendend]
				if(len(g.index.values) == 4):
					inx = g.index.values[2:4]
					#inx
					df = recording_by_point[inx[0]:inx[1]]
					can_calculate = True
				else:
					can_calculate = False
			
			if(can_calculate == True):
				# filter out invalid gaze points and fixations
				df = df[(~np.isnan(df["GazePointX (MCSpx)"])) & (~np.isnan(df["GazePointY (MCSpx)"]))]
				df = df[(~np.isnan(df["FixationPointX (MCSpx)"])) & (~np.isnan(df["FixationPointY (MCSpx)"]))]
				if(len(df) > 0):
					get_distances_accuracy(df, accuracy, CALIBRATING_POINTS[i], participant)
					get_distances_precision(df, precision, participant)


	# calculate accuracy for each participant
	accuracyList = []
	for key in accuracy:
		if accuracy[key]:
			accuracyList.append([key, sum(accuracy[key]) / float(len(accuracy[key]))])

	# save acccuracy to file
	df_accuracy = pd.DataFrame(data=accuracyList, columns=["tester_name","accuracy_"+which])
	#my_df.to_csv("output/pupilValidity/accuracy.csv", index=False, header=False)

	# calculate overallaccuracy
	#overallAccuracy = df_accuracy["accuracy_"+which].mean()
	#print("OverAll accuracy:")
	#print(overallAccuracy)


	# accuracy - priemerna vzdialenost k zadanemu bodu
	# precision -  priemer rozdielov po sebe iducich bodov


	# calculate precision for each participant
	precisionList = []
	for key in precision:
		if precision[key]:
			precisionList.append([key, sum(precision[key]) / float(len(precision[key]))])

	# save precision to file
	df_precision = pd.DataFrame(data=precisionList,columns=["tester_name","precision_" + which])
	#my_df2.to_csv("output/pupilValidity/precision.csv", index=False, header=False)

	# calculate overall precision
	#overallPrecision = df_precision["precision_"+which].mean()
	#print("OverAll precision:")
	#print(overallPrecision)
	#print("------------------------------")
	
	return [df_accuracy, df_precision]
	
def get_testers_to_filter_begin_end(PATH_CALIB, tresh_count, ac_tresh_begin, pr_tresh_begin, ac_tresh_end, pr_tresh_end, ac_tresh_between, pr_tresh_between):
	'''
	 # The beginning - calibration data before tasks 
	 # The end - calibration data after tasks 
	:param tresh_count - how many values should user have invalid to be filtered
	:param ac_tresh_begin - accuracy treshold between mean and data from the beginning
	:param pr_tresh_begin - precision treshold between mean and data from the beginning
	:param ac_tresh_end - accuracy treshold between mean and data from the end
	:param pr_tresh_end - precision treshold between mean and data from the end
	:param ac_tresh_between - accuracy treshold between data from the beginning and the end
	:param pr_tresh_between - precision treshold between data from the beginning and the end
	
	@return tester_to_filter - name of testers that we should filter from dataset
	'''
	
	# tester_names to filter from dataset
	testers_to_filter = []
	
	'''
	ac_tresh_begin = 0.95
	pr_tresh_begin = 0.95
	ac_tresh_end = 0.95
	pr_tresh_end = 0.95
	ac_tresh_between = 0.95
	pr_tresh_between = 0.95
	'''

	# Get calibration files from the beginning
	df_ac_pr_begin = calculate_accuracy_precision(PATH_CALIB, "begin")
	# Get calibration values from the end
	df_ac_pr_end = calculate_accuracy_precision(PATH_CALIB, "end")
	
	# Accuracy (ac) and precision (pr) from the beginning
	df_ac_begin = df_ac_pr_begin[0]
	df_pr_begin = df_ac_pr_begin[1]
	# Accuracy (ac) and precision (pr) from the end
	df_ac_end = df_ac_pr_end[0]
	df_pr_end = df_ac_pr_end[1]
	
	# Merge begin and end separately
	user_a_p_begin = pd.merge(df_ac_begin, df_pr_begin, on="tester_name")
	user_a_p_end = pd.merge(df_ac_end, df_pr_end, on="tester_name")
	
	# Merge begin and end together, missing values fill with Nan
	a_p_final = pd.merge(user_a_p_begin, user_a_p_end,  on="tester_name", how="left")
	
	# Calculate means for ac and pr from the beginning and the end
	overall_ac_begin = df_ac_begin.mean()[0]
	overall_pr_begin = df_pr_begin.mean()[0]

	overall_ac_end = df_ac_end.mean()[0]
	overall_pr_end = df_pr_end.mean()[0]

	# Iterate through the rows of testers data and check if his calibration data is valid according to tresholds
	for index, row in a_p_final.iterrows():
		dif_ac_to_mean_begin = abs(row['accuracy_begin'] - overall_ac_begin)
		dif_pr_to_mean_begin = abs(row['precision_begin'] - overall_ac_begin)
		if(row['accuracy_end'] != None):
			dif_ac_between = abs(row['accuracy_begin'] - row['accuracy_end'])
			dif_pr_between = abs(row['precision_begin'] - row['precision_end'])
			
			dif_ac_to_mean_end = abs(row['accuracy_end'] - overall_ac_end)
			dif_pr_to_mean_end = abs(row['precision_end'] - overall_ac_end)
			
			
		tresh_temp = 0
		if(dif_ac_to_mean_begin > ac_tresh_begin):
			tresh_temp += 1
		
		if(dif_pr_to_mean_begin > pr_tresh_begin):
			tresh_temp += 1
			
		if(dif_ac_between > ac_tresh_between):
			tresh_temp += 1
			
		if(dif_pr_between > pr_tresh_between):
			tresh_temp += 1
			
		if(dif_ac_to_mean_end > ac_tresh_end):
			tresh_temp += 1
			
		if(dif_pr_to_mean_end > pr_tresh_end):
			tresh_temp += 1
		
		
		# Check if we should filter current user
		if(tresh_temp >= tresh_count):
			testers_to_filter.append(row["tester_name"])
			
			
		#if((dif_ac_to_mean_begin > ac_tresh_begin and dif_pr_to_mean_begin > pr_tresh_begin) 
		   #or (dif_ac_between > ac_tresh_between and dif_pr_between > pr_tresh_between) 
		   #or (dif_ac_to_mean_end > ac_tresh_end and dif_pr_to_mean_end > pr_tresh_end)):
			#testers_to_filter.append(row["tester_name"])
			
	return testers_to_filter

	
def get_testers_to_filter_begin(PATH_CALIB, tresh_count, ac_tresh_begin, pr_tresh_begin):
	'''
	 # The beginning - calibration data before tasks 
	:param tresh_count - how many values should user have invalid to be filtered
	:param ac_tresh_begin - accuracy treshold between mean and data from the beginning
	:param pr_tresh_begin - precision treshold between mean and data from the beginning
	
	@return tester_to_filter - name of testers that we should filter from dataset
	'''
	
	# tester_names to filter from dataset
	testers_to_filter = []
	
	'''
	ac_tresh_begin = 0.95
	pr_tresh_begin = 0.95
	'''

	# Get calibration files from the beginning
	df_ac_pr_begin = calculate_accuracy_precision(PATH_CALIB, "begin")
	
	# Accuracy (ac) and precision (pr) from the beginning
	df_ac_begin = df_ac_pr_begin[0]
	df_pr_begin = df_ac_pr_begin[1]
	
	# Merge begin and end separately
	user_a_p_begin = pd.merge(df_ac_begin, df_pr_begin, on="tester_name")
	
	# Calculate means for ac and pr from the beginning and the end
	overall_ac_begin = df_ac_begin.mean()[0]
	overall_pr_begin = df_pr_begin.mean()[0]
	
	a_p_final = user_a_p_begin
	# Iterate through the rows of testers data and check if his calibration data is valid according to tresholds
	for index, row in a_p_final.iterrows():
		dif_ac_to_mean_begin = abs(row['accuracy_begin'] - overall_ac_begin)
		dif_pr_to_mean_begin = abs(row['precision_begin'] - overall_ac_begin)
		
		
		
		# Check if we should filter current user
		tresh_temp = 0
		if(dif_ac_to_mean_begin > ac_tresh_begin):
			tresh_temp += 1
			
		if(dif_pr_to_mean_begin > pr_tresh_begin):
			tresh_temp += 1
			
		if(tresh_temp >= tresh_count):
			testers_to_filter.append(row["tester_name"])
			
		#if((dif_ac_to_mean_begin > ac_tresh_begin) and (dif_pr_to_mean_begin > pr_tresh_begin)):
			testers_to_filter.append(row["tester_name"])
			
	return testers_to_filter
	
def filter_testers_from_dataset(df, testers_to_filter):
	'''
	:param df - dataframe with users data 
	:testers_to_filter - name of participants to filter
	
	@return df - filtered dataset
	'''
	
	# Iterate and remove data for specific tester
	for tester_name in testers_to_filter:
		df = df[df['ParticipantName'] != tester_name]
		
	return df

	
def tester_eyes_validity(df_tester, code):
	'''
	:param df_tester - tester's data
	:param code - represents highest possible code for eyes to be considered as valid  
	
	@return num_of_valid - number of valid data in percentage
	'''
	# Get data
	#df_tester = df[df['ParticipantName'] == tester_name]
	
	#df_tester['ValidityLeft'].dropna()
	
	#num_null = len(df_tester[(df_tester['ValidityLeft'].isnull()) & (df_tester['ValidityRight'].isnull())])
	#num_0_0 = len(df_tester[(df_tester['ValidityLeft'] == 0.0) & (df_tester['ValidityRight'] == 0.0)])
	# cannot with any certainty determine which eye it is
	#num_2_2 = len(df_tester[(df_tester['ValidityLeft'] == 2.0) & (df_tester['ValidityRight'] == 2.0)])
	# probably left eye
	#num_1_3 = len(df_tester[(df_tester['ValidityLeft'] == 1.0) & (df_tester['ValidityRight'] == 3.0)])
	# Probably right eye
	#num_3_1 = len(df_tester[(df_tester['ValidityLeft'] == 3.0) & (df_tester['ValidityRight'] == 1.0)]) 
	# most probably left eye
	#num_4_0 = len(df_tester[(df_tester['ValidityLeft'] == 4.0) & (df_tester['ValidityRight'] == 0.0)])
	# most probably right eye
	#num_0_4 = len(df_tester[(df_tester['ValidityLeft'] == 0.0) & (df_tester['ValidityRight'] == 4.0)])
	# No eye found
	#num_4_4 = len(df_tester[(df_tester['ValidityLeft'] == 4.0) & (df_tester['ValidityRight'] == 4.0)])
	
	# covers cases like 2 and 2 or 0 and 0
	valid_data = df_tester[(df_tester['ValidityLeft'] <= code) & (df_tester['ValidityRight'] <= code)]
	num_of_valid = ((round(len(valid_data) / len(df_tester), 3)) * 100) 
 
	return num_of_valid
