#!/usr/bin/env python3
import re
import cicspi as spi

class SubcktInstance(spi.SpiceObject):

    def __init__(self):
        self.groupName = ""
        super().__init__()


    def _setName(self,val):
        re_group = re.compile("^([^\d<>]+)(\S+)?$")
        m = re.search(re_group,val)
        if(m):
            self.groupName = m.groups()[0]
            self.groupTag = m.groups()[1]
        self.deviceName = "subckt"
        self.spiceType = "X"

    def parse(self,line,lineNumber):
        self.lineNumber = lineNumber
        self.spiceStr = line

        #- Remove parameters
        re_params =  re.compile("(\s+(\S+)\s*=\s*(\S+))+")
        m = re.search(re_params,line)
        if(m):
            #- TODO fix parameter read
            pass
            #for match in m.groups():
            #    print(match)

        line = re.sub(re_params,"",line)

        self.nodes = re.split("\s+",line)

        self.name = self.nodes[0]
        self.nodes.pop(0)
