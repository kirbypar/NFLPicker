
import pandas as pd
import operator
import math

def getCurrentData(AFC, NFC):
    """Receives a dataframe of AFC and NFC teams and some simple data, returns dictionary with
    TeamNames as keys and pointDifferential/gamesPlayed as values"""
    data = {}
    i = 0
    for index, row in AFC.iterrows():
        if (i == 0):
            i = 4
        else:
            i -= 1
            data[row['Tm']] = float(row['PD']) / (float(row['W']) + float(row['L']) +float(row['T']))
            # saves the (Point Differential)/(games played)

    for index, row in NFC.iterrows():
        if (i == 0):
            i = 4
        else:
            i -= 1
            data[row['Tm']] = float(row['PD']) / (float(row['W']) + float(row['L']) +float(row['T']))
    return data


def getCurrWeek(schedule):
    """Receives dataframe of the nfl schedule and returns the current week in the season"""
    currWeek = ""
    for index, row in schedule.iterrows():
        if isinstance(row['TOW'], float):
            currWeek = row['Week']
            break
    return currWeek


def getGames(schedule, currWeek):
    """Receives dataframe of the nfl schedule and the current week, returns a list containing tuples of matchups
    for the upcoming week"""
    games = []
    for index, row in schedule.iterrows():
        if row['Week'] == currWeek:
            games.append((row['Winner/tie'], row['Loser/tie']))
    return games


def getPredictions(games, data):
    """Receives list of games and dictionary returned from 'getCurrentData' and returns a list of tuples containing
    a value and the team with the higher value. The higher the value, the better choice for the week"""
    predictions = []
    for game in games:
        score = (float(data[game[0]]) - float(data[game[1]]))
        if score > 0:
            predictions.append((score, game[0]))
        elif score < 0:
            predictions.append((abs(score), game[1]))
        else:
            predictions.append((score, game[0], game[1]))
    predictions.sort(key=operator.itemgetter(0), reverse=True)
    return predictions

teams = 'https://www.pro-football-reference.com/years/2020/'
schedule = 'https://www.pro-football-reference.com/years/2020/games.htm'
AFC = pd.read_html(teams)[0]
NFC = pd.read_html(teams)[1]
schedule = pd.read_html(schedule)[0]

differentials = getCurrentData(AFC, NFC)

currWeek = getCurrWeek(schedule)

games = getGames(schedule, currWeek)

predictions = getPredictions(games, differentials)

for prediction in predictions:
    print(prediction)


