# March Madness 2018 Data Crawl

## Overview

This repo contains the following data, as well as the script to scrape said data:

1. `/rosters`: Rosters for every team in the tournament, as well as rosters for each of their regular season (and conference tournament) opponents.
2. `/schedules`: Schedules for each team in the tournament
3. `/boxscores`: Boxscores from every regular season (and conference tournament) game played by each of the tournament teams
4. `/misc-data`: Some additional miscellaneous data files I found on SR CBB I thought were worth including

Note that some rosters are unavailable for lower-tier teams (from schedules, the roster's of all teams in the tournament are available).

## Setup

To run the crawler, perform the following:

```sh
pip3 install -r requirements.txt  # install the required packages
python3 crawler.py                # run the crawler
```

The crawler will saved failed attempts in a corresponding log file. Certain parts of the pipeline can be skipped by changing the `PIPELINE` variable. For example, if boxscores are not desired, comment out `'boxscores'`.

## Naming Convention

Rosters are named `<team_name>-roster.csv` with `<team_name>` is the name used by [Sports Reference CBB](https://www.sports-reference.com/cbb/)

Schedules are named similarly: `<team_name>-schedule.csv`

Box scores are done a bit differently: `<date_played>-<team_name>-boxscore.csv`, where `<date_played>` is an ISO-like date of the format `YYYY-MM-DD-HH` (the format used in SR CBB's urls).
