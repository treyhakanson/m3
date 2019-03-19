# Base URL
BASE_URL = 'https://www.sports-reference.com/cbb'

# Year
YEAR = 2019

# Schools
SCHOOLS = [
    # EAST
    'north-carolina-central', 'north-dakota-state', # Play in teams
    'belmont', 'temple', # Play in teams
    'duke', 'virginia-commonwealth', 'central-florida', 'mississippi-state',
    'liberty', 'virginia-tech', 'saint-louis', 'maryland', 'louisiana-state',
    'yale', 'louisville', 'minnesota', 'michigan-state', 'bradley',

    # WEST
    'fairleigh-dickinson', 'prairie-view', # Play in teams
    'arizona-state', 'st-johns-ny', # Play in teams
    'gonzaga', 'syracuse', 'baylor', 'marquette', 'murray-state',
    'florida-state', 'vermont', 'buffalo', 'texas-tech', 'northern-kentucky',
    'nevada', 'florida', 'michigan', 'montana',

    # SOUTH
    'virginia', 'gardner-webb', 'mississippi', 'oklahoma', 'wisconsin',
    'oregon', 'kansas-state', 'california-irvine', 'villanova', 'saint-marys-ca',
    'purdue', 'old-dominion', 'cincinnati', 'iowa', 'tennessee',
    'colgate',

    # MIDWEST
    'north-carolina', 'iona', 'utah-state', 'washington', 'auburn',
    'new-mexico-state', 'kansas', 'northeastern', 'iowa-state',
    'ohio-state', 'houston', 'georgia-state', 'wofford', 'seton-hall',
    'kentucky', 'abilene-christian'
]

# Maps opponent names whose cleaned names are not correct
OPPONENT_MAP = {
    'purdue-fort-wayne': 'ipfw',
    'little-rock': 'arkansas-little-rock',
    'omaha': 'nebraska-omaha',
    'st-johns': 'st-johns-ny',
    'st-marys': 'saint-marys-ca',
    'university-of-california': 'california',
    'uc-irvine': 'california-irvine',
    'uc-davis': 'california-davis',
    'uc-riverside': 'california-riverside',
    'uc-santa-barbara': 'california-santa-barbara',
    'southeastern': 'southeastern-louisiana',
    'louisiana': 'louisiana-lafayette',
    'texas-rio-grande-valley': 'texas-pan-american',
    'point-university': 'point',
    'bethesda-university-ca': 'bethesda-ca',
    'penn-st-brandywine': 'penn-state-brandywine'
}
