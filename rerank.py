import os.path
import sys
import itertools
import operator
from collections import defaultdict
from math import log

class Purity:
    def __init__(self):
        self.patterns = []
        self.readFiles()
        self.Dt = {}
        self.setDt()
        self.purity = {}
        
               
    def readFiles(self):
        for i in range(5):
            filename = "pattern-"+str(i)+".txt"
            if os.path.isfile(filename):
                f = open(filename, "r")
                frequentItems = defaultdict(float)
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
                
    def reRank(self,i):
        f = open("purity/purity-"+str(i)+".txt","w")
        pattern = self.patterns[i]
        for itemset,sup in pattern.iteritems():
            pur = self.calPurity(itemset,sup,i)
            #rank = pur*sup
            self.purity[itemset] = pur*sup
        
        sorted_purity = sorted(self.purity.items(), key = operator.itemgetter(1), reverse = True)
        
        for item,pur_sup in sorted_purity:
            itemset = list(item)
            it = ''
            for k in itemset:
                it += k + ' '
            f.write(str(pur_sup)+" [ "+it+"]\n")
        self.purity = {}
          
    def calPurity(self,itemset,sup,i):
        ftp = sup * self.Dt[(i,i)]
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
        return log(sup)-log(maxval)
        
if __name__=="__main__":
    p = Purity()
    for i in range(5):
        p.reRank(i)

            
