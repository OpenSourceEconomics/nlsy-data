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
    plt.savefig('fig-asvab-' + label + '.png')
