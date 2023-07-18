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
quadCounter = 0

mainID = ""
internalFunction = False

functionIdList = []  # Function names
variablesListOfFunction = []  # List[[fuctionId,in or inout, varName],..] with function variables
functionParList = []

procedureIdList = []  # Procedure names
variablesListOfProcedure = []  # List[[procedureId,in or inout, varName],..] with procedure variables

currentFunctionVariablesPlace = -1

declareVariablesList = []

nesting = 1

scopeList = [""]

afterScopeList = []

scopeCounter = 0

# Open file
# fileName = input("Enter the file name: ")
fileName = sys.argv[1]

# Check if it is of the required type
if ("min" in fileName):
    fileReader = open(fileName, 'r')
else:
    print("Wrong type of input file!\nExpected .min")
    sys.exit()


# Lektikos Analyths
def lex():
    global position, line, token
    tempString = ""
    char = ''

    # pdb.set_trace()

    while (True):
        position += 1
        fileReader.seek(position)
        char = fileReader.read(1)  # Reading char by char
        tempString += char
        if (char == "\n"):
            line += 1
            tempString = tempString[:-1]
            continue
        elif (char.isspace()):  # Ignore spaces
            tempString = tempString[:-1]
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
            if (tempString in comments):  # // /*
                tempCom = checkComments(tempString)
                if (tempCom != EOFError):
                    # lex()
                    return token
                elif (tempCom == '\n'):
                    token = lex()
                else:
                    print("Problem with comments!")
                    sys.exit()
            else:
                position -= 1
                fileReader.seek(position)
                tempString = tempString[:-1]
                return tempString
        elif (tempString in groupingSymbols):  # Checks if it is a grouping symbol
            return tempString
        elif (
        tempString.isalpha()):  # Checks if it is a reserved word or variable name(Starts with char and without number)
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
                    if (tempString == "inut"):
                        return "input"
                    return tempString
        elif (tempString.isdigit()):  # Checks if it is a number
            while (True):
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
                        print("Number is out of range! at line=", line)
                        sys.exit()
                else:
                    tempString += char
        elif (char == EOFError):  # Checks for the end of file
            sys.exit()
            # return EOFError


# It checks for comments and ignores them
def checkComments(varComment):  # varComment==/* or varComment==//
    global token, position, line
    tempComment = ""
    char = ''
    if (varComment == "/*"):
        while (1):
            position += 1
            fileReader.seek(position)
            char = fileReader.read(1)
            if (char == "*"):
                tempComment += char
                position += 1
                char = fileReader.read(1)
                tempComment += char
                if (tempComment == "*/"):
                    token = lex()
                    return token
                elif (tempComment == "/*" or tempComment == "//"):
                    print("Error in comment at line=", line)
                    sys.exit()
                elif (char == EOFError):
                    print("comment never closed")
                    sys.exit()
                else:
                    pass
    elif (varComment == "//"):
        while (1):
            position += 1
            fileReader.seek(position)
            char = fileReader.read(1)
            tempComment = char
            if (tempComment == '\n'):
                line += 1
                if (char != EOFError):
                    token = lex()
                else:
                    return EOFError
                return token
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
    global mainID, token, internalFunction, nesting, afterScopeList, scopeCounter, scopeList
    token = lex()
    if (token == "program"):
        token = lex()
        mainID = token
        tempScope = Scope(nesting)
        tempEntity = Entity("-main", "main", 8)
        tempScope.addEntity(tempEntity)
        scopeList[scopeCounter] = tempScope
        if ((mainID not in reservedWords) and mainID.isalnum()):
            token = lex()
            if (token == "{"):
                token = lex()
                block(mainID)
            else:
                print("I AM HERE")
                print("'{' was expected at line=", line)
                sys.exit()
            if (token == "}"):
                if (internalFunction == False):
                    genquad("halt", "_", "_", "_")
                    genquad("end_block", mainID, "_", "_")
                    afterScopeList.append(scopeList.pop(0))
                    return 1
                else:
                    genquad("end_block", functionIdList[-1], "_", "_")
                    return 0
            else:
                print("'}' was expected at line=", line)
                sys.exit()
        else:
            print("program id expected at line=", line)
            sys.exit()
    else:
        print("the keyword 'program' was expected at line=", line)
        sys.exit()


def block(funcID):
    global internalFunction, token, mainID, scopeList
    if (funcID == mainID):
        internalFunction = False
        genquad("begin_block", mainID, "_", "_")
    else:
        tempScope = scopeList[0]
        tempEntity_1 = tempScope.getEntityList()
        tempEntity = tempEntity_1[0]
        tempEntity.setStartQuad(nextquad())
        tempEntity_1[0] = tempEntity
        tempScope.setEntityList(tempEntity_1)
        genquad("begin_block", funcID, "_", "_")
    declarations()
    token = lex()
    subprograms()
    statements()
    return 1


def declarations():
    global token
    if (token == "declare"):
        varlist()
        if (token == ";"):
            declarations()
        else:
            print("';' was expected at line=", line)
            sys.exit()
        #   else:
    #       print("keyword 'declare' was expected at line=", line)
    #       sys.exit()
    return 1


def varlist():
    global token, internalFunction, scopeList, scopeCounter, declareVariablesList
    token = lex()
    temp = Entity("", "", 0)
    temp = scopeSearch(token)
    if ((token not in reservedWords) and token.isalnum() and temp.name == "nothing"):
        declareVariable = token
        tempScope = scopeList[scopeCounter]
        totalTempScope = tempScope.getTotalOffset()
        tempEntity = Entity(token, "var", (totalTempScope + 4))
        if (internalFunction == False):
            declareVariablesList.append([mainID, declareVariable])
        else:
            declareVariablesList.append([functionIdList[-1], declareVariable])
        tempScope.addEntity(tempEntity)
        scopeList[scopeCounter] = tempScope
        token = lex()
        if (token == ","):
            varlist()
        else:
            return 1
    else:
        print("Incompatible variable name at line=", line)
        sys.exit()
    return 1


def subprograms():
    global token
    while (token == "function" or token == "procedure"):
        subprogram()
    return 1


def subprogram():
    global functionIdList, procedureIdList, token, nesting, scopeList, afterScopeList, scopeCounter
    if (token == "function"):
        token = lex()
        nesting += 1
        functionID = token
        #       token=lex()
        tempTemp = Entity("", "", 0)
        tempTemp = scopeSearch(functionID)
        if (functionID in reservedWords or tempTemp.name == functionID):
            print("Incompatible function name at line=", line)
            sys.exit()
        if (functionID in functionIdList):
            print("Function with the same name already exists at line=", line)
            sys.exit()
        if (functionID in groupingSymbols):
            print("Function id was expected at line=", line)
            sys.exit()
        tempScope = Scope(nesting)
        tempEntity = Entity(functionID, "function", 8)
        tempScope.addEntity(tempEntity)
        scopeList.insert(0, tempScope)
        token = lex()
        if (functionID.isalnum()):
            functionIdList.append(functionID)
        funcbody(functionID)
        if (token == "}"):
            afterScopeList = scopeList[scopeCounter + 1]
            tempScope = scopeList[scopeCounter]
            temp = tempScope.getEntityList()
            tempEntity = temp[0]
            entityTemp = temp[-1]
            tempEntity.setOffset(afterScopeList.getTotalOffset())
            tempEntity.setFrameLength(entityTemp.getOffset())
            afterScopeList.addEntity(tempEntity)
            genquad("end_block", functionID, "_", "_")
            nesting -= 1
            afterScopeList.append(scopeList.pop(0))
    elif (token == "procedure"):
        token = lex()
        nesting += 1
        procedureID = token
        tempTemp = Entity("", "", 0)
        tempTemp = scopeSearch(procedureID)
        if (procedureID in reservedWords):
            print("Incompatible procedure name at line=", line)
            sys.exit()
        if (procedureID in procedureIdList):
            print("Procedure with the same name already exist at line=", line)
            sys.exit()
        if (procedureID in groupingSymbols):
            print("Function id was expected at line=", line)
            sys.exit()
        tempScope = Scope(nesting)
        tempEntity = Entity(procedureID, "procedure", 8)
        tempScope.addEntity(tempEntity)
        scopeList.insert(0, scope)
        token = lex()
        if (procedureID.isalnum()):
            procedureIdList.append(procedureID)
        funcbody(procedureID)
        if (token == "}"):
            afterScopeList = scopeList[scopeCounter + 1]
            tempScope = scopeList[scopeCounter]
            temp = tempScope.getEntityList()
            tempEntity = temp[0]
            entityTemp = temp[-1]
            tempEntity.setOffset(afterScopeList.getTotalOffset())
            tempEntity.setFrameLength(entityTemp.getOffset())
            afterScopeList.addEntity(tempEntity)
            genquad("end_block", procedureID, "_", "_")
            nesting -= 1
            afterScopeList.append(scopeList.pop(0))
    else:
        print("incorrect subprogram syntax at line=", line)
        sys.exit()


def funcbody(funcName):
    global token, internalFunction
    internalFunction = True
    formalpars()
    if (token == "{"):
        token = lex()
        block(funcName)
        token = lex()
        if (token == "}"):
            genquad("end_block", funcName, "_", "_")
            token = lex()
            internalFunction = False
            return 1
        else:
            print("'}' was expected at line=", line)
            sys.exit()
    else:
        print("'{' was expected at line=", line)
        sys.exit()
    return 1


def formalpars():
    global token
    if (token == "("):
        token = lex()
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
            if (token == ','):
                token = lex()
                formalparitem()
                token = lex()
                continue
            else:
                return 1
    return 1


def formalparitem():
    global token, variablesListOfFunction, functionIdList, variablesListOfProcedure, procedureIdList, scopeCounter, scopeList
    if (token == "in"):
        token = lex()
        tempScope = scopeList[scopeCounter]
        if (token not in reservedWords):
            parInName = token
            variablesListOfFunction.append([functionIdList[-1], "in", parInName])

            tempEntity = Entity(parInName, "var", tempScope.getTotalOffset() + 4)
            tempEntity.setParMode("in")
            tempScope.addEntity(tempEntity)
            tempArg = Argument("in", "int")
            tempTemp = tempScope.getEntityList()
            tempEntity = tempTemp[0]
            tempEntity.setArgument(tempArg)
            tempTemp[0] = tempEntity
            tempScope.setEntityList(tempTemp)
            scopeList[scopeCounter] = tempScope
            return 1
        else:
            print("Incompatible variable name at line=", line)
            sys.exit()
    elif (token == "inout"):
        token = lex()
        if (token not in reservedWords):
            parInOutName = token
            variablesListOfProcedure.append([functionIdList[-1], "inout", parInOutName])

            tempEntity = Entity(parInOutName, "var", tempScope.getTotalOffset() + 4)
            tempEntity.setParMode("inout")
            tempScope.addEntity(tempEntity)
            tempArg = Argument("inout", "int")
            tempTemp = tempScope.getEntityList()
            tempEntity = tempTemp[0]
            tempEntity.setArgument(tempArg)
            tempTemp[0] = tempEntity
            tempScope.setEntityList(tempTemp)
            scopeList[scopeCounter] = tempScope
            return 1
        else:
            print("Incompatible varable name at line=", line)
            sys.exit()
    else:
        print("No valid expression at line=", line)
        return 0


def statements():
    global token
    if (token == "{"):
        token = lex()
        statement()
        #       token=lex()
        while (token == ";"):
            token = lex()
            statement()
        if (token == "}"):
            return 1
        else:
            print("'}' was exprected at line=", line)
            sys.exit()
    else:
        print("'{' was exprected at line=", line)
        sys.exit()

    # pdb.set_trace()


def statement():
    global token
    if ((token not in reservedWords) and (token not in delimeters)):
        assignmentStat()
    if (token == "if"):
        ifStat()
    if (token == "while"):
        whileStat()
    if (token == "doublewhile"):
        doublewhileStat()
    if (token == "loop"):
        loopStat()
    if (token == "exit"):
        exitStat()
    if (token == "forcase"):
        forcaseStat()
    if (token == "incase"):
        incaseStat()
    if (token == "call"):
        callStat()
    if (token == "return"):
        returnStat()
    if (token == "input"):
        inputStat()
    if (token == "print"):
        printStat()
    return 1


def assignmentStat():
    global token, declareVariablesList
    tempVarID = token
    tempScope = scopeSearch(tempVarID)
    if (tempScope.name == "nothing"):
        print("Variable:", tempVarID, "not declared at line=", line)
        sys.exit()
    if ((tempVarID not in reservedWords) and tempVarID.isalnum()):
        declareVariablesList.append([functionIdList[-1], tempVarID])
        token = lex()
        if (token == ":="):
            token = lex()
            reTemp = expression()
            if (reTemp not in reservedWords):
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
                backpatch(bTrue, nextquad())
                statements()
                token = lex()
                tempTemp = makelist(nextquad())
                genquad("jump", "_", "_", "_")
                backpatch(bFalse, nextquad())
                elsepart()
                backpatch(tempTemp, nextquad())
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    else:
        print(" '(' was expected at line=", line)
        sys.exit()
    return 1


def elsepart():
    global token
    if (token == "else"):
        statements()
        return 1
    else:
        return 0


def whileStat():
    global token, line
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
                return 1
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
    token = lex()
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
            genquad("jump", "_", "_", startForCase)
            backpatch(tempTrueList, nextquad())
            token = lex()
        else:
            print(" ':' was expected at line=", line)
            sys.exit()
    else:
        print(" 'default' expression was expected at line=", line)
        sys.exit()
    return 1


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
    global token, internalFunction, declareVariablesList
    token = lex()
    expressionTemp = expression()
    i = 0
    for varList in declareVariablesList:
        i += 1
        if (expressionTemp == varList[1]):
            genquad("retv", expressionTemp, "_", "_")
            break
        if (len(declareVariablesList) == i and expressionTemp != varList[1]):
            print("return variable not declared at line=", line)
            sys.exit()
    if (internalFunction == False):
        print("Return statement is out of function at line=", line)
        sys.exit()
    token = lex()
    return 1


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
    if (token == "("):
        token = lex()
        expressionTemp = expression()
        if (token == ")"):
            token = lex()
            genquad("out", expressionTemp, "_", "_")
            return 1
        else:
            print("')' was expected at line=", line)
            sys.exit()
    else:
        print("'(' was expected at line=", line)
        sys.exit()
    return 1


def inputStat():
    global token, line
    token = lex()
    if (token == "("):
        token = lex()
        tempSer = scopeSearch(token)
        if (token not in reservedWords and token.isalnum() and tempSer.name == token):
            genquad("inp", token, "_", "_")
            token = lex()
            token = lex()
            return 1
        else:
            print("Error with ID in input expression at line=", line)
            sys.exit()
        if (token == ")"):
            return 1
        else:
            print("')' was expected at line=", line)
            sys.exit()
    else:
        print("'(' was expected at line=", line)


def actualpars(callerID):
    global token, scopeList
    token = lex()
    if (token == "("):
        actualparlist(callerID)
        if (token == ")"):
            tempTemp = newtemp()
            scopeTemp = tempScope[0]
            tempSer = Entity("", "", 0)
            tempSer = scopeSearch(tempTemp)
            if (tempSer.name == "nothing"):
                tempEntity = Entity(tempTemp, "var", scopeTemp.getTotalOffset() + 4)
                scopeTemp.addEntity(tempEntity)
                scopeList[0] = scopeTemp
            else:
                pass
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
    global token, functionParList
    tempFunctionPars = Entity(callerID, "checkFunctionPars", 0)
    functionParList.insert(0, tempFunctionPars)
    actualparitem(callerID)
    while (token == ","):
        actualparitem(callerID)


def actualparitem(callerID):
    global token, functionParList
    token = lex()
    tempFunctionPars = functionParList[0]
    if (token == "in"):
        token = lex()
        tempArg = Argument("in", "int")
        tempFunctionPars.setArgument(tempArg)
        expressionTemp = expression()
        genquad("par", expressionTemp, "CV", "_")
    elif (token == "inout"):
        token = lex()
        tempArg = ("inout", "int")
        tempFunctionPars.setArgument(tempArg)
        genquad("par", token, "REF", "_")
        # token = lex()
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
    global token, scopeList
    optionalsignTemp = optionalsign()
    termTemp = term()  # result
    tempSer = scopeSearch(termTemp)
    """if(tempSer.name != termTemp):
        print("Variable: ", termTemp, "Not declared at line=", line)
        sys.exit()"""
    tempScope = scopeList[scopeCounter]
    while (token == "+" or token == "-"):
        optionalsignTemp = token
        token = lex()
        tempSer = Entity("", "", 0)
        tempSer = scopeSearch(token)
        """if(token != tempSer.name):
            print("Variable: ", token, "not declared at line=", line)
            sys.exit()
        else:
            pass"""
        termTemp2 = term()
        tempSer = scopeSearch(termTemp2)
        """if(termTemp2 != tempSer):
            print("Variable: ", termTemp2, "not declared at line=", line)
            sys.exit()
        else:
            pass"""
        tempTemp = newtemp()
        tempSer = scopeSearch(tempTemp)
        """if(tempSer.name=="nothing"):
            tempScope2=tempScope.getTotalOffset()
            tempEntity=Entity(tempTemp,"var",tempScope2+4)
            tempScope.addEntity(tempEntity)
        else:
            pass"""
        genquad(optionalsignTemp, termTemp, termTemp2, tempTemp)
        termTemp = tempTemp
    scopeList[scopeCounter] = tempScope
    tempSer = scopeSearch(termTemp)
    """1if(termTemp != tempSer.name):
        print("Variable: ", termTemp, "not declared at line= at 997", line)
        sys.exit()
    else:
        pass"""
    return termTemp


def term():
    global token, scopeList
    factorTemp = factor()  # result
    #   if (factorTemp not in functionIdList):
    #       print("Function: ", factorTemp, "not declared at line=", line)
    #       sys.exit()
    tempScope = scopeList[scopeCounter]
    while (token == "*" or token == "/"):
        muloper()
        tempToken = token
        token = lex()
        tempSer = Entity("", "", 0)
        tempSer = scopeSearch(token)
        if (token != tempSer.name):
            print("Variable: ", token, "not declared at line=", line)
            sys.exit()
        else:
            pass
        factorTemp2 = factor()
        tempSer = scopeSearch(factorTemp2)
        if (factorTemp2 != tempSer.name):
            print("Variable: ", factorTemp2, "not declared at line=", line)
            sys.exit()
        else:
            pass
        #       if (factorTemp2 not in functionIdList):
        #           print("Variable: ", factorTemp, "not declared at line=", line)
        #           sys.exit()
        temp = newtemp()
        tempSer = scopeSearch(temp)
        if (tempSer.name == "nothing"):
            tempScope2 = tempScope.getTotalOffset()
            tempEntity(temp, "var", tempScope2 + 4)
            tempScope.addEntity(tempEntity)
        else:
            pass
        genquad(tempToken, factorTemp, factorTemp2, temp)
        factorTemp = temp
    scopeList[scopeCounter] = tempScope
    return factorTemp  # result


def factor():
    global token
    if (str(token).isdigit()):
        tempConstant = token
        token = lex()
    elif (token == "("):
        token = lex()
        tempConstant = token
        expression()
        if (token == ")"):
            pass
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    elif (token not in reservedWords and token.isalnum()):
        tempConstant = token
        token = lex()
        tempConstant = idtail(tempConstant)
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
        if (i[0] in par_list):
            i[4] = z


def minQuadToCquad(quad, iterator):
    global currentFunctionVariablesPlace, listOfVarTemps, variablesListOfFunction
    # insideFunction=False
    cQuad = ""
    if (quad[1] == "jump"):
        cQuad = "goto L_" + str(quad[4]) + ";"
    elif (quad[1] in mulOpers or quad[1] in addOpers):
        cQuad = str(quad[4]) + "=" + str(quad[2]) + str(quad[1]) + str(quad[3]) + ";"
    elif (quad[1] in relationalOpers):
        if (quad[1] == "<>"):
            operation = "!="
        elif (quad[1] == "="):
            operation = "=="
        else:
            operation = str(quad[1])
        cQuad = "if(" + str(quad[2]) + operation + str(quad[3]) + ")" + " goto L_" + str(quad[4]) + ";"
    elif (quad[1] in assign):
        operation = "="
        cQuad = str(quad[4]) + str(operation) + str(quad[2]) + ";"
    elif (quad[1] == "halt"):
        cQuad = "return 1;"
    elif (quad[1] == "end_block" and quad[2] == mainID):
        cQuad = "\n}"
    elif (quad[1] == "end_block" and (quad[2] in functionIdList or quad[2] in procedureIdList)):
        cQuad = "goto L_" + str(iterator + 1) + ";"
    elif (quad[1] == "inp"):
        cQuad = "scanf(" + "'%d'," + quad[2] + ");"
    elif (quad[1] == "retv"):
        cQuad = "return " + str(quad[2]) + ";"
    elif (quad[1] == "out"):
        cQuad = "printf(" + "'%d'," + quad[2] + ");"
    elif (quad[1] == "begin_block"):
        if (quad[2] == mainID):
            cQuad = "int main()\n{\n   int "
            for var in declareVariablesList:
                if (var[0] == mainID):  # declared var
                    cQuad += var[1] + ","
                else:
                    cQuad += var[1] + ","
            for i in listOfVarTemps:  # T_0, T_1 etc
                cQuad += i + ","
            for j in variablesListOfFunction:
                cQuad += j[2] + ","  # in or inout variables
            for k in variablesListOfProcedure:
                cQuad += k[2] + ","

            cQuad = cQuad[:-1] + ";\n"

        # else:
        #   insideFunction=True
        #   currentFunctionVariablesPlace+=1
        #   for var in variablesListOfFunction:
        #       if(var[0]==currentFunctionVariablesPlace):
        #           temp=var[1]+var[2]
        #       temp+=temp
        #   cQuad="int"+quad[1]+"("+temp+")\n{"
    cQuad = "L_" + str(iterator) + ": " + cQuad + "\n"
    return cQuad


def makeCfile():
    global quadsList
    name = sys.argv[1].strip(".min") + "_quads.c"
    minToCquadsFile = open(name, "w+")
    minToCquadsFile.write("#include <stdio.h>\n\n")
    iterator = -1
    for quad in quadsList:
        iterator += 1
        minToCquadsFile.write(minQuadToCquad(quad, iterator))
    #       print(quad[0], quad[1], quad[2], quad[3], quad[4])
    return 1


class Entity:
    def __init__(self, name, entityType, offset):
        self.name = str(name)
        self.entityType = str(entityType)  # variable or function or constant or parameter or tempParameter
        self.offset = int(offset)
        self.startQuad = 0
        self.argumentList = []
        self.framelength = 0
        self.parMode = ""
        self.nextEntity = 0

    def setArgument(self, x):
        self.argumentList.append(x)

    def setFrameLength(self, x):
        self.framelength = x

    def setParMode(self, x):
        self.parMode = x

    def setStartQuad(self, x):
        self.startQuad = x

    def setOffset(self, x):
        self.offset = x

    def getOffset(self):
        return self.offset

    def getArgumentList(self):
        return self.argumentList

    def show(self):
        print("name: ", self.name, "offset: ", self.offset, "entity type: ", self.entityType, "par", self.parMode)
        if (self.entityType == "funtion" or self.entityType == "procedure"):
            print("nextQuad: ", self.startQuad, "framelength: ", self.framelength)


class Scope:
    def __init__(self, nestingLevel):
        self.entityList = []
        self.nestingLevel = nestingLevel
        self.enclosingScope = False

    def setEntityList(self, x):
        self.entityList = x

    def getEntityList(self):
        return self.entityList

    def addEntity(self, x):
        self.entityList.append(x)

    def showScope(self):
        print(self.nestingLevel)

    def setClosedScope(self):
        self.enclosingScope = True

    def getTotalOffset(self):
        if (len(self.entityList) == 0):
            return 0
        else:
            return (self.entityList[-1]).getOffset()

    def isLocalVar(self, x):
        for i in self.entityList:
            if (i.name == x.name):
                return 1
            else:
                return 0


def scopeSearch(x):
    global scopeList
    temp = Entity("nothing", "int", 0)
    tempName = ''
    for i in scopeList:
        tempList = i.getEntityList()
        for j in tempList:
            if (j.name == x):
                temp = j
                tempName = temp.name
                tempName.strip()
                temp.name = tempName
            else:
                # Check
                pass
    #           if(x.isdigit()):
    #               temp.name=x
    #           else:
    #               pass
    return temp


class Argument:
    def __init__(self, parMode, argType):
        self.parMode = parMode
        self.argType = argType

    def showArg(self):
        print(str(self.parMode))


def gnvlcode(x):
    global scopeList
    for i in scopeList:
        tempEntityList = i.getEntityList()
        for j in tempEntityList:
            if (j.name == x):
                cord = i.nestingLevel
                break
    temp = "lw $t0,-4($sp)\n"
    while (True):
        temp = temp + "\t\tlw $t0,-4($s0)\n"
        nesting += 1
        if (nesting > cord):
            break
    temp = temp + "\t\taddi $t0,$t0,-" + str(x.offset) + "\n"
    return temp


def loadvr(v, r):
    global nesting, scopeList
    counter = -1
    for i in scopeList:
        tempEntityList = i.getEntityList()
        for j in tempEntityList:
            if (j.name == v and counter == -1):
                newV = j
                cord = i.nestingLevel
                break
    if (str(v).isdigit()):
        temp = "li $t" + str(r) + "," + str(v) + "\n"
    elif (cord == 1):
        temp = "lw $t" + str(r) + ",-" + str(newV.offset) + "($s0)\n"
    elif ((newV.parMode == "" and nesting == cord) or (newV.parMode == "in" and nesting == cord) or (v[0:2] == "T_")):
        temp = "lw $t" + str(r) + ",-" + str(newV.offset) + "($sp)\n"
    elif (newV.parMode == "inout" and nesting == cord):
        temp = "lw $t0,-" + str(newV.offset) + "($sp)\n\t\t" + "lw $t" + str(r) + ",($t0)\n"
    elif ((newV.parMode == "" and nesting == cord) or newV.parMode == "in" or cord < nesting):
        temp = gnvlcode(newV.name) + "\t\tlw $t" + str(r) + ",($t0)\n"
    elif (newV.parMode == "inout" or cord < nesting):
        temp = gnvlcode(v) + "\t\tlw $t0,($t0)\n" + "\t\tlw $t" + str(r) + ",($t0)\n"
    else:
        temp = "Error in loadvr at line=" + str(line)
    print(temp)
    return temp


def storerv(r, v):
    global scopeList
    counter = -1
    for i in scopeList:
        tempEntityList = i.getEntityList()
        for j in tempEntityList:
            if (j.name == v and counter == -1):
                v = j
                counter = i.nestingLevel
                break
    i = scopeList[0]
    localVar = scopeList[0].isLocalVar(v.name)
    if (counter == 1):
        temp = "sw $t" + str(r) + ",-" + str(v.offset) + "($s0)\n"
    elif ((localVar == 1 or v.name[0:2] == "T_" or v.parMode == "in") and nesting == counter):
        temp = "sw $t" + str(r) + ",-" + str(v.offset) + "($sp)\n"
    elif (v.parMode == "inout" and nesting == counter):
        temp = "lw $t0,-" + str(v.offset) + "($sp)\n\t\t" + "sw $t" + str(r) + "($t0)\n"
    elif (v.parMode == "" and localVar == 1 or v.parMode == "in" or counter < nesting):
        temp = gnvlcode(v.name) + "\t\tsw $t" + str(r) + "($t0)"
    elif (v.parMode == "inout" and counter < nesting):
        temp = gnvlcode(v.name) + "\t\tlw $t0,($t0)" + "\t\tsw $t" + str(r) + "($t0\n)"
    else:
        temp = "Error i storerv at line" + str(line)
    print(temp)
    return temp


def minToAsm(quad):
    global scopeList, nesting, scopeCounter, mainID, quadCounter
    sem = True
    num3 = 3
    asm = ""
    temp = ""

    if (quad[1] == "jump"):
        asm = "\tj L_" + str(quad[4])
    elif (quad[1] == ":="):
        asm = loadvr(quad[2], 1) + storerv(1, quad[4])
    elif (quad[1] == "="):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tbeq $t" + str(1) + ",$t" + str(2) + ",L_" + str(quad[4])
    elif (quad[1] == "jump"):
        asm = "\tj L_" + str(quad[4])
    elif (quad[1] == "+"):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tadd " + "$t" + str(3) + ",$t" + str(1) + ",$t" + str(
            2) + "\n" + storerv(num3, quad[4])
    elif (quad[1] == "-"):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tsub " + "$t" + str(3) + ",$t" + str(1) + ",$t" + str(
            2) + "\n" + storerv(num3, quad[4])
    elif (quad[1] == "*"):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tmul " + "$t" + str(3) + ",$t" + str(1) + ",$t" + str(
            2) + "\n" + storerv(num3, quad[4])
    elif (quad[1] == "/"):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tdiv " + "$t" + str(3) + ",$t" + str(1) + ",$t" + str(
            2) + "\n" + storerv(num3, quad[4])
    elif (quad[1] == ">="):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tbge $t" + str(1) + ",$t" + str(2) + ",L_" + str(quad[4])
    elif (quad[1] == "<="):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tble $t" + str(1) + ",$t" + str(2) + ",L_" + str(quad[4])
    elif (quad[1] == "<>"):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tbne $t" + str(1) + ",$t" + str(2) + ",L_" + str(quad[4])
    elif (quad[1] == ">"):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tbgt $t" + str(1) + ",$t" + str(2) + ",L_" + str(quad[4])
    elif (quad[1] == "<"):
        asm = loadvr(quad[2], 1) + loadvr(quad[3], 2) + "\tblt $t" + str(1) + ",$t" + str(2) + ",L_" + str(quad[4])
    elif (quad[1] == "halt"):
        asm = "\tli $v0,10\n\t" + "syscall"
    elif (quad[1] == "inp"):
        temp = scopeSearch(quad[2])
        asm = "\tli $v0,5\n\t" + "syscall\n\t" + "\n\tmove $t0,$v0\n\t" + storerv(0, temp)
    elif (quad[1] == "out"):
        temp = scopeSearch(quad[2])
        asm = "\tli $v0,1\n" + loadvr(temp.name, 0) + "\n\tmove $a0,$t0" + "\n\t" + "syscall"
    elif (quad[1] == "retv"):
        asm = loadvr(quad[2], 1) + "\tmove $v0,$t1\n\tlw $ra,($sp)" + "\n\tjr $ra"
    elif (quad[1] == "begin_block"):
        sem = False
        if (quad[2] == mainID):
            scopeCounter = -1
            nesting = 1
            for i in afterScopeList:
                if (i.nestingLevel == 1):
                    temp = i.getTotalOffset()
            asm = asm + "\tLmain:\n" + "\tsw $ra,($sp)\n" + "\t" + "add $sp,$sp," + str(temp) + "\n\t" + "move $s0,$sp"
        else:
            scopeCounter = 0
            for j in afterScopeList:
                if (j.nestingLevel > 1):
                    temp = j.getEntityList()
                    tempEntity = temp[0]
                    if (tempEntity.name == quad[2]):
                        tempTemp = tempEntity.framelength
                        nesting = j.nestingLevel
            asm = asm + "\t" + quad[2] + ":" + "\n\t" + "sw $ra,($sp)"
    elif (quad[1] == "end_block"):
        sem = False
        tempScope = scopeList(0)
        tempScope = tempScope.getEntityList()
        tempScope = tempScope[0]
        asm = ""
    elif (quad[1] == "par" and quad[3] == "REF"):
        if (quad[0] == 0):
            for q in quadsList:
                if (q[0] == quad[0]):
                    num3 = -1
                elif (num3 == -1 and q[0] == "call"):
                    num3 = scopeSearch(q[2])
                    temp = num3.frameLength
                    break
            asm = "\tadd $fp,$sp," + str(temp) + "\n"
        else:
            asm = ""
        temp = 12 + 4 * quadCounter
        quadCounter += 1
        tempScope = scopeSearch(quad[2].strip())
        scopeTemp = scopeList[0]
        tempVar = scopeTemp.isLocalVar(tempScope.name)
        asm = "Error at asm"
        for scope in scopeList:
            if (scope.isLocalVar(tempScope.name) == 1):
                variableNesting = scope.nestingLevel
        if (nesting == variableNesting or tempScope.parMode == "" and localVar == 1):
            asm = "\tadd $t0,$sp,-" + str(tempScope.offset) + "\n\tsw $t0,-" + str(temp) + "($fp)"
        elif (nesting == variableNesting or tempScope.parMode == "inout"):
            asm = "\tlw $t0,-" + str(tempScope.offset) + "($sp)" + "\n\tsw $t0,-" + str(temp) + "($fp)"
        elif (nesting != variableNesting or localVar == 1 or tempScope.parMode == "in"):
            asm = gnlvcode(tempScope.name) + "\tsw $t0,-" + str(temp) + "($fp)"
        elif (nesting != variableNesting or tempScope.parMode == "inout"):
            asm = gnlvcode(tempScope.name) + "\tlw $t0,($t0)" + "\n\tsw $t0,-" + str(temp) + "($fp)"
    elif (quad[0] == "par" and quad[3] == "CV"):
        if (quadCounter == 0):
            for q in quadsList:
                if (q[0] == quad[0]):
                    num3 = -1
                elif (num3 == -1 and q[0] == "call"):
                    num3 = scopeSearch(q[2])
                    temp = num3.framelength
                    break
            asm = "\ttadd $fp,$sp," + str(temp) + "\n"
        else:
            asm = ""
        tempTemp = 12 + 4 * quadCounter
        quadCounter += 1
        asm = asm + loadvr(quad[2], 0) + "\t\tsw $t0, -" + str(temp) + "($fp)"
    else:
        asm = "#Error to assembly code!"
    if (sem == True):
        asm = "\tL_" + str(quad[0]) + ": \n" + asm
    else:
        pass
    return asm


def makeAsmFile():
    global currentQuadPlace
    asmFileName = fileName.strip(".min") + "_final.asm"
    asmFile = open(asmFileName, "w+")
    asmFile.write("\tj Lmain\n")
    for quad in quadsList:
        asmFile.write("\t#" + str(quad[0]) + "," + str(quad[1]) + "," + str(quad[2]) + "," + str(quad[3]) + "," + str(
            quad[4]) + minToAsm(quad))
    return 1


# Call the syntax
syntax()
# Call the makeCfile
makeCfile()
# Call makeAsmFile
makeAsmFile()

fileReader.close()  # Closing the file