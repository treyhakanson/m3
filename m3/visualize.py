import sys
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa F401
import numpy as np

from . import utils

school = sys.argv[1]
stat = sys.argv[2].upper()
pnames = sys.argv[3:]

colors = ['r', 'g', 'b', 'c', 'y', 'm', 'k']
markers = ['o', '*', 'h', 'x', 'D', '+', '^']
patches = []

school_roster = utils.load_roster(utils.roster_file_path(school))
school_schedule = utils.load_schedule(utils.schedule_file_path(school))

stats, heights, weights = utils.compute_stats(school, stat=stat)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, pname in enumerate(pnames):
    color = colors[i % len(colors)]
    marker = markers[i % len(markers)]
    patches.append(mpatches.Patch(color=color, label=pname))
    ax.scatter(np.asarray(heights), np.asarray(weights),
               zs=np.asarray(stats[pname]), c=color, marker=marker)

plt.title('%s Player Stats (%s)' % (school.upper(), stat))
plt.legend(handles=patches, loc=4)

ax.set_xlabel('Height')
ax.set_ylabel('Weight')
ax.set_zlabel(stat)

plt.show()
