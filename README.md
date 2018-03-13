# March Madness 2018 Data Crawl

This repo contains the following data, as well as the script to scrape said data:

1. `/rosters`: Rosters for every team in the tournament, as well as rosters for each of their regular season (and conference tournament) opponents.
2. `/schedules`: Schedules for each team in the tournament
3. `/boxscores`: Boxscores from every regular season (and conference tournament) game played by each of the tournament teams

To run the crawler, perform the following:

```sh
pip3 install -r requirements.txt  # install the required packages
python3 crawler.py                # run the crawler
```

The crawler will saved failed attempts in a corresponding log file. Certain parts of the pipeline can be skipped by changing the `PIPELINE` variable. For example, if boxscores are not desired, comment out `'boxscores'`.
