from sklearn import linear_model
import warnings
from contextlib import contextmanager
import sys
import os
import utils

warnings.filterwarnings(action="ignore", module="scipy",
                        message="^internal gelsd")


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


school1 = sys.argv[1]
school2 = sys.argv[2]

print('Computing projected winner of %s vs %s...'
      % (school1.upper(), school2.upper()))

with suppress_stdout():
    school1_schedule = utils.load_scheulde(utils.schedule_file_path(school1))
    school1_pts = school1_schedule['Team Points'].values
    school2_schedule = utils.load_scheulde(utils.schedule_file_path(school2))
    school2_pts = school2_schedule['Team Points'].values

    school1_avg_w, school1_avg_h = utils.avg_physiology(school1)
    school2_avg_w, school2_avg_h = utils.avg_physiology(school2)

    _, school1_ws, school1_hs = utils.compute_stats(school1)
    _, school2_ws, school2_hs = utils.compute_stats(school2)

    school1_clf = linear_model.LinearRegression()
    school2_clf = linear_model.LinearRegression()

school1_clf.fit([
    [school1_ws[i], school1_hs[i]] for i in range(len(school1_pts))
], school1_pts)
school2_clf.fit([
    [school2_ws[i], school2_hs[i]] for i in range(len(school2_pts))
], school2_pts)

p1 = school1_clf.predict([[school2_avg_w, school2_avg_h]])
p2 = school2_clf.predict([[school1_avg_w, school1_avg_h]])

print('%d - %d, %s projected to win'
      % (p1, p2, school1.upper() if p1 > p2 else school2.upper()))
