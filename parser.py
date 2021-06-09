import re 
import collections
from cdapython import Q
AND = r'(?P<AND>(((\s|\))(AND|and)(\s|\())))'
OR = r'(?P<OR>(((\s|\))(OR|or)(\s|\())))'
SUBQUERY = r'(?P<SUBQUERY>(((\s|\))(SUBQUERY|subquery)(\s|\())))'
NOT  = r'(?P<NOT>(((\s|\))(NOT|not)(\s|\())))'
LPAREN  = r'(?P<LPAREN>(\())'
RPAREN  = r'(?P<RPAREN>(\)))'
# WS      = r'(?P<WS>\s+)'
TERM = r'(?P<TERM>([\w\.\s="]+))'


main_pattern = re.compile("|".join([OR,TERM]))
Token = collections.namedtuple('Token', ['type', 'value'])
def generate_tokens(pattern,text):
    scanner = pattern.scanner(text)

    for m in iter(scanner.match,None):
        token = Token(m.lastgroup, m.group())

        if token.type != "WS":
            yield token

class ExpressionEvaluator:
    '''
    Implementation of a recursive descent parser.

    Each method implement a single grammar rule.
    It walks from left to right over grammar rule.
    It either consume the rule a generate a syntax error

    Use the ._accept() method to test and accept look ahead token.
    Use the ._expect() method to exactly match and discard the next token on the input.
        or raise a SyntaxError if it doesn't match
    '''
    def parse(self,text):
        self.tokens = generate_tokens(main_pattern,text)
        self.current_token = None
        self.next_token = None
        self._advance()
        return self.expr()

    def _advance(self):
        self.current_token, self.next_token = self.next_token, next(self.tokens,None)
        print(self.tokens)

    def _accept(self,token_type):
        if(self.next_token and self.next_token.type == token_type):
            self._advance()
            return True
        else:
            return False

    def expr(self):
        expr_value = self.term()

        while self._accept("SUBQUERY"):

            operation = self.current_token.type

            if(operation == "SUBQUERY"):
                self._advance()
                expr_value = Q().From(self.expr())
        return expr_value

    def _expect(self,token_type):
        if not self._accept(token_type):
            raise SyntaxError("Expected" + token_type)

    def term(self):
        firstQuery = None 
        term_value = self.factor()
        # TODO add SQL NOT in while check
        while self._accept("AND") or self._accept("OR"):
            operation = self.current_token.type

            if(operation == 'AND'):
                firstQuery = self.factor()
                self._advance()
                term_value = firstQuery.And(self.expr())
            elif(operation == "OR"):
                firstQuery = self.factor()
                self._advance()
                term_value = firstQuery.OR(self.expr())
            else:
                raise SyntaxError('Should not arrive here ' + operation)
        return term_value

    def factor(self):

        if(self._accept("LPAREN")):
            expr_value = self.expr()

            self._expect("RPAREN")

            return expr_value
        else:
            self._advance()
            result = str(self.current_token.value)
            return Q(result)
        
        
e = ExpressionEvaluator()

print("parse 2",e.parse('ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" OR ResearchSubject.Diagnosis.tumor_stage = "Stage IV" ').run())







