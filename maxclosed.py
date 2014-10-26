import os.path
import sys
import itertools
import operator
from collections import defaultdict

class MaxClosed:
    def __init__(self,filename,maxfile,closedfile):
        self.frequentItems = {}  
        self.maxItems = {}
        self.closedItems = {}      
        self.readFileData(filename)
        self.max = maxfile
        self.closed = closedfile
        
    def readFileData(self,filename):
        if os.path.isfile(filename):
            f = open(filename, "r")
            for line in f:
                freq = line.split()
                itemset = freq[2:len(freq)-1]
                self.frequentItems[frozenset(itemset)] = float(freq[0])
                self.closedItems[frozenset(itemset)] = float(freq[0])
                self.maxItems[frozenset(itemset)] = float(freq[0])                               
        else:
            print "Error: file ", filename, " does not exist"
            sys.exit()
            
    def findMaxClosed(self):
        for items,sup in self.frequentItems.iteritems():
            subsetList = self.subsets(items)
            for i in subsetList:
                if i in self.frequentItems:
                    self.maxItems.pop(i,None)
                    if self.frequentItems[i] == sup:
                        self.closedItems.pop(i,None)
        
        f = open(self.max, "w")
        sorted_max = sorted(self.maxItems.items(), key = operator.itemgetter(1), reverse = True)
        for item,sup in sorted_max:  
            itemset = list(item)
            it = ''
            for i in itemset:
                it += i + ' '
            f.write(str(sup)+" [ "+it+"]\n")
            
        f = open(self.closed, "w")
        sorted_closed = sorted(self.closedItems.items(), key = operator.itemgetter(1), reverse = True)
        for item,sup in sorted_closed:  
            itemset = list(item)
            it = ''
            for i in itemset:
                it += i + ' '
            f.write(str(sup)+" [ "+it+"]\n")
            
    def subsets(self, items):
        subsetList = []
        items = list(items)
        for n in range(1,len(items)):
            subsetList.extend(itertools.combinations(items,n))
        return map(frozenset, subsetList)

        
if __name__=="__main__":
    mc = MaxClosed("pattern-0.txt","max/max-0.txt","closed/closed-0.txt")
    mc.findMaxClosed()
    mc = MaxClosed("pattern-1.txt","max/max-1.txt","closed/closed-1.txt")
    mc.findMaxClosed() 
    mc = MaxClosed("pattern-2.txt","max/max-2.txt","closed/closed-2.txt")
    mc.findMaxClosed()
    mc = MaxClosed("pattern-3.txt","max/max-3.txt","closed/closed-3.txt")
    mc.findMaxClosed()
    mc = MaxClosed("pattern-4.txt","max/max-4.txt","closed/closed-4.txt")
    mc.findMaxClosed()

        
            
    
