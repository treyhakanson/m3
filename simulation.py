import sys
# import glob
import pandas as pd
from dateutil.parser import parse
from datetime import datetime
import utils

pd.set_option('display.width', 1000)

try:
    school1 = sys.argv[1]
    school2 = sys.argv[2]
except Exception as e:
    print('Must give 2 teams to simulate')
    exit()

print('%s vs %s' % (school1.upper(), school2.upper()), '\n')


def height_to_inches(h):
    ft, inches = map(lambda x: int(x), h.split('-'))
    return ft * 12 + inches


def clean_year(yr):
    yr = str(yr)
    if 'FR' in yr:
        return 1.0
    elif 'SO' in yr:
        return 2.0
    elif 'JR' in yr:
        return 3.0
    elif 'SR' in yr:
        return 4.0
    else:
        return 0.0


def adjust_date_time(row):
    dt = parse(row['Date'])
    dt = '%d-%02d-%02d' % (dt.year, dt.month, dt.day)
    tm = '%02d' % (datetime.strptime(row['Time'], '%I:%M %p/est').time().hour)
    return '%s-%s' % (dt, tm)


def load_roster(fname):
    roster = pd.read_csv(fname)
    roster['Height'] = roster['Height'].apply(height_to_inches)
    roster.dropna(subset=['PPG', 'RPG', 'APG', 'Number'], inplace=True)
    roster['PPG'] = roster['PPG'].apply(lambda x: str(x).replace(' Pts', ''))
    roster['RPG'] = roster['RPG'].apply(lambda x: str(x).replace(' Reb', ''))
    roster['APG'] = roster['APG'].apply(lambda x: str(x).replace(' Ast', ''))
    roster['Number'] = roster['Number'].apply(lambda x: int(x))
    roster['Year'] = roster['Year'].apply(clean_year)
    year_col = roster[roster['Year'] > 0]['Year']
    avg_year = round(year_col.sum() / len(year_col), 1)
    roster['Year'] = roster['Year'].replace([0.0], avg_year)
    roster = roster.drop('High School', axis=1)
    roster = roster.drop('Hometown', axis=1)
    roster = roster.drop('Unnamed: 0', axis=1)
    return roster


def load_scheulde(fname):
    schedule = pd.read_csv(fname)
    schedule = schedule.drop('Unnamed: 0', axis=1)
    schedule = schedule.drop('Network', axis=1)
    schedule = schedule.drop('Type', axis=1)
    schedule = schedule.drop('Conference', axis=1)
    schedule = schedule.drop('Home/Away', axis=1)
    schedule = schedule.drop('OT', axis=1)
    schedule = schedule.drop('Opponent Wins', axis=1)
    schedule = schedule.drop('Opponent Losses', axis=1)
    schedule = schedule.drop('Streak', axis=1)
    schedule = schedule.drop('Arena', axis=1)
    schedule['Date'] = schedule[['Date', 'Time']]\
        .apply(adjust_date_time, axis=1)
    schedule = schedule.drop('Time', axis=1)
    schedule['Opponent'] = schedule['Opponent']\
        .apply(utils.clean_opponent_name)
    schedule.dropna(inplace=True)
    schedule['Outcome'] = schedule['Outcome'].apply(lambda x: int(x == 'W'))
    schedule['Team Points'] = schedule['Team Points'].apply(lambda x: int(x))
    schedule['Opponent Points'] = schedule['Opponent Points']\
        .apply(lambda x: int(x))
    return schedule


def load_boxscore(fname):
    boxscore = pd.read_csv(fname)
    boxscore = boxscore[boxscore['MP'] > 5]
    boxscore = boxscore.drop('Unnamed: 0', axis=1)
    boxscore = boxscore.drop('FG%', axis=1)
    boxscore = boxscore.drop('2P%', axis=1)
    boxscore = boxscore.drop('3P%', axis=1)
    boxscore = boxscore.drop('FT%', axis=1)
    boxscore = boxscore.drop('TRB', axis=1)
    return boxscore


school_roster = load_roster(utils.roster_file_path(school1))
school_schedule = load_scheulde(utils.schedule_file_path(school1))

for i, game in school_schedule.iterrows():
    fname_school = utils.boxscore_file_path_alt(school1, game['Date'])
    fname_opponent = utils.boxscore_file_path_alt(game['Opponent'],
                                                  game['Date'])
    boxscore_school = load_boxscore(fname_school)
    boxscore_opponent = load_boxscore(fname_school)
