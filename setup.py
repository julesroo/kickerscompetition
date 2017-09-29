# TAFELVOETBAL COMPETITIE - ANGRY BIRDS KPN
# Jules Roovers, July 2017
# Use this file for initial setup


import random
import itertools
import pandas as pd


def setup():
    players = ["Harry",
               "Wing",
               "Vincent",
               "Willem",
               "Hesing",
               "Mathieu",
               "Jules",
               "Gast"]

    idlist = []
    for i in range(0, len(players)):
        idlist.append(i)

    zero = []
    for i in range(0, len(players)):
        zero.append(0)

    dataframe = pd.DataFrame({'ID': idlist,
                              'Spelers': players,
                              'Aantal gespeeld': zero,
                              'Aantal gewonnen': zero})

    df = dataframe[['ID', 'Spelers', 'Aantal gespeeld', 'Aantal gewonnen']]

    print(df)

    df.to_csv('data.csv', index=False, sep=';')


def schedule(players):
    set_size = 2
    schedule = set()
    teams = range(len(players))

    for comb in itertools.product(teams, repeat=set_size):
        comb = sorted(list(comb))
        if len(set(comb)) == set_size:
            schedule.add(tuple(comb))

    schedule = list(schedule)
    random.shuffle(schedule)

    sorted_schedule = []
    for i in schedule:
        sorted_schedule.append(sorted(i))

    team_one = []
    team_two = []
    zero = []


    for subset in itertools.combinations(sorted_schedule, 2):
        if not any(map(lambda v: v in subset[0], subset[1])):
            one = str(subset[0]).translate(None, " []")
            two = str(subset[1]).translate(None, " []")

            team_one.append(one)
            team_two.append(two)


    for i in range(0, len(team_one)):
        zero.append(0)

    subset_df = pd.DataFrame({'Team_one': team_one,
                              'Team_two': team_two,
                              'Gespeeld': zero,
                              'Score_team_one': zero,
                              'Score_team_two': zero,
                              'Gewonnen_one': zero,
                              'Gewonnen_two': zero})
    subset_df.to_csv('matches.csv', sep=';')

    return sorted_schedule


setup()

players_df = pd.read_csv('data.csv', sep=';', index_col='ID')
players = players_df['Spelers'].values.tolist()

schedule(players)

print('Setup complete!')
