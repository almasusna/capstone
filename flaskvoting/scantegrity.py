import string
import random

class Scantegrity:
    def __init__(self, billetNum, sizeCode, candidatesNum):
        self.billetNum = billetNum
        self.sizeCode = sizeCode
        self.candidatesNum = candidatesNum
        self.theset = self.setGen()
        self.tableP = self.createTableP()
        self.tableQ = self.createTableQ()
        self.tableR = self.createTableR()
        self.tableS = self.createTableS()


    # Function to generate random code 
    def codeGen(self,chars = string.ascii_uppercase + string.digits):
        size = self.sizeCode
        self.code = ""
        for i in range(size):
            self.code= self.code + random.choice(chars)
        return self.code

    # Generate list of codes without collisions
    def setGen(self):
        theset = set()
        while len(theset) != (self.billetNum * self.candidatesNum):
            thecode = self.codeGen()
            if thecode not in theset:
                theset.add(thecode)
        return theset

    # Create table P
    def createTableP(self):
        tableP = []
        billetNum = self.billetNum
        candidatesNum = self.candidatesNum
        theset= self.theset
        
        for i in range(billetNum):
            theBilletDict = dict()
            for j in range(candidatesNum):
                theBilletDict[j] = theset.pop()
            tableP.append(theBilletDict)

        return tableP


    # Create table Q
    def createTableQ(self):
        tableQ = []
        billetNum = self.billetNum
        candidatesNum = self.candidatesNum
        for i in range(billetNum):
            theList = list()
            for j in range(candidatesNum):
                theList.append(self.tableP[i][j])
            random.shuffle(theList)
            random.shuffle(theList)
            theDict = dict()
            for k in range(candidatesNum):
                theDict[k] = theList.pop()
            
            tableQ.append(theDict)
        
        return tableQ


    # Create table R
    def createTableR(self):
        # Insert data into Table-R
        tableR =list()
        billetNum = self.billetNum
        candidatesNum = self.candidatesNum
        tableQ = self.tableQ
        tableP = self.tableP
        for i in range(billetNum):
            for j in range(candidatesNum):
                # q is scrambled row that goes into S
                # w is columne defined by code's column position from P-Table
                w = 0
                tableR.append({'flag':False, 'Qpointer':(i,j), 'Spointer':[i,w]})

        # finding the right row for Spointer
        for i in range(len(tableR)):
            Qpointer = tableR[i]['Qpointer']
            codeInQ = tableQ[Qpointer[0]][Qpointer[1]]
            for j in range(candidatesNum):
                if codeInQ == tableP[Qpointer[0]][j]:
                    column =j
                    tableR[i]['Spointer'][1] = column
                    


        # Scramble the rows of the Spointer
        scramble = [i for i in range(billetNum)]

        for j in range(candidatesNum):
            random.shuffle(scramble)
            counter = 0
            for i in range(len(tableR)):
                if tableR[i]['Spointer'][1] == j:
                    tableR[i]['Spointer'][0] = scramble[counter] 
                    counter = counter + 1 

        random.shuffle(tableR)
        return tableR

    # Now we need to populate Table S
    def createTableS(self):
        tableS = list()
        billetNum = self.billetNum
        candidatesNum = self.candidatesNum
        tableR = self.tableR
        for i in range(billetNum):
            theDict = dict()
            for j in range(candidatesNum):
                theDict[j] = False
            tableS.append(theDict)

        # Check if there is no collisions in S-pointers for table R
        for i in range(self.billetNum*self.candidatesNum):
            x = tableR[i]['Spointer'][0]
            y = tableR[i]['Spointer'][1]
            tableS[x][y] = True
        return tableS

     
scan = Scantegrity(10, 5, 3)
for i in range(len(scan.tableP)):
    print(i, scan.tableP[i])

print()
for j in range(len(scan.tableQ)):
    print(j, scan.tableQ[j])

print()
for k in range(len(scan.tableR)):
    print(k, scan.tableR[k])

print()
for l in range(len(scan.tableS)):
    print(l, scan.tableS[l])
