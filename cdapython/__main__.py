import sys

import cdapython

import click

import cdapython.constant_variables as const
from cdapython.utils.utility import columns


@click.group()
def cli():
    pass


@click.command()
def shell():
    from cdapython import shell

    shell


@click.command()
@click.option("--filepath")
def run(filepath: str) -> None:
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            print(cdapython.Q(line.rstrip()).run().to_dataframe())


@click.command()
@click.option("--filter")
def ls_column(filter: str) -> None:
    if filter:
        for i in columns().to_list(filters=filter):
            print(i)
    else:
        for i in columns().to_list():
            print(i)


cli.add_command(shell)
cli.add_command(run)
cli.add_command(ls_column)

if __name__ == "__main__":
    cli()
