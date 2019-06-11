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
TNFI_79['SURVEY_YEAR'] = 1978
OBS_DATASET = pd.merge(OBS_DATASET, TNFI_79, how='left', left_on=['IDENTIFIER', 'SURVEY_YEAR'],
                       right_on=['IDENTIFIER', 'SURVEY_YEAR'])


def get_dataset():
    """This function returns the observed dataset."""
    # We add a crude measure on an individual's age. This is not the most accurate as the times
    # of the interview are spread all over the year.
    OBS_DATASET['AGE'] = OBS_DATASET['SURVEY_YEAR'] - OBS_DATASET['YEAR_OF_BIRTH']
    
    # constructing the family income quartile variable
    trunc_data = OBS_DATASET.loc[OBS_DATASET['SURVEY_YEAR'] == 1978, ['TNFI_TRUNC']].dropna()
    first_q = np.percentile(trunc_data, 25)
    second_q = np.percentile(trunc_data, 50)
    third_q = np.percentile(trunc_data, 75)

    OBS_DATASET['FAMILY_INCOME_QUARTILE'] = np.nan

    def func(x):
        if 'NaN' != x < first_q:
            return 'first quartile'
        elif first_q <= x < second_q:
            return 'second quartile'
        elif second_q <= x < third_q:
            return 'third quartile'
        elif third_q <= x != 'NaN':
            return 'fourth quartile'

    OBS_DATASET['FAMILY_INCOME_QUARTILE'] = OBS_DATASET['TNFI_TRUNC'].apply(func)

    return OBS_DATASET
