#!/usr/bin/env python
from data_parser import *

"""
This takes one argument - start / full for calibration data from the beginning respectively from the beginning and end of the study

"""
PATH_TO_SAVE_DATA_BEGIN = "data/calibration_data_begin/"
PATH_TO_SAVE_DATA_FULL = "data/calibration_data_begin_end/"

TASK_NAMES = ['V1_190x120.png', 'V2_950x120.png', 'V3_1710x120.png',
	   'V4_190x600.png', 'V5_950x600.png', 'V6_1710x600.png',
	   'V7_190x1080.png', 'V8_950x1080.png', 'V9_1710x1080.png',
	   'VA_950x600.png', 'VB_950x600.png', 'VC_950x600.png',
	   'VD_950x600.png']


def get_user_calibration_task(df_tester):
	"""
	:param df_tester - all user's data
	@return indexes - indexes of each user's task
	"""
   
	df_temp = df_tester['StudioEventData'] 
	_d = []
	for c in TASK_NAMES:
		ind_values = df_temp[df_temp == c].index.values
		#if(len(ind_values) > 2):
		   # _d.append([c, ind_values[0:2], ind_values[2:4]])
		#else:
		_d.append([c, ind_values[0:2]])
	  
	# sort values based on STARTING POINT of given task
	tester_sorted = sorted(_d, key=lambda x: x[1][0])
	
  
	#length_of_dataset = len(df_tester[user_index])
	length_of_dataset = len(df_tester)
	indexes = []
	
	# saving indexes
	indexes.append([tester_sorted[0][0], [tester_sorted[0][1][0], tester_sorted[1][1][0]]])

	for j in range(1,len(tester_sorted) - 1):
		indexes.append([tester_sorted[j][0], [tester_sorted[j][1][0], tester_sorted[j+1][1][0]]])
	
	#index before end of task, where begins IE_OB
	try:
		last_index = df_temp[df_temp == 'IE_uvod'].index.values[0]
	except:
		print("Didnt find IE_uvod.")
	
	indexes.append([tester_sorted[j + 1][0], [tester_sorted[j + 1][1][0], last_index]])
	
	return indexes


	
def get_user_calibration_task_second(df_tester):
	"""
	:param df_tester - all user's data
	@return indexes - indexes of each user's task
	"""
	# Only these task names
	task_names_s = TASK_NAMES[0:8]
	
	df_temp = df_tester['StudioEventData'] 
	_d = []
	for c in calib:
		ind_values = df_temp[df_temp == c].index.values
		if(len(ind_values) > 2):
			_d.append([c, ind_values[2:4]])
	  
	# Check if user has calibration at the end of the study
	if(len(ind_values) > 2):
		# sort values based on STARTING POINT of given task
		tester_sorted = sorted(_d, key=lambda x: x[1][0])

		#print(tester_sorted)

		#length_of_dataset = len(df_tester[user_index])
		length_of_dataset = len(df_tester)
		indexes = []

		# saving indexes
		indexes.append([tester_sorted[0][0], [tester_sorted[0][1][0], tester_sorted[1][1][0]]])

		for j in range(1,len(tester_sorted) - 1):
			indexes.append([tester_sorted[j][0], [tester_sorted[j][1][0], tester_sorted[j+1][1][0]]])

		#index pred koncom testu, kde uz zacina IE_OB
		try:
			last_index = df_temp[df_temp == 'VA_950x600.png'].index.values[3]
		except:
			print("Didnt find VA_950x600.png.")

		indexes.append([tester_sorted[j + 1][0], [tester_sorted[j + 1][1][0], last_index]])

		return indexes
	else:
		return 0




def transform_calibration_data_based_on_task(users):
	"""  
	Transform data from the start of the study

	:param users - all users in study and their data sort by tasks
	"""

	total_length = 0

	for task_name in TASK_NAMES:
		clear_output()
		print("Working on " + task_name)
		df_fin = pd.DataFrame()
		for tester_name in users:
			print("* Working on " + tester_name)
			#print(" * " + tester_name + " - " + str(len(users[tester_name].tasks[task_name].columns.values)))
			df_fin = df_fin.append(users[tester_name].tasks[task_name])
			#print(users[tester_name].tasks[task_name].iloc[:,-1].name)

		total_length += len(df_fin)
		print("Writing....")
		df_fin.to_csv(PATH_TO_SAVE_DATA_BEGIN + task_name[0:len(task_name)-4] + ".tsv", sep="\t", index=False)



def transform_calibration_data_based_on_task_second(users):
	"""
	Transform data from the end of the study

	:param users - all users in study and their data sort by tasks

	"""

	# Only these task names
	task_names_s = TASK_NAMES[0:8]
	
	total_length = 0

	for task_name in task_name_s:
		clear_output()
		print("Working on " + task_name)
		#df_fin = pd.DataFrame()
		df_fin = pd.read_csv("calibration_data_by_tasks0/" + task_name[0:len(task_name)-4] + ".tsv", low_memory=False, sep="\t")
		for tester_name in users:
			print("* Working on " + tester_name)
			#print(" * " + tester_name + " - " + str(len(users[tester_name].tasks[task_name].columns.values)))
			df_fin = df_fin.append(users[tester_name].tasks[task_name])
			#print(users[tester_name].tasks[task_name].iloc[:,-1].name)

		total_length += len(df_fin)
		print("Writing....")
		df_fin.to_csv(PATH_TO_SAVE_DATA_FULL + task_name[0:len(task_name)-4] + ".tsv", sep="\t", index=False)


def get_calibration_begin(df_testers):
	"""
	Get tasks for each user and create instance of class

	Get calibration data from the beginning of the study
	"""
	users_calib = {}
	for tester in df_testers:
		
		_user_tasks = get_user_calibration_task(df_testers[tester])
		users_calib[tester] = Tester()
		
		for u in _user_tasks:
			start = u[1][0]
			end = u[1][1]
			
			users_calib[tester].assign(u[0], df_testers[tester][start:end])

	transform_calibration_data_based_on_task(users_calib)


def get_calibration_full(df_testers):
	"""
	Get tasks for each user and create instance of class

	Get calibration data from the beginning and from the end of the study
	"""
	users_calib_second = {}
	for tester in df_testers:
		
		_user_tasks = get_user_calibration_task_second(df_testers[tester])
		if(_user_tasks != 0):
			users_calib_second[tester] = Tester()

			for u in _user_tasks:
				start = u[1][0]
				end = u[1][1]

				users_calib_second[tester].assign(u[0], df_testers[tester][start:end])
		else:
			continue

	transform_calibration_data_based_on_task_second(users_calib_second)


def main():

	# Pass only one argument
	if len(sys.argv) == 2:
		# from data_parser.py
		df_testers = load_testers_to_df()

		if(sys.argv[1] == "start"):
			get_calibration_begin(df_testers)
		elif(sys.argv[1] == "full"):
			get_calibration_full(df_testers)
	else:
		print("Argument's missing - start/full")

	

if __name__ == '__main__': main()

