import tkinter as tk
from tkinter import ttk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *




class Token_type(Enum):  # listing all tokens type
    Begin = 1
    End = 2
    Do = 3
    Else = 4
    EndIf = 5
    If = 6
    Integer = 7
    Dot = 8
    Semicolon = 9
    EqualOp = 10
    LessThanOp = 11
    GreaterThanOp = 12
    NotEqualOp = 13
    PlusOp = 14
    MinusOp = 15
    MultiplyOp = 16
    DivideOp = 17
    Identifier = 18
    Constant = 19
    Program = 20
    Procedure = 21
    Parameters = 22
    Declare = 23
    Error = 24
    read = 25
    write = 26

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


# Reserved word Dictionary
ReservedWords = {"IF": Token_type.If,
                 "PROGRAM": Token_type.Program,
                 "PROCEDURE": Token_type.Procedure,
                 "Parameters": Token_type.Parameters,
                 "Declare": Token_type.Declare,
                 "END": Token_type.End,
                 "BEGIN": Token_type.Begin,
                 "DO": Token_type.Do,
                 "ElSE": Token_type.Else,
                 "ENDIF": Token_type.EndIf,
                 "INTEGER": Token_type.Integer,
                 "read" : Token_type.read,
                 "write" : Token_type.write
                 }
Operators = {".": Token_type.Dot,
             ";": Token_type.Semicolon,
             "=": Token_type.EqualOp,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp
             }
Tokens = []
errors = []


def find_token(text):
    lexems = text.split()
    for le in lexems:
        if (le in ReservedWords):
            new_token = token(le, ReservedWords[le])
            Tokens.append(new_token)
        elif (le in Operators):
            new_token = token(le, Operators[le])
            Tokens.append(new_token)
        elif (re.match("^\d+(\.[0-9]*)?$", le)):
            new_token = token(le, Token_type.Constant)
            Tokens.append(new_token)
        elif (re.match("^([a-zA-Z][a-zA-Z0-9]*)$", le)):
            new_token = token(le, Token_type.Identifier)
            Tokens.append(new_token)
        else:
            new_token = token(le, Token_type.Error)
            errors.append("Lexical error  " + le)


def Parse():
    j = 0
    Children = []
    Header_dict=Header(j)
    Children.append(Header_dict["node"])
    Block_dict = Block(Header_dict["index"])
    Children.append(Block_dict["node"])
    dic_output = Match(Token_type.Dot, Block_dict["index"])
    Children.append(dic_output["node"])


    Node = Tree('Program', Children)

    return Node


def Header(j):
    Children =[]
    out = dict()
    out_pro = Match(Token_type.Program,j)
    Children.append(out_pro["node"])
    out_id = Match(Token_type.Identifier,out_pro["index"])
    Children.append(out_id["node"])
    out_sem = Match(Token_type.Semicolon,out_id["index"])
    Children.append(out_sem["node"])
    node=Tree("Header",Children)
    out["node"] = node
    out["index"] = out_sem["index"]
    return out



def Block(j):
        Children =[]
        out = dict()
        out_beg = Match(Token_type.Begin,j)
        Children.append(out_beg["node"])
        Statements_dict = Statements(out_beg["index"])
        Children.append(Statements_dict["node"])
        out_end = Match(Token_type.End,Statements_dict["index"])
        Children.append(out_end["node"])
        node = Tree("Block", Children)
        out["node"] = node
        out["index"] = out_end["index"]
        return out


def Statements(j):
   Children = []
   out = dict()

   out_rw = dict()

   if (j < len(Tokens)):
     Temp = Tokens[j].to_dict()
     if (Temp["token_type"] ==Token_type.read):
       out_rw = Match(Token_type.read, j)


     else:
       out_rw = Match(Token_type.write,j)

     Children.append(out_rw["node"])
     out_id = Match(Token_type.Identifier,out_rw["index"])
     Children.append(out_id["node"])
     node = Tree("Statements",Children)
     out["node"] = node
     out["index"] = out_id["index"]
     return out
   out["node"] = 'error'
   out["index"] = j + 1
   return out

def Match(a, j):
    output = dict()
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j
            errors.append("Syntax error : " + Temp['Lex'] + " Expected " + str(a))
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


# GUI


def Scan():
    x1 = get_input()
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()

    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()

#Scan(PROGRAM X ; BEGIN  write x END .)


def get_input():
    input_text = entry1.get()
    return input_text


root = tk.Tk()
canvas1 = tk.Canvas(root, width=400, height=300, relief='raised', bg='blue')
canvas1.pack()
label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14), bg='white')
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)
style = ttk.Style(root)
style.configure('TLabel', background='black', foreground='white')
style.configure('TFrame', background='black')


button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', highlightbackground='#3E4149',font=('helvetica', 9, 'bold'))

canvas1.create_window(200, 180, window=button1)

root.mainloop()

# In[ ]: