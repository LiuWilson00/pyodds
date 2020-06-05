import csv
import sys
import requests as rq
from bs4 import BeautifulSoup
import io
import time
import json
import methods.Football as fball
import methods.OddsGeter as odds

outputFile = 'oddsdata.json'


# Initial

outputGameList = []

for fgame in fball.footballGames.data:
    tempDict = dict()
    # print(fgame.__dict__)
    tempDict['date'] = fgame.formatDate
    tempDict['homeTeam'] = fgame.homeTeam
    tempDict['awayTeam'] = fgame.awayTeam
    tempDict['chinese_homeTeam'] = fgame.cHomeTeam
    tempDict['chinese_awayTeam'] = fgame.cAwayTeam
    tempDict['FTAG'] = fgame.FTAG
    tempDict['FTHG'] = fgame.FTHG
    tempDict['homeOdds'] = fgame.homeOdds
    tempDict['awayOdds'] = fgame.awayOdds
    outputGameList.append(tempDict)


outputJson = json.dumps(outputGameList)
with open(outputFile, 'w') as f:
    f.write(outputJson)
    f.close()


# odds.displayOdds('2012-08-17', '2012-08-19')
# odds.getPageNumbaer('2012-08-17', '2012-08-19')


# print(fball.footballGames.data[1].formatDate +
#       ' '+fball.footballGames.data[1].cHomeTeam)
# for game in fball.footballGames.data:
#     print(game.formatDate+':'+game.cHomeTeam+'vs'+game.cAwayTeam)
#     print(game.datetime)


# testNumber = 364
# print(fball.footballGames.data[testNumber].formatDate+':' +
#       fball.footballGames.data[testNumber].cHomeTeam+'vs'+fball.footballGames.data[testNumber].cAwayTeam)
# print(fball.footballGames.data[testNumber].datetime)
# temp = odds.getOddsByGame(fball.footballGames.data[testNumber])
# if(len(temp) > 0):
#     print(str(temp[0].homeOdds))
# else:
#     print(str(temp))
