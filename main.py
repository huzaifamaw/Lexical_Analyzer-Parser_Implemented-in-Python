import re
import os



CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]

TOKENS = [
    'KEY_WORD', 'IDENTIFIER', 'INTEGER_CONSTANT',
    'OPERATOR', 'SEPARATOR', 'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'DATATYPE' , 'BOOL_CONST'
]
blank_var = "#include <iostream> using namespace std; void main () { if(a<b) {return i++;}else{i=0;}switch(a){case 'A': cin>>input;cout<<abcd;default: break;}}"
print("INPUT FILE:\n", blank_var)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


integers = re.findall('^[0-9]+$|[0-9]+', blank_var)
floatn = re.findall(r'[0-9]+\.[0-9]+', blank_var)
chars = re.findall(r'\'[^\'\\\.]\'', blank_var)

TOKENS_DEF = {
    '=': 'ASSIGN',
    '&': 'ADDRESS',
    '<': 'LT',
    '>': 'GT',
    '++': 'SELF_PLUS',
    '--': 'SELF_MINUS',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '>=': 'GET',
    '<=': 'LET',
    '(': 'LL_BRACKET',
    ')': 'RL_BRACKET',
    '{': 'LB_BRACKET',
    '}': 'RB_BRACKET',
    '[': 'LM_BRACKET',
    ']': 'RM_BRACKET',
    ',': 'COMMA',
    '"': 'DOUBLE_QUOTE',
    '\'': 'SINGLE_QUOTE',
    ';': 'SEMICOLON',
    '#': 'SHARP',
    '&&': 'AND',
    '!': 'NOT',
    '||': 'OR',
    '<<': 'L_SHIFT',
    '>>': 'R_SHIFT',
    '==':'EQUALITY',
    ':':'COLON'
    
}

Keyword = ["if", "else", "while", "for", "cout", "cin", "return", "switch", "case", "break", "function",
           "using", "namespace", "include", "endl","default"]
bracket = ['(', ')', '{', '}', '[', ']']
datatype = ['int', 'float', 'char', 'string', 'bool','void']
punctuator = [',', ';', ':', ',']
arithop = ['-', '+', '*', '/', '%']
logop = ['||', '&&']
slogop = ['!']
assop = ['=']
sinlop = ['<', '>']
relop = ['<=', '>=', '!=', '==', "<<", ">>"]
incr = ['++', '--']
bool_cons = ['True','False']


class Node:

    # Function to initialise the node object
    def __init__(self, value, line_numbers, type):
        self.data = {
            "value": value,
            "LINE_NUMBERS": line_numbers,
            "TYPE": type
        }  # Assign data
        self.next = None  # Initialize next as null

# Node of a doubly linked list
class Symbol_table_Node:
    def __init__(self, name, line_numbers, type,scope):
        self.data = {
            "Name": name,
            "LINE_NUMBERS": line_numbers,
            "TYPE": type,
            "Scope": scope
        }  # Assign data
        self.next = None  # Initialize next as null
        self.prev = None
class SymbolTable:
    def __init__(self):
        self.head = None
    def push(self, name, line_numbers, type,scope):
            new_node = Symbol_table_Node(name, line_numbers, type,scope)


            new_node.next = self.head
            new_node.prev = None


            if self.head is not None:
                self.head.prev = new_node


            self.head = new_node

    def printList(self):
        node = self.head
        while (node != None):

            print(node.data)
            last = node
            node = node.next

    def FindData(self, name):
        flag = False
        node = self.head

        while (node != None):

            if (node.data['Name'] == name):
                return node.data
            last = node
            node = node.next
        if (flag == False):
            return False


class Tokkens:

    # Function to initialize head
    def __init__(self):
        self.head = None

    # This function is defined in Linked List class
    # Appends a new node at the end. This method is
    # defined inside LinkedList class shown above */
    def append(self, value, line_numbers, type):

        # 1. Create a new node
        # 2. Put in the data
        # 3. Set next as None
        new_node = Node(value, line_numbers, type)

        # 4. If the Linked List is empty, then make the
        # new node as head
        if self.head is None:
            self.head = new_node
            return

        # 5. Else traverse till the last node
        last = self.head
        while (last.next):
            last = last.next

        # 6. Change the next of last node
        last.next = new_node

    # Utility function to print the linked list
    def printList(self):
        temp = self.head
        while (temp):
            print(temp.data),
            temp = temp.next

class Token(object):

    def __init__(self, pos, value, linenumber):
        self.type = TOKENS_DEF[value] if (
                pos == 3 or pos == 4
        ) else TOKENS[pos]
        self.value = value
        self.line_number = linenumber

class Lexer(object):

    def __init__(self):
        self.tokens = []
        self.count = 1
        self.temp = ''
        self.sym = SymbolTable()

    def is_blank(self, index):
        return (
                blank_var[index] == ' '
        )

    def is_Escape(self, index):
        return (

                blank_var[index] == '\t' or
                blank_var[index] == '\n' or
                blank_var[index] == '\r'
        )

    def line_break(self, index):
        return (
                blank_var[index] == '\n' or
                blank_var[index] == '\t' or
                blank_var[index] == '\b' or
                blank_var[index] == ' '

        )

    def skip_blank(self, index, stringflag):
        while index < len(blank_var) and self.is_blank(index):
            index += 1
        return index

    def print_log(self, style, value):
        print(style, value)

    def checkforiden(self):
        if (self.temp != ''):

            i = re.findall('[a-zA-Z_][a-zA-Z_0-9]*', self.temp)

            if (self.temp in i):

                self.tokens.append(Token(1, self.temp, self.count))


                self.sym.push(self.temp, self.count, "NOT DEFINED", "NOT DEFINED")
                self.temp = ''


                # symbol table code








            else:
                print(
                    f"...{bcolors.BOLD}{bcolors.FAIL} ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n INVALID IDENTIFIER IN LINE NUMBER: {self.count} {bcolors.WARNING} {self.temp} {bcolors.ENDC}")

                exit()
                # error handler
            self.temp = ''
        else:
            return 0;

    def is_keyword(self, value):
        for item in Keyword:
            if value in item:
                return True
        return False

    def main(self):
        i = 0
        strf = False

        while i < len(blank_var):

            if (blank_var[i] == ' '):
                self.checkforiden()
                i = i + 1
                continue
            if blank_var[i] == '\n':
                self.checkforiden()
                self.count = self.count + 1
                i = i + 1
                continue
            if blank_var[i] == '#':
                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i], self.count))
                i = i + 1
                continue
            elif blank_var[i:i + 2] in logop:
                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i:i + 2], self.count))
                i = i + 1
            elif blank_var[i:i + 2] in relop:
                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i:i + 2], self.count))
                i = i + 1
            elif blank_var[i:i + 2] in incr:
                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i:i + 2], self.count))
                i = i + 1
            elif blank_var[i] in bracket:
                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i], self.count))

            elif blank_var[i] in punctuator:

                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i], self.count))

            elif blank_var[i] in sinlop:
                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i], self.count))

            elif blank_var[i] in assop:

                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i], self.count))

            elif blank_var[i] in slogop:
                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i], self.count))
            elif blank_var[i] in arithop:
                self.checkforiden()
                self.tokens.append(Token(3, blank_var[i], self.count))
            else:
                self.temp = self.temp + blank_var[i]

                if (blank_var[i] == '"'):
                    #self.tokens.append(Token(3, blank_var[i], self.count))
                    if (self.temp == '"'):
                        self.temp = ''
                        i = i + 1
                        strf = True
                        while i < len(blank_var) and blank_var[i] != '"':

                            if (blank_var[i:i + 2] == "\\t"):
                                self.temp = self.temp + '\t'
                                i = i + 2
                            elif (blank_var[i:i + 2] == "\\n"):

                                self.temp = self.temp + '\n'
                                i = i + 2
                            else:
                                self.temp = self.temp + blank_var[i]
                                i = i + 1

                            if (i == len(blank_var) or i > len(blank_var)):
                                print(
                                    f"...{bcolors.BOLD}{bcolors.FAIL} ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n STRING QUOTES NOT CLOSED IN LINE NUMBER: {self.count} {bcolors.WARNING} {self.temp} {bcolors.ENDC}")
                                exit()

                        if (len(self.temp) > 0):
                            self.tokens.append(Token(5, self.temp, self.count))
                            strf = False
                            self.temp = ''
                        #self.tokens.append(Token(3, blank_var[i], self.count))
                        i = i + 1
                        continue

                if (self.temp in integers):

                    if (blank_var[i + 1] != '.' and blank_var[i+1] not in re.findall('[0-9]',blank_var)):

                        j = re.findall('[a-zA-Z_][a-zA-Z_0-9]*', blank_var[i + 1]);

                        if (blank_var[i + 1] not in j):

                            self.tokens.append(Token(2, self.temp, self.count))
                            integers.pop(integers.index(self.temp))
                            
                            self.temp = ''


                elif (self.temp in Keyword):
                    self.tokens.append(Token(0, self.temp, self.count))
                    self.temp = ''



                elif (self.temp in datatype):
                    self.tokens.append(Token(8, self.temp, self.count))
                    self.temp = ''

                elif (self.temp in bool_cons):
                	self.tokens.append(Token(9,self.temp,self.count))
                	self.temp=''
                elif (self.temp in floatn):
                    self.tokens.append(Token(6, self.temp, self.count))
                    self.temp = ''

                if (blank_var[i] == '\''):
                    #self.tokens.append(Token(3, blank_var[i], self.count))
                    self.temp = ''
                    i = i + 1

                    if (blank_var[i] == '\''):
                        #self.tokens.append(Token(3, blank_var[i], self.count))
                        self.temp = ''
                        i = i + 1
                        continue
                    elif (blank_var[i:i + 2] == '\\n' or blank_var[i:i + 2] == '\\t' or ord(blank_var[i])):
                        if (blank_var[i:i + 2] == '\\n' or blank_var[i:i + 2 == '\\t']):
                            if (blank_var[i + 2] == '\''):
                                self.tokens.append(Token(7, blank_var[i:i + 2], self.count))
                                self.temp = ''
                                i = i + 2
                                #self.tokens.append(Token(3, blank_var[i], self.count))
                                i = i + 1
                                continue
                            else:
                                print(
                                    f"...{bcolors.BOLD}{bcolors.FAIL} ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n CHARACTER QUOTES NOT CLOSED IN LINE NUMBER: {self.count} {bcolors.WARNING} {blank_var[i]} {bcolors.ENDC}")
                                exit()
                        else:

                            if (blank_var[i + 1] == '\''):
                                self.tokens.append(Token(7, blank_var[i], self.count))
                                self.temp = ''
                                i = i + 1
                                #self.tokens.append(Token(3, blank_var[i], self.count))
                                #i = i + 1
                            else:
                                print(
                                    f"...{bcolors.BOLD}{bcolors.FAIL} ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n CHARACTER QUOTES NOT CLOSED IN LINE NUMBER: {self.count} {bcolors.WARNING} {blank_var[i]} {bcolors.ENDC}")
                                exit()

                    else:
                        print(
                            f"...{bcolors.BOLD}{bcolors.FAIL} ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n CHARACTER DECLARATION NOT VALID IN LINE NUMBER: {self.count} {bcolors.WARNING} {blank_var[i]} {bcolors.ENDC}")
                        exit()

            i = i + 1
            continue


class parser:

    def __init__(self,tok):
        self.tok=tok.head
        self.lookahead=None

    def nextToken(self):
        if(self.lookahead==None):
            return self.tok
        else:
            self.tok=self.tok.next
            return self.tok

    def includestmt(self):
        data = self.lookahead.data['value'];
        if (data == '#'):
            self.match("#")
            self.match("include")
            self.match("<")
            self.matchID(self.lookahead.data['TYPE'])
            self.match('>')
        else:
            print("ERROR IN INCLUDE STMT ")
    def includelist_(self):
        data = self.lookahead.data['value'];
        if (data == '#'):
            self.includestmt()
            self.includelist_()
        elif(data in ['$',"using"]):
            return
        else:
            print("ERROR IN INCLUDE LIST _")


    def includelist(self):
        data = self.lookahead.data['value'];
        if (data == '#'):
            self.includestmt()
            self.includelist_()
        else:
            print("ERROR IN INCLUDE LIST")

    def namespace(self):
        data = self.lookahead.data['value'];
        if(data == 'using'):
            self.match('using')
            self.match('namespace')
            self.matchID(self.lookahead.data["TYPE"])
            self.match(';')
        else:
            print("ERROR IN NAMESPACE")
    def start(self):
        data = self.lookahead.data['value'];
        if(data == '#'):
            self.includelist()
            self.namespace()
            self.program()
        elif(data == "$"):
            return
        else:
            print("ERROR IN START")



    def vardeclist_(self):
        data = self.lookahead.data['value'];
        if (data == ','):
            self.match(',')
            self.vardecinit()
            self.vardeclist_()
        elif (data == ';'):
            return
        else:
            print("ERROR IN VARRAIBLE dec list _")
    def vardecid(self):
        data = self.lookahead.data['value']

        if ( self.lookahead.data["TYPE"]=="IDENTIFIER"):
            self.matchID(self.lookahead.data["TYPE"])
            self.vardecid_()
        else:
            print("ERROR IN VARDEC ID")

    def vardecid_(self):
        data = self.lookahead.data['value'];

        if ( data == '['):
            self.match('[')
            if(self.lookahead.data['TYPE']=='INTEGER_CONSTANT'):
                self.lookahead = self.nextToken()
                self.match(']')
            else:
                print("ERROR: NOT A CONTS")
        elif ( data == ',' or data == ';' or data == '='):
            return
        else:
            print("EROR")
    def relop(self):
        data = self.lookahead.data['value'];

        if( data == '<='):
            self.match('<=')
        elif ( data == '<'):
            self.match('<')
        elif ( data == '>'):
            self.match('>')
        elif ( data == '>='):
            self.match('>=')
        elif (data == '=='):
            self.match('==')
        elif ( data == '!='):
            self.match('!=')
        else:
            print("ERROR IN RELOP !")


    def expression(self):
        data = self.lookahead.data['value'];

        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        data_next = self.lookahead.next
        if (self.lookahead.data["TYPE"] == "IDENTIFIER" and data_next.data["value"] == "++"):
        	self.matchID(self.lookahead.data["TYPE"])
        	self.match("++")
        	
        elif(self.lookahead.data["TYPE"] == "IDENTIFIER" and data_next.data["value"] == "--"):
        	self.matchID(self.lookahead.data["TYPE"])
        	self.match("--")
        elif(self.lookahead.data["TYPE"] == "IDENTIFIER" and data_next.data["value"] == "="):
        	self.matchID(self.lookahead.data["TYPE"])
        	self.match("=")
        	self.expression()
        elif (data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER'or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.simpleExp()
        else:
            print("ERROR IN EPRESSION")


    def arglist_(self):
        data = self.lookahead.data['value'];
        if(data == ','):
            self.match(',')
            self.expression()
            self.arglist_()
        elif (data ==')'):
            return
        else:
            print("ERROR IN ARG LIST _")

    def arglist(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.expression()
            self.arglist_()
        else:
            print("ERROR IN  ARG LIST")

    def args(self):
        data = self.lookahead.data['value'];

        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.arglist()
        elif ( data == ')'):
            return
        else:
            print("ERROR IN  ARGS")
    def constants(self):
        data = self.lookahead.data['value']
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if(self.lookahead.data['TYPE'] in CONST):
            self.lookahead=self.nextToken()
        else:
            print("ERROR IN CONSTANTS ")
    def factor_(self):
        data = self.lookahead.data['value']

        if(data == '('):
            self.match('(')
            self.args()
            self.match(')')
        elif ( data == '*' or data == '/' or data == '%' or data == '+' or data == '-' or data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data=="||" or data == ',' or data == ';' or data == ')' or data == "<<"):
            return
        else:
            print("ERROR IN FACTOR _ " + data)
    def factor(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER'):
            self.matchID(self.lookahead.data['TYPE'])
            self.factor_()
        elif (data == '('):
            self.match('(')
            self.expression()
            self.match(')')
        elif (self.lookahead.data['TYPE'] in CONST):
            self.constants()
        else:
            print("ERROR IN  FACTOR")



    def unaryExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.factor()
        else:
            print("ERROR IN UNARY EXP")

    def mulOp(self):
        data = self.lookahead.data['value']
        if (data =='*'):
            self.match('*')
        elif (data=='/'):
            self.match('/')
        elif (data=='%'):
            self.match('%')
        else:
            print("ERROR WITH MULOP")
    def mulExp_(self):
        data = self.lookahead.data['value']
        
        if ( data == '*' or data == '/' or data == '%'):
            self.mulOp()
            self.unaryExp()
            self.mulExp_()
        elif ( data == '+' or data == '-' or data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data=="||" or data == ',' or data == ';' or data == ')' or data=="<<"):
            return
        else:
            print("ERROR IN MUL EXP _")
    def sumOP(self):
        data = self.lookahead.data['value']
        if( data == '+'):
            self.match('+')
        elif( data == '-'):
            self.match('-')
        else:
            print("ERROR IN SUM OP")
    def sumExp_(self):
        data = self.lookahead.data['value'];
        if (data == '+' or data == '-'):
            self.sumOP()
            self.mulExp()
            self.sumExp_()
        elif (data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data=="||" or data == ',' or data == ';' or data == ')' or data=="<<"):
            return
        else:
            print("ERROR IN SUM EXP_")
    def mulExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.unaryExp()
            self.mulExp_()
        else:
            print("ERROR IN SUM EXP_")
    def sumExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.mulExp()
            self.sumExp_()
        else:
            print("ERROR IN SUM EXP")
    def relExp_(self):
        data = self.lookahead.data['value'];
        if (data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!='):
            self.relop()
            self.sumExp()
            self.relExp_()
        elif (data == '||' or data == '&&' or data ==',' or data == ';' or data == ')' or data=="<<"):
            return
        else:
            print("ERROR IN REL EXP !")
    def relExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.sumExp()
            self.relExp_()
        else:
            print("ERROR IN REL EXP !")
    def unaryRelExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (data == '!'):
            self.match('!')
            self.unaryRelExp()
        elif (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST ):
            self.relExp()
        else:
            print("ERROR IN UNARY REL EXP")


    def andExp_(self):
        data = self.lookahead.data['value'];
        if( data == '&&'):
            self.match("&&")
            self.unaryRelExp()
            self.andExp_()
        elif (data == '||' or data == ',' or data == ';' or data == ')' or data == "<<"):
            return
        else:
            print("ERROR IN AND EXP _")
    def andExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.unaryRelExp()
            self.andExp_()
        else:
            print("ERROR IN and EXP")

    def SimpleExp_(self):
        data = self.lookahead.data['value'];
        if ( data == '||'):
            self.match('||')
            self.andExp()
            self.SimpleExp_()
        elif (data == ',' or data == ';' or data == ')' or data == "<<"):
            return
        else:
            print("ERROR IN SIMPLE EXP _")
    def simpleExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if(data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER' or  data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.andExp()
            self.SimpleExp_()
        else:
            print("ERROR IN SIMPLE EXP")


    def vardecinit_(self):
        data = self.lookahead.data['value'];

        if(data == '='):
            self.match('=')
            self.simpleExp()
        elif(data == ',' or data == ';' ):
            return
        else:
            print("ERROR IN VARDECINIT_")

    def vardecinit(self):
        data = self.lookahead.data['value'];

        if (self.lookahead.data["TYPE"] == "IDENTIFIER"):
            self.vardecid()
            self.vardecinit_()
        else:
            print("ERROR IN VARRAIBLE INIT")

    def vardeclist(self):
        data = self.lookahead.data['value'];

        if (self.lookahead.data["TYPE"] == "IDENTIFIER"):
            self.vardecinit()
            self.vardeclist_()
        else:
            print("ERROR IN VARRAIBLE DECLIST")

    def varriable(self):
        data = self.lookahead.data['value'];

        if(self.lookahead.data["TYPE"] == "IDENTIFIER"):
            self.vardeclist()
            self.match(';')
        else:
            print("ERROR IN VARRAIBLE ONLY")

    def declaration__(self):
        data = self.lookahead.data['value'];
        data_next = self.lookahead.next
        if (self.lookahead.data['TYPE'] == "IDENTIFIER" and data_next.data['value'] == '('):
            self.function()
        elif (self.lookahead.data['TYPE'] == "IDENTIFIER"):
            self.varriable()
        else:
            print("ERROR IN DELARATION__")
    def declaration(self):
        data = self.lookahead.data['value'];

        if (data in datatype):
            self.typeid()
            self.declaration__()
        else:
            print("ERROR:  IN declaration FUNCTION")
    def declaration_(self):
        data = self.lookahead.data['value'];

        if (data in datatype):
            self.declaration()
            self.declaration_()
        elif (data == '$'):
            return
        else:
            print("ERROR:  IN declaration_ FUNCTION")

    def declist(self):
        data = self.lookahead.data['value'];

        if (data in datatype):
            self.declaration()
            self.declaration_()
        else:
            print("ERROR:  IN declist FUNCTION")

    def program(self):
        data = self.lookahead.data['value'];

        if ( data in datatype):
            self.declist()
        elif (data == '$'):
            return
        else:
            print("ERROR:  IN PROGRAM FUNCTION")
    def function(self):
        data = self.lookahead.data['value'];
        if(self.lookahead.data['TYPE'] == 'IDENTIFIER'):
            self.matchID(self.lookahead.data['TYPE'])
            self.match('(')
            self.paramas()
            self.match(')')
            self.match('{')
            self.stmtlist()
            self.match('}')
        elif(data == '$'):
            return
        else:
            print("ERROR IN FUNCTION SYNTAX TOKEN: ",self.lookahead.data)
            exit()
    def stmtlist(self):
        data = self.lookahead.data['value'];
        
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS', 'BOOL_CONST'
        ]
        if(data in ['!','(','if','cout','cin','while','for','switch','return','break'] or data in datatype or self.lookahead.data["TYPE"] in ["IDENTIFIER" , CONST]):
            self.statment()
            self.stmtlist_()
        else:
            print("ERROR IN STMTLIST")
    def iteration(self):
        data = self.lookahead.data['value'];
        if(data == 'for'):
            self.match('for')
            self.match('(')
            self.vardecinit()
            self.match(';')
            self.simpleExp()
            self.match(';')
            self.expression()
            self.match(')')
            self.match('{')
            self.stmtlist()
            self.match('}')
        elif(data == "while"):
        	self.match("while")
        	self.match("(")
        	self.simpleExp()
        	self.match(")")
        	self.match("{")
        	self.stmtlist()
        	self.match("}")
        else:
            print('ERROR IN ITERETION')
    def switch(self):
    	data=self.lookahead.data["value"]
    	if(data =="switch"):
    		self.match("switch")
    		self.match("(")
    		self.simpleExp()
    		self.match(")")
    		self.match("{")
    		self.caselist()
    		self.default()
    		self.match("}")
    	else:
    		print("Error in SWITCH")
    def caselist(self):
    	data = self.lookahead.data["value"]
    	if(data=="case"):
    		self.onecase()
    		self.caselist()
    	elif(data=="default" or data == "}"):
    		return
    	else:
    		print("ERROR IN CASELIST")
    		
    def onecase(self):
    		data = self.lookahead.data["value"]
    		if(data=="case"):
    			self.match("case")
    			if(self.lookahead.data["TYPE"] in CONST):
    				self.lookahead =self.nextToken()
    				self.match(":")
    				self.stmtlist()
    			else:
    				print("ERROR IN CONSTANTS IN SWITCH CASE")
    		else: 
    		     print("ERROR IN ONE CASE")
    		
    	 	
    def default(self):
    	data=self.lookahead.data["value"]
    	if(data == "default"):
    		self.match("default")
    		self.match(":")
    		self.stmtlist()
    	elif(data == "}"):
    		return
    	else:
    		print("ERROR IN DEFAULT")
    def selection(self):
    	data =self.lookahead.data["value"]
    	if(data == "if"):
    		self.match("if")
    		self.match("(")
    		self.simpleExp()
    		self.match(")")
    		self.match("{")
    		self.stmtlist()
    		self.match("}")
    		self.selection_()
    	else:
    		print("ERROR IN SELECTION: "+data)
    def selection_(self):
    	data = self.lookahead.data["value"]
    	if(data == ";"):
    		self.match(";")
    	elif(data =="else"):
    		self.match("else")
    		self.match("{")
    		self.stmtlist()
    		self.match("}")
    	else:
    		print("ERROR IN IF CONDITION: TOKEN "+data)
    		exit()
    
    def statment(self):
        data = self.lookahead.data['value'];
        if(data in ['for','while']):
            self.iteration()
        elif(data in ['return']):
            self.returnstmt()
        elif(data in ['if']):
            self.selection()
        elif(data in ['switch']):
            self.switch()
        elif(data in ['break']):
            self.match("break")
            self.match(";")
        elif(data == "continue"):
        	self.match("continue")
        	self.match(";")
        elif(data in ["cin","cout"]):
        	self.input_output()
        elif(data in datatype):
            self.declaration()
        elif (data in ['!','('] or self.lookahead.data["TYPE"] in ["IDENTIFIER", CONST]):
            self.expression()
            self.match(";")
        else:
            print("ERROR IN STATEMENT")

    def printlist(self):
    	data= self.lookahead.data["value"]
    	if(data == "<<"):
    		self.single()
    		self.printlist_()
    	else:
    		print("ERROR IN PRINTLIST :")
    def single(self):
    	data=self.lookahead.data["value"]
    	if(data == "<<"):
    		self.match("<<")
    		self.expression()
    	else:
    		print("ERROR IN SINGLE: ")
    def printlist_(self):
    	data =self.lookahead.data["value"]
    	data_next = self.lookahead.next
    	if(data == "<<" and data_next.data["value"] not in ["endl"]):
    		self.single()
    		self.printlist_()
    	elif(data == "<<" or data == ";" ):
    		return 
    	else:
    		print("ERROR IN PRINTLIST_")
    def endstmt(self):
    	data = self.lookahead.data["value"]
    	if(data == "<<"):
    		self.match("<<")
    		self.match("endl")
    		self.match(";")
    	elif(data == ";"):
    		self.match(";")
    	else:
    		print("ERROR IN ENDSTMT")
    def input_output(self):
    	data = self.lookahead.data["value"]
    	if(data == "cout"):
    		self.match("cout")
    		self.printlist()
    		self.endstmt()
    	elif(data == "cin"):
    		self.match("cin")
    		self.inputlist()
    		self.match(";")
    	else:
    		print("ERROR IN INPUT_OUTPUT TOKEN: "+self.lookahead.data)
    def inputlist(self):
    	data = self.lookahead.data["value"]
    	if(data == ">>"):
    		self.singleinput()
    		self.inputlist_()
    	else:
    		print("ERROR IN INPUTLIST")
    def inputlist_(self):
    	data = self.lookahead.data["value"]
    	if(data==">>"):
    		self.singleinput()
    		self.inputlist_()
    	elif(data == ";"):
    		return;
    	else:
    		print("ERROR IN INPUTLIST_")
    def singleinput(self):
    	data=self.lookahead.data["value"]
    	if(data == ">>"):
    		self.match(">>")
    		self.matchID(self.lookahead.data["TYPE"])
    	else:
    		print("ERROR IN SINGLEINPUT:")
    def stmtlist_(self):
        data = self.lookahead.data['value'];

        if (data in ['!', '(','cout','cin','if', 'while', 'for', 'switch', 'return', 'break'] or data in datatype or self.lookahead.data["TYPE"] in ["IDENTIFIER", CONST]):
            self.statment()
            self.stmtlist_()
        elif(data in ['}'] or data == "default"):
            return
        else:
            print("ERROR IN STMTLIST_" + data)

    def returnstmt(self):
        data = self.lookahead.data['value'];
        if(data == 'return'):
            self.match('return')
            self.expression()
            self.match(';')
        elif(data == '}'):
            return
        else:
            print("ERROR IN STATEMENT: ",self.lookahead.data)
            exit()
    def data(self):
        value = self.lookahead.data['TYPE'];
        data = self.lookahead.data['value'];
        conslist = ['INTEGER_CONSTANT','STRING_CONSTANT', 'FLOAT_CONSTANTS', 'CHAR_CONSTANTS','BOOL_CONST']
        if(value in conslist):
            self.lookahead = self.nextToken()

        elif (data == ';'):
            return
        else:
            print("ERROR IN RETURN DATA: ",self.lookahead.data)
            exit()
    def paramas(self):
        data = self.lookahead.data['value'];
        if (data in datatype):
            self.paralist()
        elif (data == ')'):
            return
        else:
            print("ERROR WITH PARAMETERS: ",self.lookahead.data)
            exit()
    def paralist(self):
        data = self.lookahead.data['value'];
        if(data in datatype):
            self.parameter()
            self.paralist_()
        else:
            print("ERROR WITH PARALIST: ", self.lookahead.data)
            exit()
    def paralist_(self):
        data = self.lookahead.data['value'];
        if(data == ','):
            self.match(',')
            self.parameter()
            self.paralist_()
        elif(data == ')'):
            return
        else:
            print("ERROR WITH PARALIST_: ", self.lookahead.data)
            exit()
    def parameter(self):
        data = self.lookahead.data['value'];
        if( data in datatype):
            self.vartypeid()
            self.paraid()
        else:
            print("ERROR WITH PARAMETERS: ", self.lookahead.data)
            exit()
    def paraid(self):
        type = self.lookahead.data['TYPE'];
        if(type == 'IDENTIFIER'):
            self.matchID(type)
            self.paraid_()
        else:
            print("ERROR IN PARAMETERS IDENTIFIER: ",self.lookahead.data)
            exit()
    def paraid_(self):
        data = self.lookahead.data['value'];
        if(data == '['):
            self.match('[')
            self.match(']')
        elif (data == ')' or data == ','):
            return
        else:
            print("ERROR IN PARAMETERS IDENTIFIER: ", self.lookahead.data)
            exit()

    def match(self,t):
        if(self.lookahead.data['value'] == t):
            self.lookahead= self.nextToken()

        else:
            print("ERROR WITH SYNATX NEAR TOKKEN: ",self.lookahead.data['value'] , " IN LINE NUMBER: ", self.lookahead.data['LINE_NUMBERS'])
            exit()
    def matchID(self,type):

        if(type=='IDENTIFIER'):
            self.lookahead = self.nextToken()
        else:
            print("ERROR IN TOKEN: " , self.lookahead.data)
            print("EXPECTED TO BE IDENTIFIER ...")
            exit()

    def typeid(self):
        data = self.lookahead.data['value'];
        type = self.lookahead.data['TYPE'];
        if(data == 'int'):
            self.match('int')
        elif(data == 'float'):
            self.match('float')
        elif(data == 'string'):
            self.match('string')
        elif(data == 'char'):
            self.match('char')
        elif(data == 'bool'):
            self.match('bool')
        elif (data == 'void'):
            self.match('void')
        else:
            print("ERROR WITH TYPE IN TOKEN: " , self.lookahead.data)
            exit()

    def vartypeid(self):
        data = self.lookahead.data['value'];
        type = self.lookahead.data['TYPE'];
        if (data == 'int'):
            self.match('int')
        elif (data == 'float'):
            self.match('float')
        elif (data == 'string'):
            self.match('string')
        elif (data == 'char'):
            self.match('char')
        elif (data == 'bool'):
            self.match('bool')
        else:
            print("ERROR WITH TYPE IN TOKEN: ", self.lookahead.data)
            exit()


def lexer():
    lexer = Lexer()
    lexer.main()
    tok = Tokkens()
    for token in lexer.tokens:
        tok.append(token.value, token.line_number, token.type)
    tok.append('$', token.line_number + 1, "EOF")
    tok.printList()
    #print("\nSYMBOL TABLE: \n")
    #lexer.sym.printList()
    #print("\n")
    check = parser(tok)
    check.lookahead = check.nextToken()
    check.start()


    if check.lookahead.data['value']  == '$':
        print("SYNTAX IS CORRECT... ")



if __name__ == '__main__':
    lexer()
