import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fileLocal = 'oddsdata.json'
oddsData = []
userSetRTP = 0.7
oddsLimit=1.01


class sessionIncome:
    def __init__(self, income=0, cost=0, profit=0):
        self.income = income
        self.cost = cost
        self.profit = profit
    def __str__(self):
        return 'income:'+str(self.income) +' cost:'+str(self.cost)+' profit:'+str(self.profit)


class oddsInformation:
    def __init__(self, RTP=0, distribution={}, _probability={}, probability={}, odds={}, _odds={}):
        self.distribution = distribution
        self._probability = _probability
        self.probability = probability
        self.odds = odds
        self._odds = _odds
        self.RTP = RTP
    def __str__(self):
        return 'distribution:'+str(self.distribution) + '  _odds:' + str(self._odds)

class oddsAlgorithm:
    def __init__(self,daFun=lambda i: True,_oddFun=lambda i: True,aaFun=False):
        self.sumInverseOdds=0
        self.daFun=daFun
        self._oddFun=_oddFun
        self._oddSum=0
        self._oddAvg=0
        self._odd=dict()
        self.odds=dict()
        self.aaFun=aaFun
        self.attractive=dict()
        self.attractiveSum=0


    def initOddsAlgorithm(self,oddDict):
        self._oddSum=0
        self._oddAvg=0
        self._odd=dict()
        self.odds=dict()
        self.attractive=dict()
        self.sumInverseOdds=0
        self.attractiveSum=0

        sumI=0
        
        for key in oddDict.keys():
            if(oddDict[key] != 0):
                sumI = sumI + 1/oddDict[key]
        self.odds=oddDict
        self.sumInverseOdds=sumI
        # print(str(self.odds))
    def attractiveAlgorithm(self):
        self.attractive=self.aaFun(_odds=self._odd,odds=self.odds,sumInverseOdds=self.sumInverseOdds)
        aSum=0
        for key in self.attractive.keys():
            aSum=aSum+self.attractive[key]
        self.attractiveSum=aSum
        # print(str(self.attractive))

    def _oddsAlgorithm(self,key):
        _oddTemp=self._oddFun(odds=self.odds[key],sumInverseOdds=self.sumInverseOdds)
        self._oddSum=self._oddSum + _oddTemp
        self._odd[key]=_oddTemp
        self._oddAvg=self._oddSum/len(self._odd)
        self.attractive[key]=1
        return _oddTemp
    def distributionAlgorithm(self,key):
        return self.daFun(odds=self.odds[key],sumInverseOdds=self.sumInverseOdds,attractive=self.attractive[key],attractiveSum=self.attractiveSum)
    def probabilityCalculate(self,key):
        return 1/self.odds[key]

    def _probabilityCalculate(self,key):
        return 1-1/self.odds[key]/self.sumInverseOdds
    



def init():
    originalData = json.load(open(fileLocal))
    for data in originalData:
        if(data['homeOdds'] != {}):
            oddsData.append(data)


def getOddsProbabilityInfo(homeOdds, awayOdds, algorithm):
    def marginOriginal(h, a):
        m = dict()
        for key in h.keys():
            if(float(h[key])!=0):
                m[key] = float(h[key])
        for key in a.keys():
            if(float(a[key])!=0):
                m[key] = float(a[key])
        return m

    mergeDict = dict()
    distribution = dict()
    _probability = dict()
    probability = dict()
    _odds = dict()
    RTP = 0
    mergeDict = marginOriginal(homeOdds, awayOdds)
    
    algorithm.initOddsAlgorithm(mergeDict)
    # print(algorithm.sumInverseOdds)

    for key in mergeDict.keys():
        if(mergeDict[key] != 0):
            probability[key]=algorithm.probabilityCalculate(key)
            _probability[key] = algorithm._probabilityCalculate(key)
            # user distribution model
            _odds[key] = algorithm._oddsAlgorithm(key)
 
    if(algorithm.aaFun!=False):
        algorithm.attractiveAlgorithm()
    
    for key in mergeDict.keys():
            distribution[key] = algorithm.distributionAlgorithm(key)
            
    
    RTP = algorithm.sumInverseOdds
    info = oddsInformation(
        RTP, distribution, _probability, probability, mergeDict, _odds)
    return info
    # print(sumInverseOdds)


def computeIncome(info, total, result):

    income = 0
    cost = 0
    profit = 0
    if(result in [ "1:0","2:0","2:1","3:0","3:1","3:2","4:0","4:1","4:2", "4:3","0:0","1:1","2:2","3:3","4:4",]):
        finalResult=result
    else:
        finalResult='other'

    for score in info.distribution.keys():
        if(finalResult == score):
            income = income + total * info.distribution[score]
            profit = total * info.distribution[score]
        else:
            income = income - total * \
                info.distribution[score] * (info._odds[score] - 1)
            cost = cost + total * \
                info.distribution[score] * (info._odds[score] - 1)
    SI = sessionIncome(income, cost, profit)
    return SI

def distributionModel1(**oddsData):
    oddsData.setdefault('odds',1)
    oddsData.setdefault('sumInverseOdds',1)
    return 1/oddsData['odds']/oddsData['sumInverseOdds']
def _oddsModel1(**oddsData):
    odds=oddsData['odds']
    sumInverseOdds=oddsData['sumInverseOdds']
    return 1/((1 - 1/odds/sumInverseOdds) +
                            (1/odds/sumInverseOdds)*(1-userSetRTP))

def distributionModel2(**oddsData):
    attractive=oddsData['attractive']
    attractiveSum=oddsData['attractiveSum']
    return attractive/attractiveSum


def attractiveModel1(**oddsData):
    # odds=oddsData['odds']
    sumInverseOdds=oddsData['sumInverseOdds']
    _odds=oddsData['_odds']
    odds=oddsData['odds']
    attractive={}
    # print(odds)
    # print(_odds)
    for _o in _odds.keys():
        attractive[_o]=1/(1+50**(-100*(_odds[_o]-oddsLimit))) * 1/odds[_o]/sumInverseOdds
    return attractive
    
init()
# print(len(oddsData))
basicTotal = 1000000
totalIncome = 0
totalCost = 0
totalProfit = 0
# SI = computeIncome(oddsInfo, 1000000,
#                    oddsData[0]['FTAG']+':'+oddsData[0]['FTHG'])
# print(oddsInfo._odds)
# model1=oddsAlgorithm(distributionModel1,_oddsModel1)
model1=oddsAlgorithm(distributionModel2,_oddsModel1,attractiveModel1)
incomeList = list()
for odds in oddsData:
    print(odds['homeTeam']+' vs ' + odds['awayTeam'] +
          '    '+odds['FTAG']+':'+odds['FTHG'])
    oddsInfo = getOddsProbabilityInfo(
        odds['homeOdds'], odds['awayOdds'], model1)
    # print(str(oddsInfo))
    
    SI = computeIncome(oddsInfo, basicTotal,
                       odds['FTAG']+':'+odds['FTHG'])
    print(str(SI))
    incomeList.append(SI)

iL=list()

for income in incomeList:
    totalIncome = totalIncome+income.income
    totalCost = totalIncome+income.cost
    totalProfit = totalIncome+income.profit
    iL.append([income.income])    
print(np.array(iL))
print('===========================')
print('all income:' + str(totalIncome))
print('all cost:' + str(totalCost))
print('all profit:' + str(totalProfit))

df = pd.DataFrame(np.array(iL),columns=['a'])
df.plot.area()
plt.show()
