import sys

import cdapython

import click

import cdapython.constant_variables as const


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


cli.add_command(shell)
cli.add_command(run)

if __name__ == "__main__":
    cli()
