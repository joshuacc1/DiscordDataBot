
class xtof():
    def __init__(self,sin,sout):
        self.sin=sin if sin else set()
        self.sout=sout if sout else set()

    def trigger(self,s):
        if not isinstance(s,set): return set()
        sint=s.intersection(self.sin) if s.issubset(self.sin) else set()
        sdiff=s.isdisjoint(self.sout) if s.isdisjoint(self.sout) else set()
        sdisj=self.sin.difference(s)

        if s.issubset(self.sin):
            return xtof(sdisj,self.sout)

class ftox():
    def __init__(self,pot=None):
        self.pot=pot if pot else []

    def addtopot(self,ing):
        if isinstance(ing,xtof):
            self.pot.append(ing)

    def f(self,x):
        res=[]
        for ing in self.pot:
            if ing.trigger(x):
                res.append(ing.trigger(x))
        newff=ftox(pot=res)
        return newff

    def printdata(self):
        import pprint
        pprint.pprint([[x.sin,x.sout] for x in self.pot])


if __name__ == "__main__":
    f = open("../Data/Police_Shootings_By_Race.csv",'r')
    header = f.readline()
    header=header.split(',')
    year=header.pop(0)
    ff=ftox()
    for line in f.readlines():
        linearr = line.split(',')
        for hind in range(len(header)):
            new=xtof({"Date",header[hind],linearr[0] + "-1-1"},{linearr[hind+1]})
            ff.addtopot(new)

    f = open("../Data/csvData.csv",'r')
    # for i in range(1,16):
    #     f.readline()

    header=f.readline()
    header=header.strip("\n")
    header = header.split(',')
    header = [x.strip() for x in header]
    year = header.pop(0)
    firstline=f.readline()
    for line in f.readlines():
        line=line.strip("\n")
        line=line.strip()
        linearr = line.split(',')
        date=linearr[0]
        date=date.split("-")
        for hind in range(len(header)):
            new=xtof({"Date",header[hind].replace('"',''),linearr[0].replace('"','')  + "-1-1"},{linearr[hind+1].replace('"','')})
            ff.addtopot(new)