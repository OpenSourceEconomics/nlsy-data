"""This module contains some auxiliary functions shared across the figures."""
import subprocess
import os

import pandas as pd
import numpy as np

# We might need to create the dataset if it does not exist in the first place.
fname = '../../data/output/original.pkl'
fname2 = '../../data/input/TNFI_TRUNC_79.csv'
if not os.path.exists(fname):
    cwd = os.getcwd()
    os.chdir('../../data/')
    subprocess.check_call('./create_data')
    os.chdir(cwd)

OBS_DATASET = pd.read_pickle(fname)
SURVEY_YEARS = OBS_DATASET['SURVEY_YEAR'].unique()

TNFI_79 = pd.read_csv(fname2)
OBS_DATASET_79_incomplete = OBS_DATASET[OBS_DATASET.SURVEY_YEAR == 1978]
OBS_DATASET_79_almost = OBS_DATASET_79_incomplete.join(TNFI_79.set_index('IDENTIFIER'), on='IDENTIFIER')
OBS_DATASET_79 = OBS_DATASET_79_almost[OBS_DATASET_79_almost.TNFI_TRUNC >= 0]

def get_dataset():
    """This function returns the observed dataset."""
    # We add a crude measure on an individual's age. This is not the most accurate as the times
    # of the interview are spread all over the year.
    OBS_DATASET['AGE'] = OBS_DATASET['SURVEY_YEAR'] - OBS_DATASET['YEAR_OF_BIRTH']

    # We construct a new race variable based on the different samples.
    OBS_DATASET['RACE_NEW'] = np.nan

    cond = OBS_DATASET['SAMPLE_ID'].isin([1, 2, 5, 6, 9, 12, 15, 18])
    OBS_DATASET.loc[cond, 'RACE_NEW'] = 'white'

    cond = OBS_DATASET['SAMPLE_ID'].isin([3, 7, 10, 13, 16, 19])
    OBS_DATASET.loc[cond, 'RACE_NEW'] = 'black'

    cond = OBS_DATASET['SAMPLE_ID'].isin([4, 811, 14, 17, 20])
    OBS_DATASET.loc[cond, 'RACE_NEW'] = 'hispanic'

    return OBS_DATASET


def get_other_dataset():

    first_q = np.percentile(OBS_DATASET_79['TNFI_TRUNC'], 25)
    second_q = np.percentile(OBS_DATASET_79['TNFI_TRUNC'], 50)
    third_q = np.percentile(OBS_DATASET_79['TNFI_TRUNC'], 75)

    OBS_DATASET_79['FAMILY_INCOME_QUARTILE'] = np.nan

    def func(x):
        if x < first_q:
            return 'first quartile'
        elif first_q <= x < second_q:
            return 'second quartile'
        elif second_q <= x < third_q:
            return 'third quartile'
        return 'fourth quartile'

    OBS_DATASET_79['FAMILY_INCOME_QUARTILE'] = OBS_DATASET_79['TNFI_TRUNC'].apply(func)

    return OBS_DATASET_79
