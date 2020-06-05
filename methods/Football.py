import csv
import sys
import json
import math
import methods.OddsGeter as oddsGeter
from datetime import datetime
# vars
fileLocal = 'methods\\E0.csv'
teamNameLocal = 'methods\\TeamName.json'
dateFormatter = "%d/%m/%y"
outputFormatter = '%Y-%m-%d'

teamName = {}

with open(teamNameLocal, 'r', encoding='utf-8') as reader:
    teamName = json.loads(reader.read())


def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % (
        '=' * int(math.floor(cur * 50 / total)),
        percent))
    sys.stdout.flush()


class games():
    def __init__(self, data=[]):
        self.data = list()

    def appendGame(self, game):
        self.data.append(game)


class game():
    def __init__(self, date, homeTeam, awayTeam, FTHG, FTAG, homeOdds, awayOdds):
        self.date = date
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.FTAG = FTAG
        self.FTHG = FTHG
        self.homeOdds = homeOdds
        self.awayOdds = awayOdds
        self.datetime = datetime.strptime(
            date, dateFormatter)
        self.formatDate = self.datetime.strftime(outputFormatter)
        if(homeTeam in teamName.keys()):
            self.cHomeTeam = teamName[homeTeam]['Chinese']
        else:
            self.cHomeTeam = ''
        if(awayTeam in teamName.keys()):
            self.cAwayTeam = teamName[awayTeam]['Chinese']
        else:
            self.cAwayTeam = ''
        # self.cFTAG = teamName[FTAG]
        # self.cFTHG = teamName[FTHG]


def getDataFromCsv(file):
    data = []
    with open(file, newline='', encoding="utf-8") as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            data.append(row)
    return data


def getOdds(game):
    data = oddsGeter.getOddsByGame(game)
    return data


def setGames():
    progress = 0
    lenFootBall = 0
    footballList = getDataFromCsv(fileLocal)
    footballGames = games()
    for index in range(len(footballList)):
        if index >= 1:
            football = footballList[index]
            footballGames.appendGame(
                game(football[1], football[2],
                     football[3], football[4], football[5], {}, {}))
    lenFootBall = len(footballGames.data)
    for football in footballGames.data:
        remoteOdd = getOdds(football)
        if(len(remoteOdd) >= 1):
            football.homeOdds = remoteOdd[0].homeOdds
            football.awayOdds = remoteOdd[0].awayOdds
        # print(football.homeTeam+' vs '+football.awayTeam)
        progress = progress+1
        progressbar(progress, lenFootBall)

        # if(len(remoteOdd) >= 1):
        #     print(football.homeTeam+':'+str(football.homeOdds))
        #     print(football.awayTeam+':'+str(football.awayOdds))
        # else:
        #     print('none odds')

    return footballGames


# init
footballGames = setGames()
