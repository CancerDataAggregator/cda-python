from rich import print
from rich.console import Console
from tdparser.lexer import LexerError
from tdparser.topdown import MissingTokensError

from cdapython.Q import Q
from cdapython.utils.utility import query

try:
    import readline
except ImportError:
    raise ImportError()


"""[summary]
    add's history to shell in current session
"""
new = True
setServer = None
setDataFrame = None
console = Console(record=True)


def help() -> None:
    print(
        """
        Welcome to Q shell's help utility
        how to use Q shell
        Enter in a Query without Single quotes Q only supports Double quotes
        Example
        ResearchSubject.id = "Enter Value"
        Functions
        help()
        exit()
        clear()
        server() set the server
        DataFrame()
        \n
        """
    )


while True:
    if new is True:
        help()
        new = False
    text = input("Q > ")
    if text == "help()":
        help()
        continue

    if text == "exit()" or text == "exit":
        break
    if text == "clear()":
        print("\n" * 100)
        continue
    if text == "server()":
        setServer = console.input("Enter your server ")
        continue
    if text == "DataFrame()":
        setDataFrame = True
        continue
    try:
        result: Q = Q(text)
        if setServer == None:
            queryResult = result.run()
        else:
            queryResult = result.run(host=setServer)

        if setDataFrame:
            queryResult = queryResult.to_dataframe()
        print(type(result), queryResult)
    except AttributeError as e:
        print(e)
    except ValueError as e:
        print(e)
    except TypeError as e:
        print(e)
    except LexerError as e:
        print(e)
    except IndexError as e:
        print(e)
    except MissingTokensError as e:
        print(e)
