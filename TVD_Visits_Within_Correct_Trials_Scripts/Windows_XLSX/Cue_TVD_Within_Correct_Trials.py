# libraries for reading and writing files as well as multithreading tasks (xlsx to csv conversion)
import glob
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

# FILE IO PATHS!
excel_input_path = './!INPUT//'  # location of our excel files # './test//' or './excel_input//'
csv_input_path = './!CONVERTED_INPUT//'  # where we want to store our converted excel files
output_path = './!OUTPUT//'  # where we want our final output dataframe to be stored

CONDITION_RULES = {
    #  name : (AOICue value, probe-column, keep_X?)
    "AX": ("A", "AOIProbe1",  True),   # == 'X'
    "AY": ("A", "AOIProbe1",  False),  # != 'X'
    "BX": ("B", "AOIProbe2",  True),
    "BY": ("B", "AOIProbe2",  False),
}

TVD_FACTOR = 16.65496782 / 1000        # constant used everywhere


def _xlsx_to_csv(xlsx_path):
    out_csv = os.path.join(csv_input_path, f'{Path(xlsx_path).stem}.csv')
    df = pd.read_excel(xlsx_path, engine='openpyxl')
    df.to_csv(out_csv, index=False)
    return Path(xlsx_path).name


def convert_excels_to_csv(parallel=True, n_workers=8):
    excel_files = glob.glob(os.path.join(excel_input_path, '*.xlsx'))
    if not excel_files:
        print("No .xlsx files detected – skipping conversion.")
        return

    os.makedirs(csv_input_path, exist_ok=True)

    if not parallel or len(excel_files) < 10:
        for f in excel_files:
            print(f'→ Converting {Path(f).name}')
            _xlsx_to_csv(f)
    else:
        print(f'→ Converting {len(excel_files)} Excel files with {n_workers} threads …')
        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = {pool.submit(_xlsx_to_csv, f): f for f in excel_files}
            for fut in as_completed(futures):
                print(f'   ✓ {fut.result()}')

    print("Excel-to-CSV conversion complete.\n")


def extract_condition(df, name, cue_val, probe_col, keep_X):
    """
    Return TVD-within-trial rows for a single AX/AY/BX/BY condition,
    including both raw count and converted tvd_within_trial. In every
    given trial, for each condition, how long did the participant look at the cue.
    (looks at contiguous ones in the AOI column)
    """
    # mask rows for this condition and the ISI epoch
    if keep_X:
        mask = (df['AOICue'] == cue_val) & (df[probe_col] == 'X')
    else:
        mask = (df['AOICue'] == cue_val) & (df[probe_col] != 'X')

    sub = df.loc[mask & (df['CurrentObject'] == 'ISI')].copy()
    if sub.empty:  # subject might have zero trials of a type
        return pd.DataFrame()

    # contiguous gaze intervals
    sub['interval'] = sub['AOI'].ne(sub['AOI'].shift()).cumsum()  # create a sub df called interval
    sub['count']    = sub.groupby(['AOI', 'interval']).cumcount() + 1  # create another sub called count

    # one row per interval, keep only cue AOI == 3 (this creates individual DFs with NewTrialID, Count cols)
    counts = (
        sub
        .groupby('interval').last()          # one row per segment (1 segment = a contiguous gaze interval)
        .query('AOI == 3')                   # cue AOI only (filter these rows to only include cue AOI)
        .query('ACC == 1')                   # correct trials only
        .groupby('NewTrialId')['count']      # group the filtered rows by trial num
        .sum()                               # add the count values in each trial = total num of gaze samples spent on AOI3 in ISI of trial.
        .reset_index(name='count')           # reformat df into NewTrialId + count
    )

    # convert count → tvd
    counts['tvd_within_trial'] = counts['count'] * TVD_FACTOR

    # label & return
    counts.insert(0, 'Subject', df['Subject'].iat[0])
    counts['condition'] = name
    return counts


def process_file(path):
    # read xlsx csv file
    df = pd.read_csv(path)

    # read gazedata csv file
    # df = pd.read_csv(path, delimiter="\t")  # delimiter indicates gazedata has tab seperated values

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
# 1 ▸ convert every .xlsx in !INPUT/ to .csv in !CONVERTED_INPUT/
convert_excels_to_csv(parallel=True, n_workers=8)

# 2 ▸ build one big DataFrame from all CSVs
all_results = pd.concat(
    [process_file(f) for f in glob.glob(os.path.join(csv_input_path, '*.csv'))],
    ignore_index=True
)

if all_results.empty:
    sys.exit("No usable data produced—check your filters and input files.")

# 3 ▸ write the Excel you actually want
outfile = os.path.join(output_path, 'Cue_TVD_Within_Correct_Trials.xlsx')
all_results.to_excel(outfile, index=False)
print(f"✓ Finished: {outfile}")

