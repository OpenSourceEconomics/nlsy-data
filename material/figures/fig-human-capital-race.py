import matplotlib.pyplot as plt
import seaborn.apionly as sns

from auxiliary import get_dataset

df = get_dataset()


# We look at racial differences in cognitive scores.
fig, ax = plt.subplots()

for group in ['white', 'black', 'hispanic']:
    dat = df[df['RACE_NEW'] == group].loc[(slice(None), 1978), 'AFQT_RAW'].dropna()
    sns.distplot(dat, label=group.capitalize())

ax.yaxis.get_major_ticks()[0].set_visible(False)
plt.xlim([0, 120])
plt.legend()
plt.xlabel('AFQT Scores')
plt.savefig('fig-human-capital-race-afqt.png')


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
    plt.savefig('fig-human-capital-race-' + score.lower() + '.png')

