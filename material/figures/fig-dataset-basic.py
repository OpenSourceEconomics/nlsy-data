"""This module creates some auxiliary graphs for the discussion of the dataset."""
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import matplotlib

from auxiliary import SURVEY_YEARS
from auxiliary import get_dataset


def set_formatter(ax):
    """This function ensures a pretty formatting"""
    formatter = matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.get_yaxis().set_major_formatter(formatter)


df = get_dataset()

# We want to plot the number of observations over time.
num_obs = []
for year in SURVEY_YEARS:
    cond = df['IS_INTERVIEWED'].loc[:, year].isin([True])
    num_obs += [df['IDENTIFIER'].loc[:, year][cond].count()]

fig, ax = plt.subplots()
set_formatter(ax)

ax.bar(df['SURVEY_YEAR'].unique(), num_obs)

ax.set_ylabel('Observations')
ax.set_xlabel('Year')

plt.savefig('fig-dataset-basic-observations.png')

# We want to plot gender.
dat = df['GENDER'].loc[:, 1978].astype('category')
dat = dat.cat.rename_categories({1: 'Male', 2: 'Female'})

fig, ax = plt.subplots()
ax.pie(dat.value_counts(normalize=True), labels=['Male', 'Female'], autopct='%1.1f%%')

plt.savefig('fig-dataset-basic-gender.png')

# We want to plot ethnic origin.
import numpy as np
df['RACE_NEW'] = np.nan
cond = df['SAMPLE_ID'].isin([1, 2, 5, 6, 9, 12, 15, 18])
df['RACE_NEW'].loc[cond] = 'White'
cond = df['SAMPLE_ID'].isin([3, 7, 10, 13, 16, 19])
df['RACE_NEW'].loc[cond] = 'Black'
cond = df['SAMPLE_ID'].isin([4, 811, 14, 17, 20])
df['RACE_NEW'].loc[cond] = 'Hispanic'


dat = df['RACE_NEW'].loc[:, 1978].astype('category')
fig, ax = plt.subplots()
ax.pie(dat.value_counts(normalize=True), labels=['White', 'Black', 'Hispanic'], autopct='%1.1f%%')
plt.savefig('fig-dataset-basic-race.png')

# We want to plot the years of birth. For pretty formatting, we remove years of birth with only a
# very small number of individuals.
dat = df['YEAR_OF_BIRTH'].loc[:, 1978]
dat = dat.value_counts().to_dict()

for year in [1955, 1956, 1965]:
    del dat[year]

fig, ax = plt.subplots()
ax.set_ylabel('Observations')
ax.set_xlabel('Year of Birth')
set_formatter(ax)
ax.bar(dat.keys(), dat.values())
plt.savefig('fig-dataset-basic-birth.png')