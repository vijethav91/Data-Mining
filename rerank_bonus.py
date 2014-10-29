import os.path
import sys
import itertools
import operator
from math import log

class Purity2:
    def __init__(self):
        self.patterns = []
        self.readFiles()
        self.Dt = {}
        self.setDt()
        self.rank = {}
        
               
    def readFiles(self):
        for i in range(5):
            filename = "pattern-"+str(i)+".txt"
            if os.path.isfile(filename):
                f = open(filename, "r")
                frequentItems = {}
                for line in f:
                    freq = line.split()
                    itemset = freq[2:len(freq)-1]
                    frequentItems[frozenset(itemset)] = float(freq[0])
                self.patterns.append(frequentItems)                                    
            else:
                print "Error: file ", filename, " does not exist"
                sys.exit()
    
    def setDt(self):
        self.Dt[(0,0)] = 10047
        self.Dt[(0,1)] = 17326
        self.Dt[(0,2)] = 17988
        self.Dt[(0,3)] = 17999
        self.Dt[(0,4)] = 17820
        self.Dt[(1,1)] = 9674
        self.Dt[(1,2)] = 17446
        self.Dt[(1,3)] = 17902
        self.Dt[(1,4)] = 17486
        self.Dt[(2,2)] = 9959
        self.Dt[(2,3)] = 18077
        self.Dt[(2,4)] = 17492
        self.Dt[(3,3)] = 10161
        self.Dt[(3,4)] = 17912
        self.Dt[(4,4)] = 9845
       
    def reRank2(self,i):
        w = 0.5
        f = open("bonus/bonus-purity-"+str(i)+".txt","w")
        pattern = self.patterns[i]
        for itemset,coverage in pattern.iteritems():
            phrase = self.calPhraseness(itemset,coverage,i)
            purity = self.calPurity(itemset,coverage,i)
            rank = ((1-w)*purity*cov) + (w*coverage*phrase)
            self.rank[itemset] = rank
        
        sorted_rank = sorted(self.rank.items(), key = operator.itemgetter(1), reverse = True)
        
        for item,rank in sorted_rank:
            itemset = list(item)
            it = ''
            for k in itemset:
                it += k + ' '
            f.write(str(rank)+" [ "+it+"]\n")
        self.rank = {}
    
    def calPhraseness(self,itemset,cov,i):
        items = list(itemset)
        temp = 0.0        
        for it in items:
            temp += log(self.patterns[i][frozenset([it])])
        return log(cov)-temp
        
                      
    def calPurity(self,itemset,cov,i):
        ftp = cov * self.Dt[(i,i)]
        maxval = 0.0
        for k in range(5):
            if k != i:
                temp = ftp
                if itemset in self.patterns[k]:
                    temp += self.patterns[k][itemset]*self.Dt[k,k]
                if k<i:
                    temp = temp/self.Dt[(k,i)]
                else:
                    temp = temp/self.Dt[(i,k)]
                if temp>maxval:
                    maxval = temp
        return log(cov)-log(maxval)
        
if __name__=="__main__":
    p = Purity2()
    for i in range(5):
        p.reRank2(i)


            
