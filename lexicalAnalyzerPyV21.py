import sys # access sys command to open a file from the command line
import re # access regular expressions 
from syntaxAnalyzerPyV21 import syntaxAnalyzer # import syntax analyzer function to call at the end

# takes a file from the command line, in readable mode. reads in as a string
with open(sys.argv[1], 'r') as file:
    programContents = file.read().strip()

# create an array to hold all created tokens and lexemes in order
tokenLexeme = []

# puts back together doubled operators / special characters that have been split up
def recreateMultiCharOperators(programContents):
    programContents = programContents.replace('=  =', '==')
    programContents = programContents.replace('!  =', '!=')
    programContents = programContents.replace('/  /', '//')
    programContents = programContents.replace('/  *', '/*')
    programContents = programContents.replace('*  /', '*/')
    programContents = programContents.replace('<  =', '<=')
    programContents = programContents.replace('>  =', '>=')
    programContents = programContents.replace('*  *', '**')
    programContents = programContents.replace('+  =', '+=')
    programContents = programContents.replace('-  =', '-=')
    programContents = programContents.replace('*  =', '*=')
    programContents = programContents.replace('/  =', '/=')
    programContents = programContents.replace('<  <', '<<')
    programContents = programContents.replace('>  >', '>>')
    programContents = programContents.replace('%  =', '%=')
    programContents = programContents.replace('@  =', '@=')
    programContents = programContents.replace('^  =', '^=')
    programContents = programContents.replace('+  x', '+x')
    programContents = programContents.replace('-  x', '-x')
    programContents = programContents.replace('~  x', '~x')
    programContents = programContents.replace('>  >  =', '>>=')
    programContents = programContents.replace('<  <  =', '<<=')
    programContents = programContents.replace('/  /  =', '//=')
    programContents = programContents.replace('*  *  =', '**=')
    programContents = programContents.replace('"  "  "', '"""')
    programContents = programContents.replace("'  '  '", "'''")
    return programContents

def main():        
    
    # create a dictionary of defined operators and their tokens
    OPERATORS = {'+': 'ADD_OP', '-': 'SUB_OP', '*': 'MULT_OP', '/': 'DIV_OP', '=': 'ASSIGN_OP', 
                 '==': 'IS_EQ_OP', '!=': 'NOT_EQ_OP', '|': 'BIT_OR_OP', 'or': 'LOGICAL_OR_OP',
                '&': 'BIT_AND_OP', 'and': 'LOGICAL_AND_OP', '%': 'MODULO_OP', '<': 'LESS_THAN_OP', 
                '>': 'GREATER_THAN_OP', '<=': 'LESS_THAN_EQ_OP', '>=': 'GREATER_THAN_EQ_OP',
                'not': 'NOT_OP', ':': 'COLON_OP', '**': 'EXPONENT_OP', '+=': 'PLUS_EQ_OP', 
                '-=': 'MINUS_EQ_OP', '*=': 'TIMES_EQUAL_OP', '/=': 'DIV_EQ_OP', '%=': 
                'MOD_EQ_OP', 'is': 'IDENT_OP', 'is not': 'NOT_IDENT_OP', 'in': 'MEMBERSHIP_OP',
                'not in': 'NOT_MEMBERSHIP_OP', '^': 'XOR_OP', '>>': 'BIT_RIGHT_OP', '<<': 'BIT_LEFT_OP',
                '//': 'FLOOR_DIV_OP', '//=': 'FLOOR_DIV_EQ_OP', '@': 'AT_OP', '@=': 'AT_EQ_OP',
                '^=': 'XOR_EQ_OP', '**=': 'POWER_EQ_OP', '<<=': 'LEFT_EQ_OP', '>>=': 'RIGHT_EQ_OP',
                '+x': 'UNARY_PLUS_OP', '-x': 'UNARY_MINUS_OP', '~x': 'BITWISE_NOT_OP'}
    
    # create a dictionary of defined keywords and their tokens
    KEYWORDS = {'as': 'KEYWORD', 'assert': 'KEYWORD', 'break': 'KEYWORD', 'class': 'KEYWORD', 
                'continue': 'KEYWORD', 'def': 'DEF_KEYWORD', 'del': 'KEYWORD', 'elif': 'ELIF_KEYWORD', 'else': 'ELSE_KEYWORD', 
                'except': 'KEYWORD', 'False': 'BOOLEAN', 'finally': 'KEYWORD', 'for': 'KEYWORD', 'from': 'KEYWORD', 
                'global': 'KEYWORD', 'if': 'IF_KEYWORD', 'import': 'KEYWORD', 'in': 'KEYWORD', 'is': 'KEYWORD', 
                'lambda': 'KEYWORD', 'None': 'KEYWORD', 'nonlocal': 'KEYWORD', 'not': 'KEYWORD', 'or': 'KEYWORD', 
                'pass': 'KEYWORD', 'raise': 'KEYWORD', 'return': 'KEYWORD', 'True': 'BOOLEAN', 'try': 'KEYWORD', 
                'while': 'WHILE_KEYWORD', 'with': 'KEYWORD', 'yield': 'KEYWORD', 'endif': 'END_IF', 'enddef': 'END_DEF',
                'endwhile': 'END_WHILE'}
    
    # create a dictionary of single character tokens
    CONCATENABLE_CHAR_TOKENS = {'(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', '\n': 'NEWLINE',  '[': 'LEFT_BRACKET',
                          ']': 'RIGHT_BRACKET',  '{': 'LEFT_BRACE',  '}': 'RIGHT_BRACE', '"': 'DOUBLE_QUOTE',
                          "'": 'SINGLE_QUOTE', ';': 'SEMICOLON', '.': 'PERIOD', ',': 'COMMA', '"""': 'TRIPLE_DOUBLE_QUOTES',
                          "'''": "TRIPLE_SINGLE_QUOTES"}
    
    # create a dictionary of variables in the program
    variables = {}
    
    # create a dictionary of methods in the program
    methods = {}
    
    # create a dictionary of classes in the program
    classes = {}
    
    # create a dictionary of errors in the program
    errors = {}
    
    # create a dictionary of identifiers that haven't been identified
    # unidentifiedIdentifiers = {} # Not sure what this is? Not currently being used. Maybe to check variables are declared at some point
    
    # a list to store characters that can be concatenated with others: \n, operators, braces, etc
    # NOTE: we don't need characters such as ** or /* here if their components are already in here
    # ex: '/' and '*' are here, so we don't need '/*'. However, these special 2-3 char
    # lexemes must be put back together in recreateMultiCharOperators()
    SPECIAL_CHARS_FOR_STRING_SPLIT = ['\n', '"', "'", '(', ')', '#', '[', ']', '{', '}', 
                                      '+', '-', '*', '/', '=', '|', '&', '%', '<', 
                                      '>', ';', ':', '.', ',', '!']
        
    # defined globally, so have to re-define in method scope, using global keyword
    global programContents
    
    """ iterate through the items that can be concatenated with others, and force them all
    to have a space before and after, for consistency, and to accurately split lexemes """
    for item in SPECIAL_CHARS_FOR_STRING_SPLIT:
        programContents = programContents.replace(item, ' ' + item + ' ')
    
    # put back together doubled operators / special characters that have been split up
    programContents = recreateMultiCharOperators(programContents)
    
    """ split the string by spaces, making a list. if we need to split by multiple items, 
    we can import re and change to re.split() """
    programContents = programContents.split(' ')
    
    # remove the generated empty words (from splitting) from the list
    while '' in programContents:
        programContents.remove('')

    # delete extraneous newlines (multiple in a row), and at beginning and end of file
    i = 0
    while i < len(programContents):
        # while there are 2 new lines in a row, delete one
        while programContents[i] == '\n' and programContents[i - 1] == '\n' and i < len(programContents) - 1:
            del programContents[i]
        i += 1
    # delete newlines at beginning of file
    while programContents[0] == '\n':
        del programContents[0]
    # delete newlines at ending of file, in case multiple in a row
    while programContents[len(programContents) - 1] == '\n':
        del programContents[len(programContents) - 1]
        
    # append one more newline so we know where the last line ends
    programContents.append('\n')
    
    # put floats back together, as they were separated with the '.' separation.
    # similarly, put back together "is not" and "not in"
    i = 0
    while i < len(programContents):
        if programContents[i] == '.' and programContents[i - 1].isnumeric() and programContents[i + 1].isnumeric():
            programContents[i - 1] = programContents[i - 1] + programContents[i] + programContents[i + 1]
            del programContents[i]
            del programContents[i]
            i -= 1
        elif programContents[i] == 'is' and programContents[i + 1] == 'not':
            programContents[i] = 'is not'
            del programContents[i + 1]
        elif programContents[i] == 'not' and programContents[i + 1] == 'in':
            programContents[i] = 'not in'
            del programContents[i + 1]
        i += 1
        
    # identify variables and add them to the variables dictionary
    i = 0
    while i < len(programContents):
        
        # variables before '='
        if programContents[i] == '=':
            j = i - 1
            while programContents[j] != '\n':
                # reg exp starts with (^) 1 of a-zA-Z_, followed by 0 or more (*) of a-zA-Z0-9_ at the end ($)
                if re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[j]):
                    variables[programContents[j]] = 'IDENTIFIER'
                j -= 1
                if j < 0:
                    break
                
        # variables after 'as'
        elif programContents[i] == 'as':
            j = i + 1
            while programContents[j] != ':':
                if programContents[j] == '\n':
                    break
                if re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[j]):
                    variables[programContents[j]] = 'IDENTIFIER'
                j += 1
        
        # variables after 'for'
        elif programContents[i] == 'for':
            j = i + 1
            while programContents[j] != 'in':
                if programContents[j] == '\n':
                    break
                if re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[j]):
                    variables[programContents[j]] = 'IDENTIFIER'
                j += 1
                
        # NOT VALID DECLARATION, so commenting this out for now
        # variables before '=='
        # elif programContents[i] == '==':
        #     j = i - 1
        #     while programContents[j] != '\n':
        #         if re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[j]):
        #             variables[programContents[j]] = 'IDENTIFIER'
        #         j -= 1
        #         if j < 0:
        #             break
    
        i += 1
    
    # identify methods and classes, and more variable options, and add them to the methods/classes/vars dictionary
    i = 0
    while i < len(programContents):
        
        # functions following 'def'
        if programContents[i] == 'def':
            methods[programContents[i + 1]] = 'METHOD_IDENTIFIER'
            # find if any new variables are named to be passed to this function
            j = i + 3
            
            # variables set as arguments for the function
            while programContents[j] != '\n':
                if re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[j]):
                    variables[programContents[j]] = 'IDENTIFIER'
                j += 1
                
        # methods preceding () where the name matches the regex and not in KEYWORDS
        elif programContents[i] == '(' and not programContents[i - 1] in KEYWORDS and re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[i - 1]):
            methods[programContents[i - 1]] = 'METHOD_IDENTIFIER'
            i += 1
            
            # possible method arguments
            while programContents[i] != ')':
                if programContents[i] == '\n':
                    break
                if re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[i]):
                    variables[programContents[i]] = 'IDENTIFIER'
                i += 1
        
        # classes being imported, gotten 'from', or declared
        elif programContents[i] == 'import' or programContents[i] == 'from' or programContents[i] == 'class':
            classes[programContents[i + 1]] = 'IDENTIFIER'
            
        # variables in a "pipe" ex. System.out.println(), where out is a variable
        elif programContents[i - 1] == '.' and (programContents[i - 2] in classes or programContents[i - 2] in methods or programContents[i - 2] in variables):
            variables[programContents[i]] = 'IDENTIFIER'
            
        # else in a "pipe" if the option is not a method [ex, has '(' following, or a variable as above]
        elif programContents[i] == '.' and re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[i - 1]):
            classes[programContents[i - 1]] = 'IDENTIFIER'
        i += 1
        
    # identify errors
    i = 0
    while i < len(programContents):
        if programContents[i] == 'raise':
            i += 1
            while programContents[i] != '\n':
                if re.fullmatch('^[a-zA-Z_][a-zA-Z0-9_]*$', programContents[i]):
                    errors[programContents[i]] = 'IDENTIFIER'
                i += 1
        i += 1
                       
    # begin printing table of our tokens and calculated lexemes
    print('\nBegin lexical analysis:\n')
    print('{:23} {}'.format('Token:', 'Lexeme:'))
    print('{:23} {}'.format('------', '-------'))

    # variables for checking if lexeme is part of a string
    isStringLiteral = False
    stringStarter = ''
        
    # for each lexeme, calculate the token and print in a table format
    i = 0
    while i < len(programContents):
        
        lexeme = programContents[i]
        
        # check if lexeme is part of a string, or a """ / ''' comment
        
        # deletes """ / ''' comments (a """ at the start of a line, through a """ at the end of a line)
        if (lexeme == '"""' or lexeme == "'''") and isStringLiteral == False and (programContents[i - 1] == '\n' or i == 0):
            del programContents[i]
            while (True):
                if programContents[i] == lexeme and programContents[i + 1] == '\n':
                    break
                del programContents[i]
            del programContents[i] # delete the next """
            del programContents[i] # delete the extra newline
            continue # continue the loop
            
        # else not a comment, so check if it's a string
        elif (lexeme == '"' or lexeme == "'" or lexeme == '"""' or lexeme == "'''") and isStringLiteral == False:
            isStringLiteral = True
            stringStarter = lexeme
            
        # if the end of the string is reached (the starting character of the string is reached again),
        # the string is over.
        # Edited for our BNF: strings can now only continue on one line,
        # So stop classifying as a STRING_LITERAL upon hitting a newline, although
        # this will definitely cause an error
        elif (lexeme == stringStarter and isStringLiteral == True) or lexeme == '\n':
            isStringLiteral = False
        
        """ search our dictionaries for the lexeme to see if it is stored, and get the 
        value (token name) from the key """
        # check if it's a string
        if isStringLiteral == True and not lexeme == stringStarter:
            token = 'STRING_LITERAL'
            
        # else when we hit a # it's not in a string, so it's a comment, so delete the comment
        elif isStringLiteral == False and lexeme == '#':
            while programContents[i] != '\n':
                del programContents[i]
            if programContents [i - 1] == '\n' or i == 0:                
                del programContents[i]
            continue
        
        # if not a string and not a comment, check our dictionaries to see what the token is
        elif lexeme.isnumeric():
            token = 'INT_LITERAL'
        elif lexeme.replace('.', '', 1).isnumeric(): # if removing one '.' results in a numeric
            token = 'FLOAT'
        elif lexeme in OPERATORS:
            token = OPERATORS[lexeme]
        elif lexeme in KEYWORDS:
            token = KEYWORDS[lexeme]
        elif lexeme in CONCATENABLE_CHAR_TOKENS:
            token = CONCATENABLE_CHAR_TOKENS[lexeme]
        elif lexeme in methods:
            token = methods[lexeme]
        elif lexeme in variables:
            token = variables[lexeme]
        elif lexeme in classes:
            token = classes[lexeme]
        elif lexeme in errors:
            token = errors[lexeme]
        else:
            token = 'Unknown'
        
        # change newline lexeme so that it doesn't print new lines
        if lexeme == '\n':
            lexeme = '\\n'

        # print the lexeme and the token in a table format
        print('{:23} {}'.format(token, lexeme))
        
        # store the token/lexeme pairs as tuples in an array
        tokenLexeme.append((token, lexeme))
        
        # increment the loop
        i += 1
    
    # append EOF token to the end of the tuple array of token/lexeme pairs    
    tokenLexeme.append(('END_OF_FILE', 'EOF'))
    print('{:23} {}'.format(tokenLexeme[len(tokenLexeme) - 1][0], tokenLexeme[len(tokenLexeme) - 1][1]))
    
    print()
    
    # lexical analysis is over, proceed to our syntax analysis, by calling the 
    # function in syntaxAnalyzerPy.py
    syntaxAnalyzer(tokenLexeme)
            
# call main() if running this file specifically
if __name__ == "__main__":
    main()