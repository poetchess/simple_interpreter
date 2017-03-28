#Token types
#EOF token is used to indicate that there is no more input left for lexical
#analysis

INTEGER, OPERATOR, EOF = 'INTEGER', 'OPERATOR', 'EOF'

class Token(object):

    def __init__(self, type, value):
        #token type: INTEGER, PLUS, EOF
        self.type = type
        #token valueL: 0~9, '+', or None
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

    def error(self):
        raise Exception('Error paring input')

    def escape_white_space(self):
        text = self.text
        text_len = len(text)
        while self.pos < text_len and text[self.pos].isspace():
            self.pos += 1

    def get_digits(self):
        digits = ''
        text = self.text
        text_len = len(text)
        while self.pos < text_len and text[self.pos].isdigit():
            digits += text[self.pos]
            self.pos += 1
        return digits

    def get_next_token(self):
        """
            Lexical analyzer (aka scanner or tokenizer)
            This method is responsible for breaking a sentence apart into 
            tokens. One token at a time.
        """
        text = self.text

        self.escape_white_space()

        #Check if self.pos index past the end of the self.text.
        #If so, return EOF token because there is no more input left to convert
        #into tokens
        if self.pos > len(text) -1:
            return Token(EOF, None)

        #Get a character at the position self.pos and decide what token to 
        #create based on the single char.
        current_char = text[self.pos]

        #If the char is a digit, convert it to integer, create an INTEGER token,
        #increment self.pos index to point to the next char after the digit,
        #and return the INTEGER token.
        if current_char.isdigit():
            digits = self.get_digits()
            token = Token(INTEGER, int(digits))
            return token

        if current_char in ['+', '-', '*', '/']:
            token = Token(OPERATOR, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        #Compare the current token type with the passed (expected) 
        #token type and if they match, 'eat' the current token and
        #assign the next token to the self.current_token, otherwise
        #raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        '''expr -> INTEGET PLUS INTEGER'''
        #Set current token to the first token taken from the input.
        self.current_token = self.get_next_token()

        #Expect the current token to be a single-digit integer.
        left = self.current_token
        self.eat(INTEGER)

        result = left.value

        while self.current_token.type != EOF:
            #Expect the current token to be an operator token.
            op = self.current_token
            self.eat(OPERATOR)

            #Expect the current token to be a single-digit integer.
            right = self.current_token
            self.eat(INTEGER)

            #At this point, self.current_token is set to EOF token.
            #And INTEGER OPERATOR INTEGER sequence of tokens has been successfully 
            #found and the method can just return the result of adding two 
            #integers, thus effectively interpreting client input.
            if op.value == '+':
                result += right.value
            elif op.value == '-':
                result -= right.value
            elif op.value == '*':
                result *= right.value
            elif op.value == '/':
                result /= right.value

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
