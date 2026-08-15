#!/usr/bin/env python3

import re
import cicspi as spi


class Subckt(spi.SpiceObject):

    circuits = None

    def getSubckt(name:str):

        if(Subckt.circuits is not None):
            if(name in Subckt.circuits):
                return Subckt.circuits[name]
        return None

    def __init__(self,parser=None):
        super().__init__(parser)
        self.instances = list()
        self.devices = list()
        self.inst_index = dict()
        if(Subckt.circuits is None and parser is not None):
            Subckt.circuits = parser
        pass

    def getInstance(self,key):

        if key in self.inst_index:
            return self.instances[self.inst_index[key]]
        elif key.upper() in self.inst_index:
            return self.instances[self.inst_index[key.upper()]]
        elif key.lower() in self.inst_index:
            return self.instances[self.inst_index[key.lower()]]
        else:
            return None

    def getInstances(self,regex):

        insts = list()
        for key in self.inst_index:
            #print(key)
            if(re.search(regex,key,re.I)):
                insts.append(self.instances[self.inst_index[key]])
        return insts

    
    def fromJson(self,o):
        super().fromJson(o)

        #- Override name to support prefix
        self.name = self.prefix + o["name"]

        for d in o["devices"]:
            dd = spi.Device()
            dd.fromJson(d)
            self.devices.append(dd)
            pass

        for i in o["instances"]:
            ii = spi.SubcktInstance()
            ii.prefix = self.prefix
            ii.fromJson(i)
            self.instances.append(ii)
            pass

    def toJson(self):
        o = super().toJson()


        o["devices"] = []
        for d in self.devices:
            o["devices"].append(d.toJson())
        o["instances"] = []
        for i in self.instances:
            o["instances"].append(i.toJson())
        return o

    def orderInstancesByGroup(self):

        instList = list()
        groups = dict()
        for i in sorted(self.instances,key=lambda x: x.name):
            group = i.groupName
            if(group not in groups):
                groups[group] = list()
            groups[group].append(i)

        for g in sorted(groups):
            arr = sorted(groups[g])
            instList += arr

        return instList

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

        instLineNumber = lineNumber + 1
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
            ss += inst.name + " " + " ".join(inst.nodes) + " " +  inst.subcktName + "\n"
        ss += ".ends " + self.name
        return ss
