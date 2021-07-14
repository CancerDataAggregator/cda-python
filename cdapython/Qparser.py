import re
import collections
AND = r'(?P<AND>((\s|\))(AND|and)(\s|\()))'
OR = r'(?P<OR>((\s|\))(OR|or)(\s|\()))'
SUBQUERY = r'(?P<SUBQUERY>((\s|\))(SUBQUERY|subquery)(\s|\()))'
NOT  = r'(?P<NOT>((\s|\))(NOT|not)(\s|\()))'
LPAREN  = r'(?P<LPAREN>\()'
RPAREN  = r'(?P<RPAREN>\))'
EQUALS = r'(?P<EQUALS>\w+=\w+)'
WS      = r'(?P<WS>\s+)'


main_pattern = re.compile("|".join((AND,OR,SUBQUERY,NOT,LPAREN, RPAREN,EQUALS,WS)))
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(pattern,text):
    print(type(text))
    scanner = pattern.scanner(text)

    for m in iter(scanner.match,None):
        token = Token(m.lastgroup, m.group())
        print(token)
        if token.type != "WS":
            yield token

class parser():
    def __init__(self,text):
        self.tokens = generate_tokens(main_pattern,text)
        self.current_token = None
        self.next_token = None
        self._advance()
        return self.expr()

    def _advance(self):
        self.current_token, self.next_token = self.next_token, next(self.tokens,None)

    def _accept(self,token_type:main_pattern) -> bool:
        """[summary]

        Args:
            token_type ([type]): [description]

        Returns:
            bool: [description]
        """
        if self.next_token and self.next_token.type == token_type:
            self._advance()
            return True
        else:
            return False
    
    def _expect(self,token_type):
        if not self._accept(token_type=token_type):
            raise SyntaxError(f"Expected {token_type}")
    def expr(self):
        '''
        expression ::= term { (+|-) term} *
        '''
        # it first expect a term according to grammer rule
        expr_value = self.term()
    def term(self):
        '''
        term ::= factor { ("*" | '/')} factor *
        '''
        term_value = self.factor()
    
    def factor(self):
        '''
        factor  ::= NUM | (expr)

        '''
        if self._accept("EQUALS"):
             print(self.current_token.value)
             return self.current_token.value
        elif self._accept("LPAREN"):
            expr_value = self.expr()

            self._expect("RPAREN")

            return expr_value
        else:
            raise SyntaxError('Expect NUMBER or LPAREN')
