"""This module creates figues that illustrate the intergenerational transmission of human
capital."""
from matplotlib.ticker import MaxNLocator

from auxiliary import get_dataset

import pandas as pd
import seaborn.apionly as sns
import matplotlib.pyplot as plt

df = get_dataset()

cond = df['AGE'].isin([35])
df = df[cond]

for parent in ['father', 'mother']:

    ax = plt.figure().add_subplot(111)

    label = 'HIGHEST_GRADE_COMPLETED_' + parent.upper()
    x = df[label]
    x = x[x.between(10, 16)]

    y = df['HIGHEST_GRADE_COMPLETED']
    y = y[y.between(10, 16)]

    hm = sns.heatmap(pd.crosstab(y, x, normalize=True), cmap="Blues", vmin=0, vmax=0.05,
        annot=False)
    hm.invert_yaxis()
    plt.yticks(rotation=0)
    plt.ylabel('Education')

    label = parent.capitalize() + "'s Education"
    plt.xlabel(label)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.savefig('fig-human-capital-intergenerational-' + parent + '.png')

