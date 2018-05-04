"""This module creates figues that illustrate the intergenerational transmission of human
capital."""
from matplotlib.ticker import MaxNLocator
import seaborn.apionly as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from auxiliary import get_dataset


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

    plt.yticks(np.linspace(0.5, 6.5, 7), range(10, 17), rotation=0)
    plt.xticks(np.linspace(0.5, 6.5, 7), range(10, 17), rotation=0)

    plt.ylabel('Education')

    label = parent.capitalize() + "'s Education"
    plt.xlabel(label)

    plt.savefig('fig-human-capital-intergenerational-' + parent + '.png')

