import os.path
import sys
import itertools
import operator
from collections import defaultdict

class Apriori:
    def __init__(self,filename,min_sup,out):
        self.data = []
        self.vocab = []        
        self.readFileData(filename)
        self.n = len(self.data)
        self.sup_count = min_sup * self.n
        self.supportData = {}
        self.L = []
        self.outfile = out
        
    def readFileData(self,filename):
        if os.path.isfile(filename):
            f = open(filename, "r")
            for line in f:
                trans = line.split()
                self.data.append(trans)
            print len(self.data)
        else:
            print "Error: file ", filename, " does not exist"
            sys.exit()
        f2 = open("vocab.txt","r")
        for line in f2:
            self.vocab.append(line.split()[1])

    def apriori(self):
        L1 = self.f1_itemsets(self.data)
        self.L.append(L1)
        k = 0
        while(len(self.L[k]) != 0):
            Ck = self.apriori_gen(self.L[k])
            temp = defaultdict(float)
            for trans in self.data:
                for item in Ck:
                    item = frozenset(item)
                    if item.issubset(trans):
                        temp[item] += 1.0
            
            k += 1
            self.L.append([])
            for itemset in temp:
                if temp[itemset] >= self.sup_count:
                    self.supportData[itemset] = temp[itemset]/self.n
                    self.L[k].append(sorted(list(itemset)))  
        print len(self.L[0])
        print len(self.L[1])
        print len(self.L[2])
        f = open(self.outfile, "w")
        sorted_support = sorted(self.supportData.items(), key = operator.itemgetter(1), reverse = True)
        for item,sup in sorted_support:  
            itemset = [self.vocab[int(x)] for x in list(item)]
            it = ''
            for i in itemset:
                it += i + ' '
            f.write(str(sup)+" [ "+it+"]\n")
            
    def apriori_gen(self,Lk):
        num = len(Lk)
        n = len(Lk[0])
        Ck = []
        for i in range(num):
            for j in range(i+1,num):
                l1 = Lk[i][:n-1]
                l2 = Lk[j][:n-1]
                if l1 == l2:
                    templist = l1
                    if Lk[i][n-1] < Lk[j][n-1]:
                        templist += [Lk[i][n-1]] + [Lk[j][n-1]]
                    else:
                        templist += [Lk[j][n-1]] + [Lk[i][n-1]]
                    if self.hasInfrequentSubset(templist, Lk) == False:
                        Ck.append(templist)
        return Ck
     
    def hasInfrequentSubset(self, c, Lk):
        n = len(Lk[0])
        for itemset in list(itertools.combinations(c,n)):
            if list(itemset) not in Lk:
                return True
            else:
                return False
           
    def f1_itemsets(self,data):
        l = defaultdict(float)
        l1 = []
        for trans in data:
            for item in trans:
                l[item] += 1.0

        for key in l:
            if l[key] >= self.sup_count:
                self.supportData[frozenset([key])] = l[key]/self.n
                l1.append(([key])) 
        return l1
                
        
if __name__=="__main__":
    print "Finding frequent patterns in topic-0.txt .."
    ap0 = Apriori("topic-0.txt",0.007,"pattern-0.txt")
    ap0.apriori()
    print "Finding frequent patterns in topic-1.txt .."    
    ap1 = Apriori("topic-1.txt",0.007,"pattern-1.txt")
    ap1.apriori()
    print "Finding frequent patterns in topic-2.txt .."    
    ap2 = Apriori("topic-2.txt",0.007,"pattern-2.txt")
    ap2.apriori()
    print "Finding frequent patterns in topic-3.txt .."    
    ap3 = Apriori("topic-3.txt",0.007,"pattern-3.txt")
    ap3.apriori()
    print "Finding frequent patterns in topic-4.txt .."    
    ap4 = Apriori("topic-4.txt",0.007,"pattern-4.txt")
    ap4.apriori()

        
            
    
