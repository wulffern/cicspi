#!/usr/bin/env python3
import re
import cicspi as spi

class SubcktInstance(spi.SpiceObject):

    def __init__(self,parser):
        self.groupName = ""
        super().__init__(parser)


    def __lt__(self, other):
        return self.name < other.name


    def _setName(self,val):
        re_group = re.compile(r"^([^\d<>]+)(\S+)?$")
        m = re.search(re_group,val)
        if(m):
            self.groupName = m.groups()[0]
            self.groupTag = m.groups()[1]
        self.deviceName = "subckt"
        self.spiceType = "X"

    def fromSubckt(self,instname,sub):

        self.name = instname
        self.nodes = sub.nodes
        self.instanceType = sub.name


    def parse(self,line,lineNumber):
        self.lineNumber = lineNumber
        self.spiceStr = line

        re_params_cdl = re.compile(r"\s*\$.*$")
        line = re.sub(re_params_cdl,"",line)


        #- Remove parameters
        re_params =  re.compile(r"(\s+(\$|\S+)\s*=\s*(\S+))+")
        m = re.search(re_params,line)
        if(m):
            #- TODO fix parameter read
            pass
            #for match in m.groups():
            #    print(match)

        line = re.sub(re_params,"",line)

        #print(line)

        self.nodes = re.split(r"\s+",line)

        #- Last name is model/type
        self.instanceType = self.nodes[-1]
        self.nodes.pop()

        if(self.instanceType not in self.parser.allinst):
            self.parser.allinst[self.instanceType] = 0

        self.parser.allinst[self.instanceType] += 1

        self.name = self.nodes[0]
        self.nodes.pop(0)
