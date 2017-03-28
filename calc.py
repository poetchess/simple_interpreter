#Token types
#EOF token is used to indicate that there is no more input left for lexical
#analysis

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):

    def __init__(self, type, value):
        #token type: INTEGER, PLUS, MINUS, EOF
        self.type = type
        #token valueL: 0~9, '+', '-', or None
        self.value = value

    def __str__(self):
        """ 
            String representation of the class instance.
            i.e.:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
                type=self.type,
                value=repr(self.value)
                )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):

    def __init__(self, text):
        #client string input, e.g. "3+5"
        self.text = text
        #self.pos in an index into self.text
        self.pos = 0
        #current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    #Lexer code
    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        '''
            Advance the 'pos' pointer and set the 'current_char' variable.
        '''
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None    #indicate end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        '''
            Return a multidigit integer consumed from the input
        '''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def get_next_token(self):
        """
            Lexical analyzer (aka scanner or tokenizer)
            This method is responsible for breaking a sentence apart into 
            tokens. One token at a time.

            Once entered, 'self.pos' points to the char to be processed. 
        """

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    #Parser / Interpreter code
    def eat(self, token_type):
        #Compare the current token type with the passed (expected) 
        #token type and if they match, 'eat' the current token and
        #assign the next token to the self.current_token, otherwise
        #raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        '''
            Return an INTEGER token value
        '''
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        #Set current token to the first token taken from the input.
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()

        return result
            
def main():
    while True:
        try:
            text = raw_input('clac>')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
