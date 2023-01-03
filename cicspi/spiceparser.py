#!/usr/bin/env python3
#
import re

import cicspi as spi


class SpiceParser(dict):

    def __init__(self):
        pass

    def _parseSubckt(self,line_number,subckt_buffer):
        ckt = spi.Subckt()
        ckt.parse(subckt_buffer,line_number)
        self[ckt.name] = ckt


    def parseFile(self,filename):
        subckt_buffer = list()
        with open(filename) as fi:

            is_subckt = False
            re_subckt_start = re.compile("^\s*\.subckt",re.I)
            re_subckt_end = re.compile("^\s*\.ends",re.I)
            re_plus = re.compile("^\s*\+")
            line_number = 0
            for l in fi:
                line = l.strip()
                line_number +=1

                # Handle plus
                if(re.search(re_plus,l)):
                    line = line.replace(re_plus,"")
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
