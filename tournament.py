# TAFELVOETBAL COMPETITIE - ANGRY BIRDS KPN
# Jules Roovers, July 2017
# Enjoy!

import random
import pandas as pd
import csv
import linecache


def new_round(players):
    t1_int = []
    t2_int = []

    if len(players) == 4:

        if len(lines) == 0:
            with open('matches.csv', 'r') as f:
                reader = csv.reader(f, delimiter=';')
                data = list(reader)
                data = data[1:]

                for x in data:
                    line = int(x[0])
                    played = int(x[1])
                    teams = x[6:8]

                    team_one = [int(x) for x in teams[0] if x != ',']
                    team_two = [int(x) for x in teams[1] if x != ',']
                    teams = team_one + team_two
                    if all(x in teams for x in players):
                        if played == 0:
                            lines.append(line)

        if len(lines) != 0:
            get_line = linecache.getline("matches.csv", lines[0] + 2)
            get_line_strip = get_line.rstrip()

            items = get_line_strip.split(';')
            team_one = list(items[6])
            t1 = [x for x in team_one if x != ',']
            team_two = list(items[7])
            t2 = [x for x in team_two if x != ',']

            for item in t1:
                t1_int.append(int(item))

            for item in t2:
                t2_int.append(int(item))

            team_players = [t1_int, t2_int]

            return team_players



        else:
            print('Deze spelers hebben al in elke mogelijke combinatie gespeeld. Probeer andere spelers.')



    else:
        with open('matches.csv', 'r') as f:
            reader = csv.reader(f, delimiter=';')
            data = list(reader)
            row_count = len(data)
            offset = random.randrange(2, row_count)
            random_line = linecache.getline("matches.csv", offset)

            random_line_strip = random_line.rstrip()

            items = random_line_strip.split(';')
            team_one = list(items[6])
            t1 = [x for x in team_one if x != ',']
            team_two = list(items[7])
            t2 = [x for x in team_two if x != ',']

            for item in t1:
                t1_int.append(int(item))

            for item in t2:
                t2_int.append(int(item))

            team_players = [t1_int, t2_int]

            if items[1] == 1:
                return new_round(list_players)

            return team_players


def match(schema):
    play_game = "n"
    one = schema[0]
    two = schema[1]
    teams = schema

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

    while play_game == "n":
        input_play = (raw_input("Met deze teams spelen? (Y/N) \n")).lower()

        if input_play == "n":
            if len(lines) > 0:
                lines.remove(lines[0])

            teams = match(new_round(list_players))

        elif input_play == "y":

            match_df.loc[team_one[0], 'Aantal gespeeld'] += 1
            match_df.loc[team_one[1], 'Aantal gespeeld'] += 1
            match_df.loc[team_two[0], 'Aantal gespeeld'] += 1
            match_df.loc[team_two[1], 'Aantal gespeeld'] += 1

            match_df.to_csv('data.csv', sep=';')

            played_df.loc[(played_df['Team_one'].str.contains(t1_str) == True) & (
                played_df['Team_two'].str.contains(t2_str) == True), 'Gespeeld'] += 1
            played_df.to_csv('matches.csv', sep=';', index=None)


        else:
            play_game = "n"
            print "Geen geldig antwoord. Gebruik Y of N.\n"

        play_game = "y"

    return teams


def play(teams_playing):
    one = teams_playing[0]
    two = teams_playing[1]

    t1 = str(teams_playing[0])
    t1_str = t1.translate(None, " []")
    t2 = str(teams_playing[1])
    t2_str = t2.translate(None, " []")

    team_one = []
    team_two = []

    for i in one:
        team_one.append(players_df.loc[int(i), 'Spelers'])
    for p in two:
        team_two.append(players_df.loc[int(p), 'Spelers'])

    winner = "n"

    while winner == "n":
        input_team_one = (raw_input("Hoeveel sets heeft Team 1 gewonnen? (Voer getal in)\n")).lower()
        try:
            val = int(input_team_one)
        except ValueError:
            print("Dat is geen getal.")
            winner = "n"

        input_team_two = (raw_input("Hoeveel sets heeft Team 2 gewonnen? (Voer getal in)\n")).lower()
        try:
            val = int(input_team_two)
        except ValueError:
            print("Dat is geen getal.")
            winner = "n"

        if input_team_one > input_team_two:
            input_winner = 1

        else:
            input_winner = 2

        played_df.loc[(played_df['Team_one'].str.contains(t1_str) == True) & (
            played_df['Team_two'].str.contains(t2_str) == True), 'Score_team_one'] = input_team_one

        played_df.loc[(played_df['Team_one'].str.contains(t1_str) == True) & (
            played_df['Team_two'].str.contains(t2_str) == True), 'Score_team_two'] = input_team_two

        if input_winner == 1:
            print('De winnaars zijn ' + str(team_one[0]) + ' en ' + str(team_one[1]) + '!')
            winner = "y"
            match_df.loc[team_one[0], 'Aantal gewonnen'] += 1
            match_df.loc[team_one[1], 'Aantal gewonnen'] += 1

            played_df.loc[(played_df['Team_one'].str.contains(t1_str) == True) & (
                played_df['Team_two'].str.contains(t2_str) == True), 'Gewonnen_one'] += 1
            played_df.to_csv('matches.csv', sep=';', index=None)

        else:
            print('De winnaars zijn ' + str(team_two[0]) + ' en ' + str(team_two[1]) + '!')
            winner = "y"
            match_df.loc[team_two[0], 'Aantal gewonnen'] += 1
            match_df.loc[team_two[1], 'Aantal gewonnen'] += 1

            played_df.loc[(played_df['Team_one'].str.contains(t1_str) == True) & (
                played_df['Team_two'].str.contains(t2_str) == True), 'Gewonnen_two'] += 1
            played_df.to_csv('matches.csv', sep=';', index=None)

    match_df.to_csv('data.csv', sep=';')


print ("--------------------------------------- \n")
print ("TAFELVOETBAL COMPETITIE 2017 - ANGRY BIRDS KPN \n")
print ("--------------------------------------- \n")

lines = []
match_df = pd.read_csv('data.csv', sep=';', index_col='Spelers')
players_df = pd.read_csv('data.csv', sep=';', index_col='ID')
played_df = pd.read_csv('matches.csv', sep=';')

print(players_df)

players = 0
list_players = []

while players == 0:
    input_players = (raw_input(
        "\nMet welke spelers wordt er gespeeld? \nVul de vier ID's in, gescheiden met een komma. \nVoor een willekeurige selectie, voer 0 in:\n")).lower()
    list_players = [int(x) for x in input_players if x != ',']

    if len(list_players) != 0 and len(list_players) != 4:
        if len(list_players) == 1:
            for x in list_players:
                if x == 0:
                    players = 1
                else:
                    print("Ongeldig aantal spelers ingegeven.")


    else:

        players = 1

play(match(new_round(list_players)))

match_df_sel = match_df[['Aantal gespeeld', 'Aantal gewonnen']]

print(match_df_sel.sort_values('Aantal gewonnen', ascending=False))
