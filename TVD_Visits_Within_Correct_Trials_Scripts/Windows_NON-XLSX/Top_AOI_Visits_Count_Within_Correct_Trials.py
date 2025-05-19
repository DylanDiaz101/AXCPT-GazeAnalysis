# libraries for reading and writing files as well as multithreading tasks (xlsx to csv conversion)
import glob
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd


# FILE IO PATHS!
csv_input_path = './!INPUT//'  # where we want to store our .gazedata files (.gazedata is a csv but delimited by /t)
output_path = './!OUTPUT//'  # where we want our final output dataframe to be stored

CONDITION_RULES = {
    #  name : (AOICue value, probe-column, keep_X?)
    "AX": ("A", "AOIProbe1",  True),   # == 'X'
    "AY": ("A", "AOIProbe1",  False),  # != 'X'
    "BX": ("B", "AOIProbe2",  True),
    "BY": ("B", "AOIProbe2",  False),
}

TVD_FACTOR = 16.65496782 / 1000        # constant used everywhere


def extract_condition(df, name, cue_val, probe_col, keep_X):
    """
    Return TVD-within-trial rows for a single AX/AY/BX/BY condition,
    including both raw count and converted tvd_within_trial. In every
    given trial, for each condition, how long did the participant look at the cue.
    (looks at contiguous ones in the AOI column)
    """
    # ---------------- select rows for this condition ---------------
    if keep_X:
        mask = (df['AOICue'] == cue_val) & (df[probe_col] == 'X')
    else:
        mask = (df['AOICue'] == cue_val) & (df[probe_col] != 'X')

    sub = df.loc[mask & (df['CurrentObject'] == 'ISI')].copy()

    # --- keep only CORRECT TRIALS -----------------------------------
    sub = sub[sub['ACC'] == 1].copy()
    if sub.empty:
        return pd.DataFrame()

    # mark contiguous gaze segments
    sub['interval'] = sub['AOI'].ne(sub['AOI'].shift()).cumsum()

    # -------- interval count for the AOI of interest -----------------
    interval_counts = (
        sub
        .groupby('interval').first()  # 1 row per contiguous segment
        .query('AOI == 1')  # ⬅️  use 1 for probe (top) script
        .groupby('NewTrialId')
        .size()
        .reset_index(name='n_intervals')
    )

    # -------- all correct trials for *this* condition ----------------
    all_trials = (
        sub[['NewTrialId']].drop_duplicates()
        .assign(n_intervals=0)  # default = 0
    )

    # left-join so trials without any interval become 0
    result = (
        all_trials.merge(interval_counts,
                         on='NewTrialId',
                         how='left',
                         suffixes=('_drop', ''))
        .fillna({'n_intervals': 0})
        .astype({'n_intervals': 'int32'})
        .loc[:, ['NewTrialId', 'n_intervals']]  # clean columns
    )

    # dress it up
    result.insert(0, 'Subject', df['Subject'].iat[0])
    result['condition'] = name
    return result


def process_file(path):
    # read gazedata csv file
    df = pd.read_csv(path, delimiter="\t")  # delimiter indicates gazedata has tab seperated values

    # keep only what we need and add NewTrialId once
    cols = ['Subject','AOI','AOICue','AOIProbe1','AOIProbe2', 'ACC',
            'CurrentObject','TrialId','ID']
    df = df[cols].copy()
    df['NewTrialId'] = df['TrialId'].ne(df['TrialId'].shift()).cumsum()

    ########################################### DROP INITIAL PRACTICE TRIALS ###########################################

    print('\nDropping initial practice trials...')  # DEBUG LINE

    # gets us the index of rows where 10 occurs
    idx_of_10 = df.index[df['TrialId'] == 10].tolist()

    practice_ends_list = []

    count = 0
    for idx_val in idx_of_10:
        # if the subsequent row after a row that has a value of 10 is 1 it means that we found the end of a practice block
        try:
            if df.loc[idx_val + 1]['TrialId'] == 1:
                practice_ends_list.append(idx_val + 1)
        except ValueError:
            break
        except KeyError:
            break

    # we get the last end value since if there are multiple practice trials we can delete everything before that
    # df[practice_end::] get everything AFTER the practice trials
    practice_end = practice_ends_list[len(practice_ends_list) - 1]

    df_2 = df[practice_end::]  # get everything after the practice trials

    print("Success!")  # DEBUG LINE

    # build each condition in a loop instead of four giant blocks
    chunks = [
        extract_condition(df_2, name, cue, probe_col, keep_X)
        for name, (cue, probe_col, keep_X) in CONDITION_RULES.items()
    ]

    out = (pd.concat(chunks, ignore_index=True)
             .sort_values('NewTrialId')
             .reset_index(drop=True))
    return out


# OUTPUT

# 1 ▸ build one big DataFrame from all CSVs
all_results = pd.concat(
    [process_file(f) for f in glob.glob(os.path.join(csv_input_path, '*.gazedata'))],
    ignore_index=True
)

if all_results.empty:
    sys.exit("No usable data produced—check your filters and input files.")

# 2 ▸ write the Excel you actually want
outfile = os.path.join(output_path, 'Top_AOI_Visits_Count_Within_Correct_Trials.xlsx')
all_results.to_excel(outfile, index=False)
print(f"✓ Finished: {outfile}")
