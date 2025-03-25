######################################################################
##        Copyright (c) 2025 Carsten Wulff Software, Norway
## ###################################################################
## Created       : wulff at 2025-3-25
## ###################################################################
##  The MIT License (MIT)
##
##  Permission is hereby granted, free of charge, to any person obtaining a copy
##  of this software and associated documentation files (the "Software"), to deal
##  in the Software without restriction, including without limitation the rights
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##  copies of the Software, and to permit persons to whom the Software is
##  furnished to do so, subject to the following conditions:
##
##  The above copyright notice and this permission notice shall be included in all
##  copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##  SOFTWARE.
##
######################################################################
import json
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
    def __init__(self,parser=None):
        self.deviceName = ""
        self.name = ""
        self.classname = ""
        self.lineNumber = -1
        self.spiceType = "unknown"
        self.spiceStr = list()
        self.nodes = list()
        self.properties = dict()
        self.prefix = ""
        self.children = list()
        self.parser = parser
        self.parent = None
        self.sbuffer = list()

        pass

    def fromJson(self,o):
        self.classname = o["class"]
        self.name = o["name"]
        self.nodes = o["nodes"]
        self.properties = o["properties"]

    def toJson(self):
        o = dict()
        o["class"] = self.classname
        o["name"] = self.name
        o["nodes"] = self.nodes
        o["properties"] = self.properties
        return o

    def printToJson(self):
        print(json.dumps(self.toJson(),indent=4))


    def isCktInstance(self):
        return self.isType("SubcktInstance")

    def isSubcktInstance(self):
        return self.isType("SubcktInstance")

    def isDevice(self):
        return self.isType("Device")


    def __repr__(self):
        return f"{self.classname} {self.name}: nodes = {self.nodes}, props = {self.properties}"



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
