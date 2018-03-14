import re
from constants import BASE_URL, OPPONENT_MAP


def schedule_url(school):
    return '%s/schools/%s/2018-schedule.html' % (BASE_URL, school)


def schedule_file_path(school):
    return 'schedules/%s-schedule.csv' % (school)


def roster_url(school):
    return '%s/schools/%s/2018.html' % (BASE_URL, school)


def roster_file_path(school):
    return 'rosters/%s-roster.csv' % (school)


def boxscore_url(school, dt, tm):
    return '%s/boxscores/%s-%s-%s.html' % (BASE_URL, dt, tm, school)


def boxscore_file_path(school, dt, tm):
    return 'boxscores/%s-%s-%s-boxscore.csv' % (school, dt, tm)


def boxscore_file_path_alt(school, dt):
    return 'boxscores/%s-%s-boxscore.csv' % (school, dt)


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
