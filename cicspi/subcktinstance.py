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

import re
import cicspi as spi

class SubcktInstance(spi.SpiceObject):

    def __init__(self,parser=None):
        self.groupName = ""
        self.subcktName = ""
        self.deviceName = ""
        super().__init__(parser)


    def __lt__(self, other):
        return self.name < other.name

    def fromJson(self,o):
        super().fromJson(o)
        self.groupName = o["groupName"]
        self.subcktName = self.prefix + o["subcktName"]
        self.deviceName = o["deviceName"]


    def toJson(self):
        o = super().toJson()
        o["subcktName"] = self.subcktName
        o["groupName"] = self.groupName
        o["deviceName"] = self.deviceName
        return o

    def _setName(self,val):
        re_group = re.compile(r"^([^\d<>]+)(\S+)?$")
        m = re.search(re_group,val)
        if(m):
            self.groupName = m.groups()[0]
            self.groupTag = m.groups()[1]
        self.deviceName = "subckt"
        self.spiceType = "X"
        self.name = val

    def fromSubckt(self,instname,sub):
        self.name = instname
        self.nodes = sub.nodes
        self.subcktName = sub.name


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

        self.nodes = re.split(r"\s+",line)

        #- Last name is model/type
        self.subcktName = self.nodes[-1]
        self.nodes.pop()

        if(self.subcktName not in self.parser.allinst):
            self.parser.allinst[self.subcktName] = 0

        self.parser.allinst[self.subcktName] += 1

        self._setName(self.nodes[0])
        self.nodes.pop(0)
