import sys

import cdapython


def run_file(path: str) -> None:
    with open(file=path, mode="r", encoding="UTF-8") as file:
        print(cdapython.Q(file.read()).to_json())


def main() -> None:
    args = sys.argv[1:]
    if args == []:
        from cdapython import shell

        shell
    else:
        run_file(sys.argv[1])


if __name__ == "__main__":
    main()
