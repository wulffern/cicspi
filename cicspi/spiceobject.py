#!/usr/bin/env python3


class SpiceObject:

    def __init__(self):
        self.deviceName = ""
        self.name = ""
        self.lineNumber = -1
        self.spiceType = "unknown"
        self.spiceStr = list()
        self.nodes = list()
        self.properties = dict()
        self.prefix = ""
        self.children = list()
        pass
