#!/usr/bin/env python3
import re


class Signal:
    re_bus = re.compile("^(\S+)(\[|<)(\d+)(<|\])$")

    def __init__(self,name):
        self.orgname = name
        self.busstart = 10000
        self.busstop = -1
        m = re.search(Signal.re_bus,name)

        if(m):
            self.name = m.groups()[0]
            self.ind = int(m.groups()[2])
            self.isbus = True
            self.addIndex(self.ind)
        else:
            self.name = name
            self.isbus = False

    def __str__(self):
        if(self.isbus):
            return "%s[%d:%d]" %(self.name,self.busstop,self.busstart)
        else:
            return self.name

    def addIndex(self,ind):
        if(not self.isbus):
            raise Exception("Cannot add bus to a singular signal")

        if(ind <= self.busstart):
            self.busstart = ind
        if(ind >= self.busstop):
            self.busstop = ind

class SpiceObject:



    def __init__(self,parser):
        self.deviceName = ""
        self.name = ""
        self.lineNumber = -1
        self.spiceType = "unknown"
        self.spiceStr = list()
        self.nodes = list()
        self.properties = dict()
        self.prefix = ""
        self.children = list()
        self.parser = parser
        self.parent = None

        pass

    def isType(self,typename):
        if(self.__class__.__name__ == typename):
            return True
        elif(super() and (super().__class__.__name__ == typename)):
            return True
        return False

    def nodesWithBus(self):
        nbus = list()

        isbus = False
        busname = ""
        busstart = 10000
        busstop = -1
        prevsig = None
        for n in sorted(self.nodes):
            sig = Signal(n)

            #- Assume bus if they are the same name
            if(prevsig and prevsig.name == sig.name):
                prevsig.addIndex(sig.ind)
                continue
            else:
                if(prevsig):
                    nbus.append(str(prevsig))
                    prevsig = None

                if(not sig.isbus):
                    nbus.append(str(sig))
                else:
                    prevsig = sig

                

        return nbus
