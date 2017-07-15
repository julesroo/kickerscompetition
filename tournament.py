# TAFELVOETBAL COMPETITIE - ANGRY BIRDS KPN
# Jules Roovers, July 2017
# Enjoy!

import random
import pandas as pd
import csv
import linecache


def new_round():
    with open('matches.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        data = list(reader)
        row_count = len(data)
        offset = random.randrange(2, row_count)
        random_line = linecache.getline("matches.csv", offset)

        random_line_strip = random_line.rstrip()

        items = random_line_strip.split(';')
        team_one = list(items[4])
        t1 = [x for x in team_one if x != ',']
        t1_int = []
        team_two = list(items[5])
        t2 = [x for x in team_two if x != ',']
        t2_int = []

        for item in t1:
            t1_int.append(int(item))

        for item in t2:
            t2_int.append(int(item))

    if items[1] == 1:
        return new_round()

    x = [t1_int, t2_int]

    return x


def match(schema):
    play = "n"

    one = schema[0]
    two = schema[1]

    t1 = str(schema[0])
    t1_str = t1.translate(None, " []")
    t2 = str(schema[1])
    t2_str = t2.translate(None, " []")

    team_one = []
    team_two = []

    for i in one:
        team_one.append(players_df.loc[int(i), 'Spelers'])
    for p in two:
        team_two.append(players_df.loc[int(p), 'Spelers'])

    print "De volgende teams spelen tegen elkaar: \n "
    print "Team 1: " + str(team_one)
    print "Team 2: " + str(team_two)

    while play == "n":
        input_play = (raw_input("Met deze teams spelen? (Y/N) \n")).lower()

        if input_play == "n":
            play = match(new_round())
        elif input_play == "y":
            play = "y"
            match_df.loc[team_one[0], 'Aantal gespeeld'] += 1
            match_df.loc[team_one[1], 'Aantal gespeeld'] += 1
            match_df.loc[team_two[0], 'Aantal gespeeld'] += 1
            match_df.loc[team_two[1], 'Aantal gespeeld'] += 1

            match_df.to_csv('data.csv', sep=';')

            played_df.loc[(played_df['Team_one'].str.contains(t1_str) == True) & (
                played_df['Team_two'].str.contains(t2_str) == True), 'Gespeeld'] += 1
            played_df.to_csv('matches.csv', sep=';', index=None)

            break
        else:
            play = "n"
            print "Geen geldig antwoord. Gebruik Y of N.\n"

    x = [one, two]

    return x


def play(teams):

    one = teams[0]
    two = teams[1]

    t1 = str(teams[0])
    t1_str = t1.translate(None, " []")
    t2 = str(teams[1])
    t2_str = t2.translate(None, " []")

    team_one = []
    team_two = []

    for i in one:
        team_one.append(players_df.loc[int(i), 'Spelers'])
    for p in two:
        team_two.append(players_df.loc[int(p), 'Spelers'])

    winner = "n"

    while winner == "n":
        input_winner = (raw_input("Welk team heeft gewonnen? (1/2) \n")).lower()

        if input_winner == "1":
            print('De winnaars zijn ' + str(team_one[0]) + ' en ' + str(team_one[1]) + '!')
            winner = "y"
            match_df.loc[team_one[0], 'Aantal gewonnen'] += 1
            match_df.loc[team_one[1], 'Aantal gewonnen'] += 1

            played_df.loc[(played_df['Team_one'].str.contains(t1_str) == True) & (
                played_df['Team_two'].str.contains(t2_str) == True), 'Gewonnen_one'] += 1
            played_df.to_csv('matches.csv', sep=';', index=None)

        elif input_winner == "2":
            print('De winnaars zijn ' + str(two[0]) + ' en ' + str(two[1]) + '!')
            winner = "y"
            match_df.loc[team_two[0], 'Aantal gewonnen'] += 1
            match_df.loc[team_two[1], 'Aantal gewonnen'] += 1

            played_df.loc[(played_df['Team_one'].str.contains(t1_str) == True) & (
                played_df['Team_two'].str.contains(t2_str) == True), 'Gewonnen_two'] += 1
            played_df.to_csv('matches.csv', sep=';', index=None)

        else:
            winner = "n"
            print "Geen geldig antwoord. Gebruik 1 of 2.\n"

    match_df.to_csv('data.csv', sep=';')


print ("--------------------------------------- \n")
print ("TAFELVOETBAL COMPETITIE 2017 - ANGRY BIRDS KPN \n")
print ("--------------------------------------- \n")

match_df = pd.read_csv('data.csv', sep=';', index_col='Spelers')
players_df = pd.read_csv('data.csv', sep=';', index_col='ID')
played_df = pd.read_csv('matches.csv', sep=';')

play(match(new_round()))

match_df_sel = match_df[['Aantal gespeeld', 'Aantal gewonnen']]

print(match_df_sel.sort_values('Aantal gewonnen', ascending=False))
