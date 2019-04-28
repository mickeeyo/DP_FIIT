#!/usr/bin/env python
from data_validation import data_validation_functions as dvf


def help():
	print("Function: calibration_filter(df, type, ac_tresh_begin = 0.95, pr_tresh_begin = 0.95, ac_tresh_end = 0.95, pr_tresh_end = 0.95, ac_tresh_between = 0.95, pr_tresh_between = 0.95)\n")
	print("# The beginning - calibration data before tasks\n# The end - calibration data after tasks\n\n*REQUIRED\n:param df - dataframe to be filtered\n:param type - type of filtration (only from the beginning OR beginning and the end)\n:param ac_tresh_begin - accuracy treshold between mean and data from the beginning\n:param pr_tresh_begin - precision treshold between mean and data from the beginning\n\n*OPTIONAL\n:param ac_tresh_end - accuracy treshold between mean and data from the end\n:param pr_tresh_end - precision treshold between mean and data from the end\n:param ac_tresh_between - accuracy treshold between data from the beginning and the end\n:param pr_tresh_between - precision treshold between data from the beginning and the end\n\n@return df - filtered dataset")

	print("\n\n*********************************************\n")

	print("Function: eyes_validity_filter(df, code = 2.0, percentage = 40)\n")
	print(":param df - dataframe with data\n:param code - represents highest possible code for eyes to be considered as valid\n:percentage - how many percentage of valid data should be at least to have valid data for participant\n\n@return df - filtered dataset")


def calibration_filter(df, type, PATH_CALIB, tresh_count = 2, ac_tresh_begin = 0.95, pr_tresh_begin = 0.95, ac_tresh_end = 0.95, pr_tresh_end = 0.95, ac_tresh_between = 0.95, pr_tresh_between = 0.95):
	'''
	 # The beginning - calibration data before tasks 
	 # The end - calibration data after tasks 
	 
	*REQUIRED
	:param df - dataframe to be filtered
	:param type - type of filtration (only from the beginning OR beginning and the end)
	:param PATH_CALIB - path to calibration data
	:param tresh_count - how many values should user have invalid to be filtered
	:param ac_tresh_begin - accuracy treshold between mean and data from the beginning
	:param pr_tresh_begin - precision treshold between mean and data from the beginning
	
	*OPTIONAL
	:param ac_tresh_end - accuracy treshold between mean and data from the end
	:param pr_tresh_end - precision treshold between mean and data from the end
	:param ac_tresh_between - accuracy treshold between data from the beginning and the end
	:param pr_tresh_between - precision treshold between data from the beginning and the end
	
	@return df - filtered dataset
	'''
	
	testers_to_filter = []
	
	if(type == "begin"):
	
		if(tresh_count > 2):
			tresh_count = 2
			
		testers_to_filter = dvf.get_testers_to_filter_begin(PATH_CALIB, tresh_count, ac_tresh_begin, pr_tresh_begin)
	elif(type == "end"):
		if(tresh_count > 6):
			tresh_count = 6
			
		testers_to_filter = dvf.get_testers_to_filter_begin_end(PATH_CALIB, tresh_count, ac_tresh_begin, pr_tresh_begin, ac_tresh_end, pr_tresh_end, ac_tresh_between, pr_tresh_between)
	
	if(len(testers_to_filter) > 0):
		df = dvf.filter_testers_from_dataset(df, testers_to_filter)
	
	return df


def eyes_validity_filter(df, code = 2.0, percentage = 40):
	'''
	:param df - dataframe with data
	:param code - represents highest possible code for eyes to be considered as valid  
	:percentage - how many percentage of valid data should be at least to have valid data for participant
	
	@return df - filtered dataset
	'''
	
	# Get all participant names
	tester_names = df['ParticipantName'].unique()
	
	testers_to_filter = []
	for tester_name in tester_names:
		df_tester = df[df['ParticipantName'] == tester_name]
		num = dvf.tester_eyes_validity(df_tester, code)
		if(num < percentage):
			testers_to_filter.append(tester_name)
	
	
	if(len(testers_to_filter) > 0):
		df = dvf.filter_testers_from_dataset(df, testers_to_filter)
	
	# Chcem vsetkych participantov s ich validacnymi cislami
	return df
