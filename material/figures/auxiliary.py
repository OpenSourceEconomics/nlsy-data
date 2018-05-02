"""This module contains some auxiliary functions shared across the figures."""
import pandas as pd

OBS_DATASET = pd.read_pickle('../../data/output/original.pkl')
SURVEY_YEARS = OBS_DATASET['SURVEY_YEAR'].unique()


def get_dataset():
    """This function returns the observed dataset."""
    return OBS_DATASET
