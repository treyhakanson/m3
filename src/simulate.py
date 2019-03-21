from sklearn import linear_model
import warnings
from contextlib import contextmanager
import sys
import os
import pandas as pd
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


def project_matchup(school1, school2):
    print('Computing projected winner of %s vs %s...'
          % (school1.upper(), school2.upper()))

    try:
        with suppress_stdout():
            school1_schedule = utils.load_schedule(
                utils.schedule_file_path(school1))
            school1_pts = school1_schedule['Team Points'].values
            school1_def = school1_schedule['Opponent Points'].values

            school2_schedule = utils.load_schedule(
                utils.schedule_file_path(school2))
            school2_pts = school2_schedule['Team Points'].values
            school2_def = school2_schedule['Opponent Points'].values

            school1_avg_w, school1_avg_h = utils.avg_physiology(school1)
            school2_avg_w, school2_avg_h = utils.avg_physiology(school2)

            _, school1_ws, school1_hs = utils.compute_stats(school1)
            _, school2_ws, school2_hs = utils.compute_stats(school2)

        school1_pts_clf = linear_model.LinearRegression()
        school2_pts_clf = linear_model.LinearRegression()

        school1_pts_clf.fit([
            [school1_ws[i], school1_hs[i]] for i in range(len(school1_pts))
        ], school1_pts)
        school2_pts_clf.fit([
            [school2_ws[i], school2_hs[i]] for i in range(len(school2_pts))
        ], school2_pts)

        school1_def_clf = linear_model.LinearRegression()
        school2_def_clf = linear_model.LinearRegression()

        school1_def_clf.fit([
            [school1_ws[i], school1_hs[i]] for i in range(len(school1_def))
        ], school1_def)
        school2_def_clf.fit([
            [school2_ws[i], school2_hs[i]] for i in range(len(school2_def))
        ], school2_def)

        p1 = school1_pts_clf.predict([[school2_avg_w, school2_avg_h]])
        p2 = school2_pts_clf.predict([[school1_avg_w, school1_avg_h]])

        def1 = school1_def_clf.predict([[school2_avg_w, school2_avg_h]])
        def2 = school2_def_clf.predict([[school1_avg_w, school1_avg_h]])

        pts1 = (p1 + def2) / 2.0
        pts2 = (p2 + def1) / 2.0

        if int(pts1) != int(pts2):
            print('%d - %d, %s projected to win'
                  % (pts1, pts2, school1.upper() if pts1 > pts2
                     else school2.upper()))
        else:
            print('%d - %d TIE, computing tiebreaker...' % (pts1, pts2))
            print('%s projected to win'
                  % (school1.upper() if school1_avg_w / school1_avg_h
                     > school2_avg_w / school2_avg_h else school2.upper()))

    except Exception as e:
        print('Failed to get projection with error:', e)
        raise e
        return


if len(sys.argv) == 2:
    matchups = pd.read_csv(sys.argv[1])
    for i, matchup in matchups.iterrows():
        project_matchup(matchup['School 1 Name'], matchup['School 2 Name'])
else:
    project_matchup(sys.argv[1], sys.argv[2])
