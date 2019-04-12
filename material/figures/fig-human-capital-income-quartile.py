#!/usr/bin/env python
"""This script creates some informative graphs on racial differences in human capital."""
import matplotlib.pyplot as plt
import seaborn as sns

from auxiliary import get_other_dataset

df = get_other_dataset()

ax = plt.figure().add_subplot(111)
for group in ['first quartile', 'second quartile', 'third quartile', 'fourth quartile']:
    cond = df['FAMILY_INCOME_QUARTILE'] == group
    dat = df.loc[(slice(None), 1978), 'AFQT_RAW'].loc[cond].dropna()
    sns.distplot(dat, label=group.capitalize())

ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.set_xlabel('AFQT Scores')
ax.set_xlim([0, 120])
ax.legend()

plt.savefig('fig-human-capital-income-quartile-afqt.png')


for score in ['ROTTER', 'ROSENBERG']:

    ax = plt.figure().add_subplot(111)
    for group in ['first quartile', 'second quartile', 'third quartile', 'fourth quartile']:
        label = score + '_SCORE'
        dat = df[df['FAMILY_INCOME_QUARTILE'] == group].loc[(slice(None), 1978), label].dropna()
        sns.distplot(dat, label=group.capitalize())

    ax.set_xlabel(score.lower().capitalize() + ' Scores')
    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.legend()

    plt.savefig('fig-human-capital-income-quartile-' + score.lower() + '.png')
