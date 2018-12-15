import pandas as pd
from shapely.geometry import Point, Polygon

AOI_PATH = "aoi/"
AOI_DATA = ["1.txt","2.txt","3.txt","4.txt","5.txt","6.txt","7.txt","8.txt"]
AOI_COLUMNS = ["Idientifier", "X-from_coordinate", "X-offset", "Y-from_coordinate", "Y-offset", "ShortID"]


def help():
	print("Function: load_and_process_aoi(file = AOI_DATA[0])\n")
	print(":param file - aoi text file with coordinates\n\n@return aoi - aoi dict represent in polygons")


def load_and_process_aoi(file = AOI_DATA[0]):
	'''
	:param file - aoi text file with coordinates

	@return aois - aoi dict represent in polygons 
	'''

	aois = {}
	aoi_file = pd.read_csv(AOI_PATH + file, names=AOI_COLUMNS, header=None, low_memory=False, sep=" ")

	# Od bodu 0,0 na osy - lavy dolny roh, lavy horny, pravy horny, pravy dolny
	for index, row in aoi_file.iterrows():
	    left_down = Point(row['X-from_coordinate'], row['Y-from_coordinate'])
	    right_down = Point(row['X-from_coordinate'] + row['X-offset'], row['Y-from_coordinate'])
	    left_up = Point(row['X-from_coordinate'], row['Y-from_coordinate'] + row['Y-offset'])
	    right_up = Point(row['X-from_coordinate'] + row['X-offset'], row['Y-from_coordinate'] + row['Y-offset'])
	    
	    aois[row['ShortID']] = Polygon(((left_down.x, left_down.y), (left_up.x, left_up.y), (right_up.x, right_up.y), (right_down.x, right_down.y)))
	
	return aois
