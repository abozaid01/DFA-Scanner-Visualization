#!/usr/bin/env python
# coding: utf-8

# In[49]:


import tkinter as tk
from enum import Enum
import re
#import pandas
#import pandastable as pt
#from nltk.tree import *
# import pandastable as pt
# from nltk.tree import *

class Token_type(Enum): # listing all tokens type
    Predicates=1 #✅
    Clauses=2 #✅
    Goal=3  #✅
    Integer=4
    Symbol=5
    Char=6
    String=7
    Real=8
    Dot=9 #✅
    EqualOp=10  #✅
    LessThanOp=11 #✅
    LessThanOrEqualOp=12 #✅
    GreaterThanOp=13 #✅
    GreaterThanOrEqualOp=14 #✅
    NotEqualOp=15 #✅
    PlusOp=16 #✅
    MinusOp=17 #✅
    MultiplyOp=18 #✅
    DivideOp=19 #✅
    Identifier=20
    Constant=21
    Error=22
    Comma=23 #✅
    Semicolon=24 #✅
    Read=25 #✅
    Readln=26 #✅
    Write=27 #✅
    Writeln=28 #✅
    LeftBracket=29
    RightBracket=30
    colon=31 #✅
    Readint=32 #✅
    Readchar=33 #✅
    predicate_name=34
    singlelinecommentstart=35 #✅
    multilinecommentstart=36 #✅
    multilinecommentend=37 #✅
    newline=38 #?
    singlelinecomment=39 #✅
    multilinecommnet=40 #✅
    assignment_operator=41 #?
    lowercasename=42
    doublequotes=43 #?
    datatypeInteger=44 
    datatypeReal=45
    datatypeString=46
    datatypeSymbol=47
    datatypeCharacter=48

# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type
    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }
    def __str__(self):
        return f"{self.lex}: {self.token_type}"    
###################### error class ############################3
class error:
    def __init__(self,error_name,details):
        self.error_name=error_name
        self.details=details
    def as_string(self):
        result = f'{self.error_name}:{self.details}'
        return result
class IllegalcharError(error):
    def __init__(self, details):
        super().__init__('Illegal character', details)
    
            
#Reserved word Dictionary
ReservedWords={"predicates":Token_type.Predicates,
               "clauses":Token_type.Clauses,
               "goal":Token_type.Goal,
               "write":Token_type.Write,
               "read":Token_type.Read,
               "reaint":Token_type.Readint,
               "readchar":Token_type.Readchar,
               "readln":Token_type.Readln,
               "writeln":Token_type.Writeln
               }
DataTypes={"integer":Token_type.datatypeInteger,
            "symbol":Token_type.datatypeSymbol,
            "char":Token_type.datatypeCharacter,
            "string":Token_type.datatypeString,
            "real":Token_type.datatypeReal
           }
Operators={".":Token_type.Dot,
          ";":Token_type.Semicolon,
          ",":Token_type.Comma, #we forgot this in the meeting
          "=":Token_type.EqualOp,
          "<":Token_type.LessThanOp,
          "<=":Token_type.LessThanOrEqualOp,
          ">":Token_type.GreaterThanOp,
          ">=":Token_type.GreaterThanOrEqualOp,
          "<>":Token_type.NotEqualOp,          
          "+":Token_type.PlusOp,
           "-":Token_type.MinusOp,
           "*":Token_type.MultiplyOp,
           "/":Token_type.DivideOp,
           "(":Token_type.LeftBracket,
           ")":Token_type.RightBracket,
           ":":Token_type.colon,
           "%":Token_type.singlelinecommentstart,
           "/*":Token_type.multilinecommentstart,
           "*/":Token_type.multilinecommentend,
           "\n":Token_type.newline,
           ':-': Token_type.assignment_operator,
           '\"':Token_type.doublequotes
          }



Tokens=[] # to add tokens to list #list of objects
errors=[]
def identify_token(lexems):
    for x in lexems:       
            if x in ReservedWords:
                #print(x)
                t=token(x,ReservedWords[x])
                Tokens.append(t)
            elif x in Operators:
                t=token(x,Operators[x])
                Tokens.append(t)
            elif x in DataTypes:
                t=token(x,DataTypes[x])
                Tokens.append(t)    
            elif re.match("^[A-Z_][a-zA-Z0-9_]*$", x):
                t=token(x,Token_type.Identifier)
                Tokens.append(t)
            elif re.match('^[0-9][0-9]*[/.][0-9]+$', x):
                t = token(x, Token_type.Real)
                Tokens.append(t)
        # regular expression to match an integer
            elif re.match('^[0-9][0-9]*$', x):
                t = token(x, Token_type.Integer)
                Tokens.append(t)
        # regular expression to match a string
            elif re.match('^[\"].*[\"]$', x):
                t = token(x, Token_type.String)
                Tokens.append(t)
            elif re.match("^[a-z][a-zA-Z0-9_]*$", x):#symbol var name
                t=token(x,Token_type.lowercasename)
                Tokens.append(t)
            elif re.match(r"%.",x):#assuming comments start at the beginning of the line
                t=token(x,Token_type.singlelinecomment)
                Tokens.append(t)
            elif re.match('^[/*"].*[*/"]$',x):
                t=token(x,Token_type.multilinecommnet)
                Tokens.append(t)
            else:
                t=token(x,Token_type.Error)
                errors.append(t)
                #return IllegalcharError(t)
                #predicate  names are the ones thatstart with small letters while symbol variables are between double quotes 


def remove_after_comment(lexems):
    for ele in lexems:
        if "*/" in ele:
            index=lexems.index(ele)
            del lexems[index+1]
        
def find_token(text):
    # complete
    start_multi_Comment=-1
    end_multi_Comment=-1
    multi_line_comment=""
    same_line=False
    for s in text:
        lexems=[]
        start = -1
        end = -1
        for ind,c in enumerate(s):
           
            if c=='%':  #detect one line of code
                lexems.append(s[ind:])
                break

            if(ind==0) and (start_multi_Comment!=-1) and ("*/" not in s):
                    if("/*" in multi_line_comment):
                        multi_line_comment=multi_line_comment+s
                        break
            
            if (ind< len(s)-1):
                if (s[ind]=='/') and (s[ind+1]=='*'):
                    start_multi_Comment=ind
                    # print("the first is ",start_multi_Comment)
                    if("*/" not in s):
                        multi_line_comment=s[start_multi_Comment:]
                        break 
                    else:
                        same_line=True
                    # elif("/*" not in s)
                    continue
            
            if (ind< len(s)-1):
                if(s[ind]=='*') and (s[ind+1]=='/'):
                    end_multi_Comment=ind+1
                    # print("the last is ",end_multi_Comment)
                    if(same_line):
                        multi_line_comment=multi_line_comment+s[start_multi_Comment:end_multi_Comment+1]
                    else:
                        multi_line_comment=multi_line_comment+s[:end_multi_Comment+1]
                    lexems.append(multi_line_comment)
                    multi_line_comment=""
                    start_multi_Comment=-1
                    end_multi_Comment=-1
                    continue
            
            if(start_multi_Comment!=-1):
                continue
            if (c=="\"") and (start==-1) :
                start=ind
                continue
            elif (c=="\"") and (end==-1) :
                end=ind
                lexems.append(s[start:end+1])
                start=-1
                end=-1
                continue
            elif start!=-1:
                continue
            elif c in Operators:
                lexems.append(c)
            elif lexems and lexems[-1] not in Operators:
                lexems[-1] += c
            else:
                lexems.append(c)
        remove_after_comment(lexems)
        identify_token(lexems)
        
        #lexems=s.split() 
        print(lexems)
    print("Tokens:")
    print([str(t) for t in Tokens])
    print("Errors")        
    print([str(t) for t in errors])
        
file = open('inp.txt', 'r')
lines= file.readlines()
input=[]
for line in lines:
     line = line.strip().replace(" ", "")
     input.append(line)
print(input)
find_token(input)
def save_out(tokens, err):
    output = open('out.txt', 'w')
    output.write(Tokens)
    output.write('\n')
    output.write(err)
    #pass