#!/usr/bin/env python3

import re
import cicspi as spi


class Subckt(spi.SpiceObject):

    def __init__(self,parser):
        super().__init__(parser)
        self.instances = list()
        self.inst_index = dict()
        pass

    def parse(self,subckt_buffer,lineNumber):
        self.lineNumber = lineNumber

        firstline = subckt_buffer[0]

        #- Get subckt name
        re_subckt = re.compile("^\s*\.subckt\s+(\S+)",flags=re.I)
        m = re.search(re_subckt,firstline)
        if(m):
            self.name = m.groups()[0]
        else:
            raise Exception("Could not parse subcktname on line %d " % self.lineNumber )

        #- Remove subckt
        firstline = re.sub(re_subckt,"",firstline).strip()


        #- Remove parameters
        re_params =  re.compile("\s+(\S+)\s*=\s*(\S+)")

        #if(m):
            #- TODO: Maybe implement paraemters in future version

        firstline = re.sub(re_params,"",firstline)

        #- Split on space
        self.nodes = re.split("\s+",firstline)

        #- Remove first and last line
        subckt_buffer.pop(0)
        subckt_buffer.pop()

        instLineNumber = lineNumber
        re_ignore = re.compile("(^\s*$)|(^\s*\*)")
        for line in subckt_buffer:
            #- Ignore comments and empty lines
            if(re.search(re_ignore,line)):
                continue

            inst = spi.SubcktInstance(self.parser)
            inst.parse(line,instLineNumber)
            inst.parent = self
            self.instances.append(inst)
            self.inst_index[inst.name] = len(self.instances)-1

        instLineNumber += 1
