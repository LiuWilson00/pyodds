import json

fileLocal = 'oddsdata.json'
oddsData = []
userSetRTP = 0.5


class sessionIncome:
    def __init__(self, income=0, cost=0, profit=0):
        self.income = income
        self.cost = cost
        self.profit = profit


class oddsInformation:
    def __init__(self, RTP=0, distribution={}, _probability={}, probability={}, odds={}, _odds={}):
        self.distribution = distribution
        self._probability = _probability
        self.probability = probability
        self.odds = odds
        self._odds = _odds
        self.RTP = RTP


def init():
    originalData = json.load(open(fileLocal))
    for data in originalData:
        if(data['homeOdds'] != {}):
            oddsData.append(data)


def getOddsProbabilityInfo(homeOdds, awayOdds):
    def marginOriginal(h, a):
        m = dict()
        for key in h.keys():
            m[key] = float(h[key])
        for key in a.keys():
            m[key] = float(a[key])
        return m

    mergeDict = dict()
    distribution = dict()
    _probability = dict()
    probability = dict()
    _odds = dict()
    RTP = 0
    mergeDict = marginOriginal(homeOdds, awayOdds)
    sumInverseOdds = 0
    for key in mergeDict.keys():
        sumInverseOdds = sumInverseOdds + 1/mergeDict[key]
        probability[key] = 1/mergeDict[key]

    for key in mergeDict.keys():
        _probability[key] = 1 - 1/mergeDict[key]/sumInverseOdds
        # user distribution model
        distribution[key] = 1/mergeDict[key]/sumInverseOdds
        _odds[key] = 1/((1 - 1/mergeDict[key]/sumInverseOdds) +
                        (1/mergeDict[key]/sumInverseOdds)*(1-userSetRTP))
    RTP = 1/sumInverseOdds
    info = oddsInformation(
        RTP, distribution, _probability, probability, mergeDict, _odds)
    return info
    # print(sumInverseOdds)


def computeIncome(info, total, result):

    income = 0
    cost = 0
    profit = 0
    for score in info.distribution.keys():
        if(result == score):
            income = income + total * info.distribution[score]
            profit = total * info.distribution[score]
        else:
            income = income - total * \
                info.distribution[score] * (info._odds[score] - 1)
            cost = cost + total * \
                info.distribution[score] * (info._odds[score] - 1)
    SI = sessionIncome(income, cost, profit)
    return SI


init()
# print(len(oddsData))
basicTotal = 1000000
# SI = computeIncome(oddsInfo, 1000000,
#                    oddsData[0]['FTAG']+':'+oddsData[0]['FTHG'])
# print(oddsInfo._odds)
incomeList = list()
for odds in oddsData:
    print(odds['homeTeam']+' vs ' + odds['awayTeam'] +
          ':'+odds['FTAG']+':'+odds['FTHG'])
    oddsInfo = getOddsProbabilityInfo(
        odds['homeOdds'], odds['awayOdds'])

    SI = computeIncome(oddsInfo, basicTotal,
                       odds['FTAG']+':'+odds['FTHG'])
    print('income:'+str(SI.income)+'  '+'cost:' +
          str(SI.cost)+'  '+'profit:' + str(SI.profit))
    incomeList.append(SI)
