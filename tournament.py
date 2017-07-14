# TAFELVOETBAL COMPETITIE - ANGRY BIRDS KPN
# Jules Roovers, July 2017
# Enjoy!

import random
import itertools
import pandas as pd

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

    return sorted_schedule


def new_round(schema):
    team_one = []
    team_two = []


    for i in range(2):
       for f in (random.choice(schema)):
            if i == 0:
                team_one.append(players_df.loc[f, 'Spelers'])
            else:
                team_two.append(players_df.loc[f, 'Spelers'])

    if any(map(lambda v: v in team_one, team_two)):
        return new_round(schedule(players))

    x = [team_one, team_two]

    return x


def match(schema):
    play = "n"

    one = schema[0]
    two = schema[1]

    print "De volgende teams spelen tegen elkaar: \n "
    print "Team 1: " + str(one)
    print "Team 2: " + str(two)

    while play == "n":
        input_play = (raw_input("Met deze teams spelen? (Y/N) \n")).lower()

        if input_play == "n":
            play = match(new_round(schedule(players)))
        elif input_play == "y":
            play = "y"
            match_df.loc[one[0], 'Aantal gespeeld'] += 1
            match_df.loc[one[1], 'Aantal gespeeld'] += 1
            match_df.loc[two[0], 'Aantal gespeeld'] += 1
            match_df.loc[two[1], 'Aantal gespeeld'] += 1

            match_df.to_csv('data.csv', sep = ';')

            break
        else:
            play = "n"
            print "Geen geldig antwoord. Gebruik Y of N.\n"


    x = [one, two]

    return x


def play(teams):
    # for player in teams:
    #    games_played[player] += 1

    one = teams[0]
    two = teams[1]

    winner = "n"

    while winner == "n":
        input_winner = (raw_input("Welk team heeft gewonnen? (1/2) \n")).lower()

        if input_winner == "1":
            print('De winnaars zijn ' + str(one[0]) + ' en ' + str(one[1]) + '!')
            winner = "y"
            match_df.loc[one[0], 'Aantal gewonnen'] += 1
            match_df.loc[one[1], 'Aantal gewonnen'] += 1
        elif input_winner == "2":
            print('De winnaars zijn ' + str(two[0]) + ' en ' + str(two[1]) + '!')
            winner ="y"
            match_df.loc[two[0], 'Aantal gewonnen'] += 1
            match_df.loc[two[1], 'Aantal gewonnen'] += 1
        else:
            winner = "n"
            print "Geen geldig antwoord. Gebruik 1 of 2.\n"

    match_df.to_csv('data.csv', sep=';')

def setup():
    players = ["Harry",
                "Wing",
                "Vincent",
                "Stephan",
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

    print('Setup complete!')


# Set round number

round_number = 1

print "TAFEL COMPETITIE 2017 - ANGRY BIRDS KPN"
print "RONDE " + str(round_number) + "\n"

players_df = pd.read_csv('data.csv', sep=';', index_col='ID')
match_df = pd.read_csv('data.csv', sep=';', index_col='Spelers')

players = players_df['Spelers'].values.tolist()


play(match(new_round(schedule(players))))













