import sys
import pandas as pd
from dateutil.parser import parse
from datetime import datetime
import utils
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa F401
import numpy as np

pd.set_option('display.width', 1000)

school = sys.argv[1]
stat = sys.argv[2]
pnames = sys.argv[3:]

print('Computing data...')


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
    # weight /= len(boxscore)
    # height /= len(boxscore)
    return (weight, height)


school_roster = load_roster(utils.roster_file_path(school))
school_schedule = load_scheulde(utils.schedule_file_path(school))

stats = {}
weights = []
heights = []

for i, game in school_schedule.iterrows():
    school_boxscore = load_boxscore(
        utils.boxscore_file_path_alt(school, game['Date']))
    opponent_boxscore = load_boxscore(
        utils.boxscore_file_path_alt(game['Opponent'], game['Date']))
    opponent_roster = load_roster(utils.roster_file_path(game['Opponent']))
    weight, height = physiology(opponent_roster, opponent_boxscore)
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
