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

plt.savefig('fig-basics-observations.png')

# We want to plot gender.
dat = df['GENDER'].loc[:, 1978].astype('category')
dat = dat.cat.rename_categories({1: 'Male', 2: 'Female'})
dat = dat.value_counts().to_dict()

fig, ax = plt.subplots()
ax.set_ylabel('Observations')
ax.set_xlabel('Gender')

set_formatter(ax)
ax.bar(dat.keys(), dat.values())
plt.savefig('fig-basics-gender.png')

# We want to plot ethnic origin.
dat = df['RACE'].loc[:, 1978].astype('category')
dat = dat.cat.rename_categories({1: 'Hispanic', 2: 'Black', 3: 'Other'})
dat = dat.value_counts().to_dict()

fig, ax = plt.subplots()
ax.set_ylabel('Observations')
ax.set_xlabel('Race')

set_formatter(ax)
ax.bar(dat.keys(), dat.values())
plt.savefig('fig-basics-race.png')

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
plt.savefig('fig-basics-birth.png')
