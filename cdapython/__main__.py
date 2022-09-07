import click

import cdapython
import cdapython.constant_variables as const

from cdapython.utils.utility import columns


@click.group()
def cli() -> None:
    pass


@click.command()
def shell() -> None:
    from cdapython import shell as Qshell

    Qshell


@click.command()
@click.option("--filepath")
def run(filepath: str) -> None:
    with open(filepath, "r") as file:
        for line in file:
            line_new: str = line.strip()
            if not line_new or line_new[0] == "#":
                continue
            print(cdapython.Q(line_new.rstrip()).run().to_dataframe())


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


def main() -> None:
    cli.main()


if __name__ == "__main__":
    main()
