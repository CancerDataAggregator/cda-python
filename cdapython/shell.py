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
    try:
        result = parser(str(text).strip())
        print(type(result), result.run())

    except AttributeError as e:
        print(e)
    except ValueError as e:
        print(e)
    except TypeError as e:
        print(e)
    except LexerError as e:
        print(e)


