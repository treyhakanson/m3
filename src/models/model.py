import csv, os
from random import uniform
from collections import OrderedDict
import pandas as pd

class Model:
    '''
    Base class for building machine learning models to evaluate on March Madness training set.
    '''

    def __init__(self):
        self.model_name = "model"

    def train(self):
        pass

    def predict(self, team, opponent):
        '''
        Given two teams, output the probability team beats opponent.
        Output: float (0 <= output <= 1) representing probability.
        '''
        return 0.5

    def test(self):
        results = _generate_march_madness_results()
        _evaluate_march_madness_results(results)

    def _generate_march_madness_results(self, random=False, rounds=6):
        '''
        Based on the current model, test on the March Madness 2019 results.

        If random=False, will pick team with >= 0.5 probability to win.
        If random=True, will use probability specified by test_result to randomize winner.

        rounds is the number of rounds to predict (1 = Round of 32, 6 = Full tournament)

        Generates output in output folder in root.
        '''
        matchups = {
            "east": pd.read_csv('../../matchups/east-matchups.round1.csv'),
            "west": pd.read_csv('../../matchups/west-matchups.round1.csv'),
            "south": pd.read_csv('../../matchups/south-matchups.round1.csv'),
            "midwest": pd.read_csv('../../matchups/midwest-matchups.round1.csv')
        }

        predictions = {
            "east": [],
            "west": [],
            "south": [],
            "midwest": [],
            "final-four": []
        }
        max_region_rounds = max(rounds,4)

        for region in matchups:
            for round in range(1, max_region_rounds):
                if (round == 1):
                    for i, matchup in matchups[region].iterrows():
                        if (round <= rounds):
                            team = matchup["School 1 Name"]
                            opponent = matchup["School 2 Name"]
                            self._add_prediction(predictions, region, 1, team, opponent, random)

                else:
                    for i in range(0, len(predictions[region]) - 1, 2):
                        matchup = predictions[region][i]
                        next_matchup = predictions[region][i+1]
                        if (round-1 == matchup["Round"] == next_matchup["Round"]):
                            team = matchup["Predicted Winning Team"]
                            opponent = next_matchup["Predicted Winning Team"]
                            self._add_prediction(predictions, region, round, team, opponent, random)
                        elif (matchup["Round"] >= round):
                            break


        if (rounds >= 5):
            east_winner = predictions["east"][-1]["Predicted Winning Team"]
            west_winner = predictions["west"][-1]["Predicted Winning Team"]
            south_winner = predictions["south"][-1]["Predicted Winning Team"]
            midwest_winner = predictions["midwest"][-1]["Predicted Winning Team"]

            east_west_winner = self._add_prediction(predictions, "final-four", 5, east_winner, west_winner, random)
            south_midwest_winner = self._add_prediction(predictions, "final-four", 5, south_winner, midwest_winner, random)

            if (rounds >= 6):
                self._add_prediction(predictions, "final-four", 6, east_west_winner, south_midwest_winner, random)

        if __name__ == '__main__':
            import pprint
            pp = pprint.PrettyPrinter(indent=3)
            pp.pprint(predictions)

        self._export_predictions(predictions, random)


    def _add_prediction(self, predictions, region, round, team_name, opponent_name, random):
        '''
        Makes prediction for team and adds it to predictions vector.
        '''
        prediction = self.predict(team_name, opponent_name)

        if (random):
            roll = uniform(0.0,1.0)
            winning_team = team_name if roll <= prediction else opponent_name
        else:
            winning_team = team_name if prediction >= 0.5 else opponent_name

        predictions[region].append(OrderedDict({
            "Round": round,
            "School 1 Name": team_name,
            "School 2 Name": opponent_name,
            "Predicted Winning Team": winning_team
        }))

        return winning_team

    def _export_predictions(self, predictions, random):
        '''
        Export predictions to output folder.
        '''
        for region in predictions:
            if (random):
                file_name = "../../output/" + region + "-randomized-predictions.csv"
            else:
                file_name = "../../output/" + region + "-predictions.csv"

            #pd.DataFrame.from_dict(predictions[region], orient="index").to_csv(file_name)

            if not os.path.exists("../../output"):
                os.makedirs("../../output")

            with open(file_name, 'w') as output:
                fp = csv.DictWriter(output, predictions[region][0].keys())
                fp.writeheader()
                fp.writerows(predictions[region])

    def _evaluate_march_madness_results(self, results, rounds=2):
        '''
        Given March Madness prediction vector, evaluate it against the true results,
        printing matchups and final accuracy.

        Rounds is the number of rounds to assess, using 2 since that's all we have now.
        '''
        expected = {
            "east": pd.read_csv('../../results/east-results.csv'),
            "midwest": pd.read_csv('../../results/midwest-results.csv'),
            "south": pd.read_csv('../../results/south-results.csv'),
            "west": pd.read_csv('../../results/west-results.csv')
        }
        return 1

if __name__ == '__main__':
    model = Model()
    model._generate_march_madness_results(random=True)
