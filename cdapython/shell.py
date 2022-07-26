from rich import print
from rich.console import Console
from tdparser.lexer import LexerError
from tdparser.topdown import MissingTokensError

from cdapython.Q import Q


class Environ:
    def __init__(self, parent=None):
        self.env = {}
        self.parent = parent

    def get(self, item):
        if item in self.env:
            return self.env[item]
        if self.parent is not None:
            return self.parent.get(item)
        return None

    def insert(self, item, value):
        self.env[item] = value

    def update(self, item, value):
        curr = self
        while curr is not None:
            if item in curr.env:
                curr.env[item] = value
                return
            curr = curr.parent
        self.env[item] = value

    def __getattr__(self, item):
        # for example use io as IO, search only in self
        # and not in parent
        return self.env[item]

    def __repr__(self):
        rep = "{}".format(self.env)
        parent = self.parent
        while parent:
            rep += "\n" + parent.__repr__()
            parent = parent.parent
        return rep


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
        print(
            f'Q {Q.get_version()} Type "help()", "copyright", "credits" or "license" for more information.'
        )
        new = False
    text = input("Q >>> ")
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
