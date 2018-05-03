"""This module creates figures that illustrate some basic relationships between labor market
success and measures of human capital."""
from auxiliary import get_dataset

import pandas as pd
import seaborn.apionly as sns
import matplotlib.pyplot as plt

df = get_dataset()

cond = df['AGE'].isin([35])
df = df[cond]

for parent in ['AFQT', 'ROSENBERG', 'ROTTER']:
    ax = plt.figure().add_subplot(111)

    if parent in ['AFQT']:
        label = 'AFQT_1'
        ylabel = 'AFQT'
    else:
        label = parent + '_SCORE'
        ylabel = parent.lower().capitalize()

    dat = df[label]
    x = pd.qcut(dat, 4, labels=False, duplicates="drop")

    dat = df['WAGE_HOURLY_JOB_1']
    y = pd.qcut(dat, 4, labels=False, duplicates="drop")

    hm = sns.heatmap(pd.crosstab(y, x, normalize=True), cmap="Blues", vmin=0, vmax=0.15, annot=True)
    plt.yticks(rotation=0)
    plt.ylabel('Hourly Wages (quartiles)')

    plt.xlabel(ylabel + ' Scores (quartiles)')
    hm.invert_yaxis()

    plt.savefig('fig-human-capital-basic-' + parent.lower() + '.png')

