import sys

import cdapython

host = "http://35.192.60.10:8080/"


def run_file(path: str) -> None:
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            print(cdapython.Q(line.rstrip()).run(host=host).to_dataframe())


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == []:
        from cdapython import shell

        shell
    else:
        run_file(sys.argv[1])
