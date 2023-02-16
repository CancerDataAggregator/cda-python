import sys

import cdapython


def run_file(path: str) -> None:
    with open(path, "r", encoding="UTF-8") as file:
        for line in file:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            print(line.split())
            print(cdapython.Q(line).run().df_to_table())


def main() -> None:
    args = sys.argv[1:]
    if args == []:
        from cdapython import shell

        shell
    else:
        run_file(sys.argv[1])


if __name__ == "__main__":
    main()
