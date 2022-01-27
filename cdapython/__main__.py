import sys

import cdapython


def run_file(path):
    with open(path) as f:
        cdapython.query(f.read()).run()


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == []:
        from cdapython import shell

        shell
    else:
        run_file(args[0])
