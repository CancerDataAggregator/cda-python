"""
This module is made as a repl for Q 
"""
from typing import Any, Dict, Union

from rich import print
from rich.console import Console

from cdapython.Q import Q
from cdapython.Q_parser import LexerError, MissingTokensError
from cdapython import columns, unique_terms


try:
    import readline  # pylint: disable=W0611
except ImportError:
    raise ImportError()


"""[summary]
    add's history to shell in current session
"""
new: bool = True
setServer: Union[str, None] = None
setDataFrame: Union[bool, None] = None
console: Console = Console(record=True)
setTable: Union[str, None] = None
setDebug: bool = False


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
        table()
        col()
        debug()
        DataFrame()
        \n
        """
    )


while True:
    if new is True:
        help()
        print(
            f"""Q {Q.get_version()} Type "help()",
            "copyright", "credits" or "license" for more information."""
        )
        new = False
    text: str = input(">>> ")
    if text == "help()":
        help()
        continue
    if text == "col()":
        print(columns().df_to_table())
        continue
    if text == "unique()":
        value = input("Enter term ")
        print(unique_terms(value).df_to_table())
        continue
    if text == "exit()" or text == "exit":
        break
    if text == "clear()":
        print("\n" * 100)
        continue
    if text == "server()":
        setServer = console.input("Enter your server ")
        continue
    if text == "table()":
        setServer = console.input("Enter your table ")
    if text == "DataFrame()":
        setDataFrame = True
        continue
    if text == "debug()":
        setDebug = True
        continue
    try:
        result: Q = Q(text)
        if setDebug:
            print(result.to_json())
        if setServer is None:
            queryResult = result.run()
        else:
            queryResult = result.run(host=setServer, table=setTable)

        if setDataFrame:
            print(queryResult.df_to_table())
        else:
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
