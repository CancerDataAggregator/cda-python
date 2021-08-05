from Q import Q
from Qparser import parser
from tdparser.lexer import LexerError

"""[summary]
    add's history to shell in current session
"""
try:
    import readline
except ImportError:
    pass  #readline not available

while True:
    text = input('Q > ')
    if(text == "exit()"):
        break
    if (text == "clear()"):
        print("\n" * 100)
        continue
    try:
        result: Q = parser(str(text).strip())
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

