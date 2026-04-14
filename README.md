# cicspi

`cicspi` is a small SPICE parsing toolbox that reads `.subckt` definitions into a Python object hierarchy and exposes a simple CLI.

## Install

```bash
python3 -m pip install cicspi
```

## CLI

Print the node list for a subckt in a SPICE file:

```bash
cicspi nodes path/to/netlist.spi my_subckt
```

## Python usage

```python
import cicspi

parser = cicspi.SpiceParser()
parser.parseFile("path/to/netlist.spi")

ckt = parser["my_subckt"]
print(ckt.nodes)
print(ckt.instances)
```

## Release flow

PyPI publishing is handled by GitHub Actions in `.github/workflows/release.yml`.
Publishing runs when a GitHub release is published, or manually through `workflow_dispatch`.
