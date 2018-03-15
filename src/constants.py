# Base URL
BASE_URL = 'https://www.sports-reference.com/cbb'

# Schools
SCHOOLS = [
    # SOUTH
    'virginia', 'maryland-baltimore-county', 'creighton', 'kansas-state',
    'kentucky', 'davidson', 'arizona', 'buffalo', 'miami-fl', 'loyola-il',
    'tennessee', 'wright-state', 'nevada', 'texas', 'cincinnati',
    'georgia-state',

    # WEST
    'texas-southern', 'north-carolina-central',  # Play in teams
    'xavier', 'missouri', 'florida-state', 'ohio-state', 'south-dakota-state',
    'gonzaga', 'north-carolina-greensboro', 'houston', 'san-diego-state',
    'michigan', 'montana', 'texas-am', 'providence', 'north-carolina',
    'lipscomb',

    # EAST
    'radford', 'long-island-university',  # Play in teams
    'ucla', 'st-bonaventure',             # Play in teams
    'villanova', 'virginia-tech', 'alabama', 'west-virginia', 'murray-state',
    'wichita-state', 'marshall', 'florida', 'texas-tech', 'stephen-f-austin',
    'butler', 'arkansas', 'purdue', 'cal-state-fullerton',

    # MIDWEST
    'syracuse', 'arizona-state',  # Play in teams
    'kansas', 'pennsylvania', 'seton-hall', 'north-carolina-state', 'clemson',
    'new-mexico-state', 'auburn', 'college-of-charleston', 'texas-christian',
    'michigan-state', 'bucknell', 'rhode-island', 'oklahoma', 'duke', 'iona'
]

# Maps opponent names whose cleaned names are not correct
OPPONENT_MAP = {
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
