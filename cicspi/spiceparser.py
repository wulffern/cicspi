#!/usr/bin/env python3
#
import re
import cicspi as spi


class SpiceParser(dict):

    def __init__(self):
        self.allinst = dict()
        pass

    def _parseSubckt(self,line_number,subckt_buffer):
        ckt = spi.Subckt(self)
        ckt.parse(subckt_buffer,line_number)
        self[ckt.name] = ckt

    def getPathInstance(self,path):

        top = self["TOP"]
        iname = path.pop(0)
        inst = top.getInstance(iname)
        if(inst):
            (inst,subpath) = inst.getPathInstance(path)
            foundpath = iname
            if(subpath is not None):
                foundpath = iname + "." + subpath

            return (inst, foundpath)
        else:
            return (None,iname)

    def parseFile(self,filename,includeLocal=False,not_subckt_buffer = None):
        #- NOT `= list()`. A default argument is evaluated once, at
        #- definition, so every SpiceParser in the process shared ONE
        #- buffer and TOP accumulated across files: parse a.spi then
        #- b.spi and b's TOP came back holding a's instances too
        #- (measured). cicpy parses more than one netlist per process in
        #- several flows, so this was reachable, not theoretical.
        #-
        #- It doubles as the marker for who owns TOP. An .include
        #- recurses with the SAME buffer, and only the outermost call
        #- may close it -- otherwise the include wraps its own
        #- `.subckt TOP` around a half-collected buffer and the caller
        #- then wraps another around that.
        outermost = not_subckt_buffer is None
        if(not_subckt_buffer is None):
            not_subckt_buffer = list()
        subckt_buffer = list()
        with open(filename) as fi:

            is_subckt = False
            is_control= False
            re_subckt_start = re.compile(r"^\s*\.subckt",re.I)
            re_subckt_end = re.compile(r"^\s*\.ends",re.I)
            re_include = re.compile(r"^\s*\.include\s+(.*)$",re.I)
            re_ignore = re.compile(r"^\s*(\.|\*|\s*$)",re.I)
            re_control_start = re.compile(r"^\s*\.control",re.I)
            re_control_end = re.compile(r"^\s*\.endc",re.I)
            re_plus = re.compile(r"^\s*\+")
            line_number = 0

            for l in fi:
                line = l.strip()
                line_number +=1

                #print(line)
                if(includeLocal and not is_subckt):
                    m =  re.search(re_include,line)
                    if(m):
                        finc = m.groups()[0]
                        if("pdk" not in finc):
                            #- includeLocal is the SECOND argument; passing
                            #- the buffer here put a list where the flag
                            #- goes and left the buffer on its default
                            self.parseFile(finc,includeLocal,not_subckt_buffer)
                            #print(finc)


                # Handle plus
                if(re.search(re_plus,l)):
                    #- A continuation outside a subckt is legal now that
                    #- top-level lines are collected too, so it extends
                    #- whichever buffer is being filled -- but there must
                    #- be a line to continue, or [-1] raises IndexError.
                    buf = subckt_buffer if is_subckt else not_subckt_buffer
                    if(not buf):
                        raise Exception("Continuation line with nothing to continue on line %d " % line_number)
                    buf[-1] += re.sub(re_plus,"",line)
                    continue

                if(re.search(re_subckt_start,line)):
                    is_subckt = True
                    subckt_buffer.clear()

                if(re.search(re_control_start,line)):
                    is_control = True


                if(is_subckt):
                    subckt_buffer.append(line)
                else:
                    if(not is_control):
                        if(not re.search(re_ignore,line)):
                            not_subckt_buffer.append(line)



                if(re.search(re_control_end,line)):
                    is_control = False


                if(re.search(re_subckt_end,line)):
                    is_subckt = False
                    self._parseSubckt(line_number,subckt_buffer)

        #- everything that sat outside a .subckt becomes one, named TOP,
        #- so the file's own top level can be asked for its instances
        #- like any other cell. A cell genuinely called TOP is
        #- overwritten by this -- worth knowing before naming one.
        if(outermost):
            not_subckt_buffer.insert(0,".subckt TOP")
            not_subckt_buffer.append(".ends")
            self._parseSubckt(0,not_subckt_buffer)
