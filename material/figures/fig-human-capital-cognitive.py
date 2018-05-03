"""This module creates informative graphs on the cognitive skills measures in the dataset."""
import matplotlib.pyplot as plt
import seaborn.apionly as sns

from auxiliary import get_dataset

df = get_dataset()

labels = []
labels += ['arithmetic-reasoning', 'word-knowledge', 'paragraph-comprehension']
labels += ['numerical-operations', 'afqt']

for label in labels:
    name = label.upper().replace('-', '_')
    if 'AFQT' in name:
        name += "_1"
    else:
        name = 'ASVAB_' + name

    fig, ax = plt.subplots()
    dat = df[name].loc[:, 1978].dropna()
    sns.distplot(dat, axlabel='Score')
    plt.savefig('fig-human-capital-cognitive-' + label + '.png')


# We look at racial differences in cognitive scores.
fig, ax = plt.subplots()

for group in ['white', 'black', 'hispanic']:
    dat = df[df['RACE_NEW'] == group].loc[(slice(None), 1978), 'AFQT_RAW'].dropna()
    sns.distplot(dat, label=group.capitalize())

ax.yaxis.get_major_ticks()[0].set_visible(False)
plt.xlim([0, 120])
plt.legend()
plt.xlabel('AFQT Scores')
plt.savefig('fig-human-capital-cognitive-race.png')
