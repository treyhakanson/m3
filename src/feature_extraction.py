import os
from pathlib import Path
from argparse import ArgumentParser
import pandas as pd
from constants import SCHOOLS
from utils import (
	load_roster,
	load_schedule,
	load_boxscore,
	roster_file_path,
	schedule_file_path,
	boxscore_file_path_alt,
	join_roster_and_boxscore
)

POSITIONS = [('G', 'G'), ('C', 'F/C'), ('F', 'F/C')]
COLUMNS = [
	'Height',
	'Weight',
	'MP',
	'2P',
	'2PA',
	'3P',
	'3PA',
	'ORB',
	'DRB',
	'FT',
	'FTA',
	'AST',
	'STL',
	'BLK',
	'TOV'
]


def initialize_feature_matrix():
	return pd.DataFrame(
		index={pos[1] for pos in POSITIONS},
		columns=COLUMNS
	).fillna(0.0)


def update_feature_matrix(fdf, bdf_joined):
	for pos, pos_key in POSITIONS:
		df = bdf_joined.loc[bdf_joined['Position'] == pos]
		df = df.drop(['Position'] + list(set(df.columns).difference(fdf.columns)), axis=1)
		df = df.mean(axis=0)
		df = df.fillna(0)
		fdf.add(df)
		fdf.loc[pos_key] = fdf.loc[pos_key].add(df)


def create_parser():
	parser = ArgumentParser()
	parser.add_argument("--schools", type=Path)
	return parser


def main(schools):
	for school in schools:
		print('Creating feature vector for %s...' % school)
		fpath = Path('../feature-vectors/%s.csv' % school)
		if fpath.exists():
			continue
		fdf = initialize_feature_matrix()
		rdf = load_roster(roster_file_path(school))
		sdf = load_schedule(schedule_file_path(school))
		for _, game in sdf.iterrows():
			opp_school = game['Opponent']
			dt = game['Date']
			bdf = load_boxscore(boxscore_file_path_alt(school, dt))
			bdf_joined = join_roster_and_boxscore(rdf, bdf)
			update_feature_matrix(fdf, bdf_joined)
		fdf = fdf / sdf.shape[0]
		fdf.to_csv(fpath)


if __name__ == '__main__':
	parser = create_parser()
	args = parser.parse_args()
	if args.schools:
		with args.schools.open(mode="r") as f:
			schools = [line.strip() for line in f]
	else:
		schools = SCHOOLS
	main(schools)
