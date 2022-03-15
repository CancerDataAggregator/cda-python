import sys

import cdapython


def run_file(path):
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line[0] == '#':
                continue
            parts = line.split()
            print(parts)
            cdapython.query(line).run(host="http://localhost:8080")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == []:
        from cdapython import shell

        shell
    else:
        run_file(sys.argv[1])
