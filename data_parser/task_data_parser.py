#!/usr/bin/env python
from data_parser import *

"""	 
 K dispozici su separatne subory .tsv pre kazdeho testera a v nich ma kazdy tester data pre ulohy 1 az 8. 
 Tieto data chceme spojit a mat ich rozdelene jednotlivo po jednotlivych taskoch v .tsv suboroch
"""
	
PATH_TO_SAVE_DATA = "data/data_by_tasks/"

def get_user_task(df_tester):
    """
    :param df_tester - all data of one specific user
    @return indexes - indexes of each user's task
    """
	
    df_temp = df_tester['StudioEventData'] 
    _d = []
    for i in range(1,9):
        _d.append(["IE_"+str(i), df_temp[df_temp == "IE_"+str(i)].index.values])
        
    # sort values based on STARTING POINT of given task
    tester_sorted = sorted(_d, key=lambda x: x[1][0])
    
    #length_of_dataset = len(df_tester[user_index])
    length_of_dataset = len(df_tester)
    indexes = []
    
    # saving indexes
    indexes.append([tester_sorted[0][0], [tester_sorted[0][1][0], tester_sorted[1][1][0]]])

    for j in range(1,len(tester_sorted) - 1):
        indexes.append([tester_sorted[j][0], [tester_sorted[j][1][0], tester_sorted[j+1][1][0]]])
    
    #index pred koncom testu, kde uz zacina IE_OB
    try:
        last_index = df_temp[df_temp == "IE_OB"].index.values[0]
    except:
        print("Didnt find IE_OB. Trying to find IE_dot")
        try:
            last_index = df_temp[df_temp == "IE_dot"].index.values[0]
        except:
            print("Didnt find IE_OB or IE_dot")
            
    indexes.append([tester_sorted[j + 1][0], [tester_sorted[j + 1][1][0], last_index]])
    
    return indexes		 

	
	
def transform_data_based_on_task(users):
	"""
	Put together  data from each tester based on task
	
	:param users - all users in study and their data sort by tasks
	
	"""
	# Task names
	task_names = ["IE_1", "IE_2", "IE_3", "IE_4", "IE_5", "IE_6", "IE_7", "IE_8"]
	total_length = 0

	for task_name in task_names:
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
		df_fin.to_csv(PATH_TO_SAVE_DATA + task_name + ".tsv", sep="\t", index=False)


def main():
	# All testers names from study
	#testers_names = []

	# Name of files in folder
	file_names = []
	# DataFrame for each tester/participant
	df_testers = {}
	
	# Not every participant has these columns, the questionnaire was filled in only by some testers
	missing_columns = ['[Q01]Value', '[Q01_1]Value', '[Q01_1_1]Value', '[Q01_1_1_1]Value', 
                   '[Q01_1_1_1_1]Value', '[Q01_1_1_1_1_1]Value', '[Q01_1_1_1_1_1_1]Value', '[Q01_1_1_1_1_1_1_1]Value']
	
	
	# from data_parser.py
	df_testers = load_testers_to_df()
		
	"""
	Get tasks for each user and create instance of class
	"""
	users = {}
	for tester in df_testers:
		
		_user_tasks = get_user_task(df_testers[tester])
		users[tester] = Tester()
		
		for u in _user_tasks:
			start = u[1][0]
			end = u[1][1]
			
			users[tester].assign(u[0], df_testers[tester][start:end])
		
	# Final magic - put together all data and save them
	transform_data_based_on_task(users)

	
# Execute only if this is called directly
if __name__ == '__main__': main()		
