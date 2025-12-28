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


    def parseFile(self,filename):
        subckt_buffer = list()
        with open(filename) as fi:

            is_subckt = False
            re_subckt_start = re.compile(r"^\s*\.subckt",re.I)
            re_subckt_end = re.compile(r"^\s*\.ends",re.I)
            re_plus = re.compile(r"^\s*\+")
            line_number = 0
            for l in fi:
                line = l.strip()
                line_number +=1

                # Handle plus
                if(re.search(re_plus,l)):
                    line = re.sub(re_plus,"",line)
                    subckt_buffer[-1] += line
                    continue

                if(re.search(re_subckt_start,line)):
                    is_subckt = True
                    subckt_buffer.clear()

                if(is_subckt):
                    subckt_buffer.append(line)

                if(re.search(re_subckt_end,line)):
                    is_subckt = False
                    self._parseSubckt(line_number,subckt_buffer)
