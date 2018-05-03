"""This module contains some auxiliary functions shared across the figures."""
import pandas as pd
import numpy as np

OBS_DATASET = pd.read_pickle('../../data/output/original.pkl')
SURVEY_YEARS = OBS_DATASET['SURVEY_YEAR'].unique()


def get_dataset():
    """This function returns the observed dataset."""
    # We add a crude measure on an individual's age. This is not the most accurate as the times
    # of the interview are spread all over the year.
    OBS_DATASET['AGE'] = OBS_DATASET['SURVEY_YEAR'] - OBS_DATASET['YEAR_OF_BIRTH']

    # We construct a new race variable based on the different samples.
    OBS_DATASET['RACE_NEW'] = np.nan

    cond = OBS_DATASET['SAMPLE_ID'].isin([1, 2, 5, 6, 9, 12, 15, 18])
    OBS_DATASET['RACE_NEW'].loc[cond] = 'white'

    cond = OBS_DATASET['SAMPLE_ID'].isin([3, 7, 10, 13, 16, 19])
    OBS_DATASET['RACE_NEW'].loc[cond] = 'black'

    cond = OBS_DATASET['SAMPLE_ID'].isin([4, 811, 14, 17, 20])
    OBS_DATASET['RACE_NEW'].loc[cond] = 'hispanic'

    return OBS_DATASET
