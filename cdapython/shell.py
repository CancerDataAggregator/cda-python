from tdparser.lexer import LexerError
from tdparser.topdown import MissingTokensError

from cdapython.Q import Q
from cdapython.utility import query

try:
    import readline
except ImportError:
    raise ImportError()


"""[summary]
    add's history to shell in current session
"""
new = True
setServer = None


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

    if text == "exit()":
        break
    if text == "clear()":
        print("\n" * 100)
        continue
    if text == "server()":
        setServer = input("Enter your server ")
        continue
    try:
        result: Q = query(text=text)
        if setServer == None:
            queryResult = result.run()
        else:
            queryResult = result.run(host=setServer)
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
