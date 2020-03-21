#Prifth Ioannhs/AM 3321/username cse63321
#Theodwrou Gewrgios Euaggelos/AM 3231/username cse63231

import string
import sys

reservedWords=["program","declare","if","else","while","doublewhile","loop","exit","forcase","incase","when","default","not","and","or","function","procedure","call","return","in","inout","input","print"]
relationalOpers=['=',"<=",">=",'>','<',"<>"]
mulOpers=['*','/']
addOpers=['+','-']
delimeters=[';',',',':']
groupingSymbols=['(',')','[',']','{','}']
comments=["/*","*/","//"]
assign=[":="]

#Variable where store the last location of the file that stopped reading
position=-1
#Variable where store the last line of the file that stopped reading
line=0

#Open file
fileName=input("Enter the file name: ")

#Check if it is of the required type
if("min" in fileName):
	fileReader=open(fileName,'r')
else:
	print("Wrong type of input file!\nExpected .min")
	exit()

#Lektikos Analyths
def lex():
	global position
	global line
	tempString=""
	char=''
	while(True):
		position+=1
		fileReader.seek(position)
		char=fileReader.read(1) #Reading char by char
		tempString=char.join(tempString)

		if not char:
			continue #Return to the top of the loop
		elif(char=='\n'):
			line+=1
		elif(tempString in relationalOpers): #Checks if it is a relational operant
			if(tempString=='<' or tempString=='>'):
				position+=1
				fileReader.seek(position)
				char=fileReader.read(1)
				tempString=char.join(tempString)
				if(tempString in relationalOpers):
					return tempString
				else:
					position-=1
					fileReader.seek(position)
					tempString=tempString[:-1]
					return tempString
			return tempString
		elif(tempString in addOpers): #Checks whether it is an add or subtract
			return tempString
		elif(tempString in delimeters): #Checks if it is a delimeter
			if(tempString==':'):
				position+=1
				fileReader.seek(position)
				char=fileReader.read(1)
				tempString=char.join(tempString)
				if(tempString in assign):
					return tempString
				else:
					position-=1
					fileReader.seek(position)
					tempString=tempString[:-1]
					return tempString
			return tempString
		elif(tempString in mulOpers):
			position+=1
			fileReader.seek(position)
			char=fileReader.read(1)
			tempString=char.join(tempString)
			if(tempString in comments):
				return tempString
			else:
				position-=1
				fileReader.seek(position)
				tempString=tempString[:-1]
				return tempString	
		elif(tempString in groupingSymbols): #Checks is it is a grouping symbol
			return tempString
		elif(tempString.isalpha()): #Checks if it is a reserved word or variable(Starts with char and without number)
			while(True):			
				position+=1
				fileReader.seek(position)
				char=fileReader.read(1)
				if((int(char) is int) or char.isalpha()):
					tempString=char.join(tempString)
					if(tempString in reservedWords):
						position+=1
						fileReader.seek(position)
						char=fileReader.read(1)
						if((char in relationalOpers) or (char in mulOpers) or (char in addOpers) or (char in delimeters) or (char in groupingSymbols) or (char in comments) or (char in assign)):
							position-=1
							fileReader.seek(position)
							return tempString

				else:
					position-=1
					fileReader.seek(position)
					return tempString
		elif(tempString.isdigit()): #Ckecks if it is a number 
			while(True):
				position+=1
				fileReader.seek(position)
				char=fileReader.read(1)
				if(not char.isdigit()):
					position-=1
					fileReader.seek(position)
					number=int(tempString)
					if(number>=32767 and number<=32767): #Checks if it belongs to the definition field
						return number
					else:
						return 0
				else:
					tempString=char.join(tempString)
		elif(char==EOFError): #Checks for the end of file
			return EOFError;							
	
#Syntaktikos Analyths
def syntax():
	token=lex()
	if(program()):
		print("syntax analisys completed at line=",l)
		return 1
	else:
		print("syntax analisys failed at line=",l)
		return 0
		
def program():
	if(token=="program"):
		token=lex()
		if(token==idtk):
			token=lex()
			block()
			return 1
		else:
			print("program id expected at line=",l)
			return 0
	else:
		print("the keyword 'program' was expected at line=",l)
		return 0
	
def block():
	declarations()
	subprograms()
	statements()
	return 1

def declarations():
	if(token=="declare"):
		token=lex()
		varlist()
		return 1
	else:
		print("the keyword 'declare' was expected at line=",l)
		return 0
	
def varlist():
	while(token==idtk):
		token=lex()
		if(token==','):
			token=lex()
		else:
			return 1

def subprograms():
	while(token==subprogramtk):
		token=lex()		
		subprogram()
	return 1
		
def subprogram():	
	if(token=="function"):
		token=lex()
		if(token==idtk):
			token=lex()
			funcbody()
			return 1
		else:
			print("no function ID found at line=",l)	
			return 0
	elif(token=="procedure"):
		token=lex()
		if(token==idtk):
			token=lex()
			funcbody()
			return 1
		else:
			print("no procedure ID found at line=",l)
			return 0
	else:
		print("incorrect subprogram syntax at line=",l)
		return 0

def funcbody():
	token=lex()	
	formalpars()	
	if(token=='{'):
		token=lex()
		block()
		if(token=='}'):
			token=lex()
			return 1
		else:
			print(" '}' expected at the end of the statement at line=",l)
			return 0
	else:
		print(" '{' expected at the beginning of the statement at line=",l)
		return 0

def formalpars():
	if(token=='('):
		token=lex()
		formalparlist()
		if(token==')'):
			token=lex()
			return 1
		else:
			print(" ')' expected after parameter list at line=",l)
			return 0
	else:
		print(" '(' expected before parameter list at line=",l)
		return 0

def formalparlist():
	token=lex()	
	formalparitem()	
	while(formalparitem()):
		if(token==','):
			token=lex()
			formalparitem()
		else:
			print(" ',' expected beetwen parameters at line=",l)
			return 0
	return 1

def formalparitem():
	if(token=="in"):
		token=lex()
		if(token==idtk):
			token=lex()
			return 1
		else:
			print("no ID found in expression at line=",l)
			return 0
	elif(token=="inout"):
		token=lex()
		if(token==idtk):
			token=lex()
			return 1
		else:
			print("no ID found inout expression at line=",l)	
			return 0
	else:
		print("No valid expression at line=",l)
		return 0

def statements():
	if(token==statementtk):
		token=lex()
		statement()
		return 1
	if(token=='{'):
		token=lex()
		while(True):
			statement()
			if(token==';'):
				token=lex()
				statement()
				if(token=='}'):
					token=lex()
					return 1
				else:
					print(" '}' was expected at line=",l)
					return 0
			else:
				print(" ';' was expected at line=",l)
				return 0
	else:
		print(" '{' was expected at line=",l)
		return 0
	
def statement():
	if(token==assignmenttk):
		token=lex()
		assignmentStat()
		return 1
	elif(token=="if"):
		token=lex()
		ifStat()
		return 1
	elif(token=="while"):
		token=lex()
		whileStat()
		return 1
	elif(token=="doublewhile"):
		token=lex()
		doublewhileStat()
		return 1
	elif(token=="loop"):
		token=lex()
		loopStat()
		return 1
	elif(token=="exit"):
		token=lex()
		exitStat()
		return 1
	elif(token=="forcase"):
		token=lex()
		forcaseStat()
		return 1
	elif(token=="incase"):
		token=lex()
		incaseStat()
		return 1
	elif(token=="call"):
		token==lex()
		callStat()
		return 1
	elif(token=="return"):
		token=lex()
		returnStat()
		return 1
	elif(token=="input"):
		token=lex()
		inputStat()
		return 1
	elif(token=="print"):
		token=lex()
		printStat()
		return 1
	else:
		print("Wrong Statement format at line=",l)
		return 0
	
def assignmentStat():
	if(token==idtk):
		token=lex()
		if(token==":="):
			token=lex()
			expression()
			return 1
		else:
			print(" ':=' was expected at line=",l)
			return 0
	else:
		print("No ID found at the begining of the expression at line=",l)
		return 0
			
def ifStat():
	if(token=='('):
		token=lex()
		condition()
		if(token==')'):
			token=lex()
			if(token=="then"):
				token=lex()
				statements()
				elsepart()
				return 1
			else:
				print(" 'then' was expected to complete if statement at line=",l)
				return 0
		else:
			print(" ')' was expected at line=",l)
			return 0
	else:
		print(" '(' was expected at line=",l)
		return 0
			
def elsepart():
	if(token=="else"):
		token=lex()
		statements()
		return 1
	else:
		return 1
		
def whileStat():	
	if(token=='('):
		token=lex()
		condition()
		if(token==')'):
			token=lex()
			statements()
			return 1
		else:
			print(" ')' was expected at line=",l)
			return 0
	else:
		print(" '(' was expected at line=",l)
		return 0
			
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
	
def forcaseStat():
	while(token=="when"):
		token=lex()
		if(token=='('):
			token=lex()
			condition()
			if(token==')'):
				token=lex()
				if(token==':'):
					token=lex()
					statements()
				else:
					print(" ':' was expected at line=",l)
					return 0
			else:
				print(" ')' was expected at line=",l)
				return 0
		else:
			print(" '(' was expected at line=",l)
			return 0
	token=lex()
	if(token=="default"):
		token=lex()
		if(token==':'):
			token=lex()
			statements()
			return 1
		else:
			print(" ':' was expected at line=",l)
			return 0
	else:
		print(" 'default' expression was expected at line=",l)
		return 0
	
def incaseStat():
	while(token=="when"):
		token=lex()
		if(token=='('):
			token=lex()
			condition()
			if(token==')'):
				token=lex()
				if(token==':'):
					token=lex()
					statements()
				else:
					print(" ':' was expected at line=",l)
					return 0
			else:
				print(" ')' was expected at line=",l)
		else:
			print(" '(' was expected at line=",l)
			return 0

def returnStat():
	expression()
	token=lex()
	return 1
	
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
	
def printStat():
	if(token=='('):
		token=lex()
		expression()
		if(token==')'):
			token=lex()
			return 1
		else:	
			print(" ')' was expected at line=",l)
			return 0
	else:
		print(" '(' was expected at line=",l)
		return 0
	
def inputStat():	
	if(token=='('):
		token=lex()
		if(token==idtk):
			token=lex()
			if(token==')'):
				token=lex()
				return 1
			else:
				print(" ')' was expected at line=",l)
				return 0
		else:
			print("No ID found in input expression at line=",l)
			return 0
	else:
		print(" '(' was expected at line=",l)
		return 0
			
def actualpars():
	if(token=='('):
		token=lex()
		actualparlist()
		if(token==')'):
			token=lex()
			return 1
		else:
			print(" ')' was expected at line=",l)
			return 0
	else:
		print(" '(' was expected at line=",l)
		return 0
	
def actualparlist():
	actualparitem()
	token=lex()
	while(token==actualparitemtk):
		token=lex()
		actualparitem()
		if(token==','):
			actualparitem()
			token=lex()
		else:
			print(" ',' was expected at line=",l)
			return 0
	return 1
	
def actualparitem():
	if(token=="in"):
		token=lex()
		expression()
		return 1
	elif(token=="inout"):
		token=lex()
		if(token==idtk):
			token=lex()
			return 1
		else:
			print("No ID found after inout expression at line=",l)
			return 0
	else:
		print("No valid expression at line=",l)
		return 0
	
def condition():
	boolterm()
	token=lex()
	while(token==booltermtk):
		token=lex()
		if(token=="or"):
			token=lex()
			boolterm()
		else:
			print("the keyword 'or' was expected at line=",l)
			return 0
	return 1
	
def boolterm():
	boolfactor()
	token=lex()
	while(token==boolfactortk):
		token=lex()
		boolfactor()
		if(token=="and"):
			token=lex()
			boolfactor()
		else:
			print("the keyword 'and' was expected at line=",l)
			return 0
	return 1
	
def boolfactor():	
	if(token=="not"):
		token=lex()
		if(token=='['):
			token=lex()
			condition()
			if(token==']'):
				token=lex()
				return 1
			else:
				print(" ']' was expected at line=",l)
				return 0
		else:
			print(" '[' was expected at line=",l)
			return 0
	elif(token=='['):
		token=lex()
		condition()
		if(token==']'):
			token=lex()
			return 1
		else:
			print(" ']' was expected at line=",l)
			return 0
	else:	
		print(" 'not' or '[' was expected at line=",l)
		return 0
	if(token!="not" and token!='[' and token!=']'):
		token=lex()
		expression()
		relationaloper()
		expression()
		return 1
			
def expression():
	optionalsign()	
	term()
	token=lex()
	while(token==addopertk):
		token=lex()
		addoper()
		term()
	return 1
		
def term():
	factor()
	token=lex()
	while(token==mulopertk):
		token=lex()
		muloper()
		factor()
	return 1
		
def factor():
	if(token==constanttk):
		token=lex()
		return 1
	if(token=='('):
		token=lex()
		expression()
		if(token==')'):
			token=lex()
			return 1
		else:
			print(" ')' was expected at line=",l)
			return 0
	else:
		print(" '(' was expected at line=",l)
		return 0
	if(token==idtk):
		token=lex()
		idtail()
		return 1
	return 1
			
def idtail():
	actualpars()
	token=lex()
	return 1
			
def relationaloper():
	if(token=='='):
		token=lex()
		return 1
	elif(token=="<="):
		token=lex()
		return 1
	elif(token==">="):
		token=lex()
		return 1
	elif(token=='>'):
		token=lex()
		return 1
	elif(token=='<'):
		token=lex()
		return 1
	elif(token=="<>"):
		token=lex()
		return 1
	else:
		print("invalid relational operant at line=",l)
		return 0
	
def addoper():
	if(token=='+'):
		token=lex()
		return 1
	elif(token=='-'):
		token=lex()
		return 1
	else:	
		return 0
	
def muloper():
	if(token=='*'):
		token=lex()
		return 1
	elif(token=='/'):
		token=lex()
		return 1
	else:
		print("invalid multiplication opernat at line=",l)
		return 0
		
def optionalsign():
	token=lex()	
	addoper()	
	return 1
				
#Call the syntax
syntax()
		
close(file) #Κλείσιμο αρχείου

