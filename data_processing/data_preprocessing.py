#!/usr/bin/env python
import pandas as pd

STUDIO_EVENTS = ['InstructionStart', 'InstructionEnd', 'ScreenRecStarted', 
				'URLStart', 'URLEnd', 'ScreenRecStopped', 'QuestionStarted','QuestionEnded']
				
				
def filter_users_data_to_task(df):
	'''
	:param df - data for specific user
	
	@return df - filtered df
	'''
	
	dt_len = len(df)
	# Get starting and ending point of screen recording
	index_started = df[df['StudioEvent'] == STUDIO_EVENTS[2]].index.values[0]
	index_stopped = df[df['StudioEvent'] == STUDIO_EVENTS[5]].index.values[0]

	last_index = df[(dt_len - 1):].index.values[0]
	
	#Calculate current ACTUAL indexes in the given dataframe
	index_started = dt_len - (last_index - index_started + 1)
	index_stopped = dt_len - (last_index - index_stopped)
	
	# Filter data where task begin and end
	df = df[index_started:index_stopped]
	
	return df


def filter_users_fixations_wod(df):
	# wod - with out duplicates
	# Filter a remain only non null fixations
	df = df[(df['FixationPointX (MCSpx)'].isnull() == False) | (df['FixationPointY (MCSpx)'].isnull() == False)]
	# Drop fixation duplicates (same fixation only with different gaze points which forms one fixation) 
	df = df.drop_duplicates(['FixationIndex'])

	return df
	
	
def filter_users_fixations_wd(df):
	# with duplicates
	# Filter a remain only non null fixations
	df = df[(df['FixationPointX (MCSpx)'].isnull() == False) | (df['FixationPointY (MCSpx)'].isnull() == False)]
	
	return df