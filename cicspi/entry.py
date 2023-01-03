#!/usr/bin/env python3

import cicspi
import sys
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename")
@click.argument("subckt")
def nodes(filename,subckt):
    spi = cicspi.SpiceParser()
    spi.parseFile(filename)
    if(subckt in spi):
        ckt = spi[subckt]
        for l in ckt.nodes:
            print(l)
    else:
        print(f"Error: {subckt} not found")
        for name in spi:
            print(name)



if __name__ == "__main__":
    cli()
