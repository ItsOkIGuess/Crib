import random
import itertools
class Card:

    def __init__(self,name,suit,value):
        self.name = name
        self.suit = suit
        self.value = value
    
    def toStr(self):
        return str(self.name) + " of " + str(self.suit)


class Deck:

    def __init__(self):
        self.cards = []
        types = ["Ace","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King"]
        suits = ["Diamonds","Clubs","Hearts","Spades"]
        weight = [1,2,3,4,5,6,7,8,9,10,10,10,10]
        for i in range(0,4):
            for j in range(0,13):
                self.cards.append(Card(types[j],suits[i],weight[j]))
        self.depth = 0
#Shuffles the deck
    def shuffle(self):
        random.shuffle(self.cards)
        self.depth = 0
#deals a hand of size n 
    def deal(self,n):
        fill = []
        i = 0
        while(i+self.depth < self.depth +n):
            fill.append(self.cards[i+self.depth])
            i = i + 1
        self.depth = self.depth + n
        return Hand(fill,n)

    def createhand(self,fill):
        return Hand(fill,len(fill))

    def createallhands(self,size):
        
        pass


class Hand:
    def __init__(self,cards,size):
        self.cards = cards
        self.size = size

#counts the points in a hand 
    def count(self,cut,crib):
        points = 0
        if(cut != None):
            full_hand = list(self.cards) + cut
        else:
            full_hand = self.cards
        ###############################################################################
        #15's
        #Helper Function
        def sumF(ls):
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
                total = total + sumF(temp)
            return total
       
        sum = sumF(full_hand)
        sum = [element for element in sum if element != -1]
        final = []
        for el in sum:
            if el not in final:
                final.append(el)
        points = points + 2*len(final)

        ###############################################################################
        #Runs
        #Helper Function
        def runs(ls):
            inRow = 0
            runs = []
            dict = {"Ace":0,"Two":0,"Three":0,"Four":0,"Five":0,"Six":0,"Seven":0,"Eight":0,"Nine":0,"Ten":0,"Jack":0,"Queen":0,"King":0}
            for card in ls:
                dict[card.name] = dict[card.name] + 1
            x = []

            for key in dict:
                sum = 0
                if dict[key] == 0 :
                    runs.append(x)
                    x = []

                if dict[key] != 0:
                    x.append(dict[key])

            for el in runs:
                if len(el) >= 3:
                    mult = 1
                    for num in el:
                        mult = mult * num
                    sum = sum + mult * len(el)
            return sum    
        points = points + runs(full_hand)
        ###############################################################################
        #Sets
        #helper function
        def sets(ls):
            sum = 0
            setsdict = {"Ace":0,"Two":0,"Three":0,"Four":0,"Five":0,"Six":0,"Seven":0,"Eight":0,"Nine":0,"Ten":0,"Jack":0,"Queen":0,"King":0}
            for card in ls:
                setsdict[card.name] = setsdict[card.name] + 1

            for key in setsdict:
                if setsdict[key] == 2:
                    sum = sum + 2
                if setsdict[key] == 3:
                    sum = sum + 6
                if setsdict[key] == 4:
                    sum = sum + 12    
            return sum
        points = points + sets(full_hand)
        #################################################################################
        #Flushes
        def flush(ls):
            sum = 0
            dictF = {"Diamonds":0,"Clubs":0,"Hearts":0,"Spades":0}
            for card in ls:
                dictF[card.suit] = dictF[card.suit] + 1
            if not crib:
                for key in dictF:
                    if dictF[key] >= 4:
                        sum = sum + dictF[key]
                return sum
            else:       
                for key in dictF:
                    if dictF[key] >= 5:
                        sum = sum + dictF[key]
                return sum
        points = points + flush(full_hand)


        #right jack
        if(cut != None):
            for card in self.cards:
                if card.name == "Jack":
                    if card.suit == cut[0].suit:
                        points = points + 1
           



        return points

#chooses highest points from best 4 of 6 from hand
    def maxPoints(self):
        fcards = itertools.combinations(self.cards,4)
        fcards = list(itertools.islice(fcards,0,None))
        max = -1
        maxIndex = 0
        for el in fcards:
            el = Hand(el,4)        
            curr = el.count(None,False)
            if curr > max:
                max = curr
                maxIndex = el
            return  maxIndex



class Game:    

    def __init__(self,name):
        self.name = name
        self.players = [[],[]]
        self.player1points = 0
        self.player2points = 0
        self.deck = Deck()
        self.maxpoints = 121
        self.crib = 1

    def round(self):
        self.deck.shuffle()
        self.players[0] = self.deck.deal(6)
        self.players[1] = self.deck.deal(6)

        player1 = self.players[0].maxPoints()
        player2 = self.players[1].maxPoints()
        
        cribhand = []
        for el in self.players[0].cards:
            if el not in player1.cards:
                cribhand.append(el)
        for el in self.players[1].cards:
            if el not in player2.cards:
                cribhand.append(el)
        cribhand = Hand(cribhand,4)
        cutcard = self.deck.deal(1)
        self.player1points = self.player1points + player1.count(cutcard.cards,False)
        
        self.player2points = self.player2points + player2.count(cutcard.cards,False)

        #print("player 1 hand")
        #for el in player1.cards:
        #    print(el.toStr())
        #print(player1.count(cutcard.cards,False))
        #print()
        #print("player 2 hand")
        #for el in player2.cards:
        #    print(el.toStr())
        #print(player2.count(cutcard.cards,False))
        #print()
        #print("cut card:")
        #print(cutcard.cards[0].toStr())
        #print()
        #print("cribhand")
        #for el in cribhand.cards:
        #    print(el.toStr())
        #print(cribhand.count(cutcard.cards,False))
        if self.crib == 1:
             self.player1points = self.player1points + cribhand.count(cutcard.cards,True)
        else:
             self.player2points = self.player2points + cribhand.count(cutcard.cards,True)

        '''print(" player " + str(self.crib) + " crib")
        print("player 1 points:")
        print(self.player1points)
        print("player 2 points:")
        print(self.player2points)'''
        self.crib = (self.crib + 1) % 2

    def fullGame(self):
        self.player1points = 0
        self.player2points = 0
        while(self.player1points < 121 and self.player2points < 121):
            self.round()
            

        if self.player1points > self.player2points:
            return 0
        else:
            return 1


class Ai:

    def __init__(self, hand):
        self.hand = hand


