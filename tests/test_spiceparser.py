"""The synthetic TOP is `parser.top`, never an entry in the parser.

Every standard-cell library in cicpy's parity corpus names its top cell
TOP. When the parser's synthetic top level took that name, it overwrote
a real `.subckt TOP`, or stood in for one written inline in the object
file. Either way cicpy built TOP with no instances and dropped the rest
of the library.
"""
import os
import tempfile
import unittest

from cicspi import SpiceParser


def _write(d, name, text):
    path = os.path.join(d, name)
    with open(path, "w") as f:
        f.write(text)
    return path


REAL_TOP = """
.subckt INV A Y VDD VSS
M1 Y A VDD VDD pch
M2 Y A VSS VSS nch
.ends
.subckt TOP A Y VDD VSS
X1 A B VDD VSS INV
X2 B Y VDD VSS INV
.ends
"""

TOP_LEVEL = """
.subckt BUF A Y VDD VSS
X1 A B VDD VSS INV
X2 B Y VDD VSS INV
.ends
xdut IN OUT VDD VSS BUF
"""


class SyntheticTop(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_real_top_survives(self):
        p = SpiceParser()
        p.parseFile(_write(self.tmp.name, "a.spi", REAL_TOP))
        self.assertEqual(len(p["TOP"].instances), 2)

    def test_real_top_survives_a_later_file(self):
        #- one parser, several files: the order cicpy reads them in
        p = SpiceParser()
        p.parseFile(_write(self.tmp.name, "a.spi", REAL_TOP))
        p.parseFile(_write(self.tmp.name, "b.spi", TOP_LEVEL))
        self.assertEqual(len(p["TOP"].instances), 2)

    def test_real_top_replaces_an_earlier_synthetic(self):
        p = SpiceParser()
        p.parseFile(_write(self.tmp.name, "b.spi", TOP_LEVEL))
        p.parseFile(_write(self.tmp.name, "a.spi", REAL_TOP))
        self.assertEqual(len(p["TOP"].instances), 2)

    def test_synthetic_top_is_not_a_cell(self):
        #- the top level is p.top; the dict is the real subcircuits
        p = SpiceParser()
        p.parseFile(_write(self.tmp.name, "b.spi", TOP_LEVEL))
        self.assertNotIn("TOP", p)
        self.assertEqual([i.name for i in p.top.instances], ["xdut"])

    def test_a_library_does_not_claim_top(self):
        #- a library file has no top level; an empty synthetic TOP in
        #- the dict made cicpy skip a TOP netlist written inline in the
        #- object file (REY_ATR in the parity corpus)
        p = SpiceParser()
        p.parseFile(_write(self.tmp.name, "lib.spi", REAL_TOP.replace(
            ".subckt TOP", ".subckt BUF")))
        self.assertIsNone(p.get("TOP"))

    def test_path_walks_the_top_level_not_the_cell(self):
        #- a real TOP holds the name, the path still starts at the
        #- file's own top level
        p = SpiceParser()
        p.parseFile(_write(self.tmp.name, "a.spi", REAL_TOP))
        p.parseFile(_write(self.tmp.name, "b.spi", TOP_LEVEL))
        inst, found = p.getPathInstance(["xdut", "X2"])
        self.assertIsNotNone(inst)
        self.assertEqual(found, "xdut.X2")


if __name__ == "__main__":
    unittest.main()
