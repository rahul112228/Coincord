class auction:
    def __init__(self):
        self.ranges = [(start,end) for end in range(4) for start in range(end+1)]
        self.winningbidsonranges=[(None,0) for _ in self.ranges]
    def bid(self,bidid,start,end,amount,verbose=False):
        if verbose:
            print(bidid," bids ",amount," on [",start,",",end,"]")
        #Bid should intersect with all winning bids by same bidder
        for rangeotherbid in [i for i,w in zip(self.ranges,self.winningbidsonranges) if w[0]==bidid]:
            if rangeotherbid[0] > end + 1 or rangeotherbid[1] + 1  < start:
                if verbose:
                    print("Invalid bid as winning on [",rangeotherbid[0],",",rangeotherbid[1],"]")
                return
        rangeindex=self.ranges.index((start,end))
        _,currentwinningbid=self.winningbidsonranges[rangeindex]
        if amount > currentwinningbid:
            self.winningbidsonranges[rangeindex] = (bidid,amount)
    def bestbidonrangeandvalue(self,start,end):
        rangeindex=self.ranges.index((start,end))
        return ((self.winningbidsonranges[rangeindex][0],start,end), self.winningbidsonranges[rangeindex][1]*(end-start+1))
    def calculatewinners(self):
        bestwinnersendingat=[([],0) for _ in range(4)]
        for i in range(4):
            bidderrange,value=self.bestbidonrangeandvalue(0,i)
            bestwinnersendingat[i]=([bidderrange],value)
            for j in range(i):
                bidderrange,value = self.bestbidonrangeandvalue(j+1,i)
                value += bestwinnersendingat[j][1]
                if value > bestwinnersendingat[i][1]:
                    newwinners=bestwinnersendingat[j][0]+[bidderrange]
                    bestwinnersendingat[i]=(newwinners,value)
        return bestwinnersendingat[3]
def example1():
    a=auction()
    a.bid("x",0,3,1,True)
    a.bid("a",0,0,2,True)
    a.bid("a",2,2,53,True)
    a.bid("b",1,1,1,True)
    a.bid("c",2,2,1,True)
    a.bid("d",3,3,1,True)
    print(a.calculatewinners())
    a.bid("x",0,3,2,True)
    print(a.calculatewinners())

import unittest
class AuctionTests(unittest.TestCase):
    def testbids(self):
        a=auction();
        #We could even allow zero bids but we don't now:
        a.bid("a",0,3,0, False)
        self.assertIsNone(a.bestbidonrangeandvalue(0,3)[0][0])
        a.bid("a",0,3,1, False)
        self.assertEqual(a.bestbidonrangeandvalue(0,3)[0][0],"a")
        #Overlapping bids are fine
        a.bid("a",0,0,1, False)
        self.assertEqual(a.bestbidonrangeandvalue(0,0)[0][0],"a")
        # Separated bids are not
        a.bid("a",2,2,1, False)
        self.assertIsNone(a.bestbidonrangeandvalue(2,2)[0][0])
        # Contiguous can be
        a.bid("a",1,1,1, False)
        self.assertEqual(a.bestbidonrangeandvalue(1,1)[0][0],"a")
        #Equal bids don't win
        a.bid("b",0,3,1, False)
        self.assertEqual(a.bestbidonrangeandvalue(0,3)[0][0],"a")
        #Higher bids do
        a.bid("b",0,3,2, False)
        self.assertEqual(a.bestbidonrangeandvalue(0,3)[0][0],"b")
        
        
        
    def testExample1(self):
        a=auction()
        a.bid("x",0,3,1)
        a.bid("a",0,0,2)
        a.bid("a",2,2,53)
        a.bid("b",1,1,1)
        a.bid("c",2,2,1)
        a.bid("d",3,3,1)
        self.assertEqual(a.calculatewinners(), ([('a', 0, 0), ('b', 1, 1), ('c', 2, 2), ('d', 3, 3)], 5))
        a.bid("x",0,3,2)
        self.assertEqual(a.calculatewinners(),([('x', 0, 3)], 8))

        
        
        
        
        
        
        
    

