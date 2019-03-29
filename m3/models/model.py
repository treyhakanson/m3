import csv, os
from random import uniform
from collections import OrderedDict
import pandas as pd

class Model:
    '''
    Base class for building machine learning models to evaluate on March Madness training set.

    Extend this model and implement train and predict :)
    '''

    def __init__(self):
        self.model_name = "model"

    def train(self):
        pass

    def predict(self, team, opponent):
        '''
        Given two teams, output the probability team beats opponent.
        Output: float (0 <= output <= 1) representing probability.
        Or if probabillity is not supported, return 1 if team is winner and 0 otherwise.
        '''
        return 0.5

    def test(self):
        results = self._generate_march_madness_results(random=True, rounds=6)
        self._evaluate_march_madness_results(results, rounds=2)

    def _generate_march_madness_results(self, random=True, rounds=6):
        '''
        Based on the current model, test on the March Madness 2019 results.

        If random=False, will pick team with >= 0.5 probability to win.
        If random=True, will use probability specified by test_result to randomize winner.

        rounds is the number of rounds to predict (1 = Round of 32, 6 = Full tournament)

        Generates output in output folder in root.
        '''
        matchups = {
            "east": pd.read_csv('./matchups/east-matchups.round1.csv'),
            "west": pd.read_csv('./matchups/west-matchups.round1.csv'),
            "south": pd.read_csv('./matchups/south-matchups.round1.csv'),
            "midwest": pd.read_csv('./matchups/midwest-matchups.round1.csv')
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
                            team = matchup["Predicted Winning School"]
                            opponent = next_matchup["Predicted Winning School"]
                            self._add_prediction(predictions, region, round, team, opponent, random)
                        elif (matchup["Round"] >= round):
                            break


        if (rounds >= 5):
            east_winner = predictions["east"][-1]["Predicted Winning School"]
            west_winner = predictions["west"][-1]["Predicted Winning School"]
            south_winner = predictions["south"][-1]["Predicted Winning School"]
            midwest_winner = predictions["midwest"][-1]["Predicted Winning School"]

            east_west_winner = self._add_prediction(predictions, "final-four", 5, east_winner, west_winner, random)
            south_midwest_winner = self._add_prediction(predictions, "final-four", 5, south_winner, midwest_winner, random)

            if (rounds >= 6):
                self._add_prediction(predictions, "final-four", 6, east_west_winner, south_midwest_winner, random)

        self._export_predictions(predictions, random)
        return predictions


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
            "Predicted Winning School": winning_team
        }))

        return winning_team

    def _export_predictions(self, predictions, random):
        '''
        Export predictions to output folder.
        '''
        for region in predictions:
            if (random):
                file_name = "./output/" + region + "-prediction-r.csv"
            else:
                file_name = "./output/" + region + "-predictions.csv"

            if not os.path.exists("./output"):
                os.makedirs("./output")

            with open(file_name, 'w') as output:
                fp = csv.DictWriter(output, predictions[region][0].keys())
                fp.writeheader()
                fp.writerows(predictions[region])

    def _evaluate_march_madness_results(self, results, rounds=2):
        '''
        Given March Madness prediction vector, evaluate it against the true results,
        printing matchups and final accuracy.

        Scoring methods are
        - ESPN: 10*round*correct_winner_choice
            http://fantasy.espn.com/tournament-challenge-bracket/2019/en/story?pageName=tcmen\howtoplay
        - PERCENT: float rerpresenting % winners guessed correctly (0 to 1)

        rounds is the number of rounds to assess (1 to 6), using 2 since that's all we have now.
        '''
        expected = {
            "east": pd.read_csv('./results/east-results.csv'),
            "midwest": pd.read_csv('./results/midwest-results.csv'),
            "south": pd.read_csv('./results/south-results.csv'),
            "west": pd.read_csv('./results/west-results.csv'),
            "final-four": pd.read_csv('./results/final-four-results.csv')
        }
        if (rounds < 5):
            del expected["final-four"]

        espn_score = 0
        total_correct = 0
        total_games = 0

        print("{:<1} {:<22} {:<22} {:<22} {:<8}".format("", "Team 1", "Team 2", "Predicted Winner", "Correct"))

        for region in expected:
            i = 0
            print("---" + region + "---")
            for matchup in results[region]:
                round = matchup["Round"]
                if (round <= rounds):
                    team = matchup["School 1 Name"]
                    opponent = matchup["School 2 Name"]

                    predicted = matchup["Predicted Winning School"]
                    winner = expected[region].iloc[i,:]["Winning School"]
                    correct = winner == predicted
                    total_games += 1

                    if (correct):
                        total_correct += 1
                        espn_score += 10 * (2 ** (round - 1))

                    correct_string = 'Y' if correct else ''
                    print("{:<1} {:<22} {:<22} {:<22} {:^8}".format(round, team, opponent, predicted, correct_string))

                else:
                    break
                i += 1

        print("--- Final result ---")
        print("ESPN Score: {}".format(espn_score))
        print("Correct: {} / {} - {:.4f}".format(total_correct, total_games, total_correct / total_games))

        return 1

if __name__ == '__main__':
    model = Model()
    model.train()
    model.test()
