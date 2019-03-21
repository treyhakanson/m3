import re
from constants import BASE_URL, OPPONENT_MAP, YEAR
import pandas as pd
from dateutil.parser import parse
from datetime import datetime
import math


def schedule_url(school):
    return '%s/schools/%s/%s-schedule.html' % (BASE_URL, school, YEAR)


def schedule_file_path(school):
    return '../schedules/%s-schedule.csv' % (school)


def roster_url(school):
    return '%s/schools/%s/%s.html' % (BASE_URL, school, YEAR)


def roster_file_path(school):
    return '../rosters/%s-roster.csv' % (school)


def boxscore_url(school, dt, tm):
    return '%s/boxscores/%s-%s-%s.html' % (BASE_URL, dt, tm, school)


def boxscore_file_path(school, dt, tm):
    return '../boxscores/%s-%s-%s-boxscore.csv' % (school, dt, tm)


def boxscore_file_path_alt(school, dt):
    return '../boxscores/%s-%s-boxscore.csv' % (school, dt)


def clean_opponent_name(name):
    name = gentle_clean_opponent_name(name)

    # Map the opponent's team name if necessary; some names are different
    # than anticipated
    return OPPONENT_MAP[name] if name in OPPONENT_MAP else name


def gentle_clean_opponent_name(name):
    name = re.sub(r'\s*\(\d+\)', '', name)       # Remove ranking
    name = re.sub(r'[^a-zA-Z0-9_ -]', '', name)  # Remove special characters
    name = re.sub(r'[\s-]+', '-', name)          # Spaces -> hyphens
    name = name.lower()                          # Lowercase string
    return name


def height_to_inches(h):
    try:
        ft, inches = map(lambda x: int(x), h.split('-'))
        return ft * 12 + inches
    except Exception as e:
        return h


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
    tm = '%02d' % (datetime.strptime(row['Time'] + 'm', '%I:%M%p').time().hour)
    return '%s-%s' % (dt, tm)


def clean_name(name):
    return " ".join(sorted(re.sub(r"(Jr\.?|Sr\.?|III)", "", name).strip().split(" ")))


def load_roster(fname):
    try:
        roster = pd.read_csv(fname)
    except Exception as e:
        # Use Chicago State's roster if the team cannot be found. Assuming that
        # if a team's roster is unavailable, they are terrible, and Chicago
        # State is the worst team whose roster is available
        roster = pd.read_csv(roster_file_path('chicago-state'))
    roster['Name'] = roster['Name'].apply(clean_name)
    roster['Height'] = roster['Height'].apply(height_to_inches)
    roster['Height'] = roster['Height'].fillna(roster['Height'].mean())
    roster['Weight'] = roster['Weight'].fillna(roster['Weight'].mean())
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
    roster.reset_index()
    return roster


def load_schedule(fname):
    schedule = pd.read_csv(fname)
    schedule = schedule.drop('Unnamed: 0', axis=1)
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
        .apply(clean_opponent_name)
    schedule.dropna(inplace=True)
    schedule['Outcome'] = schedule['Outcome'].apply(lambda x: int(x == 'W'))
    schedule['Team Points'] = schedule['Team Points'].apply(lambda x: int(x))
    schedule['Opponent Points'] = schedule['Opponent Points']\
        .apply(lambda x: int(x))
    schedule.reset_index()
    return schedule


def load_boxscore(fname):
    boxscore = pd.read_csv(fname)
    boxscore['Name'] = boxscore['Name'].apply(clean_name)
    boxscore = boxscore.drop('Unnamed: 0', axis=1)
    boxscore = boxscore.drop('FG%', axis=1)
    boxscore = boxscore.drop('2P%', axis=1)
    boxscore = boxscore.drop('3P%', axis=1)
    boxscore = boxscore.drop('FT%', axis=1)
    boxscore = boxscore.drop('TRB', axis=1)
    return boxscore


def physiology(roster, boxscore):
    '''
    height/weight factor based on percentage of total game time occupied by
    different players across all positions
    '''
    total_mins = 200.0
    weight = 0.0
    height = 0.0
    avg_height = roster['Height'].sum() / len(roster)
    avg_weight = roster['Weight'].sum() / len(roster)
    for i, player_stats in boxscore.iterrows():
        mp = player_stats['MP']
        try:
            player_info = roster[roster['Name'].str.startswith(
                ' '.join(player_stats['Name'].split(' ')[0:2]))]
            weight += mp / total_mins * player_info['Weight'].values[0]
            height += mp / total_mins * player_info['Height'].values[0]
        except Exception as e:
            print('Player %s was not in roster. Using averages: %d lbs, %d in'
                  % (' '.join(player_stats['Name'].split(' ')[0:2]), weight,
                     height))
            weight += mp / total_mins * avg_weight
            height += mp / total_mins * avg_height
    if math.isnan(weight):
        weight = 195
    if math.isnan(height):
        height = 77
    return (weight, height)


def avg_physiology(school):
    avg_weight = 0.0
    avg_height = 0.0
    roster = load_roster(roster_file_path(school))
    schedule = load_schedule(schedule_file_path(school))
    for i, game in schedule.iterrows():
        boxscore = load_boxscore(boxscore_file_path_alt(school, game['Date']))
        weight, height = physiology(roster, boxscore)
        avg_weight += weight
        avg_height += height
    avg_weight /= len(schedule)
    avg_height /= len(schedule)
    return (avg_weight, avg_height)


def compute_stats(school, stat='PTS'):
    '''TODO: need to skip teams if the roster doesn't exist'''
    points = {}
    weights = []
    heights = []

    schedule = load_schedule(schedule_file_path(school))

    print('Computing data for team %s...' % (school.upper()))

    for i, game in schedule.iterrows():
        school_boxscore = load_boxscore(
            boxscore_file_path_alt(school, game['Date']))
        opponent_boxscore = load_boxscore(
            boxscore_file_path_alt(game['Opponent'], game['Date']))
        opponent_roster = load_roster(
            roster_file_path(game['Opponent']))
        weight, height = physiology(opponent_roster, opponent_boxscore)
        weights.append(weight)
        heights.append(height)
        for i, player in school_boxscore.iterrows():
            a = points[player['Name']] if player['Name'] in points else []
            a.append(player[stat.upper()])
            points[player['Name']] = a

    return (points, weights, heights)


def join_roster_and_boxscore(rdf, bdf):
    bdf_joined = bdf.set_index("Name").join(rdf.set_index("Name"), on="Name")
    return bdf_joined
