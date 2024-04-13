#!/usr/bin/env python3

import re
import cicspi as spi


class Subckt(spi.SpiceObject):

    def __init__(self,parser=None):
        super().__init__(parser)
        self.instances = list()
        self.inst_index = dict()
        pass

    def makeInstGroupSubckt(self,startswith):
        sub = Subckt(self.parser)
        sub.name = self.name + "_" + startswith
        instnodes = dict()
        rmlist = list()
        for inst in self.instances:
            if(inst.name.startswith(startswith)):
                for n in inst.nodes:
                    instnodes[n] = 0
                sub.addInstance(inst)
                #print(inst.name)
                rmlist.append(inst)
                #self.instances.remove(inst)

        for rm in rmlist:
            print(rm)
            self.instances.remove(rm)

        sub.nodes = instnodes.keys()
        self.parser[sub.name] = sub
        ninst = spi.SubcktInstance(self.parser)
        ninst.fromSubckt(startswith,sub)
        self.addInstance(ninst)
        return sub

    def addInstance(self,inst):
        inst.parent = self
        self.instances.append(inst)
        self.inst_index[inst.name] = len(self.instances)-1

    
    def parse(self,subckt_buffer,lineNumber):
        self.lineNumber = lineNumber

        firstline = subckt_buffer[0]

        #- Get subckt name
        re_subckt = re.compile(r"^\s*\.subckt\s+(\S+)",flags=re.I)
        m = re.search(re_subckt,firstline)
        if(m):
            self.name = m.groups()[0]
        else:
            raise Exception("Could not parse subcktname on line %d " % self.lineNumber )

        #- Remove subckt
        firstline = re.sub(re_subckt,"",firstline).strip()


        #- Remove parameters
        re_params =  re.compile(r"\s+(\S+)\s*=\s*(\S+)")

        #if(m):
            #- TODO: Maybe implement paraemters in future version

        firstline = re.sub(re_params,"",firstline)

        #- Split on space
        self.nodes = re.split(r"\s+",firstline)

        #- Remove first and last line
        subckt_buffer.pop(0)
        subckt_buffer.pop()

        instLineNumber = lineNumber
        re_ignore = re.compile(r"(^\s*$)|(^\s*\*)")
        for line in subckt_buffer:
            #- Ignore comments and empty lines
            if(re.search(re_ignore,line)):
                continue

            inst = spi.SubcktInstance(self.parser)
            inst.parse(line,instLineNumber)
            self.addInstance(inst)

        instLineNumber += 1

    def tospice(self):
        ss = ".subckt " + self.name + " "+ " ".join(self.nodes) + "\n"
        for inst in sorted(self.instances):
            ss += inst.name + " " + " ".join(inst.nodes) + " " +  inst.instanceType + "\n"
        ss += ".ends " + self.name
        return ss
