# Prifth Ioannhs/AM 3321/username cse63321
#Theodwrou Gewrgios Euaggelos/AM 3231/username cse63231

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
variablesListOfFunction = []  # List[[fuctionId,in or inout, varName],..] with function variables

procedureIdList = []  #Procedure names
variablesListOfProcedure=[] # List[[procedureId,in or inout, varName],..] with procedure variables

currentFunctionVariablesPlace = -1

declareVariablesList = []

nesting=1

scopeList=[""]

afterScopeList=[]

scopeCounter=0

# Open file
#fileName = input("Enter the file name: ")
fileName=sys.argv[1]

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
                if(checkComments(tempString)==1):
                    lex()
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
            if(char=="*"):
                tempComment += char
                position+=1
                char=fileReader.read(1)
                tempComment += char

                if (tempComment == EOFError or tempComment == "*/"):
                    return 1;
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
                return 1
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
    print("token at line 215 is", token)
    token=lex()
    print("token at line 217 is", token)
    if (token == "program"):
        print("token at line 219 is", token)
        token = lex()
        print("token at line 221 is", token)
        mainID = token
        tempScope=Scope(nesting)
        tempEntity=Entity("-main", "main", 8)
        tempScope.addEntity(tempEntity)
        scopeList[scopeCounter]=tempScope
        if (mainID not in reservedWords):
            print("token at line 224 is", token)
            token=lex()
            print("token at line 226 is", token)
            if(token=="{"):
                print("token at line 228 is", token)
                token=lex()
                print("token at line 230 is", token)
                block(mainID)
            else:
                print("'{' was expectes at line=",line)
                sys.exit()
            if (token == "}"):
                if(internalFunction==False):
                    genquad("halt", "_", "_", "_")
                    genquad("end_block", mainID, "_", "_")
                    afterScopeList.append(scopeList.pop(0))
                    return 1
                else:
                    return 0
            else:
                print("PAPARIA", token)
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
        genquad("begin_block", funcID, "_", "_")
        tempScope=scopeList[0]
        tempEntity_1=tempScope.getEntityList()
        tempEntity=tempEntity_1[0]
        tempEntity.setStartQuad(nextquad())
        tempEntity_1=tempEntity
        tempScope.setEntityList(tempEntity_1)
    print("token at line 261 is", token)
    print("token at line 252 is", token)
    declarations()
    print("token at line 254 is", token)
    subprograms() #token = function
    statements()
    print("TOKEN TOKEN", token)
    print("token at line 263 is", token)
    
    return 1


def declarations():
    global token
    if(token=="declare"):
        varlist()
        if(token==";"):
            token=lex()
            declarations()
        else:
            print("';' was expected at line=", line) 
            sys.exit()         
    return 1


def varlist():
    global token, internalFunction, scopeList, scopeCounter
    token=lex()
    temp=Entity("","",0)
    temp=scopeSearch(token)
    if (token not in reservedWords and temp.name=="nothing"):
        declareVariable = token
        tempScope=scopeList[scopeCounter]
        totalTempScope=tempScope.getTotalOffset()
        tempEntity=Entity(token, "var", (totalTempScope+4))
        if (internalFunction == False):
            declareVariablesList.append([mainID, declareVariable])
        else:
            declareVariablesList.append([functionIdList[-1], declareVariable])
        print("token at line 287 is", token)
        tempScope.addEntity(tempEntity)
        scopeList[scopeCounter]=tempScope
        token = lex()  
        if (token == ","):
            print("token at line 291 is", token) 
            varlist()
        else:
            return 1
    else:
        print("Incompatible varable name at line=", line)
        sys.exit()
    return 1


def subprograms():
    global token
    print("token at line 311 is", token)
    #token=lex()
    while (token == "function" or token=="procedure"):
        print("token at line 313 is", token)
        subprogram()
        print("token at line 315 is", token)    
    return 1


def subprogram():
    global functionIdList, procedureIdList, token, nesting, scopeList, afterScopeList, scopeCounter
    print("token at line 321 is", token)
    if (token == "function"):
        token = lex()
        nesting+=1
        print("token at line 324 is", token)   
        functionID = token
        token=lex()
        print("token at line 327 is", token)
        if (functionID in reservedWords):
            print("Incompatible function name at line=", line)
            sys.exit()
        if (functionID in functionIdList):
            print("Function with the same name already exists at line=", line)
            sys.exit()
        tempScope=Scope(nesting)
        tempEntity=Entity(functionID, "function", 8)
        tempScope.addEntity(tempEntity)
        scopeList.insert(0, tempScope)

        functionIdList.append(functionID)
        funcbody(functionID)
        if (token == "}"):
            afterScopeList=scopeList[scopeCounter+1]
            tempScope=scopeList[scopeCounter]
            temp=tempScope.getEntityList()
            tempEntity=temp[0]
            tempTemp[-1]
            tempEntity.setOffset(afterScopeList.getTotalOffset())
            tempEntity.setFrameLength(tempTemp.getOffset())
            afterScopeList.addEntity(tempEntity)
            genquad("end_block", functionID, "_", "_")
            nesting-=1
            afterScopeList.append(scopeList.pop(0))
    elif (token == "procedure"):
        print("token at line 340 is", token)
        token = lex()
        nesting+=1
        print("token at line 342 is", token)
        procedureID = token
        if (procedureID in reservedWords):
            print("Incompatible procedure name at line=", line)
            sys.exit()
        if (procedureID in procedureIdList):
            print("Procedure with the ssame name already exist at line=", line)
            sys.exit()
        tempScope=Scope(nesting)
        tempEntity=Entity(procedureID, "procedure", 8)
        tempScope.addEntity(tempEntity)
        scopeList.insert(0, scope)

        procedureIdList.append(procedureID)
        funcbody(procedureID)
        if (token == "}"):
            afterScopeList=scopeList[scopeCounter+1]
            tempScope=scopeList[scopeCounter]
            temp=tempScope.getEntityList()
            tempEntity=temp[0]
            tempTemp[-1]
            tempEntity.setOffset(afterScopeList.getTotalOffset())
            tempEntity.setFrameLength(tempTemp.getOffset())
            afterScopeList.addEntity(tempEntity)
            genquad("end_block", procedureID, "_", "_")
            nesting-=1
            afterScopeList.append(scopeList.pop(0))
    else:
        print("incorrect subprogram syntax at line=", line)
        sys.exit()


def funcbody(funcName):
    global token, internalFunction
    internalFunction = True
    print("token at line 363 is", token)
    formalpars()
    print("token at line 365 is", token)
    #token=lex()
    if(token=="{"):
        token=lex()
        block(funcName)
        token=lex()
        print("THEODOROU KOITA EDW TO", token)
        if(token=="}"):
            token=lex()
            return 1
        else:
            print("PAPARIA, ", token)
            print("'}' was expected at line=", line)
            sys.exit()
    else:
        print("'{' was expected at line=", line)
        sys.exit()
    print("token at line 367 is", token)
    return 1


def formalpars():
    global token
    print("token at line 373 is", token)
    if (token == "("):
        token=lex()
        print("token at line 376 is", token)
        formalparlist()
        print("token at line 378 is", token)
        if (token == ")"):
            print("token at line 380 is", token)
            token = lex()
            print("token at line 382 is", token)
        else:
            print(" ')' expected after parameter list at line=", line)
            sys.exit()
    else:
        print(" '(' expected before parameter list at line=", line)
        sys.exit()


def formalparlist():
    global token
    print("token at line 393 is", token)
    if (token == ")"):
        return 1
    else:
        while (formalparitem()):
            print("token at line 398 is", token)
            token = lex()
            print("token at line 400 is", token)
            #if (token == ")"):
            #    return 1
            #else:
            #    return 0
            if (token == ','):
                print("token at line 406 is", token)
                token = lex()
                formalparitem()
                token=lex()
                print("token at line 408 is", token)
                continue
            else:
                return 1
    return 1


def formalparitem():
    global token, variablesListOfFunction, functionIdList, variablesListOfProcedure, procedureIdList, scopeCounter, scopeList
    print("token at line 418 is", token)
    if (token == "in"):
        token = lex()
        tempScope=scopeList[scopeCounter]
        print("token at line 421 is", token)
        if (token not in reservedWords):
            parInName = token
            variablesListOfFunction.append([functionIdList[-1], "in", parInName])
            
            tempEntity=Entity(parInName, "var", tempScope.getTotalOffset()+4)
            tempEntity.setParMode("in")
            tempScope.addEntity(tempEntity)
            tempArg=Argument("in", "int")
            tempTemp=tempScope.getEntityList()
            tempEntity=tempTemp[0]
            tempEntity.setArgument(tempArg)
            tempTemp[0]=tempEntity
            tempScope.setEntityList(tempTemp)
            scopeList[scopeCounter]=tempScope
            return 1
        else:
            print("Incompatible varable name at line=", line)
            sys.exit()
    elif (token == "inout"):
        print("token at line 430 is", token)
        token = lex()
        if (token not in reservedWords):
            parInOutName = token
            variablesListOfProcedure.append([functionIdList[-1], "inout", parInOutName])
            
            tempEntity=Entity(parInOutName, "var", tempScope.getTotalOffset()+4)
            tempEntity.setParMode("inout")
            tempScope.addEntity(tempEntity)
            tempArg=Argument("inout", "int")
            tempTemp=tempScope.getEntityList()
            tempEntity=tempTemp[0]
            tempEntity.setArgument(tempArg)
            tempTemp[0]=tempEntity
            tempScope.setEntityList(tempTemp)
            scopeList[scopeCounter]=tempScope
            return 1
        else:
            print("Incompatible varable name at line=", line)
            sys.exit()
    else:
        print("No valid expression at line=", line)
        return 0


def statements():
    global token
    print("token at line 446 is", token)
    if (token != "{"):
        #print("token at line 448 is", token)
        statement()
       #print("token at line 450 is", token)
        return 1
    elif(token == "{"):
        #print("token at line 452 is", token)
        #token = lex()
        #print("token at line 454 is", token)
        #while (statement()):
        #    print("token at line 456 is", token)
        #    token = lex()
        #    print("token at line 458 is", token)
        #    statement()
        #    print("token at line 462 is, ", token)
        #    if(token=="}"):
        #        return 1
        #    if (token != ";"):
        #        return 1
        #    if (token == ';'):
        #        print("token at line 465 is", token)
        #        token = lex()
        #        print("token at line 467 is", token)
        #        continue
        #    else:
        #        print(" ';' was expected at line=", line)
        #        sys.exit()        
    #else:
    #    print(" '{' was expected at line=", line)
    #    sys.exit()
        token=lex()
        statement()
        #token=lex()
        print("TOKEN BEFORE", token)
        while(statement()):    
            if(token==";"):
                #token=lex()
                print("TOKEN BEFORE", token)
                statement()
                print("TOKEN AFTER", token)
                #token=lex()
                if(token=="}"):
                    return 1
                elif(token==";"):
                    #token=lex() #todo
                    continue
                else:
                    print("TOKEN TOKEN TOKEN ", token)
                    print("'}' was expected at line=", line)
                    sys.exit()
            elif(token=="}"):
                return 1
            else:
                #print("';' was expected at line=", line)
                #sys.exit()
                print("im here", token)
                return 1
        token=lex()        
    return 1
                                        




#pdb.set_trace()
def statement():
    global token
    print("token at line 481 is", token)
    if ((token not in reservedWords) and (token not in delimeters)):
        assignmentStat()
        print("token at line 484 is", token)   
    if (token == "if"):
        ifStat()
        print("token at line 487 is", token)
    if (token == "while"):
        whileStat()
        print("token at line 490 is", token)
    if (token == "doublewhile"):
        doublewhileStat()
        print("token at line 493 is", token)
    if (token == "loop"):
        loopStat()
        print("token at line 496 is", token)
    if (token == "exit"):
        exitStat()
        print("token at line 499 is", token)
    if (token == "forcase"):
        forcaseStat()
        print("token at line 502 is", token)
    if (token == "incase"):
        incaseStat()
        print("token at line 505 is", token)
    if (token == "call"):
        callStat()
        print("token at line 508 is", token)
    if (token == "return"):
        returnStat()
        print("token at line 511 is", token)
    if (token == "input"):
        inputStat()
        print("token at line 514 is", token)
    if (token == "print"):
        printStat()
        print("token at line 517 is", token)
    if(token in groupingSymbols):
        token=lex()
        return 1
    #else:
    #    print("Wrong Statement format at line=", line)
    #    sys.exit()
    return 1


def assignmentStat():
    global token
    print("token at line 525 is", token)
    token=lex()
    tempVarID = token
    tempScope=scopeSearch(tempVarID)
    if(tempScope=="nothing"):
        print("Variable:", tempVarID, "not declared at line=", line)
        sys.exit()
    if (tempVarID not in reservedWords):
        #token = lex()
        print("token at line 529 is", token)
        if (token == ":="):
            token = lex()
            print("token at line 532 is", token)
            reTemp = expression() # enan arithmo
            print("token at line 534 is", token)
            if (reTemp not in reservedWords):
                genquad(":=", reTemp, "_", tempVarID)
                token=lex()
                return 1           
        else:
            print(" ':=' was expected at line=", line)
            sys.exit()
    else:
        print("Incompatible varable name at line=", line)
        sys.exit()
    #if(token==";"):
    #    assignmentStat()
    #else:
    #    return 1    
                    

def ifStat():
    global token
    print("token at line 548 is", token)
    token = lex()
    print("token at line 550 is", token)
    if (token == "("):
        bTrue, bFalse = condition()
        if (token == ")"):
            token = lex()
            print("token at line 555 is", token)
            if (token == "then"):
                token = lex()
                print("token at line 558 is", token)
                backpatch(bTrue, nextquad())
                print("token at line 560 is", token)
                statements()
                print("token at line 562 is", token)
                token = lex()
                print("token at line 564 is", token)
                tempTemp = makelist(nextquad())
                genquad("jump", "_", "_", "_")
                backpatch(bFalse, nextquad())
                print("token at line 568 is", token)
                elsepart()
                print("token at line 570 is", token)
                backpatch(tempTemp, nextquad())
                #if (token == "}"):
                #    print("token at line 573 is", token)
                #    token = lex()
                #    print("token at line 575 is", token)
                #else:
                #    print("If statement never close at line=", line)
                #    sys.exit()
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    else:
        print(" '(' was expected at line=", line)
        sys.exit()
    return 1

def elsepart():
    global token
    print("token at line 589 is", token)
    if (token == "else"):
        token = lex()
        print("token at line 592 is", token)
        statements()
        print("token at line 594 is", token)
        return 1
    else:
        return 0


def whileStat():
    global token, line
    print("token at line 602 is", token)
    token = lex()
    print("token at line 604 is", token)
    if (token == "("):
        startWhile = nextquad()
        #token=lex()
        bTrue, bFalse = condition()
        #token=lex()
        print("token at line 6666666666666666666666666 is", token)
        if (token == ")"):
            print("token at line 609 is", token)
            token = lex()
            print("token at line 111111111111111 is", token)
            #if(token=="{"):
            print("token at line 611 is", token)
            backpatch(bTrue, nextquad())
            statements()
            print("token at line 614 is", token)
            genquad("jump", "_", "_", startWhile)
            backpatch(bFalse, nextquad())
            if (token == "}"):
                print("token at line 618 is", token)
                token = lex()
                print("token at line 620 is", token)
                return 1
            else:
                print("While statement never stop at line=", line)
                sys.exit()
            #else:
            #    print("'{' expected at line=",line)
            #    sys.exit()
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    else:
        print(" '(' was expected at line=", line)
        sys.exit()


"""         
def doublewhileStat():
    print("token at line 634 is", token)
    if(token=='('):
        token=lex()
        print("token at line 637 is", token)
        condition()
        print("token at line 639 is", token)
        if(token==')'):
            token=lex()
            print("token at line 642 is", token)
            statements()
            print("token at line 644 is", token)
            if(token=="else"):
                print("token at line 646 is", token)
                token=lex()
                print("token at line 648 is", token)
                statements()
                print("token at line 650 is", token)
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
    print("token at line 663 is", token)
    statements()
    print("token at line 665 is", token)
    token=lex()
    print("token at line 667 is", token)
    return 1

def exitStat():
    print("token at line 671 is", token)
    token=lex()
    print("token at line 673 is", token) 
    return 1
"""


def forcaseStat():
    global token
    print("token at line 680 is", token)
    token=lex()
    startForCase = nextquad()
    tempTrueList = []
    while (token == "when"):
        print("token at line 684 is", token)
        token = lex()
        print("token at line 686 is", token)
        if (token == "("):
            bTrue, bFalse = condition()
            if (token == ")"):
                token = lex()
                print("token at line 691 is", token)
                if (token == ":"):
                    token = lex()
                    print("token at line 694 is", token)
                    backpatch(bTrue, nextquad())
                    statements()
                    print("token at line 697 is", token)
                    tempTrueList.append(nextquad())
                    genquad("jump", "_", "_", "_")
                    backpatch(bFalse, nextquad())
                    token = lex() #CHECK
                    print("token at line 702 is", token)
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
        print("token at line 714 is", token)
        if (token == ":"):
            token = lex()
            print("token at line 717 is", token)
            backpatch(bFalse.nextquad())
            print("token at line 719 is", token)
            statements()
            print("token at line 721 is", token)
            #if (token == "}"):
            genquad("jump", "_", "_", startForCase)
            backpatch(tempTrueList, nextquad())
            token = lex()
            print("token at line 726 is", token)
            #else:
            #    print("For case never sto at line=", line)
            #    sys.exit()
        else:
            print(" ':' was expected at line=", line)
            sys.exit()
    else:
        print(" 'default' expression was expected at line=", line)
        sys.exit()
    return 1


""" 
def incaseStat():
    print("token at line 740 is", token)
    while(token=="when"):
        print("token at line 742 is", token)
        token=lex()
        print("token at line 444 is", token)
        if(token=="("):
            print("token at line 746 is", token)
            token=lex()
            print("token at line 748 is", token)
            condition()
            print("token at line 750 is", token)
            if(token==")"):
                print("token at line 752 is", token)
                token=lex()
                print("token at line 754 is", token)
                if(token==':'):
                    print("token at line 756 is", token)
                    token=lex()
                    print("token at line 758 is", token)
                    statements()
                    print("token at line 760 is", token)
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
    print("token at line 774 is", token)
    token = lex()
    print("token at line 776 is", token)
    expressionTemp = expression()
    genquad("retv", expressionTemp, "_", "_")
    if (internalFunction == False):
        print("Return statement is out of function at line=", line)
        sys.exit()
    return 1


""" 
def callStat():
    print("token at line 786 is", token)
    if(token==idtk):
        token=lex()
        print("token at line 789 is", token)
        if(token=='('):
            print("token at line 791 is", token)
            token=lex()
            print("token at line 793 is", token)
            actualpars()
            print("token at line 795 is", token)
            if(token==')'):
                token=lex()
                print("token at line 798 is", token)
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
    print("token at line 816 is", token)  
    if(token=="("):
        token=lex()
        expressionTemp = expression()
        token=lex()
        if(token==")"):
            token=lex()
            genquad("out", expressionTemp, "_", "_")
            return 1
        else:
            print("')' was expected at line=", line)
            sys.exit()
    else:
        print("'(' was expected at line=", line)
        sys.exit()
    print("token at line 818 is", token) 
    return 1


def inputStat():
    global token, line
    print("token at line 825 is", token)
    token = lex()
    print("token at line 827 is", token)
    if(token=="("):
        token=lex()
        if (token not in reservedWords and token.isalnum()):
            genquad("inp", token, "_", "_")
            print("token at line 830 is", token)
            token = lex()
            print("token at line 832 is", token)
            return 1
        else:
            print("TOKEN", token)
            print("Error with ID in input expression at line=", line)
            sys.exit()
        if(token==")"):
            #token=lex()
            return 1
        else:
            print("')' was expected at line=", line)
            sys.exit()
    else:
        print("'(' was expected at line=", line)

def actualpars(callerID):
    global token
    print("token at line 840 is", token)
    token=lex()
    if (token == "("):
        actualparlist(callerID)
        print("token at line 843 is", token)
        #token=lex()
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
    print("token at line 859 is", token)
    actualparitem(callerID)
    print("token at line 861 is", token)
    while (token == ","):
        print("token at line 863 is", token)
        actualparitem(callerID)
        print("token at line 865 is", token)


def actualparitem(callerID):
    global token
    print("token at line 870 is", token)
    token = lex()
    print("token at line 872 is", token)
    if (token == "in"):
        print("token at line 874 is", token)
        token = lex()
        print("token at line 876 is", token)
        tempArg=Argument("in", "int")

        expressionTemp = expression()
        print("token at line 878 is", token)
        genquad("par", expressionTemp, "CV", "_")
    elif (token == "inout"):
        print("token at line 881 is", token)
        token = lex()
        print("token at line 883 is", token)
        genquad("par", token, "REF", "_")
        print("token at line 886 is", token)
        token = lex()
        print("token at line 888 is", token)
    else:
        print("No valid expression at line=", line)
        sys.exit()


def condition():
    global token
    print("token at line 899 is", token)
    bTrue, bFalse = q1True, q1False = boolterm()
    while (token == "or"):
        backpatch(bFalse, nextquad())
        q2True, q2False = boolterm()
        bTrue = merge(bTrue, q2True)
        bFalse = q2False
    print("token at line 906 is", token)
    return bTrue, bFalse


def boolterm():
    global token
    print("token at line 912 is", token)
    qTrue, qFalse = r1True, r1False = boolfactor()
    while (token == "and"):
        backpatch(qTrue, nextquad())
        r2True, r2False = boolfactor()
        qFalse = merge(qFalse, r2False)
        qTrue = r2True
    print("token at line 919 is", token)
    return qTrue, qFalse


def boolfactor():
    global token
    print("token at line 925 is", token)
    token = lex()
    print("token at line 927 is", token)
    if (token == "not"):
        print("token at line 929 is", token)
        token = lex()
        print("token at line 931 is", token)
        if (token == "["):
            # token=lex()
            print("token at line 934 is", token)
            bFalse, bTrue = condition()
            print("token at line 936 is", token)
            if (token == "]"):
                print("token at line 938 is", token)
                token = lex()
                print("token at line 940 is", token)
            else:
                print(" ']' was expected at line=", line)
                sys.exit()
        else:
            print(" '[' was expected at line=", line)
            sys.exit()
    elif (token == "["):
        print("token at line 948 is", token)
        # token=lex()
        bTrue, bFalse = condition()
        print("token at line 951 is", token)
        if (token == "]"):
            pass
        else:
            print(" ']' was expected at line=", line)
            sys.exit()
    else:
        expressionTemp = expression()
        print("token at line 959 is", token)
        tempList = emptylist()
        relationaloper()
        print("token at line 962 is", token)
        relopTemp = token
        token = lex()
        expressionTemp2 = expression()
        bTrue = makelist(nextquad())
        genquad(relopTemp, expressionTemp, expressionTemp2, "_")
        bFalse = makelist(nextquad())
        genquad("jump", "_", "_", "+")
    print("token at line 970 is", token)
    return bTrue, bFalse


def expression():
    global token # tok==(
    print("token at line 976 is", token)
    optionalsignTemp = optionalsign()
    print("token at line 978 is", token)
    termTemp = term() #0
    print("token at line 980 is", token)
    while (token == "+" or token == "-"):
        print("token at line 982 is", token)
        optionalsignTemp = token
        print("token at line 984 is", token)
        token = lex()  # or addoper(), will see
        print("token at line 986 is", token)
        termTemp2 = term()
        print("token at line 988 is", token)
        tempTemp = newtemp()
        genquad(optionalsignTemp, termTemp, termTemp2, tempTemp)
        termTemp = tempTemp
    return termTemp


def term():
#   pdb.set_trace()
    global token #while
    print("token at line 998 is", token)
    factorTemp = factor() #0
    print("token at line 1000 is", token)
#   if (factorTemp not in functionIdList):
#       print("Function: ", factorTemp, "not declared at line=", line)
#       sys.exit()
    while (token == "*" or token == "/"):
        tempToken = token
        print("token at line 1006 is", token)
        token = lex()
        print("token at line 1008 is", token)
        muloper()
        print("token at line 1010 is", token)
        factorTemp2 = factor()
        print("token at line 10012 is", token)
        if (factorTemp2 not in functionIdList):
            print("Function: ", factorTemp, "not declared at line=", line)
            sys.exit()
        temp = newtemp()
        genquad(tempToken, factorTemp, factorTemp2, temp)
        factorTemp = temp
    print("token at line 1019 is", token)
    return factorTemp


def factor():
    global token
    print("token at line 1025 is", token)
    if (str(token).isdigit()):
        tempConstant = token
        print("token at line 1028 is", token)
        token = lex()
        print("token at line 1030 is", token) 
    elif (token == "("):
        tempConstant = token
        print("token at line 1033 is", token)
        token = lex()
        print("token at line 1035 is", token)
        expression()
        print("token at line 1037 is", token)
        if (token == ")"):
            pass
        else:
            print(" ')' was expected at line=", line)
            sys.exit()
    elif (token not in reservedWords and token.isalnum()):
        tempConstant = token
        print("token at line 1045 is", token)
        token = lex()
        print("token at line 1047 is", token)
        tempConstant = idtail(tempConstant)# to tempConstant allazei epidi sthn periptosh call w = newTemp() par, w, RET, _ xriazomaste to w to opio einai temp kai epistrefei
        print("token at line 1049 is", token)
    else:
        print("Problem with factor function at line=", line)
        sys.exit()
    return tempConstant


def idtail(callerID):
    global token
    print("token at line 1058 is", token)
    name = callerID
    if (token == "("):
        name = actualpars(callerID)
    print("token at line 1062 is", token)
    return name


def relationaloper():
    global token
    print("token at line 1068 is", token)
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
    print("token at line 1084 is", token)

def addoper():
    global token
    print("token at line 1088 is", token)
    if (token == "+"):
        print("token at line 1090 is", token)
        token = lex()
        print("token at line 1092 is", token)
        return token
    elif (token == "-"):
        print("token at line 1095 is", token)
        token = lex()
        print("token at line 1097 is", token)
        return token
    else:
        print("invalid addoper at line=", line)
        sys.exit()


def muloper():
    global token
    print("token at line 1106 is", token)
    if (token == "*"):
        print("token at line 1108 is", token)
        return token
    elif (token == '/'):
        print("token at line 1111 is", token)
        return token
    else:
        print("invalid muloper at line=", line)
        sys.exit()


def optionalsign():
    global token
    print("token at line 1120 is", token)
    if (token == "+" or token == "-"):
        print("token at line 1122 is", token)
        addoper()
        print("token at line 1124 is", token)
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
    cQuad=""
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
    cQuad = "L_" + str(iterator) + ": " + cQuad
    return cQuad


def makeCfile():
    global quadsList
    minToCquadsFile = open("minToCquads.c", "w+")
    minToCquadsFile.write("#include <stdio.h>\n\nint main()\n{\n")
    iterator = -1
    for quad in quadsList:
        iterator += 1
        minToCquadsFile.write(minQuadToCquad(quad, iterator))

class Entity:
    def __init__(self, name, entityType, offset):
        self.name=str(name)
        self.entityType=str(entityType) #variable or function or constant or parameter or tempParameter
        self.offset=int(offset)
        self.startQuad=0
        self.argumentList=[]
        self.framelength=0
        self.parMode=""
        self.nextEntity=0

    def setArgument(self, x):
        self.argumentList.append(x)
    def setFrameLength(self, x):
        self.framelength=x
    def setParMode(self, x):
        self.parMode=x
    def setStartQuad(self, x):
        self.startQuad=x
    def setOffset(self, x):
        self.offset=x
    def getOffset(self):
        return self.offset
    def getArgumentList(self):
        return self.argumentList
    def show(self):
        print("name: ", self.name, "offset: ", self.offset, "entity type: ", self.entityType, "par", self.parMode)
        if(self.entityType=="funtion" or self.entityType=="procedure"):
            print("nextQuad: ", self.startQuad, "framelength: ", self.framelength)

class Scope:
    def __init__(self, nestingLevel):
        self.entityList=[]
        self.nestingLevel=nestingLevel
        self.enclosingScope=False
    
    def setEntityList(self, x):
        self.entityList=x
    def getEntityList(self):
        return self.entityList
    def addEntity(self, x):
        self.entityList.append(x)
    def showScope(self):
        print(self.nestingLevel)
    def setClosedScope(self):
        self.enclosingScope=True
    def getTotalOffset(self):
        if(len(self.entityList)==0):
            return 0
        else:
            return (self.entityList[-1]).getOffset()
    def isLocalVar(self, x):
        for i in self.entityList:
            if(i.name==x.name):
                return 1
            else:
                return 0
def scopeSearch(x):
    global scopeList
    temp=Entity("nothing", "int", 0)
    tempName=""
    for i in scopeList:
        tempList=i.getEntityList()
        for j in tempList:
            if(j.name==x):
                temp.name=j.name
    return temp

class Argument:
    def __init__(self, parMode, argType):
        self.parMode=parMode
        self.argType=argType

    def showArg(self):
        print(str(self.parMode))

def gnvlcode(x):
    for i in scopeList:
        tempEntityList=i.getEntityList()
        for j in tempEntityList:
            if(j.name==x):
                cord=i.nestingLevel
                break
    temp="lw $t0,-4($sp)\n"
    while(True):
        temp=temp+"\t\tlw $t0,-4($s0)\n"
        nesting+=1
        if(nesting>cord):
            break
    temp=temp+"\t\taddi $t0,$t0,-"+str(x.offset)+"\n"
    return temp

def loadvr(v, r):
    global nesting
    counter=-1
    for i in scopeList:
        tempEntityList=i.getEntityList()
        for j in tempEntityList:
            if(j.name==v and counter==-1):
                newV=j
                cord=i.nestingLevel
                break
    if(v.isdigit()):
        temp="li $t"+str(r)+","+str(v)+"\n"
    elif(cord==1):
        temp="lw $t"+str(r)+",-"+str(newV.offset)+"($s0)\n"
    elif((newV.parMode=="" and nesting==cord) or (newV.parMode=="in" and nesting==cord) or (v[0:2] =="T_")):
        temp="lw $t"+str(r)+",-"+str(newV.offset)+"($sp)\n"
    elif(newV.parMode=="inout" and nesting==cord):
        temp="lw $t0,-"+str(newV.offset)+"($sp)\n\t\t"+"lw $t"+str(r)+",($t0)\n"
    elif((newV.parMode=="" and nesting==cord) or newV.parMode=="in" or cord<nesting):
        temp=gnvlcode(newV.name)+"\t\tlw $t"+str(r)+",($t0)\n"
    elif(newV.parMode=="inout" or cord<nesting):
        temp=gnvlcode(v)+"\t\tlw $t0,($t0)\n"+"\t\tlw $t"+str(r)+",($t0)\n"
    else:
        temp="Error in loadvr at line="+str(line)
    print(temp)
    return temp

def storerv(r, v):
    counter=-1
    for i in scopeList:
        tempEntityList=i.getEntityList()
        for j in tempEntityList:
            if(j.name==v and counter==-1):
                counter=i.nestingLevel
                v=j
                break
    localVar=scopeList[0].isLocalVar(v.name)
    if(counter==1):
        temp="sw $t"+str(r)+",-"+str(v.offset)+"($s0)\n"
    elif((localVar==1 or v.name[0:2]=="T_" or v.parMode=="in") and nesting==counter):
        temp="sw $t"+str(r)+",-"+str(v.offset)+"($sp)\n"
    elif(v.parMode=="inout" and nesting==counter):
        temp="lw $t0,-"+str(v.offset)+"($sp)\n\t\t"+"sw $t"+str(r)+"($t0)\n"
    elif(v.parMode=="" and localVar==1 or v.parMode=="in" or counter<nesting):
        temp=gnvlcode(v.name)+"\t\tsw $t"+str(r)+"($t0)"
    elif(v.parMode=="inout" and counter<nesting):
        temp=gnvlcode(v.name)+"\t\tlw $t0,($t0)"+"\t\tsw $t"+str(r)+"($t0\n)"
    else:
        temp="Error i storerv at line"+str(line)
    print(temp)
    return temp

# Call the syntax
syntax()
# Call the makeCfile
makeCfile()

fileReader.close()  # Closing the file


