
from tdparser.topdown import MissingTokensError
from cdapython.Q import Q
from cdapython.Qparser import parser
from tdparser.lexer import LexerError
import readline

"""[summary]
    add's history to shell in current session
"""
new = True


def help():
    print("""
        Welcome to Q shell's help utility
        how to use Q shell
        Enter in a Query without Single quotes Q only supports Double quotes
        Example
        ResearchSubject.id = "Enter Value"
        Functions
        help()
        exit()
        clear()
        \n
        """)


while True:
    if(new is True):
        help()
        new = False
    text = input('Q > ')
    if(text == "help()"):
        help()
        continue

    if(text == "exit()"):
        break
    if (text == "clear()"):
        print("\n" * 100)
        continue
    try:
        result: Q = Q(text)
        print(result)
        queryResult = result.run()
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

