import sys
import pandas as pd
import utils
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa F401
import numpy as np

pd.set_option('display.width', 1000)
print('Computing data...')

school = sys.argv[1]
stat = sys.argv[2]
pnames = sys.argv[3:]

school_roster = utils.load_roster(utils.roster_file_path(school))
school_schedule = utils.load_scheulde(utils.schedule_file_path(school))

stats = {}
weights = []
heights = []

for i, game in school_schedule.iterrows():
    school_boxscore = utils.load_boxscore(
        utils.boxscore_file_path_alt(school, game['Date']))
    opponent_boxscore = utils.load_boxscore(
        utils.boxscore_file_path_alt(game['Opponent'], game['Date']))
    opponent_roster = utils.load_roster(
        utils.roster_file_path(game['Opponent']))
    weight, height = utils.physiology(opponent_roster, opponent_boxscore)
    weights.append(weight)
    heights.append(height)
    for i, player in school_boxscore.iterrows():
        a = stats[player['Name']] if player['Name'] in stats else []
        a.append(player[stat.upper()])
        stats[player['Name']] = a

for pname in pnames:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(
        np.asarray(heights),
        np.asarray(weights),
        zs=np.asarray(stats[pname])
    )
    ax.set_xlabel('Height')
    ax.set_ylabel('Weight')
    ax.set_zlabel(stat.upper())
    plt.title('%s (%s)' % (pname, school.upper()))
    plt.show()
