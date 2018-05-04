#!/usr/bin/env python
"""This module creates figures that illustrate the intergenerational transmission of human
capital."""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from auxiliary import get_dataset

df = get_dataset()

cond = df['AGE'].isin([35])
df = df[cond]

for parent in ['father', 'mother']:

    ax = plt.figure().add_subplot(111)

    label = 'HIGHEST_GRADE_COMPLETED_' + parent.upper()
    cond = df[label].between(10, 16)
    x = df.loc[cond, label]

    label = 'HIGHEST_GRADE_COMPLETED'
    cond = df[label].between(10, 16)
    y = df.loc[cond, label]

    tab = pd.crosstab(y, x, normalize=True)
    hm = sns.heatmap(tab, cmap="Blues", vmin=0, vmax=0.05, annot=False)
    hm.invert_yaxis()

    ax.set_yticks(np.linspace(0.5, 6.5, 7))
    ax.set_yticklabels(range(10, 17))
    ax.set_ylabel('Education')

    ax.set_xticks(np.linspace(0.5, 6.5, 7))
    ax.set_xticklabels(range(10, 17))
    plt.xlabel(parent.capitalize() + "'s Education")

    plt.savefig('fig-human-capital-intergenerational-' + parent + '.png')

