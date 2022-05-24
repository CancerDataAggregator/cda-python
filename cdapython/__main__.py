import sys

import cdapython


def run_file(path: str) -> None:
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            print(line.split())
            cdapython.query(line).run()


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == []:
        from cdapython import shell

        shell
    else:
        run_file(sys.argv[1])
