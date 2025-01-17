#!/usr/bin/env python3

"""
    Author: Niamh Smith [niamh.smith.17@ucl.ac.uk]
    Date: 16/01/2025


    Hey James!

    You'll want to run this in a commandline terminal like Terminal on your Mac using:
        python3 ./main.py

    You'll want to add in the details I've highlighted with comments '##' to make it work for you.

    You will also want to pip install numpy [pip3 install numpy] & docx [pip3 install python-docx] if you haven't already
    before running.

    If you have any questions or any issues with the code, please let me know :)
"""

import numpy as np
from docx import Document

## List Contract types and file paths - name the variable the contract type and equal it to its template filepath.
contracts = {'test contract': "./test_contract_blank.docx",}



## Add the variable name of each contract type to list options.
options = ['test contract']

class bcolors:
    """
        Colours to be used for command line messages and for user inputs upon run of python file.

        Class definitions are each either a Select Graphic Rendition (SGR) or 8-bit Escape (ESC) color mode code.
    """

    KEYVAR = '\033[95m'  # was HEADER
    QUESTION = '\x1b[38;5;135m'
    CHOSEN = '\x1b[38;5;50m'
    INFO = '\x1b[38;5;221m'
    ACTION = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

## Add to dictionary additional questions you'd like to be asked during creation of contract.
questions = {'Q1': f"{bcolors.QUESTION}What contract type would you like to create?{bcolors.ENDC}",
             'Q2': f'\n{bcolors.QUESTION}What is recipients name?{bcolors.ENDC}',
             'Q3': f"\n{bcolors.QUESTION}What is recipients address?{bcolors.ACTION}"
                   f"\nPlease {bcolors.UNDERLINE}use '//' at the end of the address{bcolors.ENDC}{bcolors.ACTION} "
                   f"to signal you have finished inputting the address.{bcolors.ENDC}\n",}

class ErrMessages:
    @staticmethod #√
    def ValueErrorlist():
        """
            Inputs:
                options(list) : List of the methods of data processing the user can
                                choose from.

                lock(th.Lock) : Unowned lock synchronization primitive shared
                                between threads which when called upon blocks the ability
                                of any other thread to print until the lock has finished the
                                printing commands within the current with statement it has
                                acquired and is released.
        """
        text = str(f"\n{bcolors.FAIL}ERROR: {bcolors.UNDERLINE}Contract type not implemented!{bcolors.ENDC}"
                   "{bcolors.INFO} "
                   f"\nValid implemented contract types are:{bcolors.CHOSEN}{bcolors.ITALIC} \n"
                   +f"{', '.join(options)}"
                   +"{bcolors.ENDC}")
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
        print(text)

def checkinput(func):
    """
         Testing for error in user's input response to questions asked.
    """
    def wrapper(Q, typ, ans, *args):
        """
            Inputs:
                Q(str)        : Key for one of the questions within Core.PrePopDictsAndLists.questions.

                typ(str)      : Expected type of the answer and must match a key within func._format.

                ans(list)     : List of multiple valid answer options the user can choose from

                args          : extra arguments such as a th.Lock or queue.Queue for controlling passing
                                of into between threads and/or preventing simultaneous printing of
                                multiple threads.

            Outputs:
                A(str)        : If error exception is triggered, return answer given by user when question
                                asked again by function. If error exception is not triggered, return value
                                of input A as given to function.
        """

        A = func(Q, typ, ans)
        if typ == 'list':
            try:
                if isinstance(A, list) == True:
                    if len([a for a in A if a not in ans]) != 0:
                        raise ValueError
                else:
                    if A not in ans:
                        raise ValueError
            except:
                # trigger error informing user that they've given an input which is invalid.
                eval("ErrMessages.ValueError{}()".format(typ))
                A = ask_question(Q, typ, ans)
        return A
    return wrapper

@checkinput
def ask_question(Q: str, typ: str, ans: list):
    """
        Asking required user input question.
    """
    _format = {'list': "A.split(', ') if ',' in A else [A]", 'YorN': 'A.upper()', 'none': 'A', 'multiple':'A'}
    assert Q in questions.keys(), "Q must be a key for one of the questions within ."
    assert typ in _format.keys(), "typ is the expected type of the answer and must match a key within _format."
    assert isinstance(ans, list), "ans must be a list of multiple valid answer options the user can choose from"
    print(questions[str(Q)])
    if typ != 'multiple':
        A = input()
        # if expected type is list, split string. If expected type is Yes or No, make sure string is upper case.
        A = eval(_format[typ])
    else:
        A, end = [], False
        while end == False:
            a = input()
            if '//' not in a:
                A.append(a)
            elif '//' in a:
                a = a.replace('//','')
                print(a)
                A.append(a)
                end = True
    return A

class program:
    def __init__(self):
        print(f'{bcolors.KEYVAR} Welcome to PDP contract automation {bcolors.ENDC}\n ')

        self.contype = ask_question('Q1', 'list', options)

        self.repname = ask_question('Q2','none',['none'])

        self.repadd = ask_question('Q3','multiple',['none'])

        newfile = self.writingnew()
        print(f"{bcolors.CHOSEN}The file {newfile} has been made for {self.repname} from template for {self.contype[0]} contract{bcolors.ENDC}")


    def writingnew(self):
        document = Document(contracts[self.contype[0]])
        lines = [x.text for x in document.paragraphs]
        lines_ = np.asarray(lines)
        idx4name = np.argwhere(lines_ == 'recipient name:')[0][0]
        document.paragraphs[idx4name].text  = " ".join([document.paragraphs[idx4name].text, self.repname])
        print(lines[idx4name])
        idx4add = np.argwhere(lines_ == 'recipient address:')[0][0]
        add = "\n\t".join(self.repadd)
        document.paragraphs[idx4add].text  = " ".join([document.paragraphs[idx4add].text, add])

        newfilename = "".join(['.',str(contracts[self.contype[0]]).split('.')[1], '_result.docx'])
        document.save(newfilename)

        return newfilename



if __name__ =='__main__':
    program()