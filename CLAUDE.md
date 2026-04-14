# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`cicspi` is a SPICE netlist parsing library and CLI tool. It reads `.subckt` definitions from SPICE files into a Python object hierarchy and exposes a `cicspi nodes <file> <subckt>` CLI command.

## Install and Build

```bash
# Development install
pip install -e .

# Build distribution
make build   # cleans dist/ and runs python3 -m build
```

## Linting

There is no linter configured. The project uses `ruff` in sibling packages — if adding linting, follow that convention.

## Release

Publishing to PyPI is triggered automatically by pushing a git tag. The workflow builds, publishes to PyPI (via OIDC trusted publishing), then creates a GitHub release. To release manually, push a tag:

```bash
git tag 0.x.y && git push origin 0.x.y
```

Version is defined only in `pyproject.toml` — update it there before tagging.

## Architecture

The object model is a shallow hierarchy, all inheriting from `SpiceObject`:

```
SpiceObject          (spiceobject.py)  — base: name, nodes, properties, JSON round-trip
  └─ Subckt          (subckt.py)       — one .subckt/.ends block; holds instances & devices
  └─ SubcktInstance  (subcktinstance.py) — one X-line inside a subckt
  └─ Device          (device.py)       — primitive device (currently minimal)
```

`SpiceParser` (spiceparser.py) is a `dict` subclass that maps subckt names → `Subckt` objects. It buffers lines between `.subckt` and `.ends`, joins continuation lines (`+`), then delegates to `Subckt.parse()`.

`SubcktInstance.parse()` strips CDL-style inline comments (`$...`) and key=value parameters before splitting on whitespace. The last token becomes `subcktName`; the first becomes the instance name (parsed for bus/group prefix).

`Signal` (spiceobject.py) handles bus notation in both `[N]` and `<N>` styles and collapses adjacent indices into `name[stop:start]` ranges via `nodesWithBus()`.

`Subckt.circuits` is a class-level reference to the parser dict, allowing cross-subckt lookups via `Subckt.getSubckt(name)`.

## CLI

Entry point is `cicspi.entry:cli` (Click group). Currently one command:

```bash
cicspi nodes <filename> <subckt>   # prints node list, or error + available subckts
```
