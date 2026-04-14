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

# SpiceParser is a dict: subckt name → Subckt object
ckt = parser["my_subckt"]

print(ckt.nodes)        # list of port node names
print(ckt.instances)    # list of SubcktInstance objects

# Collapse bus signals (e.g. A[0], A[1] → A[0:1])
print(ckt.nodesWithBus())

# Iterate instances
for inst in ckt.instances:
    print(inst.name, inst.subcktName, inst.nodes)

# Emit SPICE text
print(ckt.tospice())

# JSON round-trip
import json
print(json.dumps(ckt.toJson(), indent=2))
```

### Object model

| Class | Description |
|---|---|
| `SpiceParser` | `dict` subclass; maps subckt name → `Subckt`. Also tracks all instance types in `.allinst`. |
| `Subckt` | One `.subckt`/`.ends` block. Has `.name`, `.nodes`, `.instances` (list of `SubcktInstance`), `.devices`. |
| `SubcktInstance` | One `X`-line. Has `.name`, `.subcktName`, `.nodes`, `.groupName`. |
| `Device` | Primitive device (future use). |
| `SpiceObject` | Base class for all objects; provides `.properties` dict, JSON serialisation, and `.nodesWithBus()`. |

## Release flow

PyPI publishing is handled by GitHub Actions in `.github/workflows/release.yml`.
Push a tag to trigger a release:

```bash
git tag 0.x.y && git push origin 0.x.y
```

The workflow builds the package, publishes to PyPI via OIDC trusted publishing, and creates a GitHub release with the distribution artifacts attached.
