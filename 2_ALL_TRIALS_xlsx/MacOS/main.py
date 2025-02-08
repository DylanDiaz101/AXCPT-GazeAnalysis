# ALL TRIALS XLSX MacOS

# library to time our program
import time

# libraries for reading and writing files as well as multithreading tasks (xlsx to csv conversion)
import glob
import os
import re
import sys
import subprocess
import functools

from multiprocessing.dummy import Pool

# data analysis libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# FILE IO PATHS!
excel_input_path = './!INPUT//'  # location of our excel files # './test//' or './excel_input//'
csv_input_path = './!CONVERTED_INPUT//'  # where we want to store our converted excel files
output_path = './!OUTPUT//'  # where we want our final output dataframe to be stored

# Hide pandas warnings
pd.options.mode.chained_assignment = None  # default = 'warn'

# initialize timer
start_time = time.time()

############################################## CONVERT XLSX TO CSV #########################################################
print(f'\nCONVERTING XLSX FILES TO CSV...')  # DEBUG LINE

commands = []

for filepath in glob.glob(excel_input_path+'*.xlsx'):
    filename = re.search(r'(.+[\\|\/])(.+)(\.(csv|xlsx|xlx))', filepath) # extract file name on group 2 "(.+)"

    call = ["python3", "./xlsx2csv/xlsx2csv.py", filepath, csv_input_path+'{}.csv'.format(filename.group(2))]
    commands.append(call)

    print("An xlsx file was found...")  # DEBUG LINE

pool = Pool(2) # Specify How many concurrent threads

print("Conversion in process please wait...")

# If using windows use: for i, return_code in enumerate(pool.imap(functools.partial(subprocess.call, shell=True), commands)):
# If using mac use: for i, return_code in enumerate(pool.imap(subprocess.call, commands)):
for i, return_code in enumerate(pool.imap(subprocess.call, commands)):
    if return_code != 0:
        print("Command # {} failed with return code {}.".format(i, return_code))

# get all csv files and store into a list
csv_files = glob.glob(os.path.join(csv_input_path, "*.csv"))

#################################### CREATE OUTPUT DATAFRAMES AND INITIALIZE LOOP ###########################################
print('\n\nBegin iterating over gazedata files')  # DEBUG LINE

# tvd within trials output dataframes list, df's will be merged into the
# output Cue_TVD_within_trials.xlsx 
cue_tvd_within_trials_df_list = []

# initialize empty dataframe to append values to
mycolumns = [['subject_id',
              'AX_Number_of_Correct_Trials',  # num of correct trials
              'AY_Number_of_Correct_Trials',
              'BX_Number_of_Correct_Trials',
              'BY_Number_of_Correct_Trials',
              'AX_visits_top_probe', 'AX_visits_bottom_probe', 'AX_visits_cue',  # aoi visit count
              'AY_visits_top_probe', 'AY_visits_bottom_probe', 'AY_visits_cue',
              'BX_visits_top_probe', 'BX_visits_bottom_probe', 'BX_visits_cue',
              'BY_visits_top_probe', 'BY_visits_bottom_probe', 'BY_visits_cue',
              'AX_visits_cue_per_correct_trial', 'AX_visits_top_per_correct_trial',
              'AX_visits_bottom_per_correct_trial',  # visits per correct trial
              'AY_visits_cue_per_correct_trial', 'AY_visits_top_per_correct_trial',
              'AY_visits_bottom_per_correct_trial',
              'BX_visits_cue_per_correct_trial', 'BX_visits_top_per_correct_trial',
              'BX_visits_bottom_per_correct_trial',
              'BY_visits_cue_per_correct_trial', 'BY_visits_top_per_correct_trial',
              'BY_visits_bottom_per_correct_trial',
              'blk1_AX_VISITS_cue', 'blk2_AX_VISITS_cue', 'blk3_AX_VISITS_cue', 'blk4_AX_VISITS_cue',
              # visits by blocks
              'blk1_AX_VISITS_top', 'blk2_AX_VISITS_top', 'blk3_AX_VISITS_top', 'blk4_AX_VISITS_top',
              'blk1_AX_VISITS_bottom', 'blk2_AX_VISITS_bottom', 'blk3_AX_VISITS_bottom', 'blk4_AX_VISITS_bottom',
              'blk1_AY_VISITS_cue', 'blk2_AY_VISITS_cue', 'blk3_AY_VISITS_cue', 'blk4_AY_VISITS_cue',
              'blk1_AY_VISITS_top', 'blk2_AY_VISITS_top', 'blk3_AY_VISITS_top', 'blk4_AY_VISITS_top',
              'blk1_AY_VISITS_bottom', 'blk2_AY_VISITS_bottom', 'blk3_AY_VISITS_bottom', 'blk4_AY_VISITS_bottom',
              'blk1_BX_VISITS_cue', 'blk2_BX_VISITS_cue', 'blk3_BX_VISITS_cue', 'blk4_BX_VISITS_cue',
              'blk1_BX_VISITS_top', 'blk2_BX_VISITS_top', 'blk3_BX_VISITS_top', 'blk4_BX_VISITS_top',
              'blk1_BX_VISITS_bottom', 'blk2_BX_VISITS_bottom', 'blk3_BX_VISITS_bottom', 'blk4_BX_VISITS_bottom',
              'blk1_BY_VISITS_cue', 'blk2_BY_VISITS_cue', 'blk3_BY_VISITS_cue', 'blk4_BY_VISITS_cue',
              'blk1_BY_VISITS_top', 'blk2_BY_VISITS_top', 'blk3_BY_VISITS_top', 'blk4_BY_VISITS_top',
              'blk1_BY_VISITS_bottom', 'blk2_BY_VISITS_bottom', 'blk3_BY_VISITS_bottom', 'blk4_BY_VISITS_bottom',
              'AX_TVD_cue_sec', 'AX_TVD_top_sec', 'AX_TVD_bottom_sec',  # tvd
              'AY_TVD_cue_sec', 'AY_TVD_top_sec', 'AY_TVD_bottom_sec',
              'BX_TVD_cue_sec', 'BX_TVD_top_sec', 'BX_TVD_bottom_sec',
              'BY_TVD_cue_sec', 'BY_TVD_top_sec', 'BY_TVD_bottom_sec',
              'AX_TVD_cue_per_correct_trial', 'AX_TVD_top_per_correct_trial', 'AX_TVD_bottom_per_correct_trial',
              # TVD per correct trial
              'AY_TVD_cue_per_correct_trial', 'AY_TVD_top_per_correct_trial', 'AY_TVD_bottom_per_correct_trial',
              'BX_TVD_cue_per_correct_trial', 'BX_TVD_top_per_correct_trial', 'BX_TVD_bottom_per_correct_trial',
              'BY_TVD_cue_per_correct_trial', 'BY_TVD_top_per_correct_trial', 'BY_TVD_bottom_per_correct_trial',
              'AX_Initial_TVD_Cue_sec',  # initial tvd of cue in seconds
              'AY_Initial_TVD_Cue_sec',
              'BX_Initial_TVD_Cue_sec',
              'BY_Initial_TVD_Cue_sec',
              'AX_Initial_TVD_Cue_per_correct_trial',  # initial tvd of cue per correct trial
              'AY_Initial_TVD_Cue_per_correct_trial',
              'BX_Initial_TVD_Cue_per_correct_trial',
              'BY_Initial_TVD_Cue_per_correct_trial',
              'blk1_AX_TVD_cue_sec', 'blk2_AX_TVD_cue_sec', 'blk3_AX_TVD_cue_sec', 'blk4_AX_TVD_cue_sec',
              # tvd by blocks
              'blk1_AY_TVD_cue_sec', 'blk2_AY_TVD_cue_sec', 'blk3_AY_TVD_cue_sec', 'blk4_AY_TVD_cue_sec',
              'blk1_BX_TVD_cue_sec', 'blk2_BX_TVD_cue_sec', 'blk3_BX_TVD_cue_sec', 'blk4_BX_TVD_cue_sec',
              'blk1_BY_TVD_cue_sec', 'blk2_BY_TVD_cue_sec', 'blk3_BY_TVD_cue_sec', 'blk4_BY_TVD_cue_sec',
              'blk1_AX_TVD_top_sec', 'blk2_AX_TVD_top_sec', 'blk3_AX_TVD_top_sec', 'blk4_AX_TVD_top_sec',
              'blk1_AY_TVD_top_sec', 'blk2_AY_TVD_top_sec', 'blk3_AY_TVD_top_sec', 'blk4_AY_TVD_top_sec',
              'blk1_BX_TVD_top_sec', 'blk2_BX_TVD_top_sec', 'blk3_BX_TVD_top_sec', 'blk4_BX_TVD_top_sec',
              'blk1_BY_TVD_top_sec', 'blk2_BY_TVD_top_sec', 'blk3_BY_TVD_top_sec', 'blk4_BY_TVD_top_sec',
              'blk1_AX_TVD_bottom_sec', 'blk2_AX_TVD_bottom_sec', 'blk3_AX_TVD_bottom_sec', 'blk4_AX_TVD_bottom_sec',
              'blk1_AY_TVD_bottom_sec', 'blk2_AY_TVD_bottom_sec', 'blk3_AY_TVD_bottom_sec', 'blk4_AY_TVD_bottom_sec',
              'blk1_BX_TVD_bottom_sec', 'blk2_BX_TVD_bottom_sec', 'blk3_BX_TVD_bottom_sec', 'blk4_BX_TVD_bottom_sec',
              'blk1_BY_TVD_bottom_sec', 'blk2_BY_TVD_bottom_sec', 'blk3_BY_TVD_bottom_sec', 'blk4_BY_TVD_bottom_sec',
              'AX_Number_of_First_Fixations_Top_B4_Bottom_Probe', 'AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              # num of correct trials by block
              "Blk_1_AX_Number_of_Correct_Trials",
              "Blk_2_AX_Number_of_Correct_Trials",
              "Blk_3_AX_Number_of_Correct_Trials",
              "Blk_4_AX_Number_of_Correct_Trials",
              "Blk_1_AY_Number_of_Correct_Trials",
              "Blk_2_AY_Number_of_Correct_Trials",
              "Blk_3_AY_Number_of_Correct_Trials",
              "Blk_4_AY_Number_of_Correct_Trials",
              "Blk_1_BX_Number_of_Correct_Trials",
              "Blk_2_BX_Number_of_Correct_Trials",
              "Blk_3_BX_Number_of_Correct_Trials",
              "Blk_4_BX_Number_of_Correct_Trials",
              "Blk_1_BY_Number_of_Correct_Trials",
              "Blk_2_BY_Number_of_Correct_Trials",
              "Blk_3_BY_Number_of_Correct_Trials",
              "Blk_4_BY_Number_of_Correct_Trials",
              # number of first fixations
              'AY_Number_of_First_Fixations_Top_B4_Bottom_Probe', 'AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'BX_Number_of_First_Fixations_Top_B4_Bottom_Probe', 'BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'BY_Number_of_First_Fixations_Top_B4_Bottom_Probe', 'BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              # num of first fixation by block
              'Blk_1_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_1_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_2_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_2_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_3_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_3_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_4_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_4_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_1_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_1_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_2_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_2_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_3_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_3_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_4_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_4_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_1_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_1_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_2_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_2_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_3_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_3_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_4_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_4_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_1_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_1_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_2_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_2_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_3_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_3_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              'Blk_4_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
              'Blk_4_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
              # proportion of correct trials
              'Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe', 'Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
              'Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe', 'Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
              'Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe', 'Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
              'Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe', 'Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
              # proportion of correct trials by block
              'Blk_1_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
              'Blk_1_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
              'Blk_2_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
              'Blk_2_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
              'Blk_3_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
              'Blk_3_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
              'Blk_4_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
              'Blk_4_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
              'Blk_1_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
              'Blk_1_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
              'Blk_2_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
              'Blk_2_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
              'Blk_3_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
              'Blk_3_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
              'Blk_4_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
              'Blk_4_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
              'Blk_1_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
              'Blk_1_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
              'Blk_2_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
              'Blk_2_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
              'Blk_3_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
              'Blk_3_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
              'Blk_4_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
              'Blk_4_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
              'Blk_1_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
              'Blk_1_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
              'Blk_2_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
              'Blk_2_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
              'Blk_3_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
              'Blk_3_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
              'Blk_4_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
              'Blk_4_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
              'AX_Time_To_Top_Right_Probe', 'AX_Time_To_Bottom_Right_Probe',  # time to first fixation
              'AY_Time_To_Top_Right_Probe', 'AY_Time_To_Bottom_Right_Probe',
              'BX_Time_To_Top_Right_Probe', 'BX_Time_To_Bottom_Right_Probe',
              'BY_Time_To_Top_Right_Probe', 'BY_Time_To_Bottom_Right_Probe']]

output = pd.DataFrame(columns=mycolumns)

# count will be the unique identifier for each file name
count = 0

# iterate over each file
for file in csv_files:

    ############################################## BEGIN READING EACH FILE ################################################

    # read csv file
    df = pd.read_csv(file)

    # Get relevant columns from df
    df_2 = df[['Subject', 'TrialId', 'Cue', 'AOIProbe1', 'AOIProbe2', 'AOICue', 'AOI', 'AOIStimulus', 'RT',
               'CurrentObject', 'ID']]

    # Get subject id
    subject_id = df_2['Subject'][0]
    if subject_id == 0 or subject_id == np.nan:
        print('No subject id was found!')

    # debug: display subject_id - useful when trying to see which excel file was loaded last before an error!
    print('\n\nAnalyzing subject:', subject_id, '########################################')  # DEBUG LINE

    ########################################### DROP INITIAL PRACTICE TRIALS ###########################################

    print('\nDropping initial practice trials...')  # DEBUG LINE

    # gets us the index of rows where 10 occurs
    idx_of_10 = df_2.index[df_2['TrialId'] == 10].tolist()

    practice_ends_list = []

    count = 0
    for idx_val in idx_of_10:
        # if the subsequent row after a row that has a value of 10 is 1 it means that we found the end of a practice block
        try:
            if df_2.loc[idx_val + 1]['TrialId'] == 1:
                practice_ends_list.append(idx_val + 1)
        except ValueError:
            break
        except KeyError:
            break

    # we get the last end value since if there are multiple practice trials we can delete everything before that
    # df[practice_end::] get everything AFTER the practice trials
    practice_end = practice_ends_list[len(practice_ends_list) - 1]

    df_2 = df_2[practice_end::]  # get everything after the practice trials

    print("Success!")  # DEBUG LINE
    ###################################### PREPARE BLOCK CALCULATIONS #########################################

    print("\nPreparing block calculations...")  # DEBUG LINE

    # GET RELEVANT COLUMNS
    block_df = pd.DataFrame(df_2[['AOI', 'AOICue', 'CurrentObject', 'AOIProbe1', 'AOIProbe2', 'TrialId']])

    ############################################## GET ENDS OF BLOCKS #########################################################

    # once we get the index locations of the end of blocks then we can start at [0:end_index]
    # get rows where == 40 and it's subsequent row is 1 which indicates the end of a block

    # gets us the index of rows where 40 occurs
    idx_of_40 = block_df.index[block_df['TrialId'] == 40].tolist()

    block_ends_list = []

    count = 0
    for idx_val in idx_of_40:
        # if the subsequent row after a row that has a value of 40 is 1 it means that we found the end of a block
        try:
            if block_df.loc[idx_val + 1]['TrialId'] == 1:
                block_ends_list.append(idx_val + 1)
        except ValueError:
            break
        except KeyError:
            break

    block_ends_list.append(block_df.shape[0])  # last block's end will always be the at the last index position

    #     print(subject_id, len(block_ends_list))  # debug to check if block_ends_list's length == 4 blocks

    ####################################### CHECK IF EXCEL FILE HAS 4 BLOCKS #######################################

    # we pass the gazedata file and move onto the next one if there isn't actually 4 blocks in it
    if len(block_ends_list) != 4:
        print("\nThis file does not have 4 blocks!!! Moving onto next file...")
        continue

    ################################################ GET EACH BLOCK ###########################################################

    block_1 = 0
    block_2 = 0
    block_3 = 0
    block_4 = 0

    for index, val in enumerate(block_ends_list):
        if index == 0:
            block_1 = block_df[:val]
        elif index == 1:
            # index - 1 since we do not include previous row where TrialId = 40 (last row of previous block)
            block_2 = block_df[block_ends_list[index - 1]:val]
        elif index == 2:
            block_3 = block_df[block_ends_list[index - 1]:val]
        else:
            block_4 = block_df[block_ends_list[index - 1]:val]

    print("Success!")  # DEBUG LINE

    ############################### AOI VISIT COUNT ################################

    print("\nBegin AOI Visit Count analysis...")

    # For AX, AY, BX, and BY trials how many times did they visit each queue locations (AOI),
    # ONLY during the ISI and for only correct trials?

    # get relevant columns
    count_aoi = pd.DataFrame(df_2[['AOI', 'AOICue', 'CurrentObject', 'AOIProbe1', 'AOIProbe2', 'TrialId']])

    # AX - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #
    try:
        counter_AX = pd.DataFrame(count_aoi['AOI'][(count_aoi['AOI'].diff() != 0) &
                                                   (count_aoi['AOICue'] == 'A') &
                                                   (count_aoi['AOIProbe1'] == 'X') &
                                                   (count_aoi['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        counter_AX = counter_AX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename({'index': 'AOI'}, axis=1)
        counter_AX = counter_AX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        counter_AX[['Cue_Probe']] = pd.DataFrame(index=counter_AX.index, columns=['Cue_Probe']).fillna('AX')
        counter_AX = counter_AX.reset_index()

        if 3 not in counter_AX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            counter_AX = counter_AX.append(dict3, ignore_index=True)  # AOI3

        if 2 not in counter_AX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            counter_AX = counter_AX.append(dict2, ignore_index=True)  # AOI2

        if 1 not in counter_AX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            counter_AX = counter_AX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        counter_AX = 0

    # AY - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #
    try:
        counter_AY = pd.DataFrame(count_aoi['AOI'][(count_aoi['AOI'].diff() != 0) &
                                                   (count_aoi['AOICue'] == 'A') &
                                                   ~(count_aoi['AOIProbe1'] == 'X') &
                                                   (count_aoi['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        counter_AY = counter_AY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename({'index': 'AOI'}, axis=1)
        counter_AY = counter_AY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        counter_AY[['Cue_Probe']] = pd.DataFrame(index=counter_AY.index, columns=['Cue_Probe']).fillna('AY')
        counter_AY = counter_AY.reset_index()

        if 3 not in counter_AY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            counter_AY = counter_AY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in counter_AY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            counter_AY = counter_AY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in counter_AY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            counter_AY = counter_AY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        counter_AY = 0

    # BX - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #
    try:
        counter_BX = pd.DataFrame(count_aoi['AOI'][(count_aoi['AOI'].diff() != 0) &
                                                   (count_aoi['AOICue'] == 'B') &
                                                   (count_aoi['AOIProbe2'] == 'X') &
                                                   (count_aoi['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        counter_BX = counter_BX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename({'index': 'AOI'}, axis=1)
        counter_BX = counter_BX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        counter_BX[['Cue_Probe']] = pd.DataFrame(index=counter_BX.index, columns=['Cue_Probe']).fillna('BX')
        counter_BX = counter_BX.reset_index()

        if 3 not in counter_BX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            counter_BX = counter_BX.append(dict3, ignore_index=True)  # AOI3

        if 2 not in counter_BX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            counter_BX = counter_BX.append(dict2, ignore_index=True)  # AOI2

        if 1 not in counter_BX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            counter_BX = counter_BX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        counter_BX = 0

    # BY - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #
    try:
        counter_BY = pd.DataFrame(count_aoi['AOI'][(count_aoi['AOI'].diff() != 0) &
                                                   (count_aoi['AOICue'] == 'B') &
                                                   ~(count_aoi['AOIProbe2'] == 'X') &
                                                   (count_aoi['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        counter_BY = counter_BY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename({'index': 'AOI'}, axis=1)
        counter_BY = counter_BY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        counter_BY[['Cue_Probe']] = pd.DataFrame(index=counter_BY.index, columns=['Cue_Probe']).fillna('BY')
        counter_BY = counter_BY.reset_index()

        if 3 not in counter_BY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            counter_BY = counter_BY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in counter_BY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            counter_BY = counter_BY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in counter_BY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            counter_BY = counter_BY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        counter_BY = 0

    # FORMAT RESULTS --------------------------------------------------------------------------------------------------------- #

    # GET VALUES AND ASSIGN TO VARIABLES
    # AX
    try:
        AX_AOI1_visits = counter_AX['visit_counter'][counter_AX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        AX_AOI1_visits = 0
    try:
        AX_AOI2_visits = counter_AX['visit_counter'][counter_AX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        AX_AOI2_visits = 0
    try:
        AX_AOI3_visits = counter_AX['visit_counter'][counter_AX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        AX_AOI3_visits = 0

    # AY
    try:
        AY_AOI1_visits = counter_AY['visit_counter'][counter_AY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        AY_AOI1_visits = 0
    try:
        AY_AOI2_visits = counter_AY['visit_counter'][counter_AY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        AY_AOI2_visits = 0
    try:
        AY_AOI3_visits = counter_AY['visit_counter'][counter_AY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        AY_AOI3_visits = 0

    # BX
    try:
        BX_AOI1_visits = counter_BX['visit_counter'][counter_BX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        BX_AOI1_visits = 0
    try:
        BX_AOI2_visits = counter_BX['visit_counter'][counter_BX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        BX_AOI2_visits = 0
    try:
        BX_AOI3_visits = counter_BX['visit_counter'][counter_BX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        BX_AOI3_visits = 0

    # BY
    try:
        BY_AOI1_visits = counter_BY['visit_counter'][counter_BY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        BY_AOI1_visits = 0
    try:
        BY_AOI2_visits = counter_BY['visit_counter'][counter_BY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        BY_AOI2_visits = 0
    try:
        BY_AOI3_visits = counter_BY['visit_counter'][counter_BY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        BY_AOI3_visits = 0

    print("Success!")  # DEBUG LINE

    ############################### TOTAL VISIT DURATION ###############################

    print("\nBegin Total Visit Duration analysis...")

    # total visit duration (TVD) - the combined sum of the length of all their visits in that AOI (Area of Interest)
    # NOT by visit count. Need the length of ONE instance of their visit count, multiply that instance by 16.67
    # and divide by 1000 then get the next until we have all lengths of each visit and SUM all of them for a final total!
    # AOI 3 = top, AOI 2 = bottom

    # define tvd_calculation function which will take in a number in a cell of a particular column and perform operation
    def tvd_calculation(count):
        return count * 16.65496782 / 1000


    # get relevant columns (tv = total visits)
    tv = df_2[['AOI', 'AOICue', 'CurrentObject', 'AOIProbe1', 'AOIProbe2', 'TrialId']]

    # AX - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #

    # filter dataframe to correct conditions
    tv_AX = tv[(tv['AOICue'] == 'A') &
               (tv['AOIProbe1'] == 'X') &
               (tv['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AX['interval'] = (tv_AX['AOI'] != tv_AX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AX['count'] = tv_AX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AX = tv_AX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AX_cue = tv_AX[tv_AX['AOI'] == 3]
    tv_AX_top = tv_AX[tv_AX['AOI'] == 1]
    tv_AX_bottom = tv_AX[tv_AX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        tvd_ax_cue = np.vectorize(tvd_calculation)(tv_AX_cue['count']).sum()
    except ValueError:
        tvd_ax_cue = 0
    try:
        tvd_ax_top = np.vectorize(tvd_calculation)(tv_AX_top['count']).sum()
    except ValueError:
        tvd_ax_top = 0
    try:
        tvd_ax_bottom = np.vectorize(tvd_calculation)(tv_AX_bottom['count']).sum()
    except ValueError:
        tvd_ax_bottom = 0

    # AY - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #

    # filter dataframe to correct conditions
    tv_AY = tv[(tv['AOICue'] == 'A') &
               ~(tv['AOIProbe1'] == 'X') &
               (tv['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AY['interval'] = (tv_AY['AOI'] != tv_AY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AY['count'] = tv_AY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AY = tv_AY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AY_cue = tv_AY[tv_AY['AOI'] == 3]
    tv_AY_top = tv_AY[tv_AY['AOI'] == 1]
    tv_AY_bottom = tv_AY[tv_AY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        tvd_ay_cue = np.vectorize(tvd_calculation)(tv_AY_cue['count']).sum()
    except ValueError:
        tvd_ay_cue = 0
    try:
        tvd_ay_top = np.vectorize(tvd_calculation)(tv_AY_top['count']).sum()
    except ValueError:
        tvd_ay_top = 0
    try:
        tvd_ay_bottom = np.vectorize(tvd_calculation)(tv_AY_bottom['count']).sum()  # try this and if error:
    except ValueError:
        tvd_ay_bottom = 0  # set to 0 (means that participant never looked at AOI2 on AY trial)

    # BX - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #

    # filter dataframe to correct conditions
    tv_BX = tv[(tv['AOICue'] == 'B') &
               (tv['AOIProbe2'] == 'X') &
               (tv['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BX['interval'] = (tv_BX['AOI'] != tv_BX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BX['count'] = tv_BX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BX = tv_BX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BX_cue = tv_BX[tv_BX['AOI'] == 3]
    tv_BX_top = tv_BX[tv_BX['AOI'] == 1]
    tv_BX_bottom = tv_BX[tv_BX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        tvd_bx_cue = np.vectorize(tvd_calculation)(tv_BX_cue['count']).sum()
    except ValueError:
        tvd_bx_cue = 0
    try:
        tvd_bx_top = np.vectorize(tvd_calculation)(tv_BX_top['count']).sum()
    except ValueError:
        tvd_bx_top = 0
    try:
        tvd_bx_bottom = np.vectorize(tvd_calculation)(tv_BX_bottom['count']).sum()
    except ValueError:
        tvd_bx_bottom = 0

    # BY - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #

    # filter dataframe to correct conditions
    tv_BY = tv[(tv['AOICue'] == 'B') &
               ~(tv['AOIProbe2'] == 'X') &
               (tv['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BY['interval'] = (tv_BY['AOI'] != tv_BY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BY['count'] = tv_BY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BY = tv_BY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BY_cue = tv_BY[tv_BY['AOI'] == 3]
    tv_BY_top = tv_BY[tv_BY['AOI'] == 1]
    tv_BY_bottom = tv_BY[tv_BY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        tvd_by_cue = np.vectorize(tvd_calculation)(tv_BY_cue['count']).sum()
    except ValueError:
        tvd_by_cue = 0
    try:
        tvd_by_top = np.vectorize(tvd_calculation)(tv_BY_top['count']).sum()
    except ValueError:
        tvd_by_top = 0
    try:
        tvd_by_bottom = np.vectorize(tvd_calculation)(tv_BY_bottom['count']).sum()
    except ValueError:
        tvd_by_bottom = 0

    data = [[tvd_ax_cue, tvd_ax_top, tvd_ax_bottom],
            [tvd_ay_cue, tvd_ay_top, tvd_ay_bottom],
            [tvd_bx_cue, tvd_bx_top, tvd_bx_bottom],
            [tvd_by_cue, tvd_by_top, tvd_by_bottom]]

    tvd = pd.DataFrame(data=data, index=['AX', 'AY', 'BX', 'BY'],
                       columns=[['TVD_Cue_Sec', 'TVD_Top_Sec', 'TVD_Bottom_Sec']])

    print("Success!")  # DEBUG LINE

            ############################################ TVD WITHIN TRIALS (cue) #####################################################
    print("\nBegin TVD within trials analysis...")  # DEBUG LINE
    # TVD within trials meaning for each trial, how long did they look at a specific condition (AX, AY, BX, BY)

    # NewTrialId NOTE that in the resultant output xlsx file, NewTrialId's start from 11 - 170 where we expect 1 - 160.
    # this is because it WOULD start from 11 if we consider the 10 practice trials. So really 11 is 1, 12 is 2 and so on.

    # get relevant columns (tv = total visits)
    tv_within = df_2[['AOI', 'AOICue', 'CurrentObject', 'AOIProbe1', 'AOIProbe2', 'TrialId', 'ID']]

    # NewTrialId - 
    # obtain the modified DataFrame with the additional column 'NewTrialId' that starts at 1 and increments 
    # whenever there is a change in the value of column 'TrialId'. 
    # e.g TrialId = [1, 1, 1, 2, 2, 2, 3, 3, 3, 10, 10, 10, 1, 1] - repeats after 10
    #     NewTrialId = [1, 1 ,1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5] - no longer repeats; continuous/sequential
    tv_within['NewTrialId'] = (df['TrialId'] != df['TrialId'].shift()).cumsum()

    # AX - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #

    # filter dataframe to correct conditions
    tv_AX_within = tv_within[(tv_within['AOICue'] == 'A') &
               (tv_within['AOIProbe1'] == 'X') &
               (tv_within['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AX_within['interval'] = (tv_AX_within['AOI'] != tv_AX_within['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AX_within['count'] = tv_AX_within.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AX_within = tv_AX_within.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AX_cue_within = tv_AX_within[tv_AX_within['AOI'] == 3]

    # groupby NewTrialId, drop irrelevant columns, reset index so that NewTrialId is a column itself
    tv_AX_cue_within = tv_AX_cue_within.groupby('NewTrialId').sum().drop(columns=['interval', 'AOI', 'ID', 'TrialId']).reset_index()

    # new column performing calculations on count values
    tv_AX_cue_within['tvd_within_trial'] = np.vectorize(tvd_calculation)(tv_AX_cue_within['count'])

    # new column specifying that these are all AX data
    tv_AX_cue_within.insert(1, 'condition', 'AX')

    # new column for specifying subject number
    tv_AX_cue_within.insert(0, 'Subject', df_2['Subject'].iloc[0])

    # AY - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #

    # filter dataframe to correct conditions
    tv_AY_within = tv_within[(tv_within['AOICue'] == 'A') &
               ~(tv_within['AOIProbe1'] == 'X') &
               (tv_within['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AY_within['interval'] = (tv_AY_within['AOI'] != tv_AY_within['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AY_within['count'] = tv_AY_within.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AY_within = tv_AY_within.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AY_cue_within = tv_AY_within[tv_AY_within['AOI'] == 3]

    # groupby NewTrialId, drop irrelevant columns, reset index so that NewTrialId is a column itself
    tv_AY_cue_within = tv_AY_cue_within.groupby('NewTrialId').sum().drop(columns=['interval', 'AOI', 'ID', 'TrialId']).reset_index()

    # new column performing calculations on count values
    tv_AY_cue_within['tvd_within_trial'] = np.vectorize(tvd_calculation)(tv_AY_cue_within['count'])

    # new column specifying that these are all AY data
    tv_AY_cue_within.insert(1, 'condition', 'AY')

    # new column for specifying subject number
    tv_AY_cue_within.insert(0, 'Subject', df_2['Subject'].iloc[0])

    # BX - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #

    # filter dataframe to correct conditions
    tv_BX_within = tv_within[(tv_within['AOICue'] == 'B') &
               (tv_within['AOIProbe2'] == 'X') &
               (tv_within['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BX_within['interval'] = (tv_BX_within['AOI'] != tv_BX_within['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BX_within['count'] = tv_BX_within.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BX_within = tv_BX_within.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BX_cue_within = tv_BX_within[tv_BX_within['AOI'] == 3]

    # groupby NewTrialId, drop irrelevant columns, reset index so that NewTrialId is a column itself
    tv_BX_cue_within = tv_BX_cue_within.groupby('NewTrialId').sum().drop(columns=['interval', 'AOI', 'ID', 'TrialId']).reset_index()

    # new column performing calculations on count values
    tv_BX_cue_within['tvd_within_trial'] = np.vectorize(tvd_calculation)(tv_BX_cue_within['count'])

    # new column specifying that these are all BX data
    tv_BX_cue_within.insert(1, 'condition', 'BX')

    # new column for specifying subject number
    tv_BX_cue_within.insert(0, 'Subject', df_2['Subject'].iloc[0])

    # BY - PERFORM OPERATIONS ------------------------------------------------------------------------------------------------ #

    # filter dataframe to correct conditions
    tv_BY_within = tv_within[(tv_within['AOICue'] == 'B') &
               ~(tv_within['AOIProbe2'] == 'X') &
               (tv_within['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BY_within['interval'] = (tv_BY_within['AOI'] != tv_BY_within['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BY_within['count'] = tv_BY_within.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BY_within = tv_BY_within.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BY_cue_within = tv_BY_within[tv_BY_within['AOI'] == 3]

    # groupby NewTrialId, drop irrelevant columns, reset index so that NewTrialId is a column itself
    tv_BY_cue_within = tv_BY_cue_within.groupby('NewTrialId').sum().drop(columns=['interval', 'AOI', 'ID', 'TrialId']).reset_index()

    # new column performing calculations on count values
    tv_BY_cue_within['tvd_within_trial'] = np.vectorize(tvd_calculation)(tv_BY_cue_within['count'])

    # new column specifying that these are all BY data
    tv_BY_cue_within.insert(1, 'condition', 'BY')

    # new column for specifying subject number
    tv_BY_cue_within.insert(0, 'Subject', df_2['Subject'].iloc[0])

    # # -------------------------------- Formatting merged dataframes for TVD within trials ---------------------------------

    # Combine the dataframes into one
    combined_df_within = pd.concat([tv_AX_cue_within, tv_AY_cue_within, tv_BX_cue_within, tv_BY_cue_within], ignore_index=True)

    # sort the combined dataframe by 'NewTrialId' column
    combined_df_within_sorted = combined_df_within.sort_values('NewTrialId')

    # reset index so numbered from 0 up to ~160
    combined_df_within_sorted = combined_df_within_sorted.reset_index(drop=True)


    # append df
    print("Appending to cue_tvd_within_trials_df_list = []")  # DEBUG LINE
    cue_tvd_within_trials_df_list.append(combined_df_within_sorted)
    print("Success!")  # DEBUG LINE
    
    
    ################################################ BLOCK AOI VISIT COUNT ####################################################

    print("\nBegin BLOCK AOI Visit Count analysis...")  # DEBUG LINE

    # ****************************************** BLOCK 1 PERFORM OPERATIONS ***********************************************
    blk1_counter_AX = 0
    blk1_counter_AY = 0
    blk1_counter_BX = 0
    blk1_counter_BY = 0

    # AX Block 1 -------------------------------------------------------------------------------------------------------------
    try:
        blk1_counter_AX = pd.DataFrame(block_1['AOI'][(block_1['AOI'].diff() != 0) &
                                                      (block_1['AOICue'] == 'A') &
                                                      (block_1['AOIProbe1'] == 'X') &
                                                      (block_1['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk1_counter_AX = blk1_counter_AX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk1_counter_AX = blk1_counter_AX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk1_counter_AX[['Cue_Probe']] = pd.DataFrame(index=blk1_counter_AX.index, columns=['Cue_Probe']).fillna('AX')
        blk1_counter_AX = blk1_counter_AX.reset_index()

        if 3 not in blk1_counter_AX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk1_counter_AX = blk1_counter_AX.append(dict3, ignore_index=True)  # AOI3
        if 2 not in blk1_counter_AX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk1_counter_AX = blk1_counter_AX.append(dict2, ignore_index=True)  # AOI2
        if 1 not in blk1_counter_AX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk1_counter_AX = blk1_counter_AX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk1_counter_AX = 0

    # AY Block 1 -------------------------------------------------------------------------------------------------------------
    try:
        blk1_counter_AY = pd.DataFrame(block_1['AOI'][(block_1['AOI'].diff() != 0) &
                                                      (block_1['AOICue'] == 'A') &
                                                      ~(block_1['AOIProbe1'] == 'X') &
                                                      (block_1['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk1_counter_AY = blk1_counter_AY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk1_counter_AY = blk1_counter_AY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk1_counter_AY[['Cue_Probe']] = pd.DataFrame(index=blk1_counter_AY.index, columns=['Cue_Probe']).fillna('AY')
        blk1_counter_AY = blk1_counter_AY.reset_index()

        if 3 not in blk1_counter_AY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk1_counter_AY = blk1_counter_AY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk1_counter_AY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk1_counter_AY = blk1_counter_AY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk1_counter_AY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk1_counter_AY = blk1_counter_AY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk1_counter_AY = 0

    # BX Block 1 -------------------------------------------------------------------------------------------------------------
    try:
        blk1_counter_BX = pd.DataFrame(block_1['AOI'][(block_1['AOI'].diff() != 0) &
                                                      (block_1['AOICue'] == 'B') &
                                                      (block_1['AOIProbe2'] == 'X') &
                                                      (block_1['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk1_counter_BX = blk1_counter_BX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk1_counter_BX = blk1_counter_BX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk1_counter_BX[['Cue_Probe']] = pd.DataFrame(index=blk1_counter_BX.index, columns=['Cue_Probe']).fillna('BX')
        blk1_counter_BX = blk1_counter_BX.reset_index()

        if 3 not in blk1_counter_BX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk1_counter_BX = blk1_counter_BX.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk1_counter_BX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk1_counter_BX = blk1_counter_BX.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk1_counter_BX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk1_counter_BX = blk1_counter_BX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk1_counter_BX = 0

    # BY Block 1 -------------------------------------------------------------------------------------------------------------
    try:
        blk1_counter_BY = pd.DataFrame(block_1['AOI'][(block_1['AOI'].diff() != 0) &
                                                      (block_1['AOICue'] == 'B') &
                                                      ~(block_1['AOIProbe2'] == 'X') &
                                                      (block_1['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk1_counter_BY = blk1_counter_BY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk1_counter_BY = blk1_counter_BY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk1_counter_BY[['Cue_Probe']] = pd.DataFrame(index=blk1_counter_BY.index, columns=['Cue_Probe']).fillna('BY')
        blk1_counter_BY = blk1_counter_BY.reset_index()

        if 3 not in blk1_counter_BY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk1_counter_BY = blk1_counter_BY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk1_counter_BY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk1_counter_BY = blk1_counter_BY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk1_counter_BY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk1_counter_BY = blk1_counter_BY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk1_counter_BY = 0

    print("Block 1 done")  # DEBUG LINE

    # ******************************************* BLOCK 2 PERFORM OPERATIONS **************************************************
    blk2_counter_AX = 0
    blk2_counter_AY = 0
    blk2_counter_BX = 0
    blk2_counter_BY = 0

    # AX Block 2 -------------------------------------------------------------------------------------------------------------
    try:
        blk2_counter_AX = pd.DataFrame(block_2['AOI'][(block_2['AOI'].diff() != 0) &
                                                      (block_2['AOICue'] == 'A') &
                                                      (block_2['AOIProbe1'] == 'X') &
                                                      (block_2['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk2_counter_AX = blk2_counter_AX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk2_counter_AX = blk2_counter_AX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk2_counter_AX[['Cue_Probe']] = pd.DataFrame(index=blk2_counter_AX.index, columns=['Cue_Probe']).fillna('AX')
        blk2_counter_AX = blk2_counter_AX.reset_index()

        if 3 not in blk2_counter_AX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk2_counter_AX = blk2_counter_AX.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk2_counter_AX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk2_counter_AX = blk2_counter_AX.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk2_counter_AX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk2_counter_AX = blk2_counter_AX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk2_counter_AX = 0

    # AY Block 2 -------------------------------------------------------------------------------------------------------------
    try:
        blk2_counter_AY = pd.DataFrame(block_2['AOI'][(block_2['AOI'].diff() != 0) &
                                                      (block_2['AOICue'] == 'A') &
                                                      ~(block_2['AOIProbe1'] == 'X') &
                                                      (block_2['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk2_counter_AY = blk2_counter_AY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk2_counter_AY = blk2_counter_AY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk2_counter_AY[['Cue_Probe']] = pd.DataFrame(index=blk2_counter_AY.index, columns=['Cue_Probe']).fillna('AY')
        blk2_counter_AY = blk2_counter_AY.reset_index()

        if 3 not in blk2_counter_AY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk2_counter_AY = blk2_counter_AY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk2_counter_AY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk2_counter_AY = blk2_counter_AY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk2_counter_AY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk2_counter_AY = blk2_counter_AY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk2_counter_AY = 0

    # BX Block 2 -------------------------------------------------------------------------------------------------------------
    try:
        blk2_counter_BX = pd.DataFrame(block_2['AOI'][(block_2['AOI'].diff() != 0) &
                                                      (block_2['AOICue'] == 'B') &
                                                      (block_2['AOIProbe2'] == 'X') &
                                                      (block_2['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk2_counter_BX = blk2_counter_BX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk2_counter_BX = blk2_counter_BX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk2_counter_BX[['Cue_Probe']] = pd.DataFrame(index=blk2_counter_BX.index, columns=['Cue_Probe']).fillna('BX')
        blk2_counter_BX = blk2_counter_BX.reset_index()

        if 3 not in blk2_counter_BX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk2_counter_BX = blk2_counter_BX.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk2_counter_BX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk2_counter_BX = blk2_counter_BX.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk2_counter_BX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk2_counter_BX = blk2_counter_BX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk2_counter_BX = 0

    # BY Block 2 -------------------------------------------------------------------------------------------------------------
    try:
        blk2_counter_BY = pd.DataFrame(block_2['AOI'][(block_2['AOI'].diff() != 0) &
                                                      (block_2['AOICue'] == 'B') &
                                                      ~(block_2['AOIProbe2'] == 'X') &
                                                      (block_2['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk2_counter_BY = blk2_counter_BY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk2_counter_BY = blk2_counter_BY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk2_counter_BY[['Cue_Probe']] = pd.DataFrame(index=blk2_counter_BY.index, columns=['Cue_Probe']).fillna('BY')
        blk2_counter_BY = blk2_counter_BY.reset_index()

        if 3 not in blk2_counter_BY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk2_counter_BY = blk2_counter_BY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk2_counter_BY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk2_counter_BY = blk2_counter_BY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk2_counter_BY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk2_counter_BY = blk2_counter_BY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk2_counter_BY = 0

    print("Block 2 done")  # DEBUG LINE

    # ******************************************* BLOCK 3 PERFORM OPERATIONS **************************************************
    blk3_counter_AX = 0
    blk3_counter_AY = 0
    blk3_counter_BX = 0
    blk3_counter_BY = 0

    # AX Block 3 -------------------------------------------------------------------------------------------------------------
    try:
        blk3_counter_AX = pd.DataFrame(block_3['AOI'][(block_3['AOI'].diff() != 0) &
                                                      (block_3['AOICue'] == 'A') &
                                                      (block_3['AOIProbe1'] == 'X') &
                                                      (block_3['CurrentObject'] == 'ISI')].value_counts())
        # format columns
        blk3_counter_AX = blk3_counter_AX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk3_counter_AX = blk3_counter_AX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk3_counter_AX[['Cue_Probe']] = pd.DataFrame(index=blk3_counter_AX.index, columns=['Cue_Probe']).fillna('AX')
        blk3_counter_AX = blk3_counter_AX.reset_index()

        if 3 not in blk3_counter_AX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk3_counter_AX = blk3_counter_AX.append(dict3, ignore_index=True)  # AOI3
        if 2 not in blk3_counter_AX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk3_counter_AX = blk3_counter_AX.append(dict2, ignore_index=True)  # AOI2
        if 1 not in blk3_counter_AX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk3_counter_AX = blk3_counter_AX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk3_counter_AX = 0

    # AY Block 3 -------------------------------------------------------------------------------------------------------------
    try:
        blk3_counter_AY = pd.DataFrame(block_3['AOI'][(block_3['AOI'].diff() != 0) &
                                                      (block_3['AOICue'] == 'A') &
                                                      ~(block_3['AOIProbe1'] == 'X') &
                                                      (block_3['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk3_counter_AY = blk3_counter_AY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk3_counter_AY = blk3_counter_AY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk3_counter_AY[['Cue_Probe']] = pd.DataFrame(index=blk3_counter_AY.index, columns=['Cue_Probe']).fillna('AY')
        blk3_counter_AY = blk3_counter_AY.reset_index()

        if 3 not in blk3_counter_AY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk3_counter_AY = blk3_counter_AY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk3_counter_AY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk3_counter_AY = blk3_counter_AY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk3_counter_AY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk3_counter_AY = blk3_counter_AY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk3_counter_AY = 0

    # BX Block 3 -------------------------------------------------------------------------------------------------------------
    try:
        blk3_counter_BX = pd.DataFrame(block_3['AOI'][(block_3['AOI'].diff() != 0) &
                                                      (block_3['AOICue'] == 'B') &
                                                      (block_3['AOIProbe2'] == 'X') &
                                                      (block_3['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk3_counter_BX = blk3_counter_BX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk3_counter_BX = blk3_counter_BX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk3_counter_BX[['Cue_Probe']] = pd.DataFrame(index=blk3_counter_BX.index, columns=['Cue_Probe']).fillna('BX')
        blk3_counter_BX = blk3_counter_BX.reset_index()

        if 3 not in blk3_counter_BX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk3_counter_BX = blk3_counter_BX.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk3_counter_BX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk3_counter_BX = blk3_counter_BX.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk3_counter_BX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk3_counter_BX = blk3_counter_BX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk3_counter_BX = 0

    # BY Block 3 -------------------------------------------------------------------------------------------------------------
    try:
        blk3_counter_BY = pd.DataFrame(block_3['AOI'][(block_3['AOI'].diff() != 0) &
                                                      (block_3['AOICue'] == 'B') &
                                                      ~(block_3['AOIProbe2'] == 'X') &
                                                      (block_3['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk3_counter_BY = blk3_counter_BY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk3_counter_BY = blk3_counter_BY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk3_counter_BY[['Cue_Probe']] = pd.DataFrame(index=blk3_counter_BY.index, columns=['Cue_Probe']).fillna('BY')
        blk3_counter_BY = blk3_counter_BY.reset_index()

        if 3 not in blk3_counter_BY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk3_counter_BY = blk3_counter_BY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk3_counter_BY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk3_counter_BY = blk3_counter_BY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk3_counter_BY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk3_counter_BY = blk3_counter_BY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk3_counter_BY = 0

    print("Block 3 done")  # DEBUG LINE

    # ******************************************* BLOCK 4 PERFORM OPERATIONS **************************************************
    blk4_counter_AX = 0
    blk4_counter_AY = 0
    blk4_counter_BX = 0
    blk4_counter_BY = 0

    # AX Block 4 -------------------------------------------------------------------------------------------------------------
    try:
        blk4_counter_AX = pd.DataFrame(block_4['AOI'][(block_4['AOI'].diff() != 0) &
                                                      (block_4['AOICue'] == 'A') &
                                                      (block_4['AOIProbe1'] == 'X') &
                                                      (block_4['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk4_counter_AX = blk4_counter_AX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk4_counter_AX = blk4_counter_AX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk4_counter_AX[['Cue_Probe']] = pd.DataFrame(index=blk4_counter_AX.index, columns=['Cue_Probe']).fillna('AX')
        blk4_counter_AX = blk4_counter_AX.reset_index()

        if 3 not in blk4_counter_AX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk4_counter_AX = blk4_counter_AX.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk4_counter_AX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk4_counter_AX = blk4_counter_AX.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk4_counter_AX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AX'}
            blk4_counter_AX = blk4_counter_AX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk4_counter_AX = 0

    # AY Block 4 -------------------------------------------------------------------------------------------------------------
    try:
        blk4_counter_AY = pd.DataFrame(block_4['AOI'][(block_4['AOI'].diff() != 0) &
                                                      (block_4['AOICue'] == 'A') &
                                                      ~(block_4['AOIProbe1'] == 'X') &
                                                      (block_4['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk4_counter_AY = blk4_counter_AY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk4_counter_AY = blk4_counter_AY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk4_counter_AY[['Cue_Probe']] = pd.DataFrame(index=blk4_counter_AY.index, columns=['Cue_Probe']).fillna('AY')
        blk4_counter_AY = blk4_counter_AY.reset_index()

        if 3 not in blk4_counter_AY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk4_counter_AY = blk4_counter_AY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk4_counter_AY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk4_counter_AY = blk4_counter_AY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk4_counter_AY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'AY'}
            blk4_counter_AY = blk4_counter_AY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk4_counter_AY = 0

    # BX Block 4 -------------------------------------------------------------------------------------------------------------
    try:
        blk4_counter_BX = pd.DataFrame(block_4['AOI'][(block_4['AOI'].diff() != 0) &
                                                      (block_4['AOICue'] == 'B') &
                                                      (block_4['AOIProbe2'] == 'X') &
                                                      (block_4['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk4_counter_BX = blk4_counter_BX.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk4_counter_BX = blk4_counter_BX.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk4_counter_BX[['Cue_Probe']] = pd.DataFrame(index=blk4_counter_BX.index, columns=['Cue_Probe']).fillna('BX')
        blk4_counter_BX = blk4_counter_BX.reset_index()

        if 3 not in blk4_counter_BX['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk4_counter_BX = blk4_counter_BX.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk4_counter_BX['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk4_counter_BX = blk4_counter_BX.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk4_counter_BX['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BX'}
            blk4_counter_BX = blk4_counter_BX.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk4_counter_BX = 0

    # BY Block 4 -------------------------------------------------------------------------------------------------------------
    try:
        blk4_counter_BY = pd.DataFrame(block_4['AOI'][(block_4['AOI'].diff() != 0) &
                                                      (block_4['AOICue'] == 'B') &
                                                      ~(block_4['AOIProbe2'] == 'X') &
                                                      (block_4['CurrentObject'] == 'ISI')].value_counts())

        # format columns
        blk4_counter_BY = blk4_counter_BY.rename({'AOI': 'visit_counter'}, axis=1).reset_index().rename(
            {'index': 'AOI'}, axis=1)
        blk4_counter_BY = blk4_counter_BY.astype({'AOI': 'int'}).sort_values('AOI', ascending=False)
        blk4_counter_BY[['Cue_Probe']] = pd.DataFrame(index=blk4_counter_BY.index, columns=['Cue_Probe']).fillna('BY')
        blk4_counter_BY = blk4_counter_BY.reset_index()

        if 3 not in blk4_counter_BY['AOI'].values:
            dict3 = {'index': 0, 'AOI': 3, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk4_counter_BY = blk4_counter_BY.append(dict3, ignore_index=True)  # AOI3

        if 2 not in blk4_counter_BY['AOI'].values:
            dict2 = {'index': 0, 'AOI': 2, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk4_counter_BY = blk4_counter_BY.append(dict2, ignore_index=True)  # AOI2

        if 1 not in blk4_counter_BY['AOI'].values:
            dict1 = {'index': 0, 'AOI': 1, 'visit_counter': 0, 'Cue_Probe': 'BY'}
            blk4_counter_BY = blk4_counter_BY.append(dict1, ignore_index=True)  # AOI1

    except TypeError:
        blk4_counter_BY = 0

    print("Block 4 done")  # DEBUG LINE

    # FORMAT BLOCK RESULTS ***************************************************************************************************

    print("Formatting...")  # DEBUG LINE

    # Block 1 formatting -------------------------------------------------------------------------------------------------------------

    # GET VALUES AND ASSIGN TO VARIABLES

    # Sometimes index values are not as expected since if they never visited AOI2, then dataframe
    # we're accessing will only contain AOI1 and AOI3 which results in indexes 0 and 1 instead of 0, 1, and 2.

    # AX
    try:
        blk1_AX_AOI1_visits = blk1_counter_AX['visit_counter'][blk1_counter_AX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk1_AX_AOI1_visits = 0
    try:
        blk1_AX_AOI2_visits = blk1_counter_AX['visit_counter'][blk1_counter_AX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk1_AX_AOI2_visits = 0
    try:
        blk1_AX_AOI3_visits = blk1_counter_AX['visit_counter'][blk1_counter_AX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk1_AX_AOI3_visits = 0

    # AY
    try:
        blk1_AY_AOI1_visits = blk1_counter_AY['visit_counter'][blk1_counter_AY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk1_AY_AOI1_visits = 0
    try:
        blk1_AY_AOI2_visits = blk1_counter_AY['visit_counter'][blk1_counter_AY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk1_AY_AOI2_visits = 0
    try:
        blk1_AY_AOI3_visits = blk1_counter_AY['visit_counter'][blk1_counter_AY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk1_AY_AOI3_visits = 0

    # BX
    try:
        blk1_BX_AOI1_visits = blk1_counter_BX['visit_counter'][blk1_counter_BX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk1_BX_AOI1_visits = 0
    try:
        blk1_BX_AOI2_visits = blk1_counter_BX['visit_counter'][blk1_counter_BX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk1_BX_AOI2_visits = 0
    try:
        blk1_BX_AOI3_visits = blk1_counter_BX['visit_counter'][blk1_counter_BX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk1_BX_AOI3_visits = 0

        # BY
    try:
        blk1_BY_AOI1_visits = blk1_counter_BY['visit_counter'][blk1_counter_BY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk1_BY_AOI1_visits = 0
    try:
        blk1_BY_AOI2_visits = blk1_counter_BY['visit_counter'][blk1_counter_BY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk1_BY_AOI2_visits = 0
    try:
        blk1_BY_AOI3_visits = blk1_counter_BY['visit_counter'][blk1_counter_BY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk1_BY_AOI3_visits = 0

    # Block 2 formatting -------------------------------------------------------------------------------------------------------------

    # GET VALUES AND ASSIGN TO VARIABLES

    # AX
    try:
        blk2_AX_AOI1_visits = blk2_counter_AX['visit_counter'][blk2_counter_AX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk2_AX_AOI1_visits = 0
    try:
        blk2_AX_AOI2_visits = blk2_counter_AX['visit_counter'][blk2_counter_AX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk2_AX_AOI2_visits = 0
    try:
        blk2_AX_AOI3_visits = blk2_counter_AX['visit_counter'][blk2_counter_AX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk2_AX_AOI3_visits = 0

    # AY
    try:
        blk2_AY_AOI1_visits = blk2_counter_AY['visit_counter'][blk2_counter_AY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk2_AY_AOI1_visits = 0
    try:
        blk2_AY_AOI2_visits = blk2_counter_AY['visit_counter'][blk2_counter_AY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk2_AY_AOI2_visits = 0
    try:
        blk2_AY_AOI3_visits = blk2_counter_AY['visit_counter'][blk2_counter_AY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk2_AY_AOI3_visits = 0

    # BX
    try:
        blk2_BX_AOI1_visits = blk2_counter_BX['visit_counter'][blk2_counter_BX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk2_BX_AOI1_visits = 0
    try:
        blk2_BX_AOI2_visits = blk2_counter_BX['visit_counter'][blk2_counter_BX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk2_BX_AOI2_visits = 0
    try:
        blk2_BX_AOI3_visits = blk2_counter_BX['visit_counter'][blk2_counter_BX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk2_BX_AOI3_visits = 0

    # BY
    try:
        blk2_BY_AOI1_visits = blk2_counter_BY['visit_counter'][blk2_counter_BY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk2_BY_AOI1_visits = 0
    try:
        blk2_BY_AOI2_visits = blk2_counter_BY['visit_counter'][blk2_counter_BY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk2_BY_AOI2_visits = 0
    try:
        blk2_BY_AOI3_visits = blk2_counter_BY['visit_counter'][blk2_counter_BY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk2_BY_AOI3_visits = 0

    # Block 3 formatting -------------------------------------------------------------------------------------------------------------

    # GET VALUES AND ASSIGN TO VARIABLES

    # AX
    try:
        blk3_AX_AOI1_visits = blk3_counter_AX['visit_counter'][blk3_counter_AX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk3_AX_AOI1_visits = 0
    try:
        blk3_AX_AOI2_visits = blk3_counter_AX['visit_counter'][blk3_counter_AX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk3_AX_AOI2_visits = 0
    try:
        blk3_AX_AOI3_visits = blk3_counter_AX['visit_counter'][blk3_counter_AX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk3_AX_AOI3_visits = 0

    # AY
    try:
        blk3_AY_AOI1_visits = blk3_counter_AY['visit_counter'][blk3_counter_AY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk3_AY_AOI1_visits = 0
    try:
        blk3_AY_AOI2_visits = blk3_counter_AY['visit_counter'][blk3_counter_AY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk3_AY_AOI2_visits = 0
    try:
        blk3_AY_AOI3_visits = blk3_counter_AY['visit_counter'][blk3_counter_AY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk3_AY_AOI3_visits = 0

    # BX
    try:
        blk3_BX_AOI1_visits = blk3_counter_BX['visit_counter'][blk3_counter_BX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk3_BX_AOI1_visits = 0
    try:
        blk3_BX_AOI2_visits = blk3_counter_BX['visit_counter'][blk3_counter_BX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk3_BX_AOI2_visits = 0
    try:
        blk3_BX_AOI3_visits = blk3_counter_BX['visit_counter'][blk3_counter_BX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk3_BX_AOI3_visits = 0

    # BY
    try:
        blk3_BY_AOI1_visits = blk3_counter_BY['visit_counter'][blk3_counter_BY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk3_BY_AOI1_visits = 0
    try:
        blk3_BY_AOI2_visits = blk3_counter_BY['visit_counter'][blk3_counter_BY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk3_BY_AOI2_visits = 0
    try:
        blk3_BY_AOI3_visits = blk3_counter_BY['visit_counter'][blk3_counter_BY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk3_BY_AOI3_visits = 0

    # Block 4 formatting -------------------------------------------------------------------------------------------------------------

    # GET VALUES AND ASSIGN TO VARIABLES

    # AX
    try:
        blk4_AX_AOI1_visits = blk4_counter_AX['visit_counter'][blk4_counter_AX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk4_AX_AOI1_visits = 0
    try:
        blk4_AX_AOI2_visits = blk4_counter_AX['visit_counter'][blk4_counter_AX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk4_AX_AOI2_visits = 0
    try:
        blk4_AX_AOI3_visits = blk4_counter_AX['visit_counter'][blk4_counter_AX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk4_AX_AOI3_visits = 0

    # AY
    try:
        blk4_AY_AOI1_visits = blk4_counter_AY['visit_counter'][blk4_counter_AY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk4_AY_AOI1_visits = 0
    try:
        blk4_AY_AOI2_visits = blk4_counter_AY['visit_counter'][blk4_counter_AY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk4_AY_AOI2_visits = 0
    try:
        blk4_AY_AOI3_visits = blk4_counter_AY['visit_counter'][blk4_counter_AY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk4_AY_AOI3_visits = 0

    # BX
    try:
        blk4_BX_AOI1_visits = blk4_counter_BX['visit_counter'][blk4_counter_BX['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk4_BX_AOI1_visits = 0
    try:
        blk4_BX_AOI2_visits = blk4_counter_BX['visit_counter'][blk4_counter_BX['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk4_BX_AOI2_visits = 0
    try:
        blk4_BX_AOI3_visits = blk4_counter_BX['visit_counter'][blk4_counter_BX['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk4_BX_AOI3_visits = 0

    # BY
    try:
        blk4_BY_AOI1_visits = blk4_counter_BY['visit_counter'][blk4_counter_BY['AOI'] == 1].values[0]
    except (KeyError, TypeError):
        blk4_BY_AOI1_visits = 0
    try:
        blk4_BY_AOI2_visits = blk4_counter_BY['visit_counter'][blk4_counter_BY['AOI'] == 2].values[0]
    except (KeyError, TypeError):
        blk4_BY_AOI2_visits = 0
    try:
        blk4_BY_AOI3_visits = blk4_counter_BY['visit_counter'][blk4_counter_BY['AOI'] == 3].values[0]
    except (KeyError, TypeError):
        blk4_BY_AOI3_visits = 0

    print("Success!")  # DEBUG LINE

    ########################################## TVD BY BLOCKS ############################################

    print("\nBegin TVD by blocks analysis...")  # DEBUG LINE

    # TrialId goes from 1-40 and one whole block is 1-40. Four blocks in total get the tvd for each block
    # and AOI visit count for each block
    # AX_TVD_sec_block1, AX_AOI_count_block1, block2, block3, block4, etc.

    # POPULATE VARIABLES
    blk1_AX_TVD_cue_sec, blk1_AX_TVD_top_sec, blk1_AX_TVD_bottom_sec = 0, 0, 0
    blk1_AY_TVD_cue_sec, blk1_AY_TVD_top_sec, blk1_AY_TVD_bottom_sec = 0, 0, 0
    blk1_BX_TVD_cue_sec, blk1_BX_TVD_top_sec, blk1_BX_TVD_bottom_sec = 0, 0, 0
    blk1_BY_TVD_cue_sec, blk1_BY_TVD_top_sec, blk1_BY_TVD_bottom_sec = 0, 0, 0
    blk2_AX_TVD_cue_sec, blk2_AX_TVD_top_sec, blk2_AX_TVD_bottom_sec = 0, 0, 0
    blk2_AY_TVD_cue_sec, blk2_AY_TVD_top_sec, blk2_AY_TVD_bottom_sec = 0, 0, 0
    blk2_BX_TVD_cue_sec, blk2_BX_TVD_top_sec, blk2_BX_TVD_bottom_sec = 0, 0, 0
    blk2_BY_TVD_cue_sec, blk2_BY_TVD_top_sec, blk2_BY_TVD_bottom_sec = 0, 0, 0
    blk3_AX_TVD_cue_sec, blk3_AX_TVD_top_sec, blk3_AX_TVD_bottom_sec = 0, 0, 0
    blk3_AY_TVD_cue_sec, blk3_AY_TVD_top_sec, blk3_AY_TVD_bottom_sec = 0, 0, 0
    blk3_BX_TVD_cue_sec, blk3_BX_TVD_top_sec, blk3_BX_TVD_bottom_sec = 0, 0, 0
    blk3_BY_TVD_cue_sec, blk3_BY_TVD_top_sec, blk3_BY_TVD_bottom_sec = 0, 0, 0
    blk4_AX_TVD_cue_sec, blk4_AX_TVD_top_sec, blk4_AX_TVD_bottom_sec = 0, 0, 0
    blk4_AY_TVD_cue_sec, blk4_AY_TVD_top_sec, blk4_AY_TVD_bottom_sec = 0, 0, 0
    blk4_BX_TVD_cue_sec, blk4_BX_TVD_top_sec, blk4_BX_TVD_bottom_sec = 0, 0, 0
    blk4_BY_TVD_cue_sec, blk4_BY_TVD_top_sec, blk4_BY_TVD_bottom_sec = 0, 0, 0

    # ************************************* BLOCK 1 PERFORM OPERATIONS **************************************************

    # AX - Block 1 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_AX = block_1[(block_1['AOICue'] == 'A') &
                    (block_1['AOIProbe1'] == 'X') &
                    (block_1['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AX['interval'] = (tv_AX['AOI'] != tv_AX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AX['count'] = tv_AX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AX = tv_AX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AX_cue = tv_AX[tv_AX['AOI'] == 3]
    tv_AX_top = tv_AX[tv_AX['AOI'] == 1]
    tv_AX_bottom = tv_AX[tv_AX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk1_AX_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_AX_cue['count']).sum()
    except ValueError:
        blk1_AX_TVD_cue_sec = 0
    try:
        blk1_AX_TVD_top_sec = np.vectorize(tvd_calculation)(tv_AX_top['count']).sum()
    except ValueError:
        blk1_AX_TVD_top_sec = 0
    try:
        blk1_AX_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_AX_bottom['count']).sum()
    except ValueError:
        blk1_AX_TVD_bottom_sec = 0

    # AY - Block 1 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_AY = block_1[(block_1['AOICue'] == 'A') &
                    ~(block_1['AOIProbe1'] == 'X') &
                    (block_1['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AY['interval'] = (tv_AY['AOI'] != tv_AY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AY['count'] = tv_AY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AY = tv_AY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AY_cue = tv_AY[tv_AY['AOI'] == 3]
    tv_AY_top = tv_AY[tv_AY['AOI'] == 1]
    tv_AY_bottom = tv_AY[tv_AY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk1_AY_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_AY_cue['count']).sum()
    except ValueError:
        blk1_AY_TVD_cue_sec = 0
    try:
        blk1_AY_TVD_top_sec = np.vectorize(tvd_calculation)(tv_AY_top['count']).sum()
    except ValueError:
        blk1_AY_TVD_top_sec = 0
    try:
        blk1_AY_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_AY_bottom['count']).sum()  # try this and if error:
    except ValueError:
        blk1_AY_TVD_bottom_sec = 0  # set to 0 (means that participant never looked at AOI2 on AY trial)

    # BX - Block 1 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_BX = block_1[(block_1['AOICue'] == 'B') &
                    (block_1['AOIProbe2'] == 'X') &
                    (block_1['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BX['interval'] = (tv_BX['AOI'] != tv_BX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BX['count'] = tv_BX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BX = tv_BX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BX_cue = tv_BX[tv_BX['AOI'] == 3]
    tv_BX_top = tv_BX[tv_BX['AOI'] == 1]
    tv_BX_bottom = tv_BX[tv_BX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk1_BX_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_BX_cue['count']).sum()
    except ValueError:
        blk1_BX_TVD_cue_sec = 0
    try:
        blk1_BX_TVD_top_sec = np.vectorize(tvd_calculation)(tv_BX_top['count']).sum()
    except ValueError:
        blk1_BX_TVD_top_sec = 0
    try:
        blk1_BX_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_BX_bottom['count']).sum()  # try this and if error:
    except ValueError:
        blk1_BX_TVD_bottom_sec = 0  # set to 0 (means that participant never looked at AOI2 on BX trial)

    # BY - Block 1 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_BY = block_1[(block_1['AOICue'] == 'B') &
                    ~(block_1['AOIProbe2'] == 'X') &
                    (block_1['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BY['interval'] = (tv_BY['AOI'] != tv_BY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BY['count'] = tv_BY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BY = tv_BY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BY_cue = tv_BY[tv_BY['AOI'] == 3]
    tv_BY_top = tv_BY[tv_BY['AOI'] == 1]
    tv_BY_bottom = tv_BY[tv_BY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk1_BY_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_BY_cue['count']).sum()
    except ValueError:
        blk1_BY_TVD_cue_sec = 0
    try:
        blk1_BY_TVD_top_sec = np.vectorize(tvd_calculation)(tv_BY_top['count']).sum()
    except ValueError:
        blk1_BY_TVD_top_sec = 0
    try:
        blk1_BY_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_BY_bottom['count']).sum()
    except ValueError:
        blk1_BY_TVD_bottom_sec = 0

    print("Block 1 done")  # DEBUG LINE

    # ************************************* BLOCK 2 PERFORM OPERATIONS **************************************************

    # AX - Block 2 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_AX = block_2[(block_2['AOICue'] == 'A') &
                    (block_2['AOIProbe1'] == 'X') &
                    (block_2['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AX['interval'] = (tv_AX['AOI'] != tv_AX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AX['count'] = tv_AX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AX = tv_AX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AX_cue = tv_AX[tv_AX['AOI'] == 3]
    tv_AX_top = tv_AX[tv_AX['AOI'] == 1]
    tv_AX_bottom = tv_AX[tv_AX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk2_AX_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_AX_cue['count']).sum()
    except ValueError:
        blk2_AX_TVD_cue_sec = 0
    try:
        blk2_AX_TVD_top_sec = np.vectorize(tvd_calculation)(tv_AX_top['count']).sum()
    except ValueError:
        blk2_AX_TVD_top_sec = 0
    try:
        blk2_AX_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_AX_bottom['count']).sum()
    except ValueError:
        blk2_AX_TVD_bottom_sec = 0

    # AY - Block 2 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_AY = block_2[(block_2['AOICue'] == 'A') &
                    ~(block_2['AOIProbe1'] == 'X') &
                    (block_2['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AY['interval'] = (tv_AY['AOI'] != tv_AY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AY['count'] = tv_AY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AY = tv_AY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AY_cue = tv_AY[tv_AY['AOI'] == 3]
    tv_AY_top = tv_AY[tv_AY['AOI'] == 1]
    tv_AY_bottom = tv_AY[tv_AY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk2_AY_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_AY_cue['count']).sum()
    except ValueError:
        blk2_AY_TVD_cue_sec = 0
    try:
        blk2_AY_TVD_top_sec = np.vectorize(tvd_calculation)(tv_AY_top['count']).sum()
    except ValueError:
        blk2_AY_TVD_top_sec = 0
    try:
        blk2_AY_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_AY_bottom['count']).sum()  # try this and if error:
    except ValueError:
        blk2_AY_TVD_bottom_sec = 0  # set to 0 (means that participant never looked at AOI2 on AY trial)

    # BX - Block 2 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_BX = block_2[(block_2['AOICue'] == 'B') &
                    (block_2['AOIProbe2'] == 'X') &
                    (block_2['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BX['interval'] = (tv_BX['AOI'] != tv_BX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BX['count'] = tv_BX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BX = tv_BX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BX_cue = tv_BX[tv_BX['AOI'] == 3]
    tv_BX_top = tv_BX[tv_BX['AOI'] == 1]
    tv_BX_bottom = tv_BX[tv_BX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk2_BX_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_BX_cue['count']).sum()
    except ValueError:
        blk2_BX_TVD_cue_sec = 0
    try:
        blk2_BX_TVD_top_sec = np.vectorize(tvd_calculation)(tv_BX_top['count']).sum()
    except ValueError:
        blk2_BX_TVD_top_sec = 0
    try:
        blk2_BX_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_BX_bottom['count']).sum()  # try this and if error:
    except ValueError:
        blk2_BX_TVD_bottom_sec = 0  # set to 0 (means that participant never looked at AOI2 on AY trial)

    # BY - Block 2 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_BY = block_2[(block_2['AOICue'] == 'B') &
                    ~(block_2['AOIProbe2'] == 'X') &
                    (block_2['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BY['interval'] = (tv_BY['AOI'] != tv_BY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BY['count'] = tv_BY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BY = tv_BY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BY_cue = tv_BY[tv_BY['AOI'] == 3]
    tv_BY_top = tv_BY[tv_BY['AOI'] == 1]
    tv_BY_bottom = tv_BY[tv_BY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk2_BY_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_BY_cue['count']).sum()
    except ValueError:
        blk2_BY_TVD_cue_sec = 0
    try:
        blk2_BY_TVD_top_sec = np.vectorize(tvd_calculation)(tv_BY_top['count']).sum()
    except ValueError:
        blk2_BY_TVD_top_sec = 0
    try:
        blk2_BY_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_BY_bottom['count']).sum()
    except ValueError:
        blk2_BY_TVD_bottom_sec = 0

    print("Block 2 done")  # DEBUG LINE

    # ************************************* BLOCK 3 PERFORM OPERATIONS **************************************************

    # AX - Block 3 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_AX = block_3[(block_3['AOICue'] == 'A') &
                    (block_3['AOIProbe1'] == 'X') &
                    (block_3['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AX['interval'] = (tv_AX['AOI'] != tv_AX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AX['count'] = tv_AX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AX = tv_AX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AX_cue = tv_AX[tv_AX['AOI'] == 3]
    tv_AX_top = tv_AX[tv_AX['AOI'] == 1]
    tv_AX_bottom = tv_AX[tv_AX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk3_AX_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_AX_cue['count']).sum()
    except ValueError:
        blk3_AX_TVD_cue_sec = 0
    try:
        blk3_AX_TVD_top_sec = np.vectorize(tvd_calculation)(tv_AX_top['count']).sum()
    except ValueError:
        blk3_AX_TVD_top_sec = 0
    try:
        blk3_AX_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_AX_bottom['count']).sum()
    except ValueError:
        blk3_AX_TVD_bottom_sec = 0

    # AY - Block 3 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_AY = block_3[(block_3['AOICue'] == 'A') &
                    ~(block_3['AOIProbe1'] == 'X') &
                    (block_3['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AY['interval'] = (tv_AY['AOI'] != tv_AY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AY['count'] = tv_AY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AY = tv_AY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AY_cue = tv_AY[tv_AY['AOI'] == 3]
    tv_AY_top = tv_AY[tv_AY['AOI'] == 1]
    tv_AY_bottom = tv_AY[tv_AY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk3_AY_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_AY_cue['count']).sum()
    except ValueError:
        blk3_AY_TVD_cue_sec = 0
    try:
        blk3_AY_TVD_top_sec = np.vectorize(tvd_calculation)(tv_AY_top['count']).sum()
    except ValueError:
        blk3_AY_TVD_top_sec = 0
    try:
        blk3_AY_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_AY_bottom['count']).sum()  # try this and if error:
    except ValueError:
        blk3_AY_TVD_bottom_sec = 0  # set to 0 (means that participant never looked at AOI2 on AY trial)

    # BX - Block 3 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_BX = block_3[(block_3['AOICue'] == 'B') &
                    (block_3['AOIProbe2'] == 'X') &
                    (block_3['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BX['interval'] = (tv_BX['AOI'] != tv_BX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BX['count'] = tv_BX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BX = tv_BX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BX_cue = tv_BX[tv_BX['AOI'] == 3]
    tv_BX_top = tv_BX[tv_BX['AOI'] == 1]
    tv_BX_bottom = tv_BX[tv_BX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk3_BX_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_BX_cue['count']).sum()
    except ValueError:
        blk3_BX_TVD_cue_sec = 0
    try:
        blk3_BX_TVD_top_sec = np.vectorize(tvd_calculation)(tv_BX_top['count']).sum()
    except ValueError:
        blk3_BX_TVD_top_sec = 0
    try:
        blk3_BX_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_BX_bottom['count']).sum()  # try this and if error:
    except ValueError:
        blk3_BX_TVD_bottom_sec = 0  # set to 0 (means that participant never looked at AOI2 on AY trial)

    # BY - Block 3 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_BY = block_3[(block_3['AOICue'] == 'B') &
                    ~(block_3['AOIProbe2'] == 'X') &
                    (block_3['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BY['interval'] = (tv_BY['AOI'] != tv_BY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BY['count'] = tv_BY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BY = tv_BY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BY_cue = tv_BY[tv_BY['AOI'] == 3]
    tv_BY_top = tv_BY[tv_BY['AOI'] == 1]
    tv_BY_bottom = tv_BY[tv_BY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk3_BY_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_BY_cue['count']).sum()
    except ValueError:
        blk3_BY_TVD_cue_sec = 0
    try:
        blk3_BY_TVD_top_sec = np.vectorize(tvd_calculation)(tv_BY_top['count']).sum()
    except ValueError:
        blk3_BY_TVD_top_sec = 0
    try:
        blk3_BY_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_BY_bottom['count']).sum()
    except ValueError:
        blk3_BY_TVD_bottom_sec = 0

    print("Block 3 done")  # DEBUG LINE

    # ************************************* BLOCK 4 PERFORM OPERATIONS **************************************************

    # AX - Block 4 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_AX = block_4[(block_4['AOICue'] == 'A') &
                    (block_4['AOIProbe1'] == 'X') &
                    (block_4['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AX['interval'] = (tv_AX['AOI'] != tv_AX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AX['count'] = tv_AX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AX = tv_AX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AX_cue = tv_AX[tv_AX['AOI'] == 3]
    tv_AX_top = tv_AX[tv_AX['AOI'] == 1]
    tv_AX_bottom = tv_AX[tv_AX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk4_AX_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_AX_cue['count']).sum()
    except ValueError:
        blk4_AX_TVD_cue_sec = 0
    try:
        blk4_AX_TVD_top_sec = np.vectorize(tvd_calculation)(tv_AX_top['count']).sum()
    except ValueError:
        blk4_AX_TVD_top_sec = 0
    try:
        blk4_AX_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_AX_bottom['count']).sum()
    except ValueError:
        blk4_AX_TVD_bottom_sec = 0

    # AY - Block 4 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_AY = block_4[(block_4['AOICue'] == 'A') &
                    ~(block_4['AOIProbe1'] == 'X') &
                    (block_4['CurrentObject'] == 'ISI')]

    # set intervals
    tv_AY['interval'] = (tv_AY['AOI'] != tv_AY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_AY['count'] = tv_AY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_AY = tv_AY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_AY_cue = tv_AY[tv_AY['AOI'] == 3]
    tv_AY_top = tv_AY[tv_AY['AOI'] == 1]
    tv_AY_bottom = tv_AY[tv_AY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk4_AY_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_AY_cue['count']).sum()
    except ValueError:
        blk4_AY_TVD_cue_sec = 0
    try:
        blk4_AY_TVD_top_sec = np.vectorize(tvd_calculation)(tv_AY_top['count']).sum()
    except ValueError:
        blk4_AY_TVD_top_sec = 0
    try:
        blk4_AY_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_AY_bottom['count']).sum()  # try this and if error:
    except ValueError:
        blk4_AY_TVD_bottom_sec = 0  # set to 0 (means that participant never looked at AOI2 on AY trial)

    # BX - Block 4 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_BX = block_4[(block_4['AOICue'] == 'B') &
                    (block_4['AOIProbe2'] == 'X') &
                    (block_4['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BX['interval'] = (tv_BX['AOI'] != tv_BX['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BX['count'] = tv_BX.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BX = tv_BX.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BX_cue = tv_BX[tv_BX['AOI'] == 3]
    tv_BX_top = tv_BX[tv_BX['AOI'] == 1]
    tv_BX_bottom = tv_BX[tv_BX['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk4_BX_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_BX_cue['count']).sum()
    except ValueError:
        blk4_BX_TVD_cue_sec = 0
    try:
        blk4_BX_TVD_top_sec = np.vectorize(tvd_calculation)(tv_BX_top['count']).sum()
    except ValueError:
        blk4_BX_TVD_top_sec = 0
    try:
        blk4_BX_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_BX_bottom['count']).sum()  # try this and if error:
    except ValueError:
        blk4_BX_TVD_bottom_sec = 0  # set to 0 (means that participant never looked at AOI2 on AY trial)

    # BY - Block 4 ----------------------------------------------------------------------------------------------------

    # filter dataframe to correct conditions
    tv_BY = block_4[(block_4['AOICue'] == 'B') &
                    ~(block_4['AOIProbe2'] == 'X') &
                    (block_4['CurrentObject'] == 'ISI')]

    # set intervals
    tv_BY['interval'] = (tv_BY['AOI'] != tv_BY['AOI'].shift(1)).astype(float).cumsum()

    # get number/count of SAME values in each interval
    tv_BY['count'] = tv_BY.groupby(['AOI', 'interval']).cumcount() + 1
    tv_BY = tv_BY.groupby('interval').last().reset_index()

    # get only values for each specific AOI
    tv_BY_cue = tv_BY[tv_BY['AOI'] == 3]
    tv_BY_top = tv_BY[tv_BY['AOI'] == 1]
    tv_BY_bottom = tv_BY[tv_BY['AOI'] == 2]

    # get the count of each visit on each AOI and perform calculations
    try:
        blk4_BY_TVD_cue_sec = np.vectorize(tvd_calculation)(tv_BY_cue['count']).sum()
    except ValueError:
        blk4_BY_TVD_cue_sec = 0
    try:
        blk4_BY_TVD_top_sec = np.vectorize(tvd_calculation)(tv_BY_top['count']).sum()
    except ValueError:
        blk4_BY_TVD_top_sec = 0
    try:
        blk4_BY_TVD_bottom_sec = np.vectorize(tvd_calculation)(tv_BY_bottom['count']).sum()
    except ValueError:
        blk4_BY_TVD_bottom_sec = 0

    print("Block 4 done")  # DEBUG LINE
    print("Success!")  # DEBUG LINE

    ################################# NUM OF CORRECT TRIALS BY BLOCK ################################

    print("\nBegin num of correct trials by block analysis...")  # DEBUG LINE

    # initialize variables
    Blk_1_AX_Number_of_Correct_Trials = 0
    Blk_2_AX_Number_of_Correct_Trials = 0
    Blk_3_AX_Number_of_Correct_Trials = 0
    Blk_4_AX_Number_of_Correct_Trials = 0

    Blk_1_AY_Number_of_Correct_Trials = 0
    Blk_2_AY_Number_of_Correct_Trials = 0
    Blk_3_AY_Number_of_Correct_Trials = 0
    Blk_4_AY_Number_of_Correct_Trials = 0

    Blk_1_BX_Number_of_Correct_Trials = 0
    Blk_2_BX_Number_of_Correct_Trials = 0
    Blk_3_BX_Number_of_Correct_Trials = 0
    Blk_4_BX_Number_of_Correct_Trials = 0

    Blk_1_BY_Number_of_Correct_Trials = 0
    Blk_2_BY_Number_of_Correct_Trials = 0
    Blk_3_BY_Number_of_Correct_Trials = 0
    Blk_4_BY_Number_of_Correct_Trials = 0

    # -------------------------- GET RELEVANT DATAFRAMES -------------------------------

    # AX - Block 1 ----------------------------------------------------------------------------------------------------
    AX_df_correct_block_1 = block_1[(block_1['AOICue'] == 'A') &
               (block_1['AOIProbe1'] == 'X') &
               (block_1['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AX_df_correct_block_1['AOI'] = AX_df_correct_block_1['AOI'].fillna(0)
    AX_df_correct_block_1['AOI'] = AX_df_correct_block_1['AOI'].astype(int)

    # AY - Block 1 ----------------------------------------------------------------------------------------------------
    AY_df_correct_block_1 = block_1[(block_1['AOICue'] == 'A') &
                                    ~(block_1['AOIProbe1'] == 'X') &
                                    (block_1['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AY_df_correct_block_1['AOI'] = AY_df_correct_block_1['AOI'].fillna(0)
    AY_df_correct_block_1['AOI'] = AY_df_correct_block_1['AOI'].astype(int)

    # BX - Block 1 ----------------------------------------------------------------------------------------------------
    BX_df_correct_block_1 = block_1[(block_1['AOICue'] == 'B') &
                                    (block_1['AOIProbe2'] == 'X') &
                                    (block_1['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BX_df_correct_block_1['AOI'] = BX_df_correct_block_1['AOI'].fillna(0)
    BX_df_correct_block_1['AOI'] = BX_df_correct_block_1['AOI'].astype(int)

    # BY - Block 1 ----------------------------------------------------------------------------------------------------
    BY_df_correct_block_1 = block_1[(block_1['AOICue'] == 'B') &
                                    ~(block_1['AOIProbe2'] == 'X') &
                                    (block_1['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BY_df_correct_block_1['AOI'] = BY_df_correct_block_1['AOI'].fillna(0)
    BY_df_correct_block_1['AOI'] = BY_df_correct_block_1['AOI'].astype(int)

    # AX - Block 2 ----------------------------------------------------------------------------------------------------
    AX_df_correct_block_2 = block_2[(block_2['AOICue'] == 'A') &
                                    (block_2['AOIProbe1'] == 'X') &
                                    (block_2['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AX_df_correct_block_2['AOI'] = AX_df_correct_block_2['AOI'].fillna(0)
    AX_df_correct_block_2['AOI'] = AX_df_correct_block_2['AOI'].astype(int)

    # AY - Block 2 ----------------------------------------------------------------------------------------------------
    AY_df_correct_block_2 = block_2[(block_2['AOICue'] == 'A') &
                                    ~(block_2['AOIProbe1'] == 'X') &
                                    (block_2['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AY_df_correct_block_2['AOI'] = AY_df_correct_block_2['AOI'].fillna(0)
    AY_df_correct_block_2['AOI'] = AY_df_correct_block_2['AOI'].astype(int)

    # BX - Block 2 ----------------------------------------------------------------------------------------------------
    BX_df_correct_block_2 = block_2[(block_2['AOICue'] == 'B') &
                                    (block_2['AOIProbe2'] == 'X') &
                                    (block_2['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BX_df_correct_block_2['AOI'] = BX_df_correct_block_2['AOI'].fillna(0)
    BX_df_correct_block_2['AOI'] = BX_df_correct_block_2['AOI'].astype(int)

    # BY - Block 2 ----------------------------------------------------------------------------------------------------
    BY_df_correct_block_2 = block_2[(block_2['AOICue'] == 'B') &
                                    ~(block_2['AOIProbe2'] == 'X') &
                                    (block_2['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BY_df_correct_block_2['AOI'] = BY_df_correct_block_2['AOI'].fillna(0)
    BY_df_correct_block_2['AOI'] = BY_df_correct_block_2['AOI'].astype(int)

    # AX - Block 3 ----------------------------------------------------------------------------------------------------
    AX_df_correct_block_3 = block_3[(block_3['AOICue'] == 'A') &
                                    (block_3['AOIProbe1'] == 'X') &
                                    (block_3['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AX_df_correct_block_3['AOI'] = AX_df_correct_block_3['AOI'].fillna(0)
    AX_df_correct_block_3['AOI'] = AX_df_correct_block_3['AOI'].astype(int)

    # AY - Block 3 ----------------------------------------------------------------------------------------------------
    AY_df_correct_block_3 = block_3[(block_3['AOICue'] == 'A') &
                                    ~(block_3['AOIProbe1'] == 'X') &
                                    (block_3['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AY_df_correct_block_3['AOI'] = AY_df_correct_block_3['AOI'].fillna(0)
    AY_df_correct_block_3['AOI'] = AY_df_correct_block_3['AOI'].astype(int)

    # BX - Block 3 ----------------------------------------------------------------------------------------------------
    BX_df_correct_block_3 = block_3[(block_3['AOICue'] == 'B') &
                                    (block_3['AOIProbe2'] == 'X') &
                                    (block_3['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BX_df_correct_block_3['AOI'] = BX_df_correct_block_3['AOI'].fillna(0)
    BX_df_correct_block_3['AOI'] = BX_df_correct_block_3['AOI'].astype(int)

    # BY - Block 3 ----------------------------------------------------------------------------------------------------
    BY_df_correct_block_3 = block_3[(block_3['AOICue'] == 'B') &
                                    ~(block_3['AOIProbe2'] == 'X') &
                                    (block_3['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BY_df_correct_block_3['AOI'] = BY_df_correct_block_3['AOI'].fillna(0)
    BY_df_correct_block_3['AOI'] = BY_df_correct_block_3['AOI'].astype(int)

    # AX - Block 4 ----------------------------------------------------------------------------------------------------
    AX_df_correct_block_4 = block_4[(block_4['AOICue'] == 'A') &
                                    (block_4['AOIProbe1'] == 'X') &
                                    (block_4['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AX_df_correct_block_4['AOI'] = AX_df_correct_block_4['AOI'].fillna(0)
    AX_df_correct_block_4['AOI'] = AX_df_correct_block_4['AOI'].astype(int)

    # AY - Block 4 ----------------------------------------------------------------------------------------------------
    AY_df_correct_block_4 = block_4[(block_4['AOICue'] == 'A') &
                                    ~(block_4['AOIProbe1'] == 'X') &
                                    (block_4['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AY_df_correct_block_4['AOI'] = AY_df_correct_block_4['AOI'].fillna(0)
    AY_df_correct_block_4['AOI'] = AY_df_correct_block_4['AOI'].astype(int)

    # BX - Block 4 ----------------------------------------------------------------------------------------------------
    BX_df_correct_block_4 = block_4[(block_4['AOICue'] == 'B') &
                                    (block_4['AOIProbe2'] == 'X') &
                                    (block_4['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BX_df_correct_block_4['AOI'] = BX_df_correct_block_4['AOI'].fillna(0)
    BX_df_correct_block_4['AOI'] = BX_df_correct_block_4['AOI'].astype(int)

    # BY - Block 4 ----------------------------------------------------------------------------------------------------
    BY_df_correct_block_4 = block_4[(block_4['AOICue'] == 'B') &
                                    ~(block_4['AOIProbe2'] == 'X') &
                                    (block_4['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BY_df_correct_block_4['AOI'] = BY_df_correct_block_4['AOI'].fillna(0)
    BY_df_correct_block_4['AOI'] = BY_df_correct_block_4['AOI'].astype(int)

    ##################################### SLICE DATAFRAME BY TRIALID (BY BLOCKS) #####################################

    # init lists
    AX_df_list_block1 = []
    AX_df_list_block2 = []
    AX_df_list_block3 = []
    AX_df_list_block4 = []

    AY_df_list_block1 = []
    AY_df_list_block2 = []
    AY_df_list_block3 = []
    AY_df_list_block4 = []

    BX_df_list_block1 = []
    BX_df_list_block2 = []
    BX_df_list_block3 = []
    BX_df_list_block4 = []

    BY_df_list_block1 = []
    BY_df_list_block2 = []
    BY_df_list_block3 = []
    BY_df_list_block4 = []


    # BX and BY are working but AX and AY are not? Why?

    # AX SLICE BLOCK 1 *********************************************************************************************
    try:
        # get indices where value changes
        AX_index_block1 = AX_df_correct_block_1['TrialId'][AX_df_correct_block_1['TrialId'].diff() != 0].index.values
        AX_index_block1 = np.append(AX_index_block1, AX_df_correct_block_1.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
        AX_df_list_block1 = [AX_df_correct_block_1.iloc[AX_index_block1[i]:AX_index_block1[i + 1]] for i in range(len(AX_index_block1) - 1)]
        Blk_1_AX_Number_of_Correct_Trials = len(AX_df_list_block1)
    except:
        Blk_1_AX_Number_of_Correct_Trials = 0

    # AY SLICE BLOCK 1 *********************************************************************************************

    try:
        # get indices where value changes
        AY_index_block1 = AY_df_correct_block_1['TrialId'][AY_df_correct_block_1['TrialId'].diff() != 0].index.values
        AY_index_block1 = np.append(AY_index_block1, AY_df_correct_block_1.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
        AY_df_list_block1 = [AY_df_correct_block_1.iloc[AY_index_block1[i]:AY_index_block1[i + 1]] for i in range(len(AY_index_block1) - 1)]
        Blk_1_AY_Number_of_Correct_Trials = len(AY_df_list_block1)
    except:
        Blk_1_AY_Number_of_Correct_Trials = 0

    # BX SLICE BLOCK 1 *********************************************************************************************

    try:
        # get indices where value changes
        BX_index_block1 = BX_df_correct_block_1['TrialId'][BX_df_correct_block_1['TrialId'].diff() != 0].index.values
        BX_index_block1 = np.append(BX_index_block1, BX_df_correct_block_1.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
        BX_df_list_block1 = [BX_df_correct_block_1.iloc[BX_index_block1[i]:BX_index_block1[i + 1]] for i in range(len(BX_index_block1) - 1)]
        Blk_1_BX_Number_of_Correct_Trials = len(BX_df_list_block1)
    except:
        Blk_1_BX_Number_of_Correct_Trials = 0

    # BY SLICE BLOCK 1 *********************************************************************************************

    try:
    # get indices where value changes
        BY_index_block1 = BY_df_correct_block_1['TrialId'][BY_df_correct_block_1['TrialId'].diff() != 0].index.values
        BY_index_block1 = np.append(BY_index_block1, BY_df_correct_block_1.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        BY_df_list_block1 = [BY_df_correct_block_1.iloc[BY_index_block1[i]:BY_index_block1[i + 1]] for i in range(len(BY_index_block1) - 1)]
        Blk_1_BY_Number_of_Correct_Trials = len(BY_df_list_block1)
    except:
        Blk_1_BY_Number_of_Correct_Trials = 0

    # AX SLICE BLOCK 2 *********************************************************************************************
    try:
        # get indices where value changes
        AX_index_block2 = AX_df_correct_block_2['TrialId'][AX_df_correct_block_2['TrialId'].diff() != 0].index.values
        AX_index_block2 = np.append(AX_index_block2, AX_df_correct_block_2.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
        AX_df_list_block2 = [AX_df_correct_block_2.iloc[AX_index_block2[i]:AX_index_block2[i + 1]] for i in range(len(AX_index_block2) - 1)]
        Blk_2_AX_Number_of_Correct_Trials = len(AX_df_list_block2)
    except:
        Blk_2_AX_Number_of_Correct_Trials = 0

    # AY SLICE BLOCK 2 *********************************************************************************************
    try:
        # get indices where value changes
        AY_index_block2 = AY_df_correct_block_2['TrialId'][AY_df_correct_block_2['TrialId'].diff() != 0].index.values
        AY_index_block2 = np.append(AY_index_block2, AY_df_correct_block_2.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
        AY_df_list_block2 = [AY_df_correct_block_2.iloc[AY_index_block2[i]:AY_index_block2[i + 1]] for i in range(len(AY_index_block2) - 1)]
        Blk_2_AY_Number_of_Correct_Trials = len(AY_df_list_block2)
    except:
        Blk_2_AY_Number_of_Correct_Trials = 0

    # BX SLICE BLOCK 2 *********************************************************************************************
    try:
        # get indices where value changes
        BX_index_block2 = BX_df_correct_block_2['TrialId'][BX_df_correct_block_2['TrialId'].diff() != 0].index.values
        BX_index_block2 = np.append(BX_index_block2, BX_df_correct_block_2.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
        BX_df_list_block2 = [BX_df_correct_block_2.iloc[BX_index_block2[i]:BX_index_block2[i + 1]] for i in range(len(BX_index_block2) - 1)]
        Blk_2_BX_Number_of_Correct_Trials = len(BX_df_list_block2)
    except:
        Blk_2_BX_Number_of_Correct_Trials = 0

    # BY SLICE BLOCK 2 *********************************************************************************************
    try:
        # get indices where value changes
        BY_index_block2 = BY_df_correct_block_2['TrialId'][BY_df_correct_block_2['TrialId'].diff() != 0].index.values
        BY_index_block2 = np.append(BY_index_block2, BY_df_correct_block_2.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
        BY_df_list_block2 = [BY_df_correct_block_2.iloc[BY_index_block2[i]:BY_index_block2[i + 1]] for i in range(len(BY_index_block2) - 1)]
        Blk_2_BY_Number_of_Correct_Trials = len(BY_df_list_block2)
    except:
        Blk_2_BY_Number_of_Correct_Trials = 0

    # AX SLICE BLOCK 3 *********************************************************************************************
    try:
        # get indices where value changes
        AX_index_block3 = AX_df_correct_block_3['TrialId'][AX_df_correct_block_3['TrialId'].diff() != 0].index.values
        AX_index_block3 = np.append(AX_index_block3, AX_df_correct_block_3.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        AX_df_list_block3 = [AX_df_correct_block_3.iloc[AX_index_block3[i]:AX_index_block3[i + 1]] for i in range(len(AX_index_block3) - 1)]
        Blk_3_AX_Number_of_Correct_Trials = len(AX_df_list_block3)
    except:
        Blk_3_AX_Number_of_Correct_Trials = 0

    # AY SLICE BLOCK 3 *********************************************************************************************
    try:
        # get indices where value changes
        AY_index_block3 = AY_df_correct_block_3['TrialId'][AY_df_correct_block_3['TrialId'].diff() != 0].index.values
        AY_index_block3 = np.append(AY_index_block3, AY_df_correct_block_3.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        AY_df_list_block3 = [AY_df_correct_block_3.iloc[AY_index_block3[i]:AY_index_block3[i + 1]] for i in range(len(AY_index_block3) - 1)]
        Blk_3_AY_Number_of_Correct_Trials = len(AY_df_list_block3)
    except:
        Blk_3_AY_Number_of_Correct_Trials = 0

    # BX SLICE BLOCK 3 *********************************************************************************************
    try:
        # get indices where value changes
        BX_index_block3 = BX_df_correct_block_3['TrialId'][BX_df_correct_block_3['TrialId'].diff() != 0].index.values
        BX_index_block3 = np.append(BX_index_block3, BX_df_correct_block_3.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        BX_df_list_block3 = [BX_df_correct_block_3.iloc[BX_index_block3[i]:BX_index_block3[i + 1]] for i in range(len(BX_index_block3) - 1)]
        Blk_3_BX_Number_of_Correct_Trials = len(BX_df_list_block3)
    except:
        Blk_3_BX_Number_of_Correct_Trials = 0

    # BY SLICE BLOCK 3 *********************************************************************************************
    try:
        # get indices where value changes
        BY_index_block3 = BY_df_correct_block_3['TrialId'][BY_df_correct_block_3['TrialId'].diff() != 0].index.values
        BY_index_block3 = np.append(BY_index_block3, BY_df_correct_block_3.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        BY_df_list_block3 = [BY_df_correct_block_3.iloc[BY_index_block3[i]:BY_index_block3[i + 1]] for i in range(len(BY_index_block3) - 1)]
        Blk_3_BY_Number_of_Correct_Trials = len(BY_df_list_block3)
    except:
        Blk_3_BY_Number_of_Correct_Trials = 0

    # AX SLICE BLOCK 4 **********************************************************************************************
    try:
        # get indices where value changes
        AX_index_block4 = AX_df_correct_block_4['TrialId'][AX_df_correct_block_4['TrialId'].diff() != 0].index.values
        AX_index_block4 = np.append(AX_index_block4, AX_df_correct_block_4.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        AX_df_list_block4 = [AX_df_correct_block_4.iloc[AX_index_block4[i]:AX_index_block4[i + 1]] for i in range(len(AX_index_block4) - 1)]
        Blk_4_AX_Number_of_Correct_Trials = len(AX_df_list_block4)
    except:
        Blk_4_AX_Number_of_Correct_Trials = 0

    # AY SLICE BLOCK 4 **********************************************************************************************
    try:
        # get indices where value changes
        AY_index_block4 = AY_df_correct_block_4['TrialId'][AY_df_correct_block_4['TrialId'].diff() != 0].index.values
        AY_index_block4 = np.append(AY_index_block4, AY_df_correct_block_4.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        AY_df_list_block4 = [AY_df_correct_block_4.iloc[AY_index_block4[i]:AY_index_block4[i + 1]] for i in range(len(AY_index_block4) - 1)]
        Blk_4_AY_Number_of_Correct_Trials = len(AY_df_list_block4)
    except:
        Blk_4_AY_Number_of_Correct_Trials = 0

    # BX SLICE BLOCK 4 **********************************************************************************************
    try:
        # get indices where value changes
        BX_index_block4 = BX_df_correct_block_4['TrialId'][BX_df_correct_block_4['TrialId'].diff() != 0].index.values
        BX_index_block4 = np.append(BX_index_block4, BX_df_correct_block_4.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        BX_df_list_block4 = [BX_df_correct_block_4.iloc[BX_index_block4[i]:BX_index_block4[i + 1]] for i in range(len(BX_index_block4) - 1)]
        Blk_4_BX_Number_of_Correct_Trials = len(BX_df_list_block4)
    except:
        Blk_4_BX_Number_of_Correct_Trials = 0
    # BY SLICE BLOCK 4 *********************************************************************************************
    try:
        # get indices where value changes
        BY_index_block4 = BY_df_correct_block_4['TrialId'][BY_df_correct_block_4['TrialId'].diff() != 0].index.values
        BY_index_block4 = np.append(BY_index_block4, BY_df_correct_block_4.index[-1])  # add last row index as end

        # using those indices, take slices of dataframe and separate them into list of smaller dataframes
        BY_df_list_block4 = [BY_df_correct_block_4.iloc[BY_index_block4[i]:BY_index_block4[i + 1]] for i in range(len(BY_index_block4) - 1)]
        Blk_4_BY_Number_of_Correct_Trials= len(BY_df_list_block4)
    except:
        Blk_4_BY_Number_of_Correct_Trials = 0

    print("Success!")  # DEBUG LINE
    ###################################### FIRST FIXATION ###########################################

    print("\nBegin First Fixation analysis...")  # DEBUG LINE

    # define function to calculate time to first fixation
    def millisec(num):
        return num * 16.65496782


    # filter and convert df_2 values
    df_2_ff = df_2.reset_index(drop=True)
    df_2_ff['AOI'] = df_2_ff['AOI'].fillna(0)
    df_2_ff['AOI'] = df_2_ff['AOI'].astype(int)

    # init output variables
    AX_top2bottom_count, AX_bottom2top_count = 0, 0  # where top2bottom = 1, bottom2top = 2
    AX_ttff_top2bot, AX_ttff_bot2top = 0, 0
    prop_AX_top, prop_AX_bot = 0, 0
    AX_Initial_TVD_Cue_sec, AX_Initial_TVD_Cue_per_correct_trial = 0, 0

    AY_top2bottom_count, AY_bottom2top_count = 0, 0
    AY_ttff_top2bot, AY_ttff_bot2top = 0, 0
    prop_AY_top, prop_AY_bot = 0, 0
    AY_Initial_TVD_Cue_sec, AY_Initial_TVD_Cue_per_correct_trial = 0, 0

    BX_top2bottom_count, BX_bottom2top_count = 0, 0
    BX_ttff_top2bot, BX_ttff_bot2top = 0, 0
    prop_BX_top, prop_BX_bot = 0, 0
    BX_Initial_TVD_Cue_sec, BX_Initial_TVD_Cue_per_correct_trial = 0, 0

    BY_top2bottom_count, BY_bottom2top_count = 0, 0
    BY_ttff_top2bot, BY_ttff_bot2top = 0, 0
    prop_BY_top, prop_BY_bot = 0, 0
    BY_Initial_TVD_Cue_sec, BY_Initial_TVD_Cue_per_correct_trial = 0, 0

    # -------------------------- GET RELEVANT DATAFRAMES -------------------------------

    print("Getting relevant dataframes...")  # DEBUG LINE

    AX_df = df_2_ff[(df_2_ff['AOICue'] == 'A') &
                    (df_2_ff['AOIProbe1'] == 'X') &
                    (df_2_ff['CurrentObject'] == 'ISI')].reset_index(drop=True)

    AY_df = df_2_ff[(df_2_ff['AOICue'] == 'A') &
                    ~(df_2_ff['AOIProbe1'] == 'X') &
                    (df_2_ff['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BX_df = df_2_ff[(df_2_ff['AOICue'] == 'B') &
                    (df_2_ff['AOIProbe2'] == 'X') &
                    (df_2_ff['CurrentObject'] == 'ISI')].reset_index(drop=True)

    BY_df = df_2_ff[(df_2_ff['AOICue'] == 'B') &
                    ~(df_2_ff['AOIProbe2'] == 'X') &
                    (df_2_ff['CurrentObject'] == 'ISI')].reset_index(drop=True)

    ###################################### SLICE DATAFRAME BY TRIALID'S ####################################

    # AX SLICE *********************************************************************************************

    # get indices where value changes
    AX_index = AX_df['TrialId'][AX_df['TrialId'].diff() != 0].index.values
    AX_index = np.append(AX_index, AX_df.index[-1])  # add last row index as end

    # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
    AX_df_list = [AX_df.iloc[AX_index[i]:AX_index[i + 1]] for i in range(len(AX_index) - 1)]

    # debug:
    # print('AX len:', len(AX_df_list))

    # AY SLICE *********************************************************************************************

    # get indices where value changes
    AY_index = AY_df['TrialId'][AY_df['TrialId'].diff() != 0].index.values
    AY_index = np.append(AY_index, AY_df.index[-1])  # add last row index as end

    # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
    AY_df_list = [AY_df.iloc[AY_index[i]:AY_index[i + 1]] for i in range(len(AY_index) - 1)]

    # debug:
    # print('AY len:', len(AY_df_list))

    # BX SLICE *********************************************************************************************

    # get indices where value changes
    BX_index = BX_df['TrialId'][BX_df['TrialId'].diff() != 0].index.values
    BX_index = np.append(BX_index, BX_df.index[-1])  # add last row index as end

    # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
    BX_df_list = [BX_df.iloc[BX_index[i]:BX_index[i + 1]] for i in range(len(BX_index) - 1)]

    # debug:
    # print('BX len:', len(BX_df_list))

    # BY SLICE *********************************************************************************************

    # get indices where value changes
    BY_index = BY_df['TrialId'][BY_df['TrialId'].diff() != 0].index.values
    BY_index = np.append(BY_index, BY_df.index[-1])  # add last row index as end

    # using those indices, take slices of dataframe and seperate them into list of smaller dataframes
    BY_df_list = [BY_df.iloc[BY_index[i]:BY_index[i + 1]] for i in range(len(BY_index) - 1)]


    # debug:
    # print('BY len:', len(BY_df_list))

    ############################################ FIND FIRST FIXATION #######################################

    # now within each of these smaller dataframes, find first occurence of 1 or 2 or none if neither
    # and increment count for top if 1 or increment count for bot if 2
    # then calculate ttff for top and bot as well as proportion of correct trials

    def TVD_for_cue_cells(a):  # a is a series, array, or column

        a = pd.DataFrame(a).fillna(0)  # takes care of nan values
        a.loc[(a[0] > 3, 0)] = 0  # here we need to replace any values greater than 3 to 0
        a.loc[(a[0] < 3, 0)] = 0  # here we need to replace any values less than 3 to 0 (we only care about 3)
        a = np.array(a)  # automatically converts to numpy array

        try:  # handles case where array passed in is empty
            maxidx = a.argmax()  # maxidx holds position of first instance of max value index location
        except ValueError:
            return 0

        # ex: if maxidx == 6 then get everything after that
        # argmin gives us index location of minimum value (shouldn't be a minimum value so 0)
        pos = a[maxidx:].argmin()
        if a[maxidx]:
            if pos == 0:
                return a.size - maxidx
            else:
                return pos
        else:
            return 0


    # AX FIRST FIXATION *********************************************************************************************

    AX_top2bot_list = []
    AX_bot2top_list = []

    # search for first fixation
    for smol_df in AX_df_list:

        # get values in AOI column
        arr = smol_df['AOI'].values

        # increment TVD cue time (cell counts)
        AX_Initial_TVD_Cue_sec += TVD_for_cue_cells(arr)

        # get first instance of a value where value is non-zero and does not equal to 3 else None
        first_instance_list = next(([idx, val] for idx, val in enumerate(arr) if val and val != 3), None)
        try:
            first_instance = first_instance_list[1]
            rows_to_fi = first_instance_list[0]
        except:
            continue

        # add to variables depending on first fixation value
        if first_instance == 1:
            AX_top2bottom_count += 1

            # debug:
            # print('AX top2bot rows:', rows_to_fi)
            # AX_top2bot_list.append(rows_to_fi)

            # increment total rows to ff
            AX_ttff_top2bot += rows_to_fi + 0

        elif first_instance == 2:
            AX_bottom2top_count += 1

            # debug:
            # print('AX bot2top rows:', rows_to_fi)
            # AX_bot2top_list.append(rows_to_fi)

            # increment total rows to ff
            AX_ttff_bot2top += rows_to_fi + 0

        else:
            continue  # is neither so we continue

    # account for when the user never had ttff for trial_ttff_top2bot or trial_ttff_bot2top
    if AX_ttff_top2bot == 0 and AX_top2bottom_count == 0:
        AX_ttff_top2bot = np.nan
    else:
        # calculate ttff
        AX_ttff_top2bot = millisec(AX_ttff_top2bot) / AX_top2bottom_count

    if AX_ttff_bot2top == 0 and AX_bottom2top_count == 0:
        AX_ttff_bot2top = np.nan
    else:
        # calculate ttff
        AX_ttff_bot2top = millisec(AX_ttff_bot2top) / AX_bottom2top_count

    # calculate proportion
    prop_AX_top = AX_top2bottom_count / len(AX_df_list)
    prop_AX_bot = AX_bottom2top_count / len(AX_df_list)

    # calculate TVD cue in seconds
    AX_Initial_TVD_Cue_sec = (AX_Initial_TVD_Cue_sec * 16.65496782) / 1000

    # calculate TVD cue per correct trial
    AX_Initial_TVD_Cue_per_correct_trial = (AX_Initial_TVD_Cue_sec / len(AX_df_list)) * 1000

    # AY FIRST FIXATION *********************************************************************************************

    AY_top2bot_list = []
    AY_bot2top_list = []

    # search for first fixation
    for smol_df in AY_df_list:

        # get values in AOI column
        arr = smol_df['AOI'].values

        # increment TVD cue time (cell counts)
        AY_Initial_TVD_Cue_sec += TVD_for_cue_cells(arr)

        # get first instance of a value where value is non-zero and does not equal to 3 else None
        first_instance_list = next(([idx, val] for idx, val in enumerate(arr) if val and val != 3), None)

        try:
            first_instance = first_instance_list[1]
            rows_to_fi = first_instance_list[0]
        except:
            continue

        # add to variables depending on first fixation value
        if first_instance == 1:
            AY_top2bottom_count += 1

            # debug:
            # print('AY top2bot rows:', rows_to_fi)
            # AY_top2bot_list.append(rows_to_fi)

            # increment total rows to ff
            AY_ttff_top2bot += rows_to_fi + 0

        elif first_instance == 2:
            AY_bottom2top_count += 1

            # debug:
            # print('AY bot2top rows:', rows_to_fi)
            # AY_bot2top_list.append(rows_to_fi)

            # increment total rows to ff
            AY_ttff_bot2top += rows_to_fi + 0

        else:
            continue  # is neither so we continue

    # account for when the user never had ttff for trial_ttff_top2bot or trial_ttff_bot2top
    if AY_ttff_top2bot == 0 and AY_top2bottom_count == 0:
        AY_ttff_top2bot = np.nan
    else:
        # calculate ttff
        AY_ttff_top2bot = millisec(AY_ttff_top2bot) / AY_top2bottom_count

    if AY_ttff_bot2top == 0 and AY_bottom2top_count == 0:
        AY_ttff_bot2top = np.nan
    else:
        # calculate ttff
        AY_ttff_bot2top = millisec(AY_ttff_bot2top) / AY_bottom2top_count

    # calculate proportion
    prop_AY_top = AY_top2bottom_count / len(AY_df_list)
    prop_AY_bot = AY_bottom2top_count / len(AY_df_list)

    # calculate TVD cue in seconds
    AY_Initial_TVD_Cue_sec = (AY_Initial_TVD_Cue_sec * 16.65496782) / 1000

    # calculate TVD cue per correct trial
    AY_Initial_TVD_Cue_per_correct_trial = (AY_Initial_TVD_Cue_sec / len(AY_df_list)) * 1000

    # BX FIRST FIXATION *********************************************************************************************

    BX_top2bot_list = []
    BX_bot2top_list = []

    # search for first fixation
    for smol_df in BX_df_list:

        # get values in AOI column
        arr = smol_df['AOI'].values

        # increment TVD cue time (cell counts)
        BX_Initial_TVD_Cue_sec += TVD_for_cue_cells(arr)

        # get first instance of a value where value is non-zero and does not equal to 3 else None
        first_instance_list = next(([idx, val] for idx, val in enumerate(arr) if val and val != 3), None)

        try:
            first_instance = first_instance_list[1]
            rows_to_fi = first_instance_list[0]
        except:
            continue

        # add to variables depending on first fixation value
        if first_instance == 1:
            BX_top2bottom_count += 1

            # debug:
            # print('BX top2bot rows:', rows_to_fi)
            # BX_top2bot_list.append(rows_to_fi)

            # increment total rows to ff
            BX_ttff_top2bot += rows_to_fi + 0

        elif first_instance == 2:
            BX_bottom2top_count += 1

            # debug:
            # print('BX bot2top rows:', rows_to_fi)
            # BX_bot2top_list.append(rows_to_fi)

            # increment total rows to ff
            BX_ttff_bot2top += rows_to_fi + 0

        else:
            continue  # is neither so we continue

    # account for when the user never had ttff for trial_ttff_top2bot or trial_ttff_bot2top
    if BX_ttff_top2bot == 0 and BX_top2bottom_count == 0:
        BX_ttff_top2bot = np.nan
    else:
        # calculate ttff
        BX_ttff_top2bot = millisec(BX_ttff_top2bot) / BX_top2bottom_count

    if BX_ttff_bot2top == 0 and BX_bottom2top_count == 0:
        BX_ttff_bot2top = np.nan
    else:
        # calculate ttff
        BX_ttff_bot2top = millisec(BX_ttff_bot2top) / BX_bottom2top_count

    # calculate proportion
    prop_BX_top = BX_top2bottom_count / len(BX_df_list)
    prop_BX_bot = BX_bottom2top_count / len(BX_df_list)

    # calculate TVD cue in seconds
    BX_Initial_TVD_Cue_sec = (BX_Initial_TVD_Cue_sec * 16.65496782) / 1000

    # calculate TVD cue per correct trial
    BX_Initial_TVD_Cue_per_correct_trial = (BX_Initial_TVD_Cue_sec / len(BX_df_list)) * 1000

    # BY FIRST FIXATION *********************************************************************************************

    BY_top2bot_list = []
    BY_bot2top_list = []

    # search for first fixation
    for smol_df in BY_df_list:

        # get values in AOI column
        arr = smol_df['AOI'].values

        # increment TVD cue time (cell counts)
        BY_Initial_TVD_Cue_sec += TVD_for_cue_cells(arr)

        # get first instance of a value where value is non-zero and does not equal to 3 else None
        first_instance_list = next(([idx, val] for idx, val in enumerate(arr) if val and val != 3), None)
        try:
            first_instance = first_instance_list[1]
            rows_to_fi = first_instance_list[0]
        except:
            continue

        # add to variables depending on first fixation value
        if first_instance == 1:
            BY_top2bottom_count += 1

            # debug:
            # print('BY top2bot rows:', rows_to_fi)
            # BY_top2bot_list.append(rows_to_fi)

            # increment total rows to ff
            BY_ttff_top2bot += rows_to_fi + 0

        elif first_instance == 2:
            BY_bottom2top_count += 1

            # debug:
            # print('BY bot2top rows:', rows_to_fi)
            # BY_bot2top_list.append(rows_to_fi)

            # increment total rows to ff
            BY_ttff_bot2top += rows_to_fi + 0

        else:
            continue  # is neither so we continue

    # account for when the user never had ttff for trial_ttff_top2bot or trial_ttff_bot2top
    if BY_ttff_top2bot == 0 and BY_top2bottom_count == 0:
        BY_ttff_top2bot = np.nan
    else:
        # calculate ttff
        BY_ttff_top2bot = millisec(BY_ttff_top2bot) / BY_top2bottom_count

    if BY_ttff_bot2top == 0 and BY_bottom2top_count == 0:
        BY_ttff_bot2top = np.nan
    else:
        # calculate ttff
        BY_ttff_bot2top = millisec(BY_ttff_bot2top) / BY_bottom2top_count

    # calculate proportion
    prop_BY_top = BY_top2bottom_count / len(BY_df_list)
    prop_BY_bot = BY_bottom2top_count / len(BY_df_list)

    # calculate TVD cue in seconds ((total_cells * 16.65496782) / 1000)
    BY_Initial_TVD_Cue_sec = (BY_Initial_TVD_Cue_sec * 16.65496782) / 1000

    # calculate TVD cue per correct trial
    BY_Initial_TVD_Cue_per_correct_trial = (BY_Initial_TVD_Cue_sec / len(BY_df_list)) * 1000

    print("Success!")  # DEBUG LINE

    ########################################## FIRST FIXATION AND PROPORTION BY BLOCKS ####################################

    print("\nBegin first fixation and proportion by blocks...")
    # HELPER FUNCTION -----------------------------------------------------------------------------------------------------
    # this can be used for the regular first fixation above but, i'm feeling lazy today so...oh well.

    def get_first_fixation_proportions(df_list):
        """
        Calculates the proportion of correct trials and the number of first fixations
        for a given trial type (AX, AY, BX, or BY) and list of dataframes.
        Returns the calculated values as a tuple.
        """
        num_top_b4_bot = 0
        num_bot_b4_top = 0
        for smol_df in df_list:
            # get values in AOI column
            arr = smol_df['AOI'].values

            # get first instance of a value where value is non-zero and does not equal to 3 else None
            first_instance_list = next(([idx, val] for idx, val in enumerate(arr) if val and val != 3), None)
            try:
                first_instance = first_instance_list[1]
                rows_to_fi = first_instance_list[0]
            except:
                continue

            # add to variables depending on first fixation value
            if first_instance == 1:
                num_top_b4_bot += 1
            elif first_instance == 2:
                num_bot_b4_top += 1
            else:
                continue  # is neither so we continue

        # calculate proportion
        # print("Calculating a proportion top_b4_bot: ", num_top_b4_bot, "/", len(df_list))  # DEBUG LINE
        try:
            prop_top_b4_bot = num_top_b4_bot / len(df_list)
        except:
            prop_top_b4_bot = 0  # prevent div by zero error
        try:
            prop_bot_b4_top = num_bot_b4_top / len(df_list)
        except:
            prop_bot_b4_top = 0  # prevent div by zero error

        return num_top_b4_bot, num_bot_b4_top, prop_top_b4_bot, prop_bot_b4_top


    # init first fixation variables

    # number of first fixations (needed for proportion)
    Blk_1_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_1_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_1_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_1_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_1_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_1_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_1_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_1_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0

    Blk_2_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_2_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_2_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_2_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_2_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_2_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_2_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_2_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0

    Blk_3_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_3_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_3_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_3_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_3_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_3_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_3_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_3_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0

    Blk_4_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_4_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_4_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_4_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_4_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_4_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0
    Blk_4_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe = 0
    Blk_4_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe = 0

    # proportion of correct trials by block
    Blk_1_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe = 0
    Blk_1_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe = 0
    Blk_2_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe = 0
    Blk_2_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe = 0
    Blk_3_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe = 0
    Blk_3_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe = 0
    Blk_4_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe = 0
    Blk_4_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe = 0
    Blk_1_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe = 0
    Blk_1_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe = 0
    Blk_2_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe = 0
    Blk_2_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe = 0
    Blk_3_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe = 0
    Blk_3_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe = 0
    Blk_4_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe = 0
    Blk_4_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe = 0
    Blk_1_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe = 0
    Blk_1_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe = 0
    Blk_2_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe = 0
    Blk_2_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe = 0
    Blk_3_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe = 0
    Blk_3_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe = 0
    Blk_4_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe = 0
    Blk_4_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe = 0
    Blk_1_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe = 0
    Blk_1_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe = 0
    Blk_2_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe = 0
    Blk_2_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe = 0
    Blk_3_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe = 0
    Blk_3_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe = 0
    Blk_4_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe = 0
    Blk_4_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe = 0

    ###################################### BEGIN FF AND PROPORTION BY BLOCKS CALCULATIONS ###################################

    # AX BLOCK 1 ------------------------------------------------------------------------------------------------------

    Blk_1_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_1_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_1_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe, \
    Blk_1_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe = get_first_fixation_proportions(AX_df_list_block1)

    # AY BLOCK 1 ------------------------------------------------------------------------------------------------------

    Blk_1_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_1_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_1_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe, \
    Blk_1_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe = get_first_fixation_proportions(AY_df_list_block1)

    # BX BLOCK 1 ------------------------------------------------------------------------------------------------------

    Blk_1_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_1_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_1_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe, \
    Blk_1_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe = get_first_fixation_proportions(BX_df_list_block1)

    # BY BLOCK 1 ------------------------------------------------------------------------------------------------------

    Blk_1_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_1_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_1_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe, \
    Blk_1_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe = get_first_fixation_proportions(BY_df_list_block1)

    # AX BLOCK 2 ------------------------------------------------------------------------------------------------------

    Blk_2_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_2_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_2_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe, \
    Blk_2_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe = get_first_fixation_proportions(AX_df_list_block2)

    # AY BLOCK 2 ------------------------------------------------------------------------------------------------------

    Blk_2_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_2_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_2_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe, \
    Blk_2_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe = get_first_fixation_proportions(AY_df_list_block2)

    # BX BLOCK 2 ------------------------------------------------------------------------------------------------------

    Blk_2_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_2_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_2_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe, \
    Blk_2_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe = get_first_fixation_proportions(BX_df_list_block2)

    # BY BLOCK 2 ------------------------------------------------------------------------------------------------------

    Blk_2_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_2_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_2_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe, \
    Blk_2_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe = get_first_fixation_proportions(BY_df_list_block2)

    # AX BLOCK 3 ------------------------------------------------------------------------------------------------------

    Blk_3_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_3_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_3_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe, \
    Blk_3_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe = get_first_fixation_proportions(AX_df_list_block3)

    # AY BLOCK 3 ------------------------------------------------------------------------------------------------------

    Blk_3_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_3_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_3_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe, \
    Blk_3_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe = get_first_fixation_proportions(AY_df_list_block3)

    # BX BLOCK 3 ------------------------------------------------------------------------------------------------------

    Blk_3_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_3_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_3_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe, \
    Blk_3_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe = get_first_fixation_proportions(BX_df_list_block3)

    # BY BLOCK 3 ------------------------------------------------------------------------------------------------------

    Blk_3_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_3_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_3_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe, \
    Blk_3_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe = get_first_fixation_proportions(BY_df_list_block3)

    # AX BLOCK 4 ------------------------------------------------------------------------------------------------------

    Blk_4_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_4_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_4_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe, \
    Blk_4_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe = get_first_fixation_proportions(AX_df_list_block4)

    # AY BLOCK 4 ------------------------------------------------------------------------------------------------------

    Blk_4_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_4_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_4_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe, \
    Blk_4_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe = get_first_fixation_proportions(AY_df_list_block4)

    # BX BLOCK 4 ------------------------------------------------------------------------------------------------------

    Blk_4_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_4_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_4_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe, \
    Blk_4_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe = get_first_fixation_proportions(BX_df_list_block4)

    # BY BLOCK 4 ------------------------------------------------------------------------------------------------------

    Blk_4_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe, \
    Blk_4_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe, \
    Blk_4_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe, \
    Blk_4_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe = get_first_fixation_proportions(BY_df_list_block4)

    print("Success!")
    ########################################## TVD PER CORRECT TRIAL ##################################################

    print("\nCalculate TVD per correct trial...")  # DEBUG LINE

    AX_TVD_cue_per_correct_trial = (tvd_ax_cue / len(AX_df_list)) * 1000
    AX_TVD_top_per_correct_trial = (tvd_ax_top / len(AX_df_list)) * 1000
    AX_TVD_bottom_per_correct_trial = (tvd_ax_bottom / len(AX_df_list)) * 1000

    AY_TVD_cue_per_correct_trial = (tvd_ay_cue / len(AY_df_list)) * 1000
    AY_TVD_top_per_correct_trial = (tvd_ay_top / len(AY_df_list)) * 1000
    AY_TVD_bottom_per_correct_trial = (tvd_ay_bottom / len(AY_df_list)) * 1000

    BX_TVD_cue_per_correct_trial = (tvd_bx_cue / len(BX_df_list)) * 1000
    BX_TVD_top_per_correct_trial = (tvd_bx_top / len(BX_df_list)) * 1000
    BX_TVD_bottom_per_correct_trial = (tvd_bx_bottom / len(BX_df_list)) * 1000

    BY_TVD_cue_per_correct_trial = (tvd_by_cue / len(BY_df_list)) * 1000
    BY_TVD_top_per_correct_trial = (tvd_by_top / len(BY_df_list)) * 1000
    BY_TVD_bottom_per_correct_trial = (tvd_by_bottom / len(BY_df_list)) * 1000

    print("Success!")  # DEBUG LINE

    ########################################## VISITS PER CORRECT TRIAL ##################################################

    print("\nCalculate Visits per correct trial...")  # DEBUG LINE

    AX_visits_cue_per_correct_trial = (AX_AOI3_visits / len(AX_df_list))
    AX_visits_top_per_correct_trial = (AX_AOI1_visits / len(AX_df_list))
    AX_visits_bottom_per_correct_trial = (AX_AOI2_visits / len(AX_df_list))

    AY_visits_cue_per_correct_trial = (AY_AOI3_visits / len(AY_df_list))
    AY_visits_top_per_correct_trial = (AY_AOI1_visits / len(AY_df_list))
    AY_visits_bottom_per_correct_trial = (AY_AOI2_visits / len(AY_df_list))

    BX_visits_cue_per_correct_trial = (BX_AOI3_visits / len(BX_df_list))
    BX_visits_top_per_correct_trial = (BX_AOI1_visits / len(BX_df_list))
    BX_visits_bottom_per_correct_trial = (BX_AOI2_visits / len(BX_df_list))

    BY_visits_cue_per_correct_trial = (BY_AOI3_visits / len(BY_df_list))
    BY_visits_top_per_correct_trial = (BY_AOI1_visits / len(BY_df_list))
    BY_visits_bottom_per_correct_trial = (BY_AOI2_visits / len(BY_df_list))

    print("Success!")  # DEBUG LINE

    ################ FORMAT MAIN RESULTS (AOI visits, TVD, TFF, Proportion, Correct Trials) INTO OUTPUT DF ##############

    print("\nFormatting results...")

    mydata = [[subject_id,
               len(AX_df_list),  # num of correct trials
               len(AY_df_list),
               len(BX_df_list),
               len(BY_df_list),
               AX_AOI1_visits, AX_AOI2_visits, AX_AOI3_visits,  # aoi visit count
               AY_AOI1_visits, AY_AOI2_visits, AY_AOI3_visits,
               BX_AOI1_visits, BX_AOI2_visits, BX_AOI3_visits,
               BY_AOI1_visits, BY_AOI2_visits, BY_AOI3_visits,
               AX_visits_cue_per_correct_trial, AX_visits_top_per_correct_trial, AX_visits_bottom_per_correct_trial,
               # visits per correct trial
               AY_visits_cue_per_correct_trial, AY_visits_top_per_correct_trial, AY_visits_bottom_per_correct_trial,
               BX_visits_cue_per_correct_trial, BX_visits_top_per_correct_trial, BX_visits_bottom_per_correct_trial,
               BY_visits_cue_per_correct_trial, BY_visits_top_per_correct_trial, BY_visits_bottom_per_correct_trial,
               blk1_AX_AOI3_visits, blk2_AX_AOI3_visits, blk3_AX_AOI3_visits, blk4_AX_AOI3_visits,  # visits by blocks
               blk1_AX_AOI1_visits, blk2_AX_AOI1_visits, blk3_AX_AOI1_visits, blk4_AX_AOI1_visits,
               blk1_AX_AOI2_visits, blk2_AX_AOI2_visits, blk3_AX_AOI2_visits, blk4_AX_AOI2_visits,
               blk1_AY_AOI3_visits, blk2_AY_AOI3_visits, blk3_AY_AOI3_visits, blk4_AY_AOI3_visits,
               blk1_AY_AOI1_visits, blk2_AY_AOI1_visits, blk3_AY_AOI1_visits, blk4_AY_AOI1_visits,
               blk1_AY_AOI2_visits, blk2_AY_AOI2_visits, blk3_AY_AOI2_visits, blk4_AY_AOI2_visits,
               blk1_BX_AOI3_visits, blk2_BX_AOI3_visits, blk3_BX_AOI3_visits, blk4_BX_AOI3_visits,
               blk1_BX_AOI1_visits, blk2_BX_AOI1_visits, blk3_BX_AOI1_visits, blk4_BX_AOI1_visits,
               blk1_BX_AOI2_visits, blk2_BX_AOI2_visits, blk3_BX_AOI2_visits, blk4_BX_AOI2_visits,
               blk1_BY_AOI3_visits, blk2_BY_AOI3_visits, blk3_BY_AOI3_visits, blk4_BY_AOI3_visits,
               blk1_BY_AOI1_visits, blk2_BY_AOI1_visits, blk3_BY_AOI1_visits, blk4_BY_AOI1_visits,
               blk1_BY_AOI2_visits, blk2_BY_AOI2_visits, blk3_BY_AOI2_visits, blk4_BY_AOI2_visits,
               tvd_ax_cue, tvd_ax_top, tvd_ax_bottom,  # tvd
               tvd_ay_cue, tvd_ay_top, tvd_ay_bottom,
               tvd_bx_cue, tvd_bx_top, tvd_bx_bottom,
               tvd_by_cue, tvd_by_top, tvd_by_bottom,
               AX_TVD_cue_per_correct_trial, AX_TVD_top_per_correct_trial, AX_TVD_bottom_per_correct_trial,
               # TVD per correct trial
               AY_TVD_cue_per_correct_trial, AY_TVD_top_per_correct_trial, AY_TVD_bottom_per_correct_trial,
               BX_TVD_cue_per_correct_trial, BX_TVD_top_per_correct_trial, BX_TVD_bottom_per_correct_trial,
               BY_TVD_cue_per_correct_trial, BY_TVD_top_per_correct_trial, BY_TVD_bottom_per_correct_trial,
               AX_Initial_TVD_Cue_sec,  # initial tvd of cue in seconds
               AY_Initial_TVD_Cue_sec,
               BX_Initial_TVD_Cue_sec,
               BY_Initial_TVD_Cue_sec,
               AX_Initial_TVD_Cue_per_correct_trial,  # initial tvd of cue per correct trial
               AY_Initial_TVD_Cue_per_correct_trial,
               BX_Initial_TVD_Cue_per_correct_trial,
               BY_Initial_TVD_Cue_per_correct_trial,
               blk1_AX_TVD_cue_sec, blk2_AX_TVD_cue_sec, blk3_AX_TVD_cue_sec, blk4_AX_TVD_cue_sec,  # tvd by blocks
               blk1_AY_TVD_cue_sec, blk2_AY_TVD_cue_sec, blk3_AY_TVD_cue_sec, blk4_AY_TVD_cue_sec,
               blk1_BX_TVD_cue_sec, blk2_BX_TVD_cue_sec, blk3_BX_TVD_cue_sec, blk4_BX_TVD_cue_sec,
               blk1_BY_TVD_cue_sec, blk2_BY_TVD_cue_sec, blk3_BY_TVD_cue_sec, blk4_BY_TVD_cue_sec,
               blk1_AX_TVD_top_sec, blk2_AX_TVD_top_sec, blk3_AX_TVD_top_sec, blk4_AX_TVD_top_sec,
               blk1_AY_TVD_top_sec, blk2_AY_TVD_top_sec, blk3_AY_TVD_top_sec, blk4_AY_TVD_top_sec,
               blk1_BX_TVD_top_sec, blk2_BX_TVD_top_sec, blk3_BX_TVD_top_sec, blk4_BX_TVD_top_sec,
               blk1_BY_TVD_top_sec, blk2_BY_TVD_top_sec, blk3_BY_TVD_top_sec, blk4_BY_TVD_top_sec,
               blk1_AX_TVD_bottom_sec, blk2_AX_TVD_bottom_sec, blk3_AX_TVD_bottom_sec, blk4_AX_TVD_bottom_sec,
               blk1_AY_TVD_bottom_sec, blk2_AY_TVD_bottom_sec, blk3_AY_TVD_bottom_sec, blk4_AY_TVD_bottom_sec,
               blk1_BX_TVD_bottom_sec, blk2_BX_TVD_bottom_sec, blk3_BX_TVD_bottom_sec, blk4_BX_TVD_bottom_sec,
               blk1_BY_TVD_bottom_sec, blk2_BY_TVD_bottom_sec, blk3_BY_TVD_bottom_sec, blk4_BY_TVD_bottom_sec,
               # num of correct trials by blocks
               Blk_1_AX_Number_of_Correct_Trials,
               Blk_2_AX_Number_of_Correct_Trials,
               Blk_3_AX_Number_of_Correct_Trials,
               Blk_4_AX_Number_of_Correct_Trials,
               Blk_1_AY_Number_of_Correct_Trials,
               Blk_2_AY_Number_of_Correct_Trials,
               Blk_3_AY_Number_of_Correct_Trials,
               Blk_4_AY_Number_of_Correct_Trials,
               Blk_1_BX_Number_of_Correct_Trials,
               Blk_2_BX_Number_of_Correct_Trials,
               Blk_3_BX_Number_of_Correct_Trials,
               Blk_4_BX_Number_of_Correct_Trials,
               Blk_1_BY_Number_of_Correct_Trials,
               Blk_2_BY_Number_of_Correct_Trials,
               Blk_3_BY_Number_of_Correct_Trials,
               Blk_4_BY_Number_of_Correct_Trials,
               AX_top2bottom_count, AX_bottom2top_count,  # num of first fixation
               AY_top2bottom_count, AY_bottom2top_count,
               BX_top2bottom_count, BX_bottom2top_count,
               BY_top2bottom_count, BY_bottom2top_count,
               # num of first fixation by block
               Blk_1_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_1_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_2_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_2_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_3_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_3_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_4_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_4_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_1_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_1_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_2_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_2_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_3_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_3_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_4_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_4_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_1_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_1_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_2_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_2_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_3_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_3_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_4_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_4_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_1_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_1_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_2_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_2_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_3_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_3_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               Blk_4_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe,
               Blk_4_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe,
               prop_AX_top, prop_AX_bot,  # proportion of correct trials
               prop_AY_top, prop_AY_bot,
               prop_BX_top, prop_BX_bot,
               prop_BY_top, prop_BY_bot,
               # proportion of correct trials by block
               Blk_1_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe,
               Blk_1_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe,
               Blk_2_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe,
               Blk_2_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe,
               Blk_3_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe,
               Blk_3_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe,
               Blk_4_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe,
               Blk_4_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe,
               Blk_1_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe,
               Blk_1_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe,
               Blk_2_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe,
               Blk_2_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe,
               Blk_3_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe,
               Blk_3_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe,
               Blk_4_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe,
               Blk_4_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe,
               Blk_1_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe,
               Blk_1_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe,
               Blk_2_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe,
               Blk_2_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe,
               Blk_3_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe,
               Blk_3_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe,
               Blk_4_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe,
               Blk_4_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe,
               Blk_1_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe,
               Blk_1_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe,
               Blk_2_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe,
               Blk_2_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe,
               Blk_3_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe,
               Blk_3_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe,
               Blk_4_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe,
               Blk_4_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe,
               AX_ttff_top2bot, AX_ttff_bot2top,  # time to first fixation
               AY_ttff_top2bot, AY_ttff_bot2top,
               BX_ttff_top2bot, BX_ttff_bot2top,
               BY_ttff_top2bot, BY_ttff_bot2top
               ]
              ]

    mycolumns = [['subject_id',
                  'AX_Number_of_Correct_Trials',  # num of correct trials
                  'AY_Number_of_Correct_Trials',
                  'BX_Number_of_Correct_Trials',
                  'BY_Number_of_Correct_Trials',
                  'AX_visits_top_probe', 'AX_visits_bottom_probe', 'AX_visits_cue',  # aoi visit count
                  'AY_visits_top_probe', 'AY_visits_bottom_probe', 'AY_visits_cue',
                  'BX_visits_top_probe', 'BX_visits_bottom_probe', 'BX_visits_cue',
                  'BY_visits_top_probe', 'BY_visits_bottom_probe', 'BY_visits_cue',
                  'AX_visits_cue_per_correct_trial', 'AX_visits_top_per_correct_trial',
                  'AX_visits_bottom_per_correct_trial',  # visits per correct trial
                  'AY_visits_cue_per_correct_trial', 'AY_visits_top_per_correct_trial',
                  'AY_visits_bottom_per_correct_trial',
                  'BX_visits_cue_per_correct_trial', 'BX_visits_top_per_correct_trial',
                  'BX_visits_bottom_per_correct_trial',
                  'BY_visits_cue_per_correct_trial', 'BY_visits_top_per_correct_trial',
                  'BY_visits_bottom_per_correct_trial',
                  'blk1_AX_VISITS_cue', 'blk2_AX_VISITS_cue', 'blk3_AX_VISITS_cue', 'blk4_AX_VISITS_cue',
                  # visits by blocks
                  'blk1_AX_VISITS_top', 'blk2_AX_VISITS_top', 'blk3_AX_VISITS_top', 'blk4_AX_VISITS_top',
                  'blk1_AX_VISITS_bottom', 'blk2_AX_VISITS_bottom', 'blk3_AX_VISITS_bottom', 'blk4_AX_VISITS_bottom',
                  'blk1_AY_VISITS_cue', 'blk2_AY_VISITS_cue', 'blk3_AY_VISITS_cue', 'blk4_AY_VISITS_cue',
                  'blk1_AY_VISITS_top', 'blk2_AY_VISITS_top', 'blk3_AY_VISITS_top', 'blk4_AY_VISITS_top',
                  'blk1_AY_VISITS_bottom', 'blk2_AY_VISITS_bottom', 'blk3_AY_VISITS_bottom', 'blk4_AY_VISITS_bottom',
                  'blk1_BX_VISITS_cue', 'blk2_BX_VISITS_cue', 'blk3_BX_VISITS_cue', 'blk4_BX_VISITS_cue',
                  'blk1_BX_VISITS_top', 'blk2_BX_VISITS_top', 'blk3_BX_VISITS_top', 'blk4_BX_VISITS_top',
                  'blk1_BX_VISITS_bottom', 'blk2_BX_VISITS_bottom', 'blk3_BX_VISITS_bottom', 'blk4_BX_VISITS_bottom',
                  'blk1_BY_VISITS_cue', 'blk2_BY_VISITS_cue', 'blk3_BY_VISITS_cue', 'blk4_BY_VISITS_cue',
                  'blk1_BY_VISITS_top', 'blk2_BY_VISITS_top', 'blk3_BY_VISITS_top', 'blk4_BY_VISITS_top',
                  'blk1_BY_VISITS_bottom', 'blk2_BY_VISITS_bottom', 'blk3_BY_VISITS_bottom', 'blk4_BY_VISITS_bottom',
                  'AX_TVD_cue_sec', 'AX_TVD_top_sec', 'AX_TVD_bottom_sec',  # tvd
                  'AY_TVD_cue_sec', 'AY_TVD_top_sec', 'AY_TVD_bottom_sec',
                  'BX_TVD_cue_sec', 'BX_TVD_top_sec', 'BX_TVD_bottom_sec',
                  'BY_TVD_cue_sec', 'BY_TVD_top_sec', 'BY_TVD_bottom_sec',
                  'AX_TVD_cue_per_correct_trial', 'AX_TVD_top_per_correct_trial', 'AX_TVD_bottom_per_correct_trial',
                  # TVD per correct trial
                  'AY_TVD_cue_per_correct_trial', 'AY_TVD_top_per_correct_trial', 'AY_TVD_bottom_per_correct_trial',
                  'BX_TVD_cue_per_correct_trial', 'BX_TVD_top_per_correct_trial', 'BX_TVD_bottom_per_correct_trial',
                  'BY_TVD_cue_per_correct_trial', 'BY_TVD_top_per_correct_trial', 'BY_TVD_bottom_per_correct_trial',
                  'AX_Initial_TVD_Cue_sec',  # initial tvd of cue in seconds
                  'AY_Initial_TVD_Cue_sec',
                  'BX_Initial_TVD_Cue_sec',
                  'BY_Initial_TVD_Cue_sec',
                  'AX_Initial_TVD_Cue_per_correct_trial',  # initial tvd of cue per correct trial
                  'AY_Initial_TVD_Cue_per_correct_trial',
                  'BX_Initial_TVD_Cue_per_correct_trial',
                  'BY_Initial_TVD_Cue_per_correct_trial',
                  'blk1_AX_TVD_cue_sec', 'blk2_AX_TVD_cue_sec', 'blk3_AX_TVD_cue_sec', 'blk4_AX_TVD_cue_sec',
                  # tvd by blocks
                  'blk1_AY_TVD_cue_sec', 'blk2_AY_TVD_cue_sec', 'blk3_AY_TVD_cue_sec', 'blk4_AY_TVD_cue_sec',
                  'blk1_BX_TVD_cue_sec', 'blk2_BX_TVD_cue_sec', 'blk3_BX_TVD_cue_sec', 'blk4_BX_TVD_cue_sec',
                  'blk1_BY_TVD_cue_sec', 'blk2_BY_TVD_cue_sec', 'blk3_BY_TVD_cue_sec', 'blk4_BY_TVD_cue_sec',
                  'blk1_AX_TVD_top_sec', 'blk2_AX_TVD_top_sec', 'blk3_AX_TVD_top_sec', 'blk4_AX_TVD_top_sec',
                  'blk1_AY_TVD_top_sec', 'blk2_AY_TVD_top_sec', 'blk3_AY_TVD_top_sec', 'blk4_AY_TVD_top_sec',
                  'blk1_BX_TVD_top_sec', 'blk2_BX_TVD_top_sec', 'blk3_BX_TVD_top_sec', 'blk4_BX_TVD_top_sec',
                  'blk1_BY_TVD_top_sec', 'blk2_BY_TVD_top_sec', 'blk3_BY_TVD_top_sec', 'blk4_BY_TVD_top_sec',
                  'blk1_AX_TVD_bottom_sec', 'blk2_AX_TVD_bottom_sec', 'blk3_AX_TVD_bottom_sec',
                  'blk4_AX_TVD_bottom_sec',
                  'blk1_AY_TVD_bottom_sec', 'blk2_AY_TVD_bottom_sec', 'blk3_AY_TVD_bottom_sec',
                  'blk4_AY_TVD_bottom_sec',
                  'blk1_BX_TVD_bottom_sec', 'blk2_BX_TVD_bottom_sec', 'blk3_BX_TVD_bottom_sec',
                  'blk4_BX_TVD_bottom_sec',
                  'blk1_BY_TVD_bottom_sec', 'blk2_BY_TVD_bottom_sec', 'blk3_BY_TVD_bottom_sec',
                  'blk4_BY_TVD_bottom_sec',
                  # num of correct trials by block
                  "Blk_1_AX_Number_of_Correct_Trials",
                  "Blk_2_AX_Number_of_Correct_Trials",
                  "Blk_3_AX_Number_of_Correct_Trials",
                  "Blk_4_AX_Number_of_Correct_Trials",
                  "Blk_1_AY_Number_of_Correct_Trials",
                  "Blk_2_AY_Number_of_Correct_Trials",
                  "Blk_3_AY_Number_of_Correct_Trials",
                  "Blk_4_AY_Number_of_Correct_Trials",
                  "Blk_1_BX_Number_of_Correct_Trials",
                  "Blk_2_BX_Number_of_Correct_Trials",
                  "Blk_3_BX_Number_of_Correct_Trials",
                  "Blk_4_BX_Number_of_Correct_Trials",
                  "Blk_1_BY_Number_of_Correct_Trials",
                  "Blk_2_BY_Number_of_Correct_Trials",
                  "Blk_3_BY_Number_of_Correct_Trials",
                  "Blk_4_BY_Number_of_Correct_Trials",
                  # number of first fixations
                  'AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  # num of first fixation by block
                  'Blk_1_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_1_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_2_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_2_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_3_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_3_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_4_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_4_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_1_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_1_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_2_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_2_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_3_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_3_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_4_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_4_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_1_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_1_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_2_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_2_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_3_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_3_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_4_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_4_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_1_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_1_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_2_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_2_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_3_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_3_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  'Blk_4_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                  'Blk_4_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                  # proportion of correct trials
                  'Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                  'Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                  'Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                  'Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                  'Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                  'Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                  'Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                  'Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                  # proportion of correct trials by block
                  'Blk_1_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                  'Blk_1_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                  'Blk_2_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                  'Blk_2_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                  'Blk_3_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                  'Blk_3_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                  'Blk_4_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                  'Blk_4_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                  'Blk_1_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                  'Blk_1_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                  'Blk_2_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                  'Blk_2_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                  'Blk_3_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                  'Blk_3_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                  'Blk_4_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                  'Blk_4_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                  'Blk_1_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                  'Blk_1_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                  'Blk_2_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                  'Blk_2_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                  'Blk_3_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                  'Blk_3_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                  'Blk_4_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                  'Blk_4_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                  'Blk_1_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                  'Blk_1_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                  'Blk_2_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                  'Blk_2_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                  'Blk_3_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                  'Blk_3_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                  'Blk_4_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                  'Blk_4_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                  # time to first fixation
                  'AX_Time_To_Top_Right_Probe', 'AX_Time_To_Bottom_Right_Probe',
                  'AY_Time_To_Top_Right_Probe', 'AY_Time_To_Bottom_Right_Probe',
                  'BX_Time_To_Top_Right_Probe', 'BX_Time_To_Bottom_Right_Probe',
                  'BY_Time_To_Top_Right_Probe', 'BY_Time_To_Bottom_Right_Probe']]

    # create results dataframe populated with values
    results = pd.DataFrame(data=mydata, columns=mycolumns)

    # append main results into output block dataframe
    output = pd.concat([output, results])

    print("Success!")  # DEBUG LINE

    ###################################### OUTPUT RESULTS ##########################################

    print(f'\n\nOutputting results for {subject_id}')  # DEBUG LINE

# output tvd within trials (cue) results
merged_cueTVD_within_trials = pd.concat(cue_tvd_within_trials_df_list, ignore_index=True)  # merge all cue tvd within trials dataframes 
merged_cueTVD_within_trials.to_excel('./!OUTPUT//Cue_TVD_within_trials.xlsx', index=False)  # output result to file

# output into output folder as excel file 'df' will probably be a new name by the end
output.to_excel(f'{output_path}' + '//' + f'AXCPT_ALL_TRIALS_MAIN_OUTPUT.xlsx')

# reset output dataframe for next run # AOI1 = top, AOI2 = bottom, AOI3 = cue
output = pd.DataFrame(columns=[['subject_id',
                                'AX_Number_of_Correct_Trials',  # num of correct trials
                                'AY_Number_of_Correct_Trials',
                                'BX_Number_of_Correct_Trials',
                                'BY_Number_of_Correct_Trials',
                                'AX_visits_top_probe', 'AX_visits_bottom_probe', 'AX_visits_cue',  # aoi visit count
                                'AY_visits_top_probe', 'AY_visits_bottom_probe', 'AY_visits_cue',
                                'BX_visits_top_probe', 'BX_visits_bottom_probe', 'BX_visits_cue',
                                'BY_visits_top_probe', 'BY_visits_bottom_probe', 'BY_visits_cue',
                                'AX_visits_cue_per_correct_trial', 'AX_visits_top_per_correct_trial',
                                'AX_visits_bottom_per_correct_trial',  # visits per correct trial
                                'AY_visits_cue_per_correct_trial', 'AY_visits_top_per_correct_trial',
                                'AY_visits_bottom_per_correct_trial',
                                'BX_visits_cue_per_correct_trial', 'BX_visits_top_per_correct_trial',
                                'BX_visits_bottom_per_correct_trial',
                                'BY_visits_cue_per_correct_trial', 'BY_visits_top_per_correct_trial',
                                'BY_visits_bottom_per_correct_trial',
                                'blk1_AX_VISITS_cue', 'blk2_AX_VISITS_cue', 'blk3_AX_VISITS_cue', 'blk4_AX_VISITS_cue',
                                # visits by blocks
                                'blk1_AX_VISITS_top', 'blk2_AX_VISITS_top', 'blk3_AX_VISITS_top', 'blk4_AX_VISITS_top',
                                'blk1_AX_VISITS_bottom', 'blk2_AX_VISITS_bottom', 'blk3_AX_VISITS_bottom',
                                'blk4_AX_VISITS_bottom',
                                'blk1_AY_VISITS_cue', 'blk2_AY_VISITS_cue', 'blk3_AY_VISITS_cue', 'blk4_AY_VISITS_cue',
                                'blk1_AY_VISITS_top', 'blk2_AY_VISITS_top', 'blk3_AY_VISITS_top', 'blk4_AY_VISITS_top',
                                'blk1_AY_VISITS_bottom', 'blk2_AY_VISITS_bottom', 'blk3_AY_VISITS_bottom',
                                'blk4_AY_VISITS_bottom',
                                'blk1_BX_VISITS_cue', 'blk2_BX_VISITS_cue', 'blk3_BX_VISITS_cue', 'blk4_BX_VISITS_cue',
                                'blk1_BX_VISITS_top', 'blk2_BX_VISITS_top', 'blk3_BX_VISITS_top', 'blk4_BX_VISITS_top',
                                'blk1_BX_VISITS_bottom', 'blk2_BX_VISITS_bottom', 'blk3_BX_VISITS_bottom',
                                'blk4_BX_VISITS_bottom',
                                'blk1_BY_VISITS_cue', 'blk2_BY_VISITS_cue', 'blk3_BY_VISITS_cue', 'blk4_BY_VISITS_cue',
                                'blk1_BY_VISITS_top', 'blk2_BY_VISITS_top', 'blk3_BY_VISITS_top', 'blk4_BY_VISITS_top',
                                'blk1_BY_VISITS_bottom', 'blk2_BY_VISITS_bottom', 'blk3_BY_VISITS_bottom',
                                'blk4_BY_VISITS_bottom',
                                'AX_TVD_cue_sec', 'AX_TVD_top_sec', 'AX_TVD_bottom_sec',  # tvd
                                'AY_TVD_cue_sec', 'AY_TVD_top_sec', 'AY_TVD_bottom_sec',
                                'BX_TVD_cue_sec', 'BX_TVD_top_sec', 'BX_TVD_bottom_sec',
                                'BY_TVD_cue_sec', 'BY_TVD_top_sec', 'BY_TVD_bottom_sec',
                                'AX_TVD_cue_per_correct_trial', 'AX_TVD_top_per_correct_trial',
                                'AX_TVD_bottom_per_correct_trial',  # TVD per correct trial
                                'AY_TVD_cue_per_correct_trial', 'AY_TVD_top_per_correct_trial',
                                'AY_TVD_bottom_per_correct_trial',
                                'BX_TVD_cue_per_correct_trial', 'BX_TVD_top_per_correct_trial',
                                'BX_TVD_bottom_per_correct_trial',
                                'BY_TVD_cue_per_correct_trial', 'BY_TVD_top_per_correct_trial',
                                'BY_TVD_bottom_per_correct_trial',
                                'AX_Initial_TVD_Cue_sec',  # initial tvd of cue in seconds
                                'AY_Initial_TVD_Cue_sec',
                                'BX_Initial_TVD_Cue_sec',
                                'BY_Initial_TVD_Cue_sec',
                                'AX_Initial_TVD_Cue_per_correct_trial',  # initial tvd of cue per correct trial
                                'AY_Initial_TVD_Cue_per_correct_trial',
                                'BX_Initial_TVD_Cue_per_correct_trial',
                                'BY_Initial_TVD_Cue_per_correct_trial',
                                'blk1_AX_TVD_cue_sec', 'blk2_AX_TVD_cue_sec', 'blk3_AX_TVD_cue_sec',
                                'blk4_AX_TVD_cue_sec',  # tvd by blocks
                                'blk1_AY_TVD_cue_sec', 'blk2_AY_TVD_cue_sec', 'blk3_AY_TVD_cue_sec',
                                'blk4_AY_TVD_cue_sec',
                                'blk1_BX_TVD_cue_sec', 'blk2_BX_TVD_cue_sec', 'blk3_BX_TVD_cue_sec',
                                'blk4_BX_TVD_cue_sec',
                                'blk1_BY_TVD_cue_sec', 'blk2_BY_TVD_cue_sec', 'blk3_BY_TVD_cue_sec',
                                'blk4_BY_TVD_cue_sec',
                                'blk1_AX_TVD_top_sec', 'blk2_AX_TVD_top_sec', 'blk3_AX_TVD_top_sec',
                                'blk4_AX_TVD_top_sec',
                                'blk1_AY_TVD_top_sec', 'blk2_AY_TVD_top_sec', 'blk3_AY_TVD_top_sec',
                                'blk4_AY_TVD_top_sec',
                                'blk1_BX_TVD_top_sec', 'blk2_BX_TVD_top_sec', 'blk3_BX_TVD_top_sec',
                                'blk4_BX_TVD_top_sec',
                                'blk1_BY_TVD_top_sec', 'blk2_BY_TVD_top_sec', 'blk3_BY_TVD_top_sec',
                                'blk4_BY_TVD_top_sec',
                                'blk1_AX_TVD_bottom_sec', 'blk2_AX_TVD_bottom_sec', 'blk3_AX_TVD_bottom_sec',
                                'blk4_AX_TVD_bottom_sec',
                                'blk1_AY_TVD_bottom_sec', 'blk2_AY_TVD_bottom_sec', 'blk3_AY_TVD_bottom_sec',
                                'blk4_AY_TVD_bottom_sec',
                                'blk1_BX_TVD_bottom_sec', 'blk2_BX_TVD_bottom_sec', 'blk3_BX_TVD_bottom_sec',
                                'blk4_BX_TVD_bottom_sec',
                                'blk1_BY_TVD_bottom_sec', 'blk2_BY_TVD_bottom_sec', 'blk3_BY_TVD_bottom_sec',
                                'blk4_BY_TVD_bottom_sec',
                                # num of correct trials by block
                                "Blk_1_AX_Number_of_Correct_Trials",
                                "Blk_2_AX_Number_of_Correct_Trials",
                                "Blk_3_AX_Number_of_Correct_Trials",
                                "Blk_4_AX_Number_of_Correct_Trials",
                                "Blk_1_AY_Number_of_Correct_Trials",
                                "Blk_2_AY_Number_of_Correct_Trials",
                                "Blk_3_AY_Number_of_Correct_Trials",
                                "Blk_4_AY_Number_of_Correct_Trials",
                                "Blk_1_BX_Number_of_Correct_Trials",
                                "Blk_2_BX_Number_of_Correct_Trials",
                                "Blk_3_BX_Number_of_Correct_Trials",
                                "Blk_4_BX_Number_of_Correct_Trials",
                                "Blk_1_BY_Number_of_Correct_Trials",
                                "Blk_2_BY_Number_of_Correct_Trials",
                                "Blk_3_BY_Number_of_Correct_Trials",
                                "Blk_4_BY_Number_of_Correct_Trials",
                                'AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',  # number of first fixations
                                'AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                # num of first fixation by block
                                'Blk_1_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_1_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_2_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_2_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_3_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_3_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_4_AX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_4_AX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_1_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_1_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_2_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_2_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_3_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_3_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_4_AY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_4_AY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_1_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_1_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_2_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_2_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_3_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_3_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_4_BX_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_4_BX_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_1_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_1_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_2_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_2_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_3_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_3_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                'Blk_4_BY_Number_of_First_Fixations_Top_B4_Bottom_Probe',
                                'Blk_4_BY_Number_of_First_Fixations_Bottom_B4_Top_Probe',
                                # proportion of correct trials
                                'Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                                'Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                                'Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                                'Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                                'Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                                'Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                                'Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                                'Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                                # proportion of correct trials by block
                                'Blk_1_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                                'Blk_1_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                                'Blk_2_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                                'Blk_2_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                                'Blk_3_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                                'Blk_3_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                                'Blk_4_Proportion_of_Correct_Trials_AX_Top_B4_Bottom_Probe',
                                'Blk_4_Proportion_of_Correct_Trials_AX_Bot_B4_Top_Probe',
                                'Blk_1_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                                'Blk_1_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                                'Blk_2_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                                'Blk_2_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                                'Blk_3_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                                'Blk_3_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                                'Blk_4_Proportion_of_Correct_Trials_AY_Top_B4_Bottom_Probe',
                                'Blk_4_Proportion_of_Correct_Trials_AY_Bot_B4_Top_Probe',
                                'Blk_1_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                                'Blk_1_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                                'Blk_2_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                                'Blk_2_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                                'Blk_3_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                                'Blk_3_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                                'Blk_4_Proportion_of_Correct_Trials_BX_Top_B4_Bottom_Probe',
                                'Blk_4_Proportion_of_Correct_Trials_BX_Bot_B4_Top_Probe',
                                'Blk_1_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                                'Blk_1_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                                'Blk_2_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                                'Blk_2_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                                'Blk_3_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                                'Blk_3_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                                'Blk_4_Proportion_of_Correct_Trials_BY_Top_B4_Bottom_Probe',
                                'Blk_4_Proportion_of_Correct_Trials_BY_Bot_B4_Top_Probe',
                                'AX_Time_To_Top_Right_Probe', 'AX_Time_To_Bottom_Right_Probe',  # time to first fixation
                                'AY_Time_To_Top_Right_Probe', 'AY_Time_To_Bottom_Right_Probe',
                                'BX_Time_To_Top_Right_Probe', 'BX_Time_To_Bottom_Right_Probe',
                                'BY_Time_To_Top_Right_Probe', 'BY_Time_To_Bottom_Right_Probe']])

# success message and time it took
print('\nAnalysis was successful! Operation completed in --- %s seconds --- !' % round(time.time() - start_time, 2))

# prompt user to exit program
while True:
    user_input = input("\n\nPress enter to exit the program: ")
    if user_input == "exit" or user_input == "\n" or user_input == "":
        print("Exiting program...")
        break
    else:
        user_input = input("\nERROR: Press enter to exit the program: ")
