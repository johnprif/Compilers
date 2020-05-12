# Prifth Ioannhs/AM 3321/username cse63321
# Theodwrou Gewrgios Euaggelos/AM 3231/username cse63231

import sys, pdb

reservedWords = ["program", "declare", "if", "else", "while", "doublewhile", "loop", "exit", "forcase", "incase",
                 "when", "default", "not", "and", "or", "function", "procedure", "call", "return", "in", "inout",
                 "input", "print"]
relationalOpers = ['=', "<=", ">=", '>', '<', "<>"]
mulOpers = ['*', '/']
addOpers = ['+', '-']
delimeters = [';', ',', ':']
groupingSymbols = ['(', ')', '[', ']', '{', '}']
comments = ["/*", "*/", "//"]
assign = [":="]

token = ""

# Variable where store the last location of the file that stopped reading
position = -1
# Variable where store the last line of the file that stopped reading
line = 0

currentQuadPlace = -1
quadsList = []
listOfVarTemps = []  # list with T_
tempCounter = -1

mainID = ""
internalFunction = False

functionIdList = []  # Function names
variablesListOfFunction = []  # List[List[List]] with function variables

currentFunctionVariablesPlace = -1

procedureIdList = []  # Procedure names
variablesListOfProcedure = []  # Lis[List[List]] with procedure variables

declareVariablesList = []

# Open file
fileName = input("Enter the file name: ")

# Check if it is of the required type
if ("min" in fileName):
    fileReader = open(fileName, 'r')
else:
    print("Wrong type of input file!\nExpected .min")
    sys.exit()


# Lektikos Analyths
def lex():
    global position
    global line
    tempString = ""
    char = ''

    #pdb.set_trace()

    while (True):
        position += 1
        fileReader.seek(position)
        char = fileReader.read(1)  # Reading char by char
        tempString += char 

        if (char == "\n"):
            line += 1
            tempString=tempString[:-1]
            continue
        elif (char.isspace()):  # Ignore spaces
            tempString=tempString[:-1]
            continue 
        elif (tempString in relationalOpers):  # Checks if it is a relational operant
            if (tempString == '<' or tempString == '>'):
                position += 1
                fileReader.seek(position)
                char = fileReader.read(1)
                tempString += char
                if (tempString in relationalOpers):
                    return tempString
                else:
                    position -= 1
                    fileReader.seek(position)
                    tempString = tempString[:-1]
                    return tempString
            return tempString
        elif (tempString in addOpers):  # Checks whether it is an add or subtract
            return tempString
        elif (char in delimeters):  # Checks if it is a delimeter
            if (char == ':'):
                position += 1
                fileReader.seek(position)
                char = fileReader.read(1)
                tempString += char
                if (tempString in assign):
                    return tempString
                else:
                    position -= 1
                    fileReader.seek(position)
                    tempString = tempString[:-1]
                    return tempString
            return tempString
        elif (tempString in mulOpers):
            position += 1
            fileReader.seek(position)
            char = fileReader.read(1)
            tempString += char
            if (tempString in comments): #// /*
                checkComments(tempString)
                token=lex()
            # return tempString
            else:
                position -= 1
                fileReader.seek(position)
                tempString = tempString[:-1]
                return tempString
        elif (tempString in groupingSymbols):  # Checks if it is a grouping symbol
            return tempString
        elif (tempString.isalpha()):  # Checks if it is a reserved word or variable name(Starts with char and without number)
            while (True):
                position += 1
                fileReader.seek(position)
                char = fileReader.read(1)

                if (char.isdigit() or char.isalpha()):
                    tempString += char
                    if (tempString in reservedWords):
                        position += 1
                        fileReader.seek(position)
                        char = fileReader.read(1)
                        if ((char in relationalOpers) or (char in mulOpers) or (char in addOpers) or (
                                char in delimeters) or (char in groupingSymbols) or (char in comments) or (
                                char in assign) or char.isspace()):
                            position -= 1
                            fileReader.seek(position)
                            return tempString
                else:
                    position -= 1
                    fileReader.seek(position)
                    if(tempString=="inut"):
                        return "input"
                    return tempString
        elif (tempString.isdigit()):  # Checks if it is a number
            while (True):
                print("Priftis: ", tempString)
                position += 1
                fileReader.seek(position)
                char = fileReader.read(1)
                if (not char.isdigit()):
                    position -= 1
                    fileReader.seek(position)
                    number = int(tempString)
                    if (number >= -32767 and number <= 32767):  # Checks if it belongs to the definition field
                        return number
                    else:
                        print("Number is out of range! at line=",line)
                        sys.exit()
                else:
                    tempString += char
        elif (char == EOFError):  # Checks for the end of file
            return EOFError


# It checks for comments and ignores them
def checkComments(varComment): #varComment==/* or varComment==//
    global token, position, line
    tempComment=""
    char=''
    #print("We are here in checkComments, tempComment: ", tempComment)
    if (varComment == "/*"):
        while (1):
            position += 1
            fileReader.seek(position)
            char = fileReader.read(1)
            # print("char:%c\n"%(char))
            if(char=="*"):
                tempComment += char
                position+=1
                char=fileReader.read(1)
                tempComment += char
                # print(tempComment)
                # print(tempComment == "*/")
                if (tempComment == EOFError or tempComment == "*/"):
                    #token=lex()
                    # print(token)
                    # print("vgika\n")
                    break
                elif (tempComment == "/*" or tempComment == "//"):
                    print("Error in comment at line=", line)
                    sys.exit()
    elif (varComment == "//"):
        while (1):
            position += 1
            fileReader.seek(position)
            char = fileReader.read(1)
            tempComment=char
            if (tempComment == EOFError or tempComment == '\n'):
                line+=1
                token=lex()
                break
            elif (tempComment == "//" or tempComment == "/*" or tempComment == "*/"):
                print("Error in comment at line=", line)
                sys.exit()


# Syntaktikos Analyths
def syntax():
    if (program()):
        print("Syntax analisys completed! ")
        return 1
    else:
        print("Syntax analisys failed! ")
        sys.exit()


def program():
    global mainID, token
    token=lex()
    if (token == "program"):
        token = lex()
        mainID = token
        if (mainID not in reservedWords):
            token=lex()
            block(mainID)
            if (token == "}"):
                print("We are here in program, token:", token)
                genquad("halt", "_", "_")
                genquad("end_block", mainID, "_", "_")
                return 1
        else:
            print("program id expected at line=", line)
            sys.exit()
    else:
        print("the keyword 'program' was expected at line=", line)
        sys.exit()


def block(funcID):
    global internalFunction, token
    if(token=="{"):
        token=lex()
        declarations()
        subprograms()
        if (funcID == mainID):
            internalFunction = False
            genquad("begin_block", mainID, "_", "_")
        else:
            genquad("begin_block", funcID, "_", "_")
            statements()
            print("We are here in block, token:", token)
    else:
        print("'{' was expected at line=",line)
        sys.exit()
    return 1


def declarations():
    global token
    if (token == "declare"):
        token=lex()
        varlist()
    return 1


def varlist():
    global token, internalFunction

    if (token not in reservedWords):
        declareVariable = token
        if (internalFunction == False):
            declareVariablesList.append([mainID, declareVariable])
        else:
            declareVariablesList.append([functionIdList[-1], declareVariable])
        token = lex()
        if (token == ","):
            token=lex()
            varlist()
        elif (token == ";"):
            token = lex()
            if (token == "declare"):  # Check for new declare after ';'
                token=lex()
                varlist()
        else:
            print("Error at declaration variable at line=", line)
            sys.exit()
    else:
        print("Incompatible varable name at line=", line)
        sys.exit()
    return 1


def subprograms():
    global token

    while (token == "function"):
        subprogram()    
    return 1


def subprogram():
    global functionIdList, procedureIdList, token

    if (token == "function"):
        token = lex()   
        functionID = token
        if (functionID in reservedWords):
            print("Incompatible function name at line=", line)
            sys.exit()
        if (functionID in functionIdList):
            print("Function with the same name already exists at line=", line)
            sys.exit()

        functionIdList.append(functionID)
        funcbody(functionID)
        if (token == "}"):
            genquad("end_block", functionID, "_", "_")
    elif (token == "procedure"):
        token = lex()
        procedureID = token
        if (procedureID in reservedWords):
            print("Incompatible procedure name at line=", line)
            sys.exit()
        if (procedureID in procedureIdList):
            print("Procedure with the ssame name already exist at line=", line)
            sys.exit()

        procedureIdList.append(procedureID)
        funcbody(procedureID)
        if (token == "}"):
            genquad("end_block", procedureID, "_", "_")
    else:
        print("incorrect subprogram syntax at line=", line)
        sys.exit()


def funcbody(funcName):
    global token, internalFunction
    internalFunction = True
    formalpars()
    block(funcName)
    return 1


def formalpars():
    global token
    token = lex()
    if (token == "("):
        token=lex()
        formalparlist()
        if (token == ")"):
            token = lex()
        else:
            print(" ')' expected after parameter list at line=", line)
            sys.exit()
    else:
        print(" '(' expected before parameter list at line=", line)
        sys.exit()


def formalparlist():
    global token
    if (token == ")"):
        return 1
    else:
        while (formalparitem()):
            token = lex()
            if (token == ")"):
                return 1
            else:
                return 0
            if (token == ','):
                token = lex()
                continue
            else:
                print(" ',' expected beetwen parameters at line=", line)
                sys.exit()
    return 1


def formalparitem():
    global token, variablesListOfFunction, functionIdList
    if (token == "in"):
        token = lex()
        if (token not in reservedWords):
            parInName = token
            variablesListOfFunction.append([functionIdList[-1], "in", parInName])
            return 1
        else:
            print("Incompatible varable name at line=", line)
            sys.exit()
    elif (token == "inout"):
        token = lex()
        if (token not in reservedWords):
            parInOutName = token
            variablesListOfFunction.append([functionIdList[-1], "inout", parInOutName])
            return 1
        else:
            print("Incompatible varable name at line=", line)
            sys.exit()
    else:
        print("No valid expression at line=", line)
        return 0


def statements():
    global token
    if (token != "{"):
        statement()
    elif (token == "{"):
        token = lex()
        while (statement()):
            token = lex()
            if (token == '}'):
                return 1
            else:
                print(" '}' was expected at line=", line)
                sys.exit()
            if (token == ';'):
                token = lex()
                continue
            else:
                print(" ';' was expected at line=", line)
                sys.exit()
    else:
        print(" '{' was expected at line=", line)
        sys.exit()


def statement():
    global token
    if (token not in reservedWords):
        assignmentStat()
    elif (token == "if"):
        ifStat()
    elif (token == "while"):
        whileStat()
    elif (token == "doublewhile"):
        doublewhileStat()
    elif (token == "loop"):
        loopStat()
    elif (token == "exit"):
        exitStat()
    elif (token == "forcase"):
        forcaseStat()
    elif (token == "incase"):
        incaseStat()
    elif (token == "call"):
        callStat()
    elif (token == "return"):
        returnStat()
    elif (token == "input"):
        inputStat()
    elif (token == "print"):
        printStat()
    else:
        print("Wrong Statement format at line=", line)
        sys.exit()


def assignmentStat():
    global token
    tempVarID = token
    if (tempVarID not in reservedWords):
        token = lex()
        if (token == ":="):
            token = lex()
            print("We are here in assignmentStat, token:", token)
            reTemp = expression()
            print("We are here in assignmentStat, reTemp:", reTemp)
            if (reTemp not in reservedWords):
                print("we are here in assignmentStat before genquad")
                genquad(":=", reTemp, "_", tempVarID)
                return 1
        else:
            print(" ':=' was expected at line=", line)
            sys.exit()
    else:
        print("Incompatible varable name at line=", line)
        sys.exit()


def ifStat():
    global token
    token = lex()
    if (token == "("):
        bTrue, bFalse = condition()
        if (token == ")"):
            token = lex()
            if (token == "then"):
                token = lex()
                backpatch(bTrue, nextquad())
                statements()
                token = lex()
                tempTemp = makelist(nextquad())
                genquad("jump", "_", "_", "_")
                backpatch(bFalse, nextquad())
                elsepart()
                backpatch(tempTemp, nextquad())
                if (token == "}"):
                    token = lex()
                else:
                    print("If statement never close at line=", line)
                    sys.exit()
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    else:
        print(" '(' was expected at line=", line)
        sys.exit()


def elsepart():
    global token
    if (token == "else"):
        token = lex()
        statements()
        return 1
    else:
        return 0


def whileStat():
    global token
    print("We are here in whileStat, token:", token)
    token = lex()
    if (token == "("):
        startWhile = nextquad()
        bTrue, bFalse = condition()
        if (token == ")"):
            token = lex()
            backpatch(bTrue, nextquad())
            statements()
            genquad("jump", "_", "_", startWhile)
            backpatch(bFalse, nextquad())
            if (token == "}"):
                token = lex()
            else:
                print("While statement never stop at line=", line)
                sys.exit()
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    else:
        print(" '(' was expected at line=", line)
        sys.exit()


"""         
def doublewhileStat():
    if(token=='('):
        token=lex()
        condition()
        if(token==')'):
            token=lex()
            statements()
            if(token=="else"):
                token=lex()
                statements()
                return 1
            else:
                print("the keyword 'else' was expected at line=",l)
                return 0
        else:
            print(" ')' was expected at line=",l)
            return 0
    else:
        print(" '(' was expected at line=",l)
        return 0

def loopStat():
    statements()
    token=lex()
    return 1

def exitStat():
    token=lex() 
    return 1
"""


def forcaseStat():
    global token
    startForCase = nextquad()
    tempTrueList = []
    while (token == "when"):
        token = lex()
        if (token == "("):
            bTrue, bFalse = condition()
            if (token == ")"):
                token = lex()
                if (token == ":"):
                    token = lex()
                    backpatch(bTrue, nextquad())
                    statements()
                    tempTrueList.append(nextquad())
                    genquad("jump", "_", "_", "_")
                    backpatch(bFalse, nextquad())
                    token = lex()
                else:
                    print(" ':' was expected at line=", line)
                    sys.exit()
            else:
                print(" ')' was expected at line=", line)
                sys.exit()
        else:
            print(" '(' was expected at line=", line)
            sys.exit()
    if (token == "default"):
        token = lex()
        if (token == ":"):
            token = lex()
            backpatch(bFalse.nextquad())
            statements()
            if (token == "}"):
                genquad("jump", "_", "_", startForCase)
                backpatch(tempTrueList, nextquad())
                token = lex()
            else:
                print("For case never sto at line=", line)
                sys.exit()
        else:
            print(" ':' was expected at line=", line)
            sys.exit()
    else:
        print(" 'default' expression was expected at line=", line)
        sys.exit()


""" 
def incaseStat():
    while(token=="when"):
        token=lex()
        if(token=="("):
            token=lex()
            condition()
            if(token==")"):
                token=lex()
                if(token==':'):
                    token=lex()
                    statements()
                else:
                    print(" ':' was expected at line=",line)
                    sys.exit()
            else:
                print(" ')' was expected at line=",line)
        else:
            print(" '(' was expected at line=",line)
            sys.exit()
"""


def returnStat():
    global token, internalFunction
    token = lex()
    expressionTemp = expression()
    genquad("retv", expressionTemp, "_", "_")
    if (internalFunction == False):
        print("Return statement is out of function at line=", line)
        sys.exit()


""" 
def callStat():
    if(token==idtk):
        token=lex()
        if(token=='('):
            token=lex()
            actualpars()
            if(token==')'):
                token=lex()
                return 1
            else:
                print(" ')' was expected at line=",l)
                return 0
        else:
            print(" '(' was expected at line=",l)
            return 0
    else:
        print("call ID expected at line=",l)
        return 0
"""


def printStat():
    global token
    token = lex()
    expressionTemp = expression()
    genquad("out", expressionTemp, "_", "_")
    return 1


def inputStat():
    global token
    token = lex()
    if (token not in reservedWords and token.isalnum()):
        genquad("inp", token, "_", "_")
        token = lex()
    else:
        print("Error with ID in input expression at line=", line)
        sys.exit()


def actualpars(callerID):
    global token
    if (token == "("):
        actualparlist(callerID)
        if (token == ")"):
            tempTemp = newtemp()
            genquad("par", tempTemp, "RET", "_")
            genquad("call", callerID, "_", "_")
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    else:
        print(" '(' was expected at line=", line)
        sys.exit()
    return tempTemp


def actualparlist(callerID):
    global token
    actualparitem(callerID)
    while (token == ","):
        actualparitem(callerID)


def actualparitem(callerID):
    global token
    token = lex()
    if (token == "in"):
        token = lex()
        expressionTemp = expression()
        genquad("par", expressionTemp, "CV", "_")
    elif (token == "inout"):
        token = lex()
        if (token not in reservedWords):
            genquad("par", token, "REF", "_")
            token = lex()
        else:
            print("No ID found after inout expression at line=", line)
            sys.exit()
    else:
        print("No valid expression at line=", line)
        sys.exit()


def condition():
    global token
    bTrue, bFalse = q1True, q1False = boolterm()
    while (token == "or"):
        backpatch(bFalse, nextquad())
        q2True, q2False = boolterm()
        bTrue = merge(bTrue, q2True)
        bFalse = q2False
    return bTrue, bFalse


def boolterm():
    global token
    qTrue, qFalse = r1True, r1False = boolfactor()
    while (token == "and"):
        backpatch(qTrue, nextquad())
        r2True, r2False = boolfactor()
        qFalse = merge(qFalse, r2False)
        qTrue = r2True
    return qTrue, qFalse


def boolfactor():
    global token
    token = lex()
    if (token == "not"):
        token = lex()
        if (token == "["):
            # token=lex()
            bFalse, bTrue = condition()
            if (token == "]"):
                token = lex()
            else:
                print(" ']' was expected at line=", line)
                sys.exit()
        else:
            print(" '[' was expected at line=", line)
            sys.exit()
    elif (token == "["):
        # token=lex()
        bTrue, bFalse = condition()
        if (token == "]"):
            pass
        else:
            print(" ']' was expected at line=", line)
            sys.exit()
    else:
        expressionTemp = expression()
        tempList = emptylist()
        relationaloper()
        relopTemp = token
        token = lex()
        expressionTemp2 = expression()
        bTrue = makelist(nextquad())
        genquad(relopTemp, expressionTemp, expressionTemp2, "_")
        bFalse = makelist(nextquad())
        genquad("jump", "_", "_", "+")
    return bTrue, bFalse


def expression():
    global token
    optionalsignTemp = optionalsign()
    termTemp = term() #0
    while (token == "+" or token == "-"):
        optionalsignTemp = token
        token = lex()  # or addoper(), will see
        termTemp2 = term()
        tempTemp = newtemp()
        genquad(optionalsignTemp, termTemp, termTemp2, tempTemp)
        termTemp = tempTemp
    return termTemp


def term():
#   pdb.set_trace()
    global token #while
    print("We are here in temp, token:",token)
    factorTemp = factor() #0
    print("We are here in temp, factorTemp:", factorTemp)
#   if (factorTemp not in functionIdList):
#       print("Function: ", factorTemp, "not declared at line=", line)
#       sys.exit()
    while (token == "*" or token == "/"):
        tempToken = token
        token = lex()
        muloper()
        factorTemp2 = factor()
        if (factorTemp2 not in functionIdList):
            print("Function: ", factorTemp, "not declared at line=", line)
            sys.exit()
        temp = newtemp()
        genquad(tempToken, factorTemp, factorTemp2, temp)
        factorTemp = temp
    return factorTemp


def factor():
    global token
    if (str(token).isdigit()):
        tempConstant = token
        token = lex()
        print("We are here in factor, token:", token)
    elif (token == "("):
        tempConstant = token
        token = lex()
        expression()
        if (token == ")"):
            pass
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    elif (token not in reservedWords and token.isalnum()):
        tempConstant = token
        token = lex()
        tempConstant = idtail(tempConstant)  # to tempConstant allazei epidi sthn periptosh call w = newTemp() par, w, RET, _ xriazomaste to w to opio einai temp kai epistrefei
    else:
        print("Problem with factor function at line=", line)
        sys.exit()
    return tempConstant


def idtail(callerID):
    global token
    name = callerID
    if (token == "("):
        name = actualpars(callerID)
    return name


def relationaloper():
    global token
    if (token == '='):
        return 1
    elif (token == "<="):
        return 1
    elif (token == ">="):
        return 1
    elif (token == '>'):
        return 1
    elif (token == '<'):
        return 1
    elif (token == "<>"):
        return 1
    else:
        print("invalid relational operant at line=", line)
        sys.exit()


def addoper():
    global token
    if (token == "+"):
        token = lex()
        return token
    elif (token == "-"):
        token = lex()
        return token
    else:
        print("invalid addoper at line=", line)
        sys.exit()


def muloper():
    global token
    if (token == "*"):
        return token
    elif (token == '/'):
        return token
    else:
        print("invalid muloper at line=", line)
        sys.exit()


def optionalsign():
    global token
    if (token == "+" or token == "-"):
        addoper()
    return token


def nextquad():
    global currentQuadPlace
    return currentQuadPlace + 1


def genquad(op, x, y, z):
    global currentQuadPlace, quadsList
    currentQuadPlace += 1
    if (z in reservedWords):
        print("Error in name of z at line=", line)
        sys.exit()
    quadsList.append([currentQuadPlace, op, x, y, z])
    return 1


def newtemp():
    global tempCounter, listOfVarTemps
    tempCounter += 1
    tempVarStringNumber = str(tempCounter)
    tempVarName = "T_" + tempVarStringNumber
    listOfVarTemps.append(tempVarName)
    return tempVarName


def emptylist():
    newEmptyList = []
    return newEmptyList


def makelist(x):
    newList = []
    newList.append(x)
    return newList


def merge(list1, list2):
    newList = list1 + list2
    return newList


def backpatch(par_list, z):
    global quadsList
    for i in quadsList:
        if (i[3] == "_"):
            i[3] = z


def minQuadToCquad(quad, iterator):
    global currentFunctionVariablesPlace
    # insideFunction=False
    if (quad[0] == "jump"):
        cQuad = "goto L_" + quad[3] + ";\n"
    elif (quad[0] in mulOpers or quad[0] in addOpers):
        cQuad = quad[3] + "=" + quad[1] + quad[0] + quad[2] + ";\n"
    elif (quad[0] in relationalOpers):
        if (quad[0] == "<>"):
            operation = "!="
        elif (quad[0] == "="):
            operation = "=="
        else:
            operation = quad[0]
        cQuad = "if(" + quad[1] + operation + quad[2] + ")" + " goto L_" + quad[3] + ";\n"
    elif (quad[0] in assign):
        operation = "="
        cQuad = quad[3] + operation + quad[1] + ";\n"
    elif (quad[0] == "halt"):
        cQuad = "return 1;\n"
    elif (quad[0] == "end_block"):
        cQuad = "}"
    elif (quad[0] == "inp"):
        cQuad = "scanf(%d," + quad[1] + ");\n"
    elif (quad[0] == "retv"):
        cQuad = "return " + quad[1] + ";\n"
    elif (quad[0] == "out"):
        cQuad = "printf(%d" + quad[1] + ");\n"
    elif (quad[0] == "begin_block"):
        if (quad[1] == mainID):
            cQuad = "int main()\n{\n   int "
            for var in declareVariable:
                if (var[0] == mainID):
                    cQuad += var[1] + ","
            cQuad = cQuad[:-1] + ";\n"
            return cQuad
        #else:
        #   insideFunction=True
        #   currentFunctionVariablesPlace+=1
        #   for var in variablesListOfFunction:
        #       if(var[0]==currentFunctionVariablesPlace):
        #           temp=var[1]+var[2]
        #       temp+=temp
        #   cQuad="int"+quad[1]+"("+temp+")\n{" 
    cQuad = "L_" + iterator + ": " + cQuad
    return cQuad


def makeCfile():
    global quadsList
    minToCquadsFile = open("minToCquads.c", "w+")
    minToCquadsFile.write("#include <stdio.h>\n\nint main()\n{\n")
    iterator = -1
    for quad in quadsList:
        iterator += 1
        minToCquadsFile.write(minQuadToCquad(quad, iterator))

# Call the syntax
syntax()
# Call the makeCfile
makeCfile()

close(file)  # Closing the file


