import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
remoteURL = 'https://odds.zquu.com/historybd.html?companyid=1,'

scoreList = [
    [
        '1:0', '2:0', '2:1', '3:0', '3:1', '3:2', '4:0', '4:1', '4:2', '4:3', '0:0', '1:1', '2:2', '3:3', '4:4', 'other'
    ],  [
        '0:1', '0:2', '1:2', '0:3', '1:3', '2:3', '0:4', '1:4', '2:4', '3:4']
]


class oddsData():
    def __init__(self, homeTeam='', awayTeam='', homeOdds=[], awayOdds=[]):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.homeOdds = homeOdds,
        self.awayOdds = awayOdds


def haveChild(tag, childName):
    childs = tag.find_all(childName)
    if(len(childs) != 0):
        return True
    return False


def displayOdds(sdate, edate):
    data = {'sdate': sdate, 'edate': edate, 'page': ''}
    r = rq.post(remoteURL, data=data)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table_tag = soup.find_all("table", id='wMyData')
    tbody_tag = table_tag[0].find_all('tbody')

    for tag in tbody_tag:
        if(not haveChild(tag, 'tbody') and haveChild(tag, 'tr')):
            time = tag.find_all("td", class_='time')
            teams = tag.find_all("td", class_='hc')
            rowTags = tag.find_all("tr")
            vsText = ''

            for t in time:
                print('比賽時間:'+t.text)

            for t in teams:
                vsText = vsText + ' ' + t.text
            if(vsText != ''):
                print('比賽隊伍'+vsText)

            status = 0
            for row in rowTags:

                teamName = row.find_all('td', class_='hc')
                scoreOdds = row.find_all(class_='bgy1')
                oddIndex = 0
                if(len(teamName) > 0):
                    print(teamName[0].text)
                for odds in scoreOdds:
                    if(odds.text != None):
                        print(scoreList[status][oddIndex]+' '+odds.text)
                        oddIndex = oddIndex+1

                if(len(teamName) > 0):
                    status = status+1


def getPageNumbaer(sdate, edate):
    data = {'sdate': sdate, 'edate': edate, 'page': ''}
    r = rq.post(remoteURL, data=data)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table_tag = soup.find_all("table", id='wMyData')
    tbody_tag = table_tag[0].find_all('tbody')
    font_tag = tbody_tag[len(tbody_tag)-1].find_all('font')
    return int(font_tag[0].text)


def getOddsByGame(game):
    sdate = game.datetime
    edate = game.datetime + timedelta(days=1)
    pageNumber = getPageNumbaer(sdate, edate)
    oddList = []

    for page in range(int(pageNumber/30)):

        # print(str(tempOdd))
        data = {'sdate':  sdate, 'edate': edate, 'page': page+1}
        r = rq.post(
            remoteURL, data=data)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        table_tag = soup.find_all("table", id='wMyData')
        tbody_tag = table_tag[0].find_all('tbody')

        for tag in tbody_tag:
            tempOdd = oddsData()

            status = 0
            if(not haveChild(tag, 'tbody') and haveChild(tag, 'tr')):
                # time = tag.find_all("td", class_='time')
                # teams = tag.find_all("td", class_='hc')
                rowTags = tag.find_all("tr")

                for row in rowTags:
                    teamName = row.find_all('td', class_='hc')
                    scoreOdds = row.find_all(class_='bgy1')
                    homeOddDist = dict()
                    awayOddDist = dict()
                    oddIndex = 0
                    # if(len(teamName) > 0):
                    #     print(teamName[0].text +
                    #           str(str(teamName[0].text.strip()) == str(game.cHomeTeam.strip())) + game.cHomeTeam + ' ' + str(teamName[0].text == '西布朗'))
                    if(len(teamName) > 0 and teamName[0].text.strip().find(game.cHomeTeam.strip()) >= 0 and status == 0):
                        tempOdd.homeTeam = teamName[0].text.strip()
                    elif(len(teamName) > 0 and teamName[0].text.strip().find(game.cAwayTeam.strip()) >= 0 and status == 1):
                        tempOdd.awayTeam = teamName[0].text.strip()
                    if(tempOdd.homeTeam != ''):
                        for odds in scoreOdds:
                            if(odds.text != None):
                                # print(scoreList[status][oddIndex]+':'+odds.text)
                                if(status == 0):
                                    # print(str(homeOddDist))
                                    homeOddDist[scoreList[status]
                                                [oddIndex]] = odds.text
                                    oddIndex = oddIndex+1

                                if(status == 1):
                                    awayOddDist[scoreList[status]
                                                [oddIndex]] = odds.text
                                    oddIndex = oddIndex+1
                    if(status == 0 and tempOdd.homeTeam != ''):
                        tempOdd.homeOdds = homeOddDist
                    elif(status == 1 and tempOdd.homeTeam != '' and tempOdd.awayTeam != ''):
                        tempOdd.awayOdds = awayOddDist

                    if(len(teamName) > 0):
                        status = status+1
            if(tempOdd.homeTeam != '' and tempOdd.awayTeam != ''):
                oddList.append(tempOdd)
    return oddList
    # print(oddList[0].homeTeam + ' ' + str(oddList[0].homeOdds) +
    #       oddList[0].awayTeam + ' '+str(oddList[0].awayOdds))
    # for key in oddList[0].homeOdds.keys():
    #     print(oddList[0].homeOdds[key])
