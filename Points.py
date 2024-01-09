import Cardclasses as cc
import itertools
import matplotlib.pyplot as plt
import numpy as np

def sumtest(ls):

    sum = 0
    x = []
    total = []
    
    if len(ls) == 1:
        return [-1]
    
    for el in ls:
        sum = sum + el.value
    
    if sum == 15:
    
        for el in ls:
            x.append(el.toStr())

        return[x]

    for i in range(0,len(ls)):
        temp = []
        for j in range(0,len(ls)):
            if(j != i):
                temp.append(ls[j])

        total = total + sumtest(temp)

    return total


d = cc.Deck()
#d.shuffle()

fcards = itertools.combinations(d.cards,5)
fcards = list(itertools.islice(fcards,0,None))
def getData(type,cardcombs):
    pointsFour = []
    for el in fcards:
        
        el = (cc.Hand(el,5))
        if (type != "None"):
            for card in el.cards:
                if(card.name == type):
                    pointsFour.append(el.count(None))
        if (type == "None"):
            pointsFour.append(el.count(None))
    return pointsFour


types = ["Ace","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King"]
for type in types:
    cardType = type
    result = getData(cardType,fcards)
    histlist = [0]*40
    for el in result:
        histlist[el] = histlist[el] + 1

    x = np.arange(0,40)
    ticks = []
    for el in x:
        ticks.append(str(el))
    print(type)
    print("Raw numbers")
    print(histlist)
    print("Average points")
    print(sum(result)/len(result))
    print("Percentage of hands worth Zero")
    print(histlist[0]/sum(histlist[1:])*100)
    print()
    
    fig, ax = plt.subplots()
    ax.bar(x,histlist,tick_label=ticks,width=1.2,edgecolor= "black")
    ax.set_ylabel("Number of Hands")
    ax.set_xlabel("Hand Value")
    ax.set_title("Card Type: " + cardType)
    plt.show()

    