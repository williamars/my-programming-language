import sys

EOF = "EOF"
INITIAL = "INITIAL"
INT = "INT"
MINUS = "MINUS"
PLUS = "PLUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
OPEN_PARENTESIS = "OPEN_PARENTESIS"
CLOSE_PARENTESIS = "CLOSE_PARENTESIS"
OPEN_KEY = "OPEN_KEY"
CLOSE_KEY = "CLOSE_KEY"
EQUAL = "EQUAL"
SEMICOLON = "SEMICOLON"
IDENTIFIER = "IDENTIFIER"
PRINTF = "PRINTF"
SCANF = "SCANF"
WHILE = "WHILE"
IF = "IF"
ELSE = "ELSE"
EQUALEQUAL = "EQUALEQUAL"
OR = "OR"
AND = "AND"
NOT = "NOT"
GREATER_THAN = "GREATER_THAN"
LESS_THAN = "LESS_THAN"
POINT = "POINT"
COMMA = "COMMA"
TYPE = "TYPE"
STR = "STR"
RETURN = "RETURN"
VOID = "VOID"
FUNCTION = "FUNCTION"

reserved_words = ["printf", "scanf", "while", "if", "else", "int", "str", "void", "return"]
reserved_tokens = [PRINTF, SCANF, WHILE, IF, ELSE, TYPE, TYPE, TYPE, RETURN]

class PrePro:
    def filter(code):
        new_code = ""
        i = 0
        open = False
        while i < len(code):
            if code[i] == "/" and code[i+1] == "*":
                open = True
                i += 2
            while open and i < len(code)-1:
                if code[i] == "*" and code[i+1] == "/":
                    open = False
                    i += 2
                else:
                    i += 1
            if i < len(code):
                new_code += code[i]
            i += 1
        if open:
            raise Exception("You need to close comment")
        return new_code

class FuncTable:
    table = {}

    def get(identifier):
        return FuncTable.table[identifier]

    def set(identifier, result):
        tree = FuncTable.get(identifier)
        if result[1] == tree[1]:
            FuncTable.table[identifier] = (result[0], tree[1])
        else:
            raise Exception("Type mismatch")

    def create(name, type, value):
        if name not in FuncTable.table.keys():
            FuncTable.table[name] = (value, type)
        else:
            raise Exception("Identifier already exists")

class SymbolTable:
    def __init__(self, table):
        self.table = table

    def get(self, identifier):
        return self.table[identifier]

    def set(self, identifier, result):
        tree = self.get(identifier)
        # print(tree, identifier, result)
        if result[1] == tree[1]:
            self.table[identifier] = (result[0], tree[1])
        else:
            raise Exception("Type mismatch")

    def create(self, name, type):
        if name not in self.table.keys():
            if type == "str":
                type = STR
                self.table[name] = ("", type)
            elif type == "int":
                type = INT
                self.table[name] = (0, type)
        else:
            raise Exception("Identifier already exists")

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        pass

class VarDec(Node):
    def Evaluate(self, st):
        for identifier in self.children:
            st.create(identifier.value, self.value)
class FuncDec(Node):
    def Evaluate(self, st):
        FuncTable.create(self.children[0].children[0].value, self.children[0].value, self)

class FuncCall(Node):
    def Evaluate(self, st):
        func_dec, type_func_dec = FuncTable.get(self.value)
        symbolTable = SymbolTable({})
        symbolTable.create(func_dec.children[0].children[0].value, type_func_dec)
        if (len(func_dec.children) > 2):
            index = 1
            while (index < len(func_dec.children)-1):
                vardec = func_dec.children[index]
                identifier = vardec.children[0]
                tipo = vardec.value
                valor_pareamento = self.children[index-1]
                symbolTable.create(identifier.value, tipo)
                symbolTable.set(identifier.value, valor_pareamento.Evaluate(st))
                index += 1
        return func_dec.children[-1].Evaluate(symbolTable)

class Return(Node):
    def Evaluate(self, st):
        return self.children[0].Evaluate(st)

class BinOp(Node):
    def Evaluate(self, st):
        left = self.children[0].Evaluate(st)
        right = self.children[1].Evaluate(st)
        if self.value == "+":
            if left[1] == INT and right[1] == INT:
                return (left[0] + right[0], INT)
            raise Exception("Need to sum two ints")
        elif self.value == "-":
            if left[1] == INT and right[1] == INT:
                return (left[0] - right[0], INT)
            raise Exception("Need to sub two ints")
        elif self.value == "*":
            if left[1] == INT and right[1] == INT:
                return (left[0] * right[0], INT)
            raise Exception("Need to mult two ints")
        elif self.value == ">":
            variable = left[0] > right[0]
            if variable:
                return (1, INT)
            return (0, INT)
        elif self.value == "<":
            variable = left[0] < right[0]
            if variable:
                return (1, INT)
            return (0, INT)
        elif self.value == "/":
            if left[1] == INT and right[1] == INT:
                return (left[0] // right[0], INT)
            raise Exception("Need to div two ints")
        elif self.value == "==":
            if left[1] == right[1]:
                variable = left[0] == right[0]
                if variable:
                    return (1, INT)
                return (0, INT)
            raise Exception("Need to compare two variables with the same type")
        elif self.value == "&&":
            if left[1] == INT and right[1] == INT:
                variable = left[0] and right[0]
                if variable:
                    return (1, INT)
                return (0, INT)
            raise Exception("Need to compare two variables with the same type")
        elif self.value == "||":
            if left[1] == INT and right[1] == INT:
                variable = left[0] or right[0]
                if variable:
                    return (1, INT)
                return (0, INT)
            raise Exception("Need to compare two variables with the same type")
        elif self.value == ".":
            return (str(left[0]) + str(right[0]), STR)
         
class UnOp(Node):
    def Evaluate(self, st):
        if self.value == "+":
            return (1 * self.children[0].Evaluate(st)[0], INT)
        elif self.value == "-":
            return (-1 * self.children[0].Evaluate(st)[0], INT)
        elif self.value == "!":
            variable = not self.children[0].Evaluate(st)[0]
            if variable:
                return (1, INT)
            return (0, INT)

class IntVal(Node):
    def Evaluate(self, st):
        return (self.value, INT)

class StrVal(Node):
    def Evaluate(self, st):
        return (self.value, STR)

class NoOp(Node):
    def Evaluate(self, st):
        pass

class Block(Node):
    def Evaluate(self, st):
        for child in self.children:
            if child.value == RETURN:
                return child.Evaluate(st)
            child.Evaluate(st)

class Identifier(Node):
    def Evaluate(self, st):
        return st.get(self.value)

class Assignment(Node):
    def Evaluate(self, st):
        right = self.children[1].Evaluate(st)
        st.set(self.value, right)

class Printf(Node):
    def Evaluate(self, st):
        print(self.children[0].Evaluate(st)[0])

class Scanf(Node):
    def Evaluate(self, st):
        return (int(input()), INT)

class If(Node):
    def Evaluate(self, st):
        if self.children[0].Evaluate(st)[0] == 1:
            self.children[1].Evaluate(st)
        elif len(self.children) > 2:
            self.children[2].Evaluate(st)

class While(Node):
    def Evaluate(self, st):
        while self.children[0].Evaluate(st)[0] == 1:
            self.children[1].Evaluate(st)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, origin, position, actual):
        self.origin = origin
        self.position = position
        self.actual = actual

    def selectNext(self):
        while (self.position < len(self.origin) and (self.origin[self.position] == " " or self.origin[self.position] == "\n")):
            self.position += 1
        if self.position >= len(self.origin):
            self.actual = Token(EOF, "EOF")
        elif self.origin[self.position] == "+":
            self.position += 1
            self.actual = Token(PLUS, "+")
        elif self.origin[self.position] == "-":
            self.position += 1
            self.actual = Token(MINUS, "-")
        elif self.origin[self.position] == "*":
            self.position += 1
            self.actual = Token(MULTIPLY, "*")
        elif self.origin[self.position] == "/":
            self.position += 1
            self.actual = Token(DIVIDE, "/")
        elif self.origin[self.position] == "(":
            self.position += 1
            self.actual = Token(OPEN_PARENTESIS, "(")
        elif self.origin[self.position] == ")":
            self.position += 1
            self.actual = Token(CLOSE_PARENTESIS, ")")
        elif self.origin[self.position] == "=":
            self.position += 1
            if self.origin[self.position] == "=":
                self.position += 1
                self.actual = Token(EQUALEQUAL, "==")
            else:
                self.actual = Token(EQUAL, "=")
        elif self.origin[self.position] == "{":
            self.position += 1
            self.actual = Token(OPEN_KEY, "{")
        elif self.origin[self.position] == "}":
            self.position += 1
            self.actual = Token(CLOSE_KEY, "}")
        elif self.origin[self.position] == ";":
            self.position += 1
            self.actual = Token(SEMICOLON, ";")   
        elif self.origin[self.position] == ">":
            self.position += 1
            self.actual = Token(GREATER_THAN, ">")
        elif self.origin[self.position] == "<":
            self.position += 1
            self.actual = Token(LESS_THAN, "<")
        elif self.origin[self.position] == "!":
            self.position += 1
            self.actual = Token(NOT, "!")
        elif self.origin[self.position] == "&" and  self.origin[self.position + 1] == "&":
            self.position += 2
            self.actual = Token(AND, "&&")
        elif self.origin[self.position] == "|" and self.origin[self.position + 1] == "|":
            self.position += 2
            self.actual = Token(OR, "||")
        elif self.origin[self.position] == ",":
            self.position += 1
            self.actual = Token(COMMA, ",")
        elif self.origin[self.position] == ".":
            self.position += 1
            self.actual = Token(POINT, ".")
        elif self.origin[self.position] == '"':
            candidate = ""
            self.position += 1
            while self.position < len(self.origin) and self.origin[self.position] != '"':
                candidate += self.origin[self.position]
                self.position += 1
            self.position += 1
            self.actual = Token(STR, str(candidate))
        elif self.origin[self.position].isdigit():
            candidate = self.origin[self.position]
            self.position += 1
            while self.position < len(self.origin) and self.origin[self.position].isdigit():
                candidate += self.origin[self.position]
                self.position += 1
            self.actual = Token(INT, int(candidate))
        elif self.origin[self.position].isalpha():
            candidate = self.origin[self.position]
            self.position += 1
            while self.position < len(self.origin) and (self.origin[self.position].isalpha() or self.origin[self.position] == "_" or self.origin[self.position].isdigit()):
                candidate += self.origin[self.position]
                self.position += 1
            if candidate in reserved_words:
                index = reserved_words.index(candidate)
                self.actual = Token(reserved_tokens[index], candidate)
            else:
               self.actual = Token(IDENTIFIER, candidate)
        else:
            raise Exception("The expression has a invalid caractere: " + self.origin[self.position])

class Parser:
    tokens: Tokenizer = None

    def parseExpression():
        node = Parser.parseTerm()
        while Parser.tokens.actual.type == PLUS or Parser.tokens.actual.type == MINUS or Parser.tokens.actual.type == OR or Parser.tokens.actual.type == POINT:
            if Parser.tokens.actual.type == PLUS:
                Parser.tokens.selectNext()
                node = BinOp("+", [node, Parser.parseTerm()])
            if Parser.tokens.actual.type == MINUS:
                Parser.tokens.selectNext()
                node = BinOp("-", [node, Parser.parseTerm()])
            if Parser.tokens.actual.type == OR:
                Parser.tokens.selectNext()
                node = BinOp("||", [node, Parser.parseTerm()])
            if Parser.tokens.actual.type == POINT:
                Parser.tokens.selectNext()
                node = BinOp(".", [node, Parser.parseTerm()])
        return node

    def parseRelExpression():
        node = Parser.parseExpression()
        while Parser.tokens.actual.type == EQUALEQUAL or Parser.tokens.actual.type == GREATER_THAN or Parser.tokens.actual.type == LESS_THAN:
            if Parser.tokens.actual.type == EQUALEQUAL:
                Parser.tokens.selectNext()
                node = BinOp("==", [node, Parser.parseExpression()])
            if Parser.tokens.actual.type == GREATER_THAN:
                Parser.tokens.selectNext()
                node = BinOp(">", [node, Parser.parseExpression()])
            if Parser.tokens.actual.type == LESS_THAN:
                Parser.tokens.selectNext()
                node = BinOp("<", [node, Parser.parseExpression()])
        return node
    
    def parseTerm():
        node = Parser.parseFactor()
        while Parser.tokens.actual.type == MULTIPLY or Parser.tokens.actual.type == DIVIDE or Parser.tokens.actual.type == AND:
            if Parser.tokens.actual.type == MULTIPLY:
                Parser.tokens.selectNext()
                node = BinOp("*", [node, Parser.parseFactor()])
            if Parser.tokens.actual.type == DIVIDE:
                Parser.tokens.selectNext()
                node = BinOp("/", [node, Parser.parseFactor()])
            if Parser.tokens.actual.type == AND:
                Parser.tokens.selectNext()
                node = BinOp("&&", [node, Parser.parseFactor()])
        return node

    def parseProgram():
        node = Block("", [])
        while Parser.tokens.actual.type != EOF:
            node.children.append(Parser.parseDeclaration())
        return node

    def parseDeclaration():
        if Parser.tokens.actual.type == TYPE:
            tipo = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == IDENTIFIER:
                vardec = [VarDec(tipo, [Identifier(Parser.tokens.actual.value, [])])]
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == OPEN_PARENTESIS:
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type != CLOSE_PARENTESIS:
                        if Parser.tokens.actual.type == TYPE:
                            tipo = Parser.tokens.actual.value
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.type == IDENTIFIER:
                                vardec.append(VarDec(tipo, [Identifier(Parser.tokens.actual.value, [])]))
                                Parser.tokens.selectNext()
                                while Parser.tokens.actual.type == COMMA:
                                    Parser.tokens.selectNext()
                                    if Parser.tokens.actual.type == TYPE:
                                        tipo = Parser.tokens.actual.value
                                        Parser.tokens.selectNext()
                                        if Parser.tokens.actual.type == IDENTIFIER:
                                            vardec.append(VarDec(tipo, [Identifier(Parser.tokens.actual.value, [])]))
                                            Parser.tokens.selectNext()
                                        else:
                                            raise ValueError
                                    else:
                                        raise ValueError
                            else:
                                raise ValueError
                        else:
                            raise ValueError
                    if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                        Parser.tokens.selectNext()
                        vardec.append(Parser.parseBlock())
                        node = FuncDec("", vardec)
                else:
                    raise Exception("Expected (")
            else:
                raise Exception("Expected identifier")
        return node


    def parseBlock():
        if Parser.tokens.actual.type == OPEN_KEY:
            Parser.tokens.selectNext()
            node = Block("", [])
            while Parser.tokens.actual.type != CLOSE_KEY:
                node.children.append(Parser.parseStatement())
            Parser.tokens.selectNext()
            return node
        else:
            raise Exception("You can't initialize without a { char")

    def parseStatement():
        if Parser.tokens.actual.type == SEMICOLON:
            Parser.tokens.selectNext()
            node = NoOp("", [])
        elif Parser.tokens.actual.type == IDENTIFIER:
            nome_identifier = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == OPEN_PARENTESIS:
                Parser.tokens.selectNext()
                node = FuncCall(nome_identifier, [])
                if Parser.tokens.actual.type != CLOSE_PARENTESIS:
                    node.children.append(Parser.parseRelExpression())
                    while Parser.tokens.actual.type == COMMA:
                        Parser.tokens.selectNext()
                        node.children.append(Parser.parseRelExpression())
                    if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                        Parser.tokens.selectNext()
                    else:
                        raise Exception("You need to close parentesis")
            elif Parser.tokens.actual.type == EQUAL:
                Parser.tokens.selectNext()
                identifier = Identifier(nome_identifier, [])
                node = Assignment(identifier.value, [identifier, Parser.parseRelExpression()])
                if Parser.tokens.actual.type == SEMICOLON:
                    Parser.tokens.selectNext()
                else:
                    raise Exception("You dont finalize with ;")
            else:
                raise Exception("parseStamement while")
        elif Parser.tokens.actual.type == PRINTF:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == OPEN_PARENTESIS:
                Parser.tokens.selectNext()
                node = Printf("", [Parser.parseRelExpression()])
                if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == SEMICOLON:
                        Parser.tokens.selectNext()
                    else:
                        raise Exception("You dont finalize with ;")
                else:
                    raise Exception("You need to close parentesis")
            else:
                raise Exception("You do not open parentesis after print")
        
        elif Parser.tokens.actual.type == TYPE:
            valor_tipo = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == IDENTIFIER:
                identifiers = [Identifier(Parser.tokens.actual.value, [])]
                Parser.tokens.selectNext()
                while Parser.tokens.actual.type == COMMA:
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == IDENTIFIER:
                        identifiers.append(Identifier(Parser.tokens.actual.value, []))
                        Parser.tokens.selectNext()

                    else:
                        raise Exception("You need to define a identifier")
                node = VarDec(valor_tipo, identifiers)
            else:
                raise Exception("You need to define a identifier")
        elif Parser.tokens.actual.type == OPEN_KEY:
            node = Parser.parseBlock()
        elif Parser.tokens.actual.type == IF:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == OPEN_PARENTESIS:
                Parser.tokens.selectNext()
                children_1 = Parser.parseRelExpression()
                if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                    Parser.tokens.selectNext()
                    children_2 = Parser.parseStatement()
                    if Parser.tokens.actual.type == ELSE:
                        Parser.tokens.selectNext()
                        children_3 = Parser.parseStatement()
                        node = If(IF, [children_1, children_2, children_3])
                    else:
                        node = If(IF, [children_1, children_2])
                else:
                    raise Exception("You need to close parentesis")
            else:
                raise Exception("You need to open parentesis after while")
        elif Parser.tokens.actual.type == RETURN:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == OPEN_PARENTESIS:
                Parser.tokens.selectNext()
                node = Parser.parseRelExpression()
                if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                    Parser.tokens.selectNext()
                    node = Return(RETURN, [node])
                else:
                    raise Exception("You need to close parentesis")
            else:
                raise Exception("You need to open parentesis in return")
        elif Parser.tokens.actual.type == WHILE:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == OPEN_PARENTESIS:
                Parser.tokens.selectNext()
                node = Parser.parseRelExpression()
                if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                    Parser.tokens.selectNext()
                    node = While(WHILE, [node, Parser.parseStatement()])
                else:
                    raise Exception("You need to close parentesis")
        else:
            raise Exception("No value entry")
        return node

    def parseFactor():
        node = None
        if Parser.tokens.actual.type == INT:
            node = IntVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == STR:
            node = StrVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == IDENTIFIER:
            nome_identifier = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == OPEN_PARENTESIS:
                Parser.tokens.selectNext()
                node = FuncCall(nome_identifier, [])
                if Parser.tokens.actual.type != CLOSE_PARENTESIS:
                    node.children.append(Parser.parseRelExpression())
                    while Parser.tokens.actual.type == COMMA:
                        Parser.tokens.selectNext()
                        node.children.append(Parser.parseRelExpression())
                    if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                        Parser.tokens.selectNext()
                    else:
                        raise Exception("You need to close parentesis")
            else:
                node = Identifier(nome_identifier, [])
        elif Parser.tokens.actual.type == PLUS:
            Parser.tokens.selectNext()
            node = UnOp("+", [Parser.parseFactor()])
        elif Parser.tokens.actual.type == MINUS:
            Parser.tokens.selectNext()
            node = UnOp("-", [Parser.parseFactor()])
        elif Parser.tokens.actual.type == NOT:
            Parser.tokens.selectNext()
            node = UnOp("!", [Parser.parseFactor()])
        elif Parser.tokens.actual.type == OPEN_PARENTESIS:
            Parser.tokens.selectNext()
            node = Parser.parseRelExpression()
            if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                Parser.tokens.selectNext()
            else:
                raise Exception("You dont close the parentesis")
        elif Parser.tokens.actual.type == SCANF:
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == OPEN_PARENTESIS:
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == CLOSE_PARENTESIS:
                    Parser.tokens.selectNext()
                    node = Scanf(SCANF, [])
                else:
                    raise Exception("You need to close parentesis of scanf")
            else:
                raise Exception("You need to open parentesis after scanf")
        else:
            raise Exception("Invalid character")
        return node

    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(origin = code, position = 0, actual = Token(None, ""))
        Parser.tokens.selectNext()

        retorno = Parser.parseProgram()
        retorno.children.append(FuncCall("main", []))
        symbolTableGlobal = SymbolTable({})
        returnOfAll = retorno.Evaluate(symbolTableGlobal)

        if Parser.tokens.actual.type != EOF:
            raise Exception("You cannot put this input")
        return returnOfAll

if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise Exception("You need to pass arguments")
    
    filename = sys.argv[1]

    f = open(filename, 'r')
    args = f.read()
    f.close()
    
    Parser.run(args)