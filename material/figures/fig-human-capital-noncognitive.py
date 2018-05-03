"""This module creates informative graphs on the cognitive skills measures in the dataset."""
import matplotlib.pyplot as plt
import seaborn.apionly as sns

from auxiliary import get_dataset

df = get_dataset()


# We look at racial differences in cognitive scores.

for score in ['ROTTER', 'ROSENBERG']:
    fig, ax = plt.subplots()

    for group in ['white', 'black', 'hispanic']:
        label = score + '_SCORE'
        dat = df[df['RACE_NEW'] == group].loc[(slice(None), 1978), label].dropna()
        sns.distplot(dat, label=group.capitalize())



    ax.yaxis.get_major_ticks()[0].set_visible(False)
    #plt.xlim([0, 40])
    plt.legend()

    label = score.lower().capitalize() + ' Scores'
    plt.xlabel(label)
    plt.savefig('fig-human-capital-noncognitve-' + score.lower() + '.png')
