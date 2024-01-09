import Cardclasses as cc


g = cc.Game("crib")
wins = [0,0]
for i in range(0,1000000):
    temp = g.fullGame()   

    wins[temp] = wins[temp] + 1

print(wins)