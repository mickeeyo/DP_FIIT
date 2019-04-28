import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import glob
from IPython.display import clear_output
import numpy as np
import sys

# Path to save files
PATH_TO_DATA = "data/data_by_users/"

class Tester:
	"""
	"""
	def __init__(self):
		self.tasks = {}
	   
	def assign(self, name, data):
		 self.tasks[name] = data

	
		
def load_testers_to_df():
	"""
	:param path - path to the file where testers data are stored
	@return df_testers - key - user , value - all user's data
	"""

	df_testers = {}

	file_paths = glob.glob(PATH_TO_DATA + '/*.tsv')
	# structure 'path\\name_of_file.format'
	for f in file_paths:
		# Transform path
		file_names.append(f.replace("\\","/"))
		#testers_names.append(f[15:23])


	# For each file from folder - path
	for f in file_names:
		df_testers[f[15:23]] = pd.read_csv(f, sep="\t",low_memory=False)
		
		if(len(df_testers[f[15:23]].columns.values) == 82):
			# Where should missing columns start
			index = 5
			for col in missing_columns:
				df_testers[f[15:23]].insert(loc = index, column = col, value = np.nan)
				index += 1
				
		name_last_column = df_testers[f[15:23]].iloc[:,-1].name
		# Drop last column - "unknown"
		df_testers[f[15:23]] = df_testers[f[15:23]].drop(columns=[name_last_column])
		
	return df_testers	