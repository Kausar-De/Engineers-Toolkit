import tkinter as tk #For GUI
import tkinter.ttk as ttk #For styling
from PIL import ImageTk, Image #For image processing
import numpy as np #For matrix operations
import math #For math expressions
import matplotlib #For graph operations
import matplotlib.pyplot as plt #For pyplot
matplotlib.use('TkAgg') #Makes TkAgg the backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #For canvas and nav toolbar
from matplotlib.figure import Figure
import requests, json #For API calls
import webbrowser #For opening web browser with tkinter button
import cmath #For complex number operations
from sympy import Symbol #For equation symbols
from sympy.solvers import solve #For equation solving

LargeFont = ('Verdana', 12) #Standard large font to be used throughout
TitleFont = ('Times New Roman', 20, 'bold') #Standard font to be used for headline text
LabelFont = ('Arial', 13, 'bold') #Standard font to be used for labels

uHist = [] #Usage History array

expression = '' #Global variable declarations
uStatement = ''
prec = 2
evar = math.e
pivar = math.pi
phivar = 1.618033988749894

class Calculator(tk.Tk): #Main program class w/ container

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Engineer's Toolkit") #Program title
        
        container = tk.Frame(self) #Code for main container
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {} #Code for accomodating different frames in which code will run

        for F in (StartPage, ChoicePage, ArithPage, NumpyPage, MatPlotLibPage, ConverterPage, ComplexPage, HistPage): #Iterates through the different pages
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')

        self.show_frame(StartPage) #Shows the starting page

    def show_frame(self, cont): #This function is used to display the different frames

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame): #This class is for the starting page, which will be displayed first

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831') #Defines the frame, as well as inherits from container class

        def setPreci(): #This function sets global precision
            try:
                global prec
                
                val = int(precifield.get())

                prec = val
                precvar.set('Precision is now ' + str(prec))
            except:
                precvar.set('ERROR')

        def msclick(event): #This function is to empty precifield upon mouse click
            precifield.delete(0, 'end')
            return None

        precvar = tk.StringVar()
        precvar.set('Enter Precision (Default 2)')

        label1 = tk.Label(self, text = 'Welcome to the Toolkit!', font = TitleFont, fg = '#00adb5', bg = '#222831') #These labels are for displaying the title text
        label1.grid(row = 0, column = 1, padx = 250, pady = 10) #To position label
        label2 = tk.Label(self, text = 'Please press START to continue or QUIT to exit!', font = TitleFont, fg = '#00adb5', bg = '#222831')
        label2.grid(row = 1, column = 1, padx = 150, pady = 10)

        startlf = tk.LabelFrame(self, bg = '#222831', borderwidth = 0, highlightthickness = 0) #This label enables positioning buttons centrally
        startlf.grid(row = 2, column = 1, padx = 420, pady = 10)

        s = ttk.Style() #Button styling
        s.theme_use('alt')
        s.configure('btn.TButton', font = ('Arial', 12), foreground = '#eeeeee', background = '#00adb5')
        s.map('btn.TButton', foreground = [('active', '!disabled', '#00adb5')], background = [('active', '#393e46')])

        startbutton = ttk.Button(startlf, text = 'START', style = 'btn.TButton', command = lambda: controller.show_frame(ChoicePage)) #This button redirects to ChoicePage
        startbutton.grid(row = 0, column = 0, padx = 10, pady = 50, sticky = 'e')

        quitbutton = ttk.Button(startlf, text = 'QUIT', style = 'btn.TButton', command = lambda: quit()) #This button ends the program
        quitbutton.grid(row = 0, column = 1, padx = 10, pady = 50, sticky = 'w')

        precilf = tk.LabelFrame(self, bg = '#393e46', borderwidth = 0, highlightthickness = 0) #This label enables positioning buttons centrally
        precilf.grid(row = 3, column = 1, padx = 420, pady = 10, sticky = 'n')
        
        precilabel = tk.Label(precilf, text = 'Set global precision:', font = LabelFont, fg = '#00adb5', bg = '#222831')
        precilabel.grid(row = 0, column = 0, padx = 10, pady = 10)

        precifield = tk.Entry(precilf, textvariable = precvar, width = 22, font = LargeFont) #This entry field displays user input and output
        precifield.grid(row = 1, column = 0, ipadx = 0.1, ipady = 3, padx = 10, pady = 10)
        precifield.bind('<Button-1>', msclick)

        precibutton = ttk.Button(precilf, text = 'SET', style = 'btn.TButton', command = lambda: setPreci())
        precibutton.grid(row = 2, column = 0, padx = 10, pady = 10)        
        
class ChoicePage(tk.Frame): #This class is for the second page, where user can choose which part of calculator to use

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831')

        label = tk.Label(self, text = 'So, what are we doing?', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title label
        label.grid(row = 0, column = 0, padx = 435, sticky = 'nsew') 

        backbutton = ttk.Button(self, text = 'Back', style = 'btn.TButton', command = lambda: controller.show_frame(StartPage)) #This button takes us to the previous page
        backbutton.grid(row = 0, column = 0, padx = 10, pady = 20, sticky = 'e')

        histbutton = ttk.Button(self, text = 'History', style = 'btn.TButton', command = lambda: controller.show_frame(HistPage)) #This button takes us to the usage history page
        histbutton.grid(row = 0, column = 0, padx = 10, pady = 20, sticky = 'w')

        choiceslf = tk.LabelFrame(self, bg = '#222831', borderwidth = 0, highlightthickness = 0) #This label enables positioning buttons centrally
        choiceslf.grid(row = 1, column = 0, padx = 10, pady = 90)

        arithbutton = ttk.Button(choiceslf, text = 'Arithmetic', style = 'btn.TButton', command = lambda: controller.show_frame(ArithPage)) #Button to take us to arithmetic operations
        arithbutton.grid(row = 0, column = 0, padx = 10, pady = 20)
        arithbutton.config(width = '17')

        numpybutton = ttk.Button(choiceslf, text = 'Matrices, Trig & Logs', style = 'btn.TButton', command = lambda: controller.show_frame(NumpyPage)) #Button to take us to numpy operations
        numpybutton.grid(row = 0, column = 1, padx = 10, pady = 20)
        numpybutton.config(width = '17')

        convbutton = ttk.Button(choiceslf, text = 'Converter', style = 'btn.TButton', command = lambda: controller.show_frame(ConverterPage)) #Button to take us to converter page 
        convbutton.grid(row = 0, column = 2, padx = 10, pady = 20)
        convbutton.config(width = '17')

        graphbutton = ttk.Button(choiceslf, text = 'Graphs', style = 'btn.TButton', command = lambda: controller.show_frame(MatPlotLibPage)) #Button to take us to matplotlib operations 
        graphbutton.grid(row = 1, column = 0, padx = 10, pady = 20)
        graphbutton.config(width = '17')

        docsbutton = ttk.Button(choiceslf, text = 'Cheat Sheet', style = 'btn.TButton') #Button to take us to documentations page (PLANNED)
        docsbutton.grid(row = 1, column = 1, padx = 10, pady = 20)
        docsbutton.config(width = '17')

        complexbutton = ttk.Button(choiceslf, text = 'Complex & Equations', style = 'btn.TButton', command = lambda: controller.show_frame(ComplexPage)) #Button to take us to complex and equation operations
        complexbutton.grid(row = 1, column = 2, padx = 10, pady = 20)
        complexbutton.config(width = '17')

class ArithPage(tk.Frame): #This class is for the Arithmetic operations page

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831')

        def click(num): #This functions enables button inputs
            global prec
            global expression
            
            expression = expression + str(num) #Num argument is substituted by input from calculator buttons
            equation.set(expression)

        def solve(): #This function equates the inputted expression
            try:
                global prec
                global expression
                global uStatement
                global uHist
                
                ans = str(round(eval(expression), prec)) #Using eval to calculate user inputed expression and is then converted to string
                uStatement = str(expression + ' = ' + ans + '\n') #Usage history statement
                uHist.append(uStatement)
                equation.set(ans) #Displays answer in inputfield
                expression = ans
            except:
                equation.set('ERROR')
                expression = ''

        def changeConst(): #This function replaces the buttons mentioned with constants
            try:
                btnconst['text'] = 'Revert'
                btnconst['command'] = revertConst
                btne['text'] = 'eV'
                btne['command'] = lambda: click(round((1.602 * 10**-19), prec))
                btnexp['text'] = 'h'
                btnexp['command'] = lambda: click(round((6.62607004 * 10**-34), prec))                                
                btnpi['text'] = 'G'
                btnpi["command"] = lambda: click(round((6.67408 * 10**-11), prec))
                btnphi['text'] = 'N(A)'
                btnphi['command'] = lambda: click(round((6.02214 * 10**23), prec))
                btnlbr['text'] = 'k'
                btnlbr['command'] = lambda: click(round((1.38064852 * 10**-23), prec))               
                btnrbr['text'] = 'c'
                btnrbr['command'] = lambda: click(round((299792458), prec))
            except:
                raise

        def revertConst(): #This function reverts everything back to normal
            try:
                btnconst['text'] = 'Constants'
                btnconst['command'] = changeConst
                btne['text'] = 'e'
                btne['command'] = lambda: click(round(evar, prec))
                btnexp['text'] = '**'
                btnexp['command'] = lambda: click('**')
                btnpi['text'] = '\u03C0'
                btnpi['command'] = lambda: click(round(pivar, prec))
                btnphi['text'] = '\u03C6'
                btnphi['command'] = lambda: click(round(phivar, prec))
                btnlbr['text'] = '('
                btnlbr['command'] = lambda: click('(')              
                btnrbr['text'] = ')'
                btnrbr['command'] = lambda: click(')')
            except:
                raise

        def clr(): #This function is for behaviour of CLEAR button for arithmetic
            global expression
            expression = ''
            equation.set('Enter your Input')

        def clrmod(): #This function is for behaviour of CLEAR button for modulus
            mod1var.set('Enter Dividend')
            mod2var.set('Enter Divisor')
            modansvar.set('Answer Here')

        def clrabs(): #This function is for behaviour of CLEAR button for absolute value
            absvar.set('Enter your input')
            absansvar.set('Answer Here')

        def clrperc(): #This function is for behaviour of CLEAR button for percentage
            perc1var.set('Enter Part')
            perc2var.set('Enter Whole')
            percansvar.set('Answer Here')
            
        def msclick1(event): #This function is to empty modfield1 upon mouse click
            modfield1.delete(0, 'end')
            return None

        def msclick2(event): #Above function for modfield2
            modfield2.delete(0, 'end')
            return None

        def msclick3(event): #Above function for absfield
            absfield.delete(0, 'end')
            return None

        def msclick4(event): #Above function for percfield1
            percfield1.delete(0, 'end')
            return None

        def msclick5(event): #Above function for percfield2
            percfield2.delete(0, 'end')
            return None

        def modsolve(): #This function calculates modulus
            try:
                global uHist
                global uStatement
                
                dividend, divisor = float(modfield1.get()), float(modfield2.get()) #Acquires dividend and divisor
                
                ans = round((dividend % divisor), prec) #Calculates modulus
                uStatement = str('The modulus of ' + str(dividend) + ' and ' + str(divisor) + ' is ' + str(ans) + '\n') #Usage history statement
                uHist.append(uStatement) 
                modansvar.set(ans)
            except:
                mod1var.set('ERROR')
                mod2var.set('ERROR')

        def abssolve(): #This function calculates absolute value
            try:
                global uHist
                global uStatement
                
                abso = float(absfield.get()) #Acquires value for absolute
                
                ans = round((abs(abso)), prec) #Calculates absolute 
                uStatement = str('The absolute value of ' + str(abso) + ' is ' + str(ans) + '\n') #Usage history statement                
                uHist.append(uStatement) 
                absansvar.set(ans)
            except:
                absvar.set('ERROR')

        def percsolve(): #This function calculates percentage
            try:
                global uHist
                global uStatement
                
                part, whole = float(percfield1.get()), float(percfield2.get()) #Acquires numbers for percentage
                
                ans = round(((part / whole)*100), prec) #Calculates percentage
                ans = str(ans) + '%' #Displays answer with % sign at the end
                uStatement = str(str(part) + ' is ' + ans + ' of ' + str(whole) + '\n') #Usage history statement                
                uHist.append(uStatement) 
                percansvar.set(ans)
            except:
                perc1var.set('ERROR')
                perc2var.set('ERROR')

        equation = tk.StringVar() #These variables are the text variables for all the Entry fields
        equation.set('Enter your Input')
        mod1var = tk.StringVar()
        mod1var.set('Enter Dividend')
        mod2var = tk.StringVar()
        mod2var.set('Enter Divisor')
        absvar = tk.StringVar()
        absvar.set('Enter Number')
        modansvar = tk.StringVar()
        modansvar.set('Answer Here')
        absansvar = tk.StringVar()
        absansvar.set('Answer Here')
        perc1var = tk.StringVar()
        perc1var.set('Enter Part')
        perc2var = tk.StringVar()
        perc2var.set('Enter Whole')
        percansvar = tk.StringVar()
        percansvar.set('Answer Here')        

        label = tk.Label(self, text = 'Arithmetic', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title Label
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        arilf = tk.LabelFrame(self, text = 'Arithmetic:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains all the stuff for simple arithmetic
        arilf.grid(row = 1, column = 0, padx = 10, pady = 10)

        inputfield = tk.Entry(arilf, textvariable = equation, font = LargeFont, state = 'readonly') #This entry field displays user input and output
        inputfield.grid(columnspan = 4, ipadx = 20, ipady = 3, pady = 15)

        btn1 = ttk.Button(arilf, text = '1', style = 'btn.TButton', command = lambda: click(1)) #Calculator buttons
        btn1.grid(row = 5, column = 0, padx = 10, pady = 10)

        btn2 = ttk.Button(arilf, text = '2', style = 'btn.TButton', command = lambda: click(2))
        btn2.grid(row = 5, column = 1, padx = 10, pady = 10)

        btn3 = ttk.Button(arilf, text = '3', style = 'btn.TButton', command = lambda: click(3))
        btn3.grid(row = 5, column = 2, padx = 10, pady = 10)

        btn4 = ttk.Button(arilf, text = '4', style = 'btn.TButton', command = lambda: click(4))
        btn4.grid(row = 4, column = 0, padx = 10, pady = 10)

        btn5 = ttk.Button(arilf, text = '5', style = 'btn.TButton', command = lambda: click(5))
        btn5.grid(row = 4, column = 1, padx = 10, pady = 10)

        btn6 = ttk.Button(arilf, text = '6', style = 'btn.TButton', command = lambda: click(6))
        btn6.grid(row = 4, column = 2, padx = 10, pady = 10)

        btn7 = ttk.Button(arilf, text = '7', style = 'btn.TButton', command = lambda: click(7))
        btn7.grid(row = 3, column = 0, padx = 10, pady = 10)

        btn8 = ttk.Button(arilf, text = '8', style = 'btn.TButton', command = lambda: click(8))
        btn8.grid(row = 3, column = 1, padx = 10, pady = 10)

        btn9 = ttk.Button(arilf, text = '9', style = 'btn.TButton', command = lambda: click(9))
        btn9.grid(row = 3, column = 2, padx = 10, pady = 10)

        btn0 = ttk.Button(arilf, text = '0', style = 'btn.TButton', command = lambda: click(0))
        btn0.grid(row = 6, column = 1, padx = 10, pady = 10)

        btndec = ttk.Button(arilf, text = '.', style = 'btn.TButton', command = lambda: click('.'))
        btndec.grid(row = 6, column = 0, padx = 10, pady = 10)

        btneql = ttk.Button(arilf, text = '=', style = 'btn.TButton', command = lambda: solve())
        btneql.grid(row = 6, column = 2, padx = 10, pady = 10)

        btndiv = ttk.Button(arilf, text = '/', style = 'btn.TButton', command = lambda: click('/'))
        btndiv.grid(row = 3, column = 3, padx = 10, pady = 10)

        btnmult = ttk.Button(arilf, text = '*', style = 'btn.TButton', command = lambda: click('*'))
        btnmult.grid(row = 4, column = 3, padx = 10, pady = 10)

        btnmin = ttk.Button(arilf, text = '-', style = 'btn.TButton', command = lambda: click('-'))
        btnmin.grid(row = 5, column = 3, padx = 10, pady = 10)

        btnplus = ttk.Button(arilf, text = '+', style = 'btn.TButton', command = lambda: click('+'))
        btnplus.grid(row = 6, column = 3, padx = 10, pady = 10)

        btnlbr = ttk.Button(arilf, text = '(', style = 'btn.TButton', command = lambda: click('('))
        btnlbr.grid(row = 1, column = 2, padx = 10, pady = 10)

        btnrbr = ttk.Button(arilf, text = ')', style = 'btn.TButton', command = lambda: click(')'))
        btnrbr.grid(row = 1, column = 3, padx = 10, pady = 10)

        btne = ttk.Button(arilf, text = 'e', style = 'btn.TButton', command = lambda: click(round(evar, prec)))
        btne.grid(row = 2, column = 1, padx = 10, pady = 10)

        btnpi = ttk.Button(arilf, text = '\u03C0', style = 'btn.TButton', command = lambda: click(round(pivar, prec)))
        btnpi.grid(row = 1, column = 0, padx = 10, pady = 10)

        btnexp = ttk.Button(arilf, text = '**', style = 'btn.TButton', command = lambda: click('**'))
        btnexp.grid(row = 2, column = 2, padx = 10, pady = 10)

        btnflrdiv = ttk.Button(arilf, text = '//', style = 'btn.TButton', command = lambda: click('//'))
        btnflrdiv.grid(row = 2, column = 3, padx = 10, pady = 10)

        btnconst = ttk.Button(arilf, text = 'Constants', style = 'btn.TButton', command = lambda: changeConst())
        btnconst.grid(row = 2, column = 0, padx = 10, pady = 10)

        btnphi = ttk.Button(arilf, text = '\u03C6', style = 'btn.TButton', command = lambda: click(round(phivar, prec)))
        btnphi.grid(row = 1, column = 1, padx = 10, pady = 10)

        btnclr = ttk.Button(arilf, text = 'Clear', style = 'btn.TButton', command = lambda: clr()) #Button to clear inputfield
        btnclr.grid(row = 0, column = 3, padx = 10, pady = 10)
        
        modabslf = tk.LabelFrame(self, text = 'Modulus, Absolute and Percentage:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains everything else
        modabslf.grid(row = 1, column = 2, padx = 10, pady = 10)

        modlabel = tk.Label(modabslf, text = 'Modulus:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Modulus Label
        modlabel.grid(row = 0, column = 0, padx = 10, pady = 7.5, sticky = 'w')

        perclabel = tk.Label(modabslf, text = 'Percentage:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Percentage Label
        perclabel.grid(row = 5, column = 0, padx = 10, pady = 7.5, sticky = 'w')

        abslabel = tk.Label(modabslf, text = 'Absolute value:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Absolute Value Label
        abslabel.grid(row = 3, column = 0, padx = 10, pady = 7.5, sticky = 'w')

        modfield1 = tk.Entry(modabslf, font = LargeFont, width = 12, textvariable = mod1var) #This entry field is for dividend in modulus
        modfield1.grid(row = 1, column = 0, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)
        modfield1.bind('<Button-1>', msclick1)

        modfield2 = tk.Entry(modabslf, font = LargeFont, width = 12, textvariable = mod2var) #This entry field is for divisor in modulus
        modfield2.grid(row = 1, column = 1, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)
        modfield2.bind('<Button-1>', msclick2)

        modansfield = tk.Entry(modabslf, font = LargeFont, width = 12, textvariable = modansvar, state = 'readonly') #This entry field is for displaying modulus answer
        modansfield.grid(row = 2, column = 0, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)

        percfield1 = tk.Entry(modabslf, font = LargeFont, width = 12, textvariable = perc1var) #This entry field is for part in percentage
        percfield1.grid(row = 6, column = 0, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)
        percfield1.bind('<Button-1>', msclick4)

        percfield2 = tk.Entry(modabslf, font = LargeFont, width = 12, textvariable = perc2var) #This entry field is for whole in percentage
        percfield2.grid(row = 6, column = 1, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)
        percfield2.bind('<Button-1>', msclick5)

        percansfield = tk.Entry(modabslf, font = LargeFont, width = 12, textvariable = percansvar, state = 'readonly') #This entry field is for displaying percentage answer
        percansfield.grid(row = 7, column = 0, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)

        absfield = tk.Entry(modabslf, font = LargeFont, width = 12, textvariable = absvar) #This entry field is for absolute value
        absfield.grid(row = 4, column = 0, ipadx = 1, padx = 10, ipady = 3, pady = 7.5)
        absfield.bind('<Button-1>', msclick3)

        absansfield = tk.Entry(modabslf, font = LargeFont, width = 12, textvariable = absansvar, state = 'readonly') #This entry field is for displaying absolute answer
        absansfield.grid(row = 4, column = 1, ipadx = 1, padx = 10, ipady = 3, pady = 7.5)

        btnmod = ttk.Button(modabslf, text = 'Modulus', style = 'btn.TButton', command = lambda: modsolve()) #Button for calculating modulus
        btnmod.grid(row = 1, column = 2, padx = 10, pady = 7.5)

        btnabs = ttk.Button(modabslf, text = 'Absolute', style = 'btn.TButton', command = lambda: abssolve()) #Button for calculating absolute value
        btnabs.grid(row = 4, column = 2, padx = 10, pady = 7.5)

        btnperc = ttk.Button(modabslf, text = 'Percentage', style = 'btn.TButton', command = lambda: percsolve()) #Button for calculating percentage
        btnperc.grid(row = 6, column = 2, padx = 10, pady = 7.5)

        btnclr1 = ttk.Button(modabslf, text = 'Clear', style = 'btn.TButton', command = lambda: clrmod()) #Clear buttons
        btnclr1.grid(row = 0, column = 2, padx = 10, pady = 7.5, sticky = 'e')

        btnclr2 = ttk.Button(modabslf, text = 'Clear', style = 'btn.TButton', command = lambda: clrabs())
        btnclr2.grid(row = 3, column = 2, padx = 10, pady = 7.5, sticky = 'e')

        btnclr3 = ttk.Button(modabslf, text = 'Clear', style = 'btn.TButton', command = lambda: clrperc())
        btnclr3.grid(row = 5, column = 2, padx = 10, pady = 7.5, sticky = 'e')

        backbutton = ttk.Button(self, text = 'Back', style = 'btn.TButton', command = lambda: controller.show_frame(ChoicePage)) #This button takes us to the previous page
        backbutton.grid(row = 0, column = 2, padx = 10, sticky = 'e')

        histbutton = ttk.Button(self, text = 'History', style = 'btn.TButton', command = lambda: controller.show_frame(HistPage)) #This button takes us to the history page
        histbutton.grid(row = 0, column = 0, padx = 10, sticky = 'w')

class NumpyPage(tk.Frame): #This class is for Matrices, Trig and Logs page

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831')

        def matAdd(): #This function is for matrix addition
            try:
                global uHist
                global uStatement

                anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                mat1 = mattext1.get('1.0', 'end-1c') #Turn user input into list
                list1 = list(map(float, mat1.split())) 
                i=0
                col1 = int(matcolfield1.get()) #Make nested list divided based on user input of column count
                mat1nl=[]
                while i<len(list1):
                    mat1nl.append(list1[i : i + col1])
                    i += col1
                arr1 = np.array(mat1nl) #Convert nested list into numpy array

                mat2 = mattext2.get('1.0', 'end-1c') #Same but for mattext2
                list2 = list(map(float, mat2.split()))
                j=0
                col2 = int(matcolfield2.get())
                mat1n2=[]
                while j<len(list2):
                    mat1n2.append(list2[j : j + col2])
                    j += col2
                arr2 = np.array(mat1n2)
            
                ans = np.add(arr1, arr2).round(decimals = prec) #Calculate sum
                anslist = ans.tolist() #Display sum in same format as user input
                for i in anslist:
                    istr = ' '.join([str(elem) for elem in i]) 
                    istr = istr + '\n'
                    anstext.insert(tk.END, istr)

                mat3 = anstext.get('1.0', 'end-1c') #Usage history statement
                uStatement = str('The addition of' + '\n' + mat1 + '\n' + 'and' + '\n' + mat2 + '\n' + 'is' + '\n' + mat3)
                uHist.append(uStatement)
            except:
                anstext.delete('1.0', 'end')
                anstext.insert(tk.END, "ERROR")

        def matSub(): #This function is for matrix subtraction
            try:
                global uHist
                global uStatement

                anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                mat1 = mattext1.get('1.0', 'end-1c') #Turn user input into list
                list1 = list(map(float, mat1.split())) 
                i=0
                col1 = int(matcolfield1.get()) #Make nested list divided based on user input of column count
                mat1nl=[]
                while i<len(list1):
                    mat1nl.append(list1[i : i + col1])
                    i += col1
                arr1 = np.array(mat1nl) #Convert nested list into numpy array

                mat2 = mattext2.get('1.0', 'end-1c') #Same but for mattext2
                list2 = list(map(float, mat2.split()))
                j=0
                col2 = int(matcolfield2.get())
                mat1n2=[]
                while j<len(list2):
                    mat1n2.append(list2[j : j + col2])
                    j += col2
                arr2 = np.array(mat1n2)
            
                ans = np.subtract(arr1, arr2).round(decimals = prec) #Calculate difference
                anslist = ans.tolist() #Display difference in same format as user input
                for i in anslist:
                    istr = ' '.join([str(elem) for elem in i]) 
                    istr = istr + '\n'
                    anstext.insert(tk.END, istr)

                mat3 = anstext.get('1.0', 'end-1c') #Usage history statement
                uStatement = str('The difference between' + '\n' + mat1 + '\n' + 'and' + '\n' + mat2 + '\n' + 'is' + '\n' + mat3)
                uHist.append(uStatement)
            except:
                anstext.delete('1.0', 'end')
                anstext.insert(tk.END, "ERROR")

        def matMul(): #This function is for matrix multiplication
            try:
                global uHist
                global uStatement

                anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                mat1 = mattext1.get('1.0', 'end-1c') #Turn user input into list
                list1 = list(map(float, mat1.split())) 
                i=0
                col1 = int(matcolfield1.get()) #Make nested list divided based on user input of column count
                mat1nl=[]
                while i<len(list1):
                    mat1nl.append(list1[i : i + col1])
                    i += col1
                arr1 = np.array(mat1nl) #Convert nested list into numpy array

                mat2 = mattext2.get('1.0', 'end-1c') #Same but for mattext2
                list2 = list(map(float, mat2.split()))
                j=0
                col2 = int(matcolfield2.get())
                mat1n2=[]
                while j<len(list2):
                    mat1n2.append(list2[j : j + col2])
                    j += col2
                arr2 = np.array(mat1n2)
            
                ans = np.dot(arr1, arr2).round(decimals = prec) #Calculate product
                anslist = ans.tolist() #Display product in same format as user input
                for i in anslist:
                    istr = ' '.join([str(elem) for elem in i]) 
                    istr = istr + '\n'
                    anstext.insert(tk.END, istr)

                mat3 = anstext.get('1.0', 'end-1c') #Usage history statement
                uStatement = str('The product of' + '\n' + mat1 + '\n' + 'and' + '\n' + mat2 + '\n' + 'is' + '\n' + mat3)
                uHist.append(uStatement)
            except:
                anstext.delete('1.0', 'end')
                anstext.insert(tk.END, "ERROR")       

        def matDiv(): #This function is for matrix division
            try:
                global uHist
                global uStatement
                
                if matdivfield.get() != 'Divisor' or '': #This is for dividing matrix by user inputted number
                    anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                    mat1 = mattext3.get('1.0', 'end-1c') #Turn user input into list
                    list1 = list(map(float, mat1.split())) 
                    i=0
                    col1 = int(matcolfield3.get()) #Make nested list divided based on user input of column count
                    mat1nl=[]
                    while i<len(list1):
                        mat1nl.append(list1[i : i + col1])
                        i += col1
                    arr1 = np.array(mat1nl) #Convert nested list into numpy array

                    div = float(matdivfield.get()) #Gets divisor in float form
                
                    ans = np.divide(arr1, div).round(decimals = prec) #Calculate division
                    anslist = ans.tolist() #Display division in same format as user input
                    for i in anslist:
                        istr = ' '.join([str(elem) for elem in i]) 
                        istr = istr + '\n'
                        anstext.insert(tk.END, istr)

                    mat3 = anstext.get('1.0', 'end-1c') #Usage history statement
                    uStatement = str('The division of' + '\n' + mat1 + '\n' + 'and' + '\n' + str(div) + '\n' + 'is' + '\n' + mat3)
                    uHist.append(uStatement)
                
                elif matdivfield.get() == 'Divisor' or '': #This is for dividing matrices by each-other
                    anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                    mat1 = mattext1.get('1.0', 'end-1c') #Turn user input into list
                    list1 = list(map(float, mat1.split())) 
                    i=0
                    col1 = int(matcolfield1.get()) #Make nested list divided based on user input of column count
                    mat1nl=[]
                    while i<len(list1):
                        mat1nl.append(list1[i : i + col1])
                        i += col1
                    arr1 = np.array(mat1nl) #Convert nested list into numpy array

                    mat2 = mattext2.get('1.0', 'end-1c') #Same but for mattext2
                    list2 = list(map(float, mat2.split()))
                    j=0
                    col2 = int(matcolfield2.get())
                    mat1n2=[]
                    while j<len(list2):
                        mat1n2.append(list2[j : j + col2])
                        j += col2
                    arr2 = np.array(mat1n2)
                
                    ans = np.divide(arr1, arr2).round(decimals = prec) #Calculate division
                    anslist = ans.tolist() #Display division in same format as user input
                    for i in anslist:
                        istr = ' '.join([str(elem) for elem in i]) 
                        istr = istr + '\n'
                        anstext.insert(tk.END, istr)

                    mat3 = anstext.get('1.0', 'end-1c') #Usage history statement
                    uStatement = str('The division of' + '\n' + mat1 + '\n' + 'and' + '\n' + mat2 + '\n' + 'is' + '\n' + mat3)
                    uHist.append(uStatement)
            except:
                anstext.delete('1.0', 'end')
                anstext.insert(tk.END, "ERROR")

        def matInv(): #This function is for matrix inverse
            try:
                global uHist
                global uStatement

                anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                mat1 = mattext3.get('1.0', 'end-1c') #Turn user input into list
                list1 = list(map(float, mat1.split())) 
                i=0
                col1 = int(matcolfield3.get()) #Make nested list divided based on user input of column count
                mat1nl=[]
                while i<len(list1):
                    mat1nl.append(list1[i : i + col1])
                    i += col1
                arr1 = np.array(mat1nl) #Convert nested list into numpy array

                ans = np.linalg.inv(arr1).round(decimals = prec) #Calculate inverse
                anslist = ans.tolist() #Display inverse in same format as user input
                for i in anslist:
                    istr = ' '.join([str(elem) for elem in i]) 
                    istr = istr + '\n'
                    anstext.insert(tk.END, istr)

                mat2 = anstext.get('1.0', 'end-1c') #Usage history statement
                uStatement = str('The inverse of' + '\n' + mat1 + '\n' + 'is' + '\n' + mat2)
                uHist.append(uStatement)
            except:
                anstext.delete('1.0', 'end')
                anstext.insert(tk.END, "ERROR")      

        def matTrace(): #This function is for matrix trace
            try:
                global uHist
                global uStatement

                anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                mat1 = mattext3.get('1.0', 'end-1c') #Turn user input into list
                list1 = list(map(float, mat1.split())) 
                i=0
                col1 = int(matcolfield3.get()) #Make nested list divided based on user input of column count
                mat1nl=[]
                while i<len(list1):
                    mat1nl.append(list1[i : i + col1])
                    i += col1
                arr1 = np.array(mat1nl) #Convert nested list into numpy array
            
                ans = round(np.trace(arr1), prec) #Calculate trace
                anstext.insert(tk.END, ans)

                mat2 = anstext.get('1.0', 'end-1c') #Usage history statement
                uStatement = str('The trace of' + '\n' + mat1 + '\n' + 'is' + '\n' + mat2 + '\n')
                uHist.append(uStatement)
            except:
                anstext.delete('1.0', 'end')
                anstext.insert(tk.END, "ERROR")       

        def matDet(): #This function is for matrix determinant
            try:
                global uHist
                global uStatement

                anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                mat1 = mattext3.get('1.0', 'end-1c') #Turn user input into list
                list1 = list(map(float, mat1.split())) 
                i=0
                col1 = int(matcolfield3.get()) #Make nested list divided based on user input of column count
                mat1nl=[]
                while i<len(list1):
                    mat1nl.append(list1[i : i + col1])
                    i += col1
                arr1 = np.array(mat1nl) #Convert nested list into numpy array
            
                ans = round(np.linalg.det(arr1), prec) #Calculate determinant
                anstext.insert(tk.END, ans) 

                mat2 = anstext.get('1.0', 'end-1c') #Usage history statement
                uStatement = str('The determinant of' + '\n' + mat1 + '\n' + 'is' + '\n' + mat2 + '\n')
                uHist.append(uStatement)
            except:
                anstext.delete('1.0', 'end')
                anstext.insert(tk.END, "ERROR")       

        def matTrans(): #This function is for matrix transpose
            try:
                global uHist
                global uStatement

                anstext.delete('1.0', 'end') #Remove existing quantity in anstext

                mat1 = mattext3.get('1.0', 'end-1c') #Turn user input into list
                list1 = list(map(float, mat1.split())) 
                i=0
                col1 = int(matcolfield3.get()) #Make nested list divided based on user input of column count
                mat1nl=[]
                while i<len(list1):
                    mat1nl.append(list1[i : i + col1])
                    i += col1
                arr1 = np.array(mat1nl) #Convert nested list into numpy array

                ans = np.transpose(arr1) #Calculate inverse
                anslist = ans.tolist() #Display inverse in same format as user input
                for i in anslist:
                    istr = ' '.join([str(elem) for elem in i]) 
                    istr = istr + '\n'
                    anstext.insert(tk.END, istr)

                mat2 = anstext.get('1.0', 'end-1c') #Usage history statement
                uStatement = str('The transpose of' + '\n' + mat1 + '\n' + 'is' + '\n' + mat2)
                uHist.append(uStatement)
            except:
                anstext.delete('1.0', 'end')
                anstext.insert(tk.END, "ERROR")       

        def reset(): #This is to program reset button
            matcolfield1.delete(0, 'end')
            mat1var.set('Enter Columns')
            
            matcolfield2.delete(0, 'end')
            mat2var.set('Enter Columns')
            
            matcolfield3.delete(0, 'end')
            mat3var.set('Columns')

            matdivfield.delete(0, 'end')
            matdivvar.set('Divisor')

            mattext1.delete('1.0', 'end')
            mattext2.delete('1.0', 'end')
            mattext3.delete('1.0', 'end')
            anstext.delete('1.0', 'end')

        def trigSin(): #This function is for calculating sin
            try:
                global uHist
                global uStatement

                trigval = str(trigfield.get()) #Acquires trigfield input as string to accomodate fraction inputs
                trigfinal = float(eval(trigval)) #Evaluates fraction input and converts it to float for math module
                
                choice = radiovar.get()
                if choice == 1:
                    trigdeg = round(math.radians(trigfinal), prec)
                    ans = str(round(math.sin(trigdeg), prec)) #Calculates sin rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Sin of ' + trigval + ' degrees is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)                
                elif choice == 2:
                    ans = str(round(math.sin(trigfinal), prec)) #Calculates sin rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Sin of ' + trigval + ' radians is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)

                trigvar.set(ans) #Display answer
            except:
                trigvar.set('ERROR')

        def trigCos(): #This function is for calculating cos
            try:
                global uHist
                global uStatement

                trigval = str(trigfield.get()) #Acquires trigfield input as string to accomodate fraction inputs
                trigfinal = float(eval(trigval)) #Evaluates fraction input and converts it to float for math module

                choice = radiovar.get()
                if choice == 1:
                    trigdeg = round(math.radians(trigfinal), prec)
                    ans = str(round(math.cos(trigdeg), prec)) #Calculates cos rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Cos of ' + trigval + ' degrees is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)                
                elif choice == 2:
                    ans = str(round(math.cos(trigfinal), prec)) #Calculates cos rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Cos of ' + trigval + ' radians is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)

                trigvar.set(ans) #Display answer
            except:
                trigvar.set('ERROR')

        def trigTan(): #This function is for calculating tan
            try:
                global uHist
                global uStatement

                trigval = str(trigfield.get()) #Acquires trigfield input as string to accomodate fraction inputs
                trigfinal = float(eval(trigval)) #Evaluates fraction input and converts it to float for math module

                choice = radiovar.get()
                if choice == 1:
                    trigdeg = round(math.radians(trigfinal), prec)
                    ans = str(round(math.tan(trigdeg), prec)) #Calculates tan rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Tan of ' + trigval + ' degrees is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)                
                elif choice == 2:
                    ans = str(round(math.tan(trigfinal), prec)) #Calculates tan rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Tan of ' + trigval + ' radians is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)

                trigvar.set(ans) #Display answer
            except:
                trigvar.set('ERROR')

        def trigArcsin(): #This function is for calculating arcsin
            try:
                global uHist
                global uStatement

                trigval = str(trigfield.get()) #Acquires trigfield input as string to accomodate fraction inputs
                trigfinal = float(eval(trigval)) #Evaluates fraction input and converts it to float for math module
                
                choice = radiovar.get()
                if choice == 1:
                    trigdeg = round(math.radians(trigfinal), prec)
                    ans = str(round(math.asin(trigdeg), prec)) #Calculates arcsin rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Arcsin of ' + trigval + ' degrees is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)                
                elif choice == 2:
                    ans = str(round(math.asin(trigfinal), prec)) #Calculates arcsin rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Arcsin of ' + trigval + ' radians is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)

                trigvar.set(ans) #Display answer
            except:
                trigvar.set('ERROR')

        def trigArccos(): #This function is for calculating arccos
            try:
                global uHist
                global uStatement

                trigval = str(trigfield.get()) #Acquires trigvar input as string to accomodate fraction inputs
                trigfinal = float(eval(trigval)) #Evaluates fraction input and converts it to float for math module

                choice = radiovar.get()
                if choice == 1:
                    trigdeg = round(math.radians(trigfinal), prec)
                    ans = str(round(math.acos(trigdeg), prec)) #Calculates cos rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Arccos of ' + trigval + ' degrees is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)                
                elif choice == 2:
                    ans = str(round(math.acos(trigfinal), prec)) #Calculates cos rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Arccos of ' + trigval + ' radians is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)

                trigvar.set(ans) #Display answer
            except:
                trigvar.set('ERROR')

        def trigArctan(): #This function is for calculating arctan
            try:
                global uHist
                global uStatement

                trigval = str(trigfield.get()) #Acquires trigvar input as string to accomodate fraction inputs
                trigfinal = float(eval(trigval)) #Evaluates fraction input and converts it to float for math module

                choice = radiovar.get()
                if choice == 1:
                    trigdeg = round(math.radians(trigfinal), prec)
                    ans = str(round(math.atan(trigdeg), prec)) #Calculates arctan rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Arctan of ' + trigval + ' degrees is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)                
                elif choice == 2:
                    ans = str(round(math.atan(trigfinal), prec)) #Calculates arctan rounded to 2 places, converts it to string for entry widget
                    uStatement = str('Arctan of ' + trigval + ' radians is ' + ans + '\n') #Usage history statement
                    uHist.append(uStatement)

                trigvar.set(ans) #Display answer
            except:
                trigvar.set('ERROR')

        def clrTrig(): #This is to program trig clear button
            trigfield.delete(0, 'end')
            trigvar.set('Enter Angle')

        def loge(): #This function is for calculating natural log
            try:
                global uHist
                global uStatement

                logval = str(logfield.get())#Acquires logfield input as string to accomodate fraction inputs
                logfinal = float(eval(logval)) #Evaluates fraction input and converts it to float for math module

                ans = str(round(math.log(logfinal), prec)) #Calculates ln , converts it to string for entry widget
                uStatement = str('Natural log of ' + logval + ' is ' + ans + '\n') #Usage history statement
                uHist.append(uStatement)
                logvar.set(ans) #Display answer
            except:
                logvar.set('ERROR')

        def logx(): #This function is for calculating log base x
            try:
                global uHist
                global uStatement

                logval = str(logfield.get()) #Acquires logfield input as string to accomodate fraction inputs
                base = float(logbasefield.get()) #Acquires logbasefield input for custom base
                logfinal = float(eval(logval)) #Evaluates fraction input and converts it to float for math module

                ans = str(round(math.log(logfinal, base), prec)) #Calculates log base x , converts it to string for entry widget
                uStatement = str('Log base ' + str(base) + ' of ' + logval + ' is ' + ans + '\n') #Usage history statement
                uHist.append(uStatement)
                logvar.set(ans) #Display answer
            except:
                logvar.set('ERROR')
                logbasevar.set('ERROR')

        def antilog(): #This function is for calculating natural log
            try:
                global uHist
                global uStatement

                logval = str(logfield.get())#Acquires logfield input as string to accomodate fraction inputs
                logfinal = float(eval(logval)) #Evaluates fraction input and converts it to float for math module

                ans = str(round(np.exp(logfinal), prec)) #Calculates antilog base e rounded to 2 places, converts it to string for entry widget
                uStatement = str('Antilog of ' + logval + ' is ' + ans + '\n') #Usage history statement
                uHist.append(uStatement)
                logvar.set(ans) #Display answer
            except:
                logvar.set('ERROR')

        def clrLog(): #This is to program log clear button
            logfield.delete(0, 'end')
            logvar.set('Enter Value')
            logbasefield.delete(0, 'end')
            logbasevar.set('Enter Base')            

        def msclick1(event): #This function is to empty matcolfield1 upon mouse click
            matcolfield1.delete(0, 'end')
            return None

        def msclick2(event): #Above function for matcolfield2
            matcolfield2.delete(0, 'end')
            return None

        def msclick3(event): #Above function for mattext1
            mattext1.delete('1.0', 'end')
            return None

        def msclick4(event): #Above function for mattext2
            mattext2.delete('1.0', 'end')
            return None

        def msclick5(event): #Above function for mattext3
            mattext3.delete('1.0', 'end')
            return None

        def msclick6(event): #Above function for matcolfield3
            matcolfield3.delete(0, 'end')
            return None

        def msclick7(event): #Above function for matdivfield
            matdivfield.delete(0, 'end')
            return None

        def msclick8(event): #Above function for trigfield
            trigfield.delete(0, 'end')
            return None

        def msclick9(event): #Above function for logfield
            logfield.delete(0, 'end')
            return None

        def msclick10(event): #Above function for logbasefield
            logbasefield.delete(0, 'end')
            return None

        mat1var = tk.StringVar() #These variables are the text variables for all the Entry fields
        mat1var.set('Enter Columns')
        mat2var = tk.StringVar()
        mat2var.set('Enter Columns')
        mat3var = tk.StringVar()
        mat3var.set('Columns')
        matdivvar = tk.StringVar()
        matdivvar.set('Divisor')
        trigvar = tk.StringVar()
        trigvar.set('Enter Angle')
        logvar = tk.StringVar()
        logvar.set('Enter Value')
        logbasevar = tk.StringVar()
        logbasevar.set('Enter Base')
        radiovar = tk.IntVar()
        radiovar.set(1)

        label1 = tk.Label(self, text = 'Matrices, Logs', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title label
        label1.grid(row = 0, column = 1, padx = 0, pady = 0)

        label2 = tk.Label(self, text = ' & Trigonometry', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title label
        label2.grid(row = 1, column = 1, padx = 0, pady = 0, sticky = 'n')

        backbutton = ttk.Button(self, text = 'Back', style = 'btn.TButton', command = lambda: controller.show_frame(ChoicePage)) #This button takes us to the previous page
        backbutton.grid(row = 0, column = 2, padx = 10, pady = 20, sticky = 'e')

        histbutton = ttk.Button(self, text = 'History', style = 'btn.TButton', command = lambda: controller.show_frame(HistPage)) #This button takes us to the usage history page
        histbutton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')

        matopslf = tk.LabelFrame(self, text = 'Matrix Operations:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains all the stuff to be used for numpy matrices
        matopslf.grid(row = 1, column = 0, padx = 10, pady = 10)

        mat1label = tk.Label(matopslf, text = 'Matrix 1:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Matrix 1 label
        mat1label.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'w')

        mat2label = tk.Label(matopslf, text = 'Matrix 2:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Matrix 2 label
        mat2label.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'w')

        mat3label = tk.Label(matopslf, text = 'Other ops:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Matrix 3 label
        mat3label.grid(row = 0, column = 2, padx = 10, pady = 5, sticky = 'w')

        mat4label = tk.Label(matopslf, text = 'Answers:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Answer matrix label
        mat4label.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = 'w')

        matcolfield1 = tk.Entry(matopslf, font = LargeFont, width = 12, textvariable = mat1var) #This field takes number of columns of matrix 1 for splitting into nested list
        matcolfield1.grid(row = 1, column = 0, ipadx = 0.1, ipady = 3, padx = 5, pady = 7.5)
        matcolfield1.bind('<Button-1>', msclick1)

        matcolfield2 = tk.Entry(matopslf, font = LargeFont, width = 12, textvariable = mat2var) #This field takes number of columns of matrix 2 for splitting into nested list
        matcolfield2.grid(row = 1, column = 1, ipadx = 0.1, ipady = 3, padx = 5, pady = 7.5)
        matcolfield2.bind('<Button-1>', msclick2)

        matcolfield3 = tk.Entry(matopslf, width = 8, textvariable = mat3var) #This field takes divisor for division
        matcolfield3.grid(row = 1, column = 2, ipadx = 0.1, ipady = 5, padx = 10, pady = 7.5, sticky = 'w')
        matcolfield3.bind('<Button-1>', msclick6)

        matdivfield = tk.Entry(matopslf, width = 8, textvariable = matdivvar) #This field takes divisor for division
        matdivfield.grid(row = 1, column = 2, ipadx = 0.1, ipady = 5, padx = 10, pady = 7.5, sticky = 'e')
        matdivfield.bind('<Button-1>', msclick7)

        mattext1 = tk.Text(matopslf, font = LargeFont, height = 7, width = 12) #This field takes input for matrix 1
        mattext1.grid(row = 2, column = 0, padx = 5, pady = 10)
        mattext1.bind('<Button-1>', msclick3)

        mattext2 = tk.Text(matopslf, font = LargeFont, height = 7, width = 12) #This field takes input for matrix 2
        mattext2.grid(row = 2, column = 1, padx = 5, pady = 10)
        mattext2.bind('<Button-1>', msclick4)

        mattext3 = tk.Text(matopslf, font = LargeFont, height = 7, width = 12) #This field takes input for matrix 3
        mattext3.grid(row = 2, column = 2, padx = 5, pady = 10)
        mattext3.bind('<Button-1>', msclick5)

        anstext = tk.Text(matopslf, font = LargeFont, height = 7, width = 12) #This field displays answer matrix
        anstext.grid(row = 2, column = 3, padx = 5, pady = 10)

        btnmatadd = ttk.Button(matopslf, text = 'Add', style = 'btn.TButton', command = lambda: matAdd()) #These buttons are for the different matrix operations
        btnmatadd.grid(row = 3, column = 0, padx = 10, pady = 10)

        btnmatsub = ttk.Button(matopslf, text = 'Subtract', style = 'btn.TButton', command = lambda: matSub()) 
        btnmatsub.grid(row = 3, column = 1, padx = 10, pady = 10)

        btnmatmul = ttk.Button(matopslf, text = 'Multiply', style = 'btn.TButton', command = lambda: matMul()) 
        btnmatmul.grid(row = 4, column = 0, padx = 10, pady = 10)

        btnmatdiv = ttk.Button(matopslf, text = 'Divide', style = 'btn.TButton', command = lambda: matDiv()) 
        btnmatdiv.grid(row = 4, column = 1, padx = 10, pady = 10)

        btninv = ttk.Button(matopslf, text = 'Inverse', style = 'btn.TButton', command = lambda: matInv()) 
        btninv.grid(row = 4, column = 2, padx = 10, pady = 10)

        btntrace = ttk.Button(matopslf, text = 'Trace', style = 'btn.TButton', command = lambda: matTrace()) 
        btntrace.grid(row = 3, column = 2, padx = 10, pady = 10)

        btndet = ttk.Button(matopslf, text = 'Determinant', style = 'btn.TButton', command = lambda: matDet()) 
        btndet.grid(row = 3, column = 3, padx = 10, pady = 10)

        btntranspose = ttk.Button(matopslf, text = 'Transpose', style = 'btn.TButton', command = lambda: matTrans()) 
        btntranspose.grid(row = 4, column = 3, padx = 10, pady = 10)

        resetbtn = ttk.Button(matopslf, text = 'Reset', style = 'btn.TButton', command = lambda: reset()) #This button resets all the fields in matrix label frame
        resetbtn.grid(row = 1, column = 3, padx = 10, pady = 10)

        otheropslf = tk.LabelFrame(self, text = 'Trigonometry and Logarithms:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains everything for trig and logs
        otheropslf.grid(row = 1, column = 2, padx = 10, pady = 10)

        triglabel = tk.Label(otheropslf, text = 'Trigonometry:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Algebra Label
        triglabel.grid(row = 0, column = 0, padx = 2, pady = 10)

        trigfield = tk.Entry(otheropslf, width = 21, font = LargeFont, textvariable = trigvar) #This field takes input for trigonometric operation
        trigfield.grid(row = 1, column = 0, columnspan = 2, ipadx = 0.1, ipady = 3, padx = 2, pady = 7.5)
        trigfield.bind('<Button-1>', msclick8)

        clrtrigbutton = ttk.Button(otheropslf, text = 'Clear', style = 'btn.TButton', command = lambda: clrTrig()) #This button clears trigfield
        clrtrigbutton.grid(row = 1, column = 2, padx = 2, pady = 10)

        s = ttk.Style()
        s.theme_use('alt')
        s.configure('btn.TRadiobutton', font = ('Arial', 12, 'bold'), foreground = '#00adb5', background = '#222831', indicatorrelief = tk.FLAT, indicatormargin =- 1, indicatordiameter =- 1, relief = tk.RAISED, focusthickness = 0, highlightthickness = 0, padding = 5)
        s.map('btn.TRadiobutton', background=[('selected', '#222831'), ('active', '#222831')])

        degradio = ttk.Radiobutton(otheropslf, text = 'Degree', style = 'btn.TRadiobutton', variable = radiovar, value = 1)
        degradio.grid(row = 0, column = 1, padx = 2, pady = 10)

        radradio = ttk.Radiobutton(otheropslf, text = 'Radian', style = 'btn.TRadiobutton', variable = radiovar, value = 2)
        radradio.grid(row = 0, column = 2, padx = 2, pady = 10)

        btnsin = ttk.Button(otheropslf, text = 'Sin', style = 'btn.TButton', command = lambda: trigSin()) #These buttons are for different trig operations
        btnsin.grid(row = 2, column = 0, padx = 0, pady = 10)           

        btncos = ttk.Button(otheropslf, text = 'Cos', style = 'btn.TButton', command = lambda: trigCos())
        btncos.grid(row = 2, column = 1, padx = 0, pady = 10)

        btntan = ttk.Button(otheropslf, text = 'Tan', style = 'btn.TButton', command = lambda: trigTan())
        btntan.grid(row = 2, column = 2, padx = 7, pady = 10)

        btnarcsin = ttk.Button(otheropslf, text = 'Sin (-1)', style = 'btn.TButton', command = lambda: trigArcsin())
        btnarcsin.grid(row = 3, column = 0, padx = 0, pady = 10)           

        btnarccos = ttk.Button(otheropslf, text = 'Cos (-1)', style = 'btn.TButton', command = lambda: trigArccos())
        btnarccos.grid(row = 3, column = 1, padx = 0, pady = 10)

        btnarctan = ttk.Button(otheropslf, text = 'Tan (-1)', style = 'btn.TButton', command = lambda: trigArctan())
        btnarctan.grid(row = 3, column = 2, padx = 7, pady = 10)

        loglabel = tk.Label(otheropslf, text = 'Logarithms:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Log Label
        loglabel.grid(row = 4, column = 0, padx = 2, pady = 7.5)

        logfield = tk.Entry(otheropslf, width = 10, font = LargeFont, textvariable = logvar) #This field takes input for logarithmic operation
        logfield.grid(row = 5, column = 0, ipadx = 0.1, ipady = 3, padx = 2, pady = 7.5)
        logfield.bind('<Button-1>', msclick9)

        logbasefield = tk.Entry(otheropslf, width = 10, font = LargeFont, textvariable = logbasevar) #This field takes custom base for logarithmic operation
        logbasefield.grid(row = 5, column = 1, ipadx = 0.1, ipady = 3, padx = 2, pady = 7.5)
        logbasefield.bind('<Button-1>', msclick10)

        clrlogbutton = ttk.Button(otheropslf, text = 'Clear', style = 'btn.TButton', command = lambda: clrLog()) #This button clears logfield and logbasefield
        clrlogbutton.grid(row = 5, column = 2, padx = 2, pady = 7.5)

        btnlog = ttk.Button(otheropslf, text = 'Log (e)', style = 'btn.TButton', command = lambda: loge()) #These buttons are for different log operations
        btnlog.grid(row = 6, column = 0, padx = 0, pady = 10)           

        btnlog10 = ttk.Button(otheropslf, text = 'Log (x)', style = 'btn.TButton', command = lambda: logx())
        btnlog10.grid(row = 6, column = 1, padx = 0, pady = 10)

        btnantilog = ttk.Button(otheropslf, text = 'Antilog', style = 'btn.TButton', command = lambda: antilog())
        btnantilog.grid(row = 6, column = 2, padx = 7, pady = 10)

class MatPlotLibPage(tk.Frame): #This class is for Graph page

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831')

        def plotLG(): #This function is for plotting line graph
            try:
                global uHist
                global uStatement                

                X = graphtext1.get('1.0', 'end-1c') #Turn user input into list
                Xlist = list(map(float, X.split()))                
                Xlist = [round(i, prec) for i in Xlist]

                Y = graphtext2.get('1.0', 'end-1c') #Turn user input into list
                Ylist = list(map(float, Y.split()))
                Ylist = [round(i, prec) for i in Ylist]

                XTick = graphtext5.get('1.0', 'end-1c') #Turn user input into list
                XTicklist = list(map(float, XTick.split()))                
                XTicklist = [round(i, prec) for i in XTicklist]

                YTick = graphtext6.get('1.0', 'end-1c') #Turn user input into list
                YTicklist = list(map(float, YTick.split()))                
                YTicklist = [round(i, prec) for i in YTicklist]

                XLbl = graphtext7.get('1.0', 'end-1c') #Takes X Axis label from user                

                YLbl = graphtext8.get('1.0', 'end-1c') #Takes Y Axis label from user  

                GraphTitle = graphtext9.get('1.0', 'end-1c') #Takes graph title from user                            

                f = Figure(figsize = (6.93, 3.3), dpi = 100) #Defines graph dimensions
                a = f.add_subplot(111)
                a.set_xticks(XTicklist)
                a.set_xticklabels(XTicklist)
                a.set_yticks(YTicklist)
                a.set_yticklabels(YTicklist)
                a.set_xlabel(XLbl)
                a.set_ylabel(YLbl)
                a.set_title(GraphTitle)
                a.plot(Xlist, Ylist, color = '#00adb5') #Plots the graph
                
                a.set_facecolor('#222831') #Graph colours
                f.patch.set_facecolor('#222831')
                a.tick_params(axis='x', colors='#00adb5', which = 'both')
                a.tick_params(axis='y', colors='#00adb5', which = 'both')
                a.spines['bottom'].set_color('#eeeeee')
                a.spines['left'].set_color('#eeeeee')
                a.xaxis.label.set_color('#00adb5')
                a.xaxis.set_label_coords(0.5, -0.087)
                a.yaxis.label.set_color('#00adb5')
                a.title.set_color('#00adb5')
                a.spines['top'].set_visible(False) #Hides top and right axis
                a.spines['right'].set_visible(False)

                uStatement = str('You plotted a line graph with coordinates ' + X + ', ' + Y + '\n') #Usage history statement
                uHist.append(uStatement)

                canvas = FigureCanvasTkAgg(f, plotlf) #Draws graph for viewing
                canvas.draw()
                canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)
            except:
                graphtext1.delete('1.0', 'end')
                graphtext1.insert(tk.END, 'ERROR')
                graphtext2.delete('1.0', 'end')
                graphtext2.insert(tk.END, 'ERROR')                

        def plotBG(): #This function is for plotting bar graph
            try:
                global uHist
                global uStatement                
                
                X = graphtext1.get('1.0', 'end-1c') #Turn user input into list
                Xlist = list(map(float, X.split()))                
                Xlist = [round(i, prec) for i in Xlist]

                Y = graphtext2.get('1.0', 'end-1c') #Turn user input into list
                Ylist = list(map(float, Y.split()))
                Ylist = [round(i, prec) for i in Ylist]

                XTick = graphtext5.get('1.0', 'end-1c') #Turn user input into list
                XTicklist = list(map(float, XTick.split()))                
                XTicklist = [round(i, prec) for i in XTicklist]

                YTick = graphtext6.get('1.0', 'end-1c') #Turn user input into list
                YTicklist = list(map(float, YTick.split()))                
                YTicklist = [round(i, prec) for i in YTicklist]

                XLbl = graphtext7.get('1.0', 'end-1c') #Takes X Axis label from user                

                YLbl = graphtext8.get('1.0', 'end-1c') #Takes Y Axis label from user                              

                GraphTitle = graphtext9.get('1.0', 'end-1c') #Takes graph title from user 

                f = Figure(figsize = (6.93, 3.3), dpi = 100) #Defines graph dimensions
                a = f.add_subplot(111)
                a.set_xticks(XTicklist)
                a.set_xticklabels(XTicklist)
                a.set_yticks(YTicklist)
                a.set_yticklabels(YTicklist)
                a.set_xlabel(XLbl)
                a.set_ylabel(YLbl)
                a.set_title(GraphTitle)
                a.bar(Xlist, Ylist, color = '#00adb5') #Plots the graph
                
                a.set_facecolor('#222831') #Graph colours
                f.patch.set_facecolor('#222831')
                a.tick_params(axis='x', colors='#00adb5', which = 'both')
                a.tick_params(axis='y', colors='#00adb5', which = 'both')
                a.spines['bottom'].set_color('#eeeeee')
                a.spines['left'].set_color('#eeeeee')
                a.xaxis.label.set_color('#00adb5')
                a.xaxis.set_label_coords(0.5, -0.087)
                a.yaxis.label.set_color('#00adb5')
                a.title.set_color('#00adb5')
                a.spines['top'].set_visible(False) #Hides top and right axis
                a.spines['right'].set_visible(False)

                uStatement = str('You plotted a bar graph with coordinates ' + X + ', ' + Y + '\n') #Usage history statement
                uHist.append(uStatement)

                canvas = FigureCanvasTkAgg(f, plotlf) #Draws graph for viewing
                canvas.draw()
                canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)
            except:
                graphtext1.delete('1.0', 'end')
                graphtext1.insert(tk.END, 'ERROR')
                graphtext2.delete('1.0', 'end')
                graphtext2.insert(tk.END, 'ERROR')

        def plotSC(): #This function is for plotting scatter plot                
            try:
                global uHist
                global uStatement

                X = graphtext1.get('1.0', 'end-1c') #Turn user input into list
                Xlist = list(map(float, X.split()))                
                Xlist = [round(i, prec) for i in Xlist]

                Y = graphtext2.get('1.0', 'end-1c') #Turn user input into list
                Ylist = list(map(float, Y.split()))
                Ylist = [round(i, prec) for i in Ylist]

                XTick = graphtext5.get('1.0', 'end-1c') #Turn user input into list
                XTicklist = list(map(float, XTick.split()))                
                XTicklist = [round(i, prec) for i in XTicklist]

                YTick = graphtext6.get('1.0', 'end-1c') #Turn user input into list
                YTicklist = list(map(float, YTick.split()))                
                YTicklist = [round(i, prec) for i in YTicklist]

                XLbl = graphtext7.get('1.0', 'end-1c') #Takes X Axis label from user                

                YLbl = graphtext8.get('1.0', 'end-1c') #Takes Y Axis label from user                              

                GraphTitle = graphtext9.get('1.0', 'end-1c') #Takes graph title from user 

                f = Figure(figsize = (6.93, 3.3), dpi = 100) #Defines graph dimensions
                a = f.add_subplot(111)
                a.set_xticks(XTicklist)
                a.set_xticklabels(XTicklist)
                a.set_yticks(YTicklist)
                a.set_yticklabels(YTicklist)
                a.set_xlabel(XLbl)
                a.set_ylabel(YLbl)
                a.set_title(GraphTitle)
                a.scatter(Xlist, Ylist, color = '#00adb5') #Plots the graph
                
                a.set_facecolor('#222831') #Graph colours
                f.patch.set_facecolor('#222831')
                a.tick_params(axis='x', colors='#00adb5', which = 'both')
                a.tick_params(axis='y', colors='#00adb5', which = 'both')
                a.spines['bottom'].set_color('#eeeeee')
                a.spines['left'].set_color('#eeeeee')
                a.xaxis.label.set_color('#00adb5')
                a.xaxis.set_label_coords(0.5, -0.087)
                a.yaxis.label.set_color('#00adb5')
                a.title.set_color('#00adb5')
                a.spines['top'].set_visible(False) #Hides top and right axis
                a.spines['right'].set_visible(False)

                uStatement = str('You plotted a scatter plot with coordinates ' + X + ', ' + Y + '\n') #Usage history statement
                uHist.append(uStatement)

                canvas = FigureCanvasTkAgg(f, plotlf) #Draws graph for viewing
                canvas.draw()
                canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)
            except:
                graphtext1.delete('1.0', 'end')
                graphtext1.insert(tk.END, 'ERROR')
                graphtext2.delete('1.0', 'end')
                graphtext2.insert(tk.END, 'ERROR')

        def plotHG(): #This function is for plotting histogram             
            try:
                global uHist
                global uStatement

                X = graphtext1.get('1.0', 'end-1c') #Turn user input into list
                Xlist = list(map(float, X.split()))                
                Xlist = [round(i, prec) for i in Xlist]

                Y = graphtext2.get('1.0', 'end-1c') #Turn user input into list
                Ylist = list(map(float, Y.split()))
                Ylist = [round(i, prec) for i in Ylist]

                XTick = graphtext5.get('1.0', 'end-1c') #Turn user input into list
                XTicklist = list(map(float, XTick.split()))                
                XTicklist = [round(i, prec) for i in XTicklist]

                YTick = graphtext6.get('1.0', 'end-1c') #Turn user input into list
                YTicklist = list(map(float, YTick.split()))                
                YTicklist = [round(i, prec) for i in YTicklist]

                XLbl = graphtext7.get('1.0', 'end-1c') #Takes X Axis label from user                

                YLbl = graphtext8.get('1.0', 'end-1c') #Takes Y Axis label from user                              

                GraphTitle = graphtext9.get('1.0', 'end-1c') #Takes graph title from user 

                f = Figure(figsize = (6.93, 3.3), dpi = 100) #Defines graph dimensions
                a = f.add_subplot(111)
                a.set_xticks(XTicklist)
                a.set_xticklabels(XTicklist)
                a.set_yticks(YTicklist)
                a.set_yticklabels(YTicklist)
                a.set_xlabel(XLbl)
                a.set_ylabel(YLbl)
                a.set_title(GraphTitle)
                a.hist(Xlist, Ylist, color = '#00adb5') #Plots the graph
                
                a.set_facecolor('#222831') #Graph colours
                f.patch.set_facecolor('#222831')
                a.tick_params(axis='x', colors='#00adb5', which = 'both')
                a.tick_params(axis='y', colors='#00adb5', which = 'both')
                a.spines['bottom'].set_color('#eeeeee')
                a.spines['left'].set_color('#eeeeee')
                a.xaxis.label.set_color('#00adb5')
                a.xaxis.set_label_coords(0.5, -0.087)
                a.yaxis.label.set_color('#00adb5')
                a.title.set_color('#00adb5')
                a.spines['top'].set_visible(False) #Hides top and right axis
                a.spines['right'].set_visible(False)

                uStatement = str('You plotted a histogram with coordinates ' + X + ', ' + Y + '\n') #Usage history statement
                uHist.append(uStatement)

                canvas = FigureCanvasTkAgg(f, plotlf) #Draws graph for viewing
                canvas.draw()
                canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)
            except:
                graphtext1.delete('1.0', 'end')
                graphtext1.insert(tk.END, 'ERROR')
                graphtext2.delete('1.0', 'end')
                graphtext2.insert(tk.END, 'ERROR')

        def plotPC(): #This function is for plotting pie chart
            try:
                global uHist
                global uStatement                

                X = graphtext3.get('1.0', 'end-1c') #Turn user input into list
                Xlist = list(map(str, X.split()))                

                Y = graphtext4.get('1.0', 'end-1c') #Turn user input into list
                Ylist = list(map(float, Y.split()))
                Ylist = [round(i, prec) for i in Ylist]

                GraphTitle = graphtext9.get('1.0', 'end-1c') #Takes graph title from user 

                wp = {'linewidth' : 1, 'edgecolor' : '#00adb5'} #For wedge properties
                f = Figure(figsize = (6.93, 3.3), dpi = 100) #Defines graph dimensions
                a = f.add_subplot(111)
                a.set_title(GraphTitle)
                a.pie(Ylist, labels =  Xlist, shadow = True, startangle = 90, wedgeprops = wp, textprops = dict(color = '#00adb5')) #Plots the graph
                
                a.set_facecolor('#222831') #Graph colours
                f.patch.set_facecolor('#222831')
                a.tick_params(axis = 'x', colors = '#00adb5', which = 'both')
                a.tick_params(axis = 'y', colors = '#00adb5', which = 'both')
                a.spines['bottom'].set_color('#eeeeee')
                a.spines['left'].set_color('#eeeeee')
                a.spines['top'].set_visible(False) #Hides top and right axis
                a.spines['right'].set_visible(False)
                a.title.set_color('#00adb5')

                uStatement = str('You plotted a pie chart with labels ' + X + ' and data ' + Y + '\n') #Usage history statement
                uHist.append(uStatement)

                canvas = FigureCanvasTkAgg(f, plotlf) #Draws graph for viewing
                canvas.draw()
                canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)
            except:
                graphtext3.delete('1.0', 'end')
                graphtext3.insert(tk.END, 'ERROR')
                graphtext4.delete('1.0', 'end')
                graphtext4.insert(tk.END, 'ERROR')

        def plotAUTC(): #This function is for plotting area bounded by 2 curves
            try:
                global uHist
                global uStatement                

                choice = xyvar.get()
                if choice == 1:
                    X = graphtext1.get('1.0', 'end-1c') #Turn user input into list
                    Xlist = list(map(float, X.split()))                
                    Xlist = [round(i, prec) for i in Xlist]
                    
                    Y1 = graphtext3.get('1.0', 'end-1c') #Turn user input into list
                    Y1list = list(map(float, Y1.split()))                
                    Y1list = [round(i, prec) for i in Y1list]

                    Y2 = graphtext4.get('1.0', 'end-1c') #Turn user input into list
                    Y2list = list(map(float, Y2.split()))
                    Y2list = [round(i, prec) for i in Y2list]

                    XTick = graphtext5.get('1.0', 'end-1c') #Turn user input into list
                    XTicklist = list(map(float, XTick.split()))                
                    XTicklist = [round(i, prec) for i in XTicklist]

                    YTick = graphtext6.get('1.0', 'end-1c') #Turn user input into list
                    YTicklist = list(map(float, YTick.split()))                
                    YTicklist = [round(i, prec) for i in YTicklist]

                    XLbl = graphtext7.get('1.0', 'end-1c') #Takes X Axis label from user                

                    YLbl = graphtext8.get('1.0', 'end-1c') #Takes Y Axis label from user  

                    GraphTitle = graphtext9.get('1.0', 'end-1c') #Takes graph title from user 

                    f = Figure(figsize = (6.93, 3.3), dpi = 100) #Defines graph dimensions
                    a = f.add_subplot(111)
                    a.set_xticks(XTicklist)
                    a.set_xticklabels(XTicklist)
                    a.set_yticks(YTicklist)
                    a.set_yticklabels(YTicklist)
                    a.set_xlabel(XLbl)
                    a.set_ylabel(YLbl)
                    a.plot(Xlist, Y1list, color = '#00adb5') #Plots the graph
                    a.plot(Xlist, Y2list, color = '#00adb5')
                    a.set_title(GraphTitle)
                    a.fill_between(Xlist, Y1list, Y2list, color = '#393e46')

                    a.set_facecolor('#222831') #Graph colours
                    f.patch.set_facecolor('#222831')
                    a.tick_params(axis='x', colors='#00adb5', which = 'both')
                    a.tick_params(axis='y', colors='#00adb5', which = 'both')
                    a.spines['bottom'].set_color('#eeeeee')
                    a.spines['left'].set_color('#eeeeee')
                    a.xaxis.label.set_color('#00adb5')
                    a.xaxis.set_label_coords(0.5, -0.087)
                    a.yaxis.label.set_color('#00adb5')
                    a.title.set_color('#00adb5')
                    a.spines['top'].set_visible(False) #Hides top and right axis
                    a.spines['right'].set_visible(False)

                    uStatement = str('You plotted AUTC with X coordinates ' + X + '\nand Y coordinates ' + Y1 + ', ' + Y2 + '\n') #Usage history statement
                    uHist.append(uStatement)

                    canvas = FigureCanvasTkAgg(f, plotlf) #Draws graph for viewing
                    canvas.draw()
                    canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)
                elif choice == 2:
                    Y = graphtext2.get('1.0', 'end-1c') #Turn user input into list
                    Ylist = list(map(float, Y.split()))                
                    Ylist = [round(i, prec) for i in Ylist]
                    
                    X1 = graphtext3.get('1.0', 'end-1c') #Turn user input into list
                    X1list = list(map(float, X1.split()))                
                    X1list = [round(i, prec) for i in X1list]

                    X2 = graphtext4.get('1.0', 'end-1c') #Turn user input into list
                    X2list = list(map(float, X2.split()))
                    X2list = [round(i, prec) for i in X2list]

                    XTick = graphtext5.get('1.0', 'end-1c') #Turn user input into list
                    XTicklist = list(map(float, XTick.split()))                
                    XTicklist = [round(i, prec) for i in XTicklist]

                    YTick = graphtext6.get('1.0', 'end-1c') #Turn user input into list
                    YTicklist = list(map(float, YTick.split()))                
                    YTicklist = [round(i, prec) for i in YTicklist]

                    XLbl = graphtext7.get('1.0', 'end-1c') #Takes X Axis label from user                

                    YLbl = graphtext8.get('1.0', 'end-1c') #Takes Y Axis label from user  

                    GraphTitle = graphtext9.get('1.0', 'end-1c') #Takes graph title from user 

                    f = Figure(figsize = (7.55, 3.3), dpi = 100) #Defines graph dimensions
                    a = f.add_subplot(111)
                    a.set_xticks(XTicklist)
                    a.set_xticklabels(XTicklist)
                    a.set_yticks(YTicklist)
                    a.set_yticklabels(YTicklist)
                    a.set_xlabel(XLbl)
                    a.set_ylabel(YLbl)
                    a.plot(X1list, Ylist, color = '#00adb5') #Plots the graph
                    a.plot(X2list, Ylist, color = '#00adb5')
                    a.set_title(GraphTitle)
                    a.fill_betweenx(Ylist, X1list, X2list, color = '#393e46')

                    a.set_facecolor('#222831') #Graph colours
                    f.patch.set_facecolor('#222831')
                    a.tick_params(axis='x', colors='#00adb5', which = 'both')
                    a.tick_params(axis='y', colors='#00adb5', which = 'both')
                    a.spines['bottom'].set_color('#eeeeee')
                    a.spines['left'].set_color('#eeeeee')
                    a.xaxis.label.set_color('#00adb5')
                    a.xaxis.set_label_coords(0.5, -0.087)
                    a.yaxis.label.set_color('#00adb5')
                    a.title.set_color('#00adb5')
                    a.spines['top'].set_visible(False) #Hides top and right axis
                    a.spines['right'].set_visible(False)

                    uStatement = str('You plotted AUTC with Y coordinates ' + Y + '\nand X coordinates ' + X1 + ', ' + X2 + '\n') #Usage history statement
                    uHist.append(uStatement)

                    canvas = FigureCanvasTkAgg(f, plotlf) #Draws graph for viewing
                    canvas.draw()
                    canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)
            except:
                graphtext1.delete('1.0', 'end')
                graphtext1.insert(tk.END, 'ERROR')
                graphtext2.delete('1.0', 'end')
                graphtext2.insert(tk.END, 'ERROR')
                graphtext3.delete('1.0', 'end')
                graphtext3.insert(tk.END, 'ERROR')
                graphtext4.delete('1.0', 'end')
                graphtext4.insert(tk.END, 'ERROR')                            

        def reset(): #This function is for resetting all input text fields         
            graphtext1.delete('1.0', 'end')
            graphtext1.insert(tk.END, 'Enter X Coordinates')
            graphtext2.delete('1.0', 'end')
            graphtext2.insert(tk.END, 'Enter Y Coordinates')
            graphtext3.delete('1.0', 'end')
            graphtext3.insert(tk.END, 'Enter Data')
            graphtext4.delete('1.0', 'end')
            graphtext4.insert(tk.END, 'Enter Data')

        def resetAxis(): #This function is for resetting axis limit text fields         
            graphtext5.delete('1.0', 'end')
            graphtext5.insert(tk.END, 'Enter X Axis Ticks')
            graphtext6.delete('1.0', 'end')
            graphtext6.insert(tk.END, 'Enter Y Axis Ticks')

        def resetGraph(): #This function is for resetting the graph
            try:
                f = Figure(figsize = (6.93, 3.3), dpi = 100)
                a = f.add_subplot(111)
                a.plot([0], [0])

                a.set_facecolor('#222831') #Graph colours
                f.patch.set_facecolor('#222831')
                a.tick_params(axis='x', colors='#00adb5', which = 'both')
                a.tick_params(axis='y', colors='#00adb5', which = 'both')
                a.spines['bottom'].set_color('#eeeeee')
                a.spines['left'].set_color('#eeeeee')
                a.spines['top'].set_visible(False) #Hides top and right axis
                a.spines['right'].set_visible(False)
 
                canvas = FigureCanvasTkAgg(f, plotlf)
                canvas.draw()
                canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)                
            except:
                graphtext1.delete('1.0', 'end')
                graphtext1.insert(tk.END, 'ERROR')
                graphtext2.delete('1.0', 'end')
                graphtext2.insert(tk.END, 'ERROR')
                graphtext3.delete('1.0', 'end')
                graphtext3.insert(tk.END, 'ERROR')
                graphtext4.delete('1.0', 'end')
                graphtext4.insert(tk.END, 'ERROR') 

        def msclick1(event): #This function is to empty graphtext1 upon mouse click
            graphtext1.delete('1.0', 'end')
            return None

        def msclick2(event): #Above function for graphtext2
            graphtext2.delete('1.0', 'end')
            return None

        def msclick3(event): #Above function for graphtext3
            graphtext3.delete('1.0', 'end')
            return None

        def msclick4(event): #Above function for graphtext4
            graphtext4.delete('1.0', 'end')
            return None

        def msclick5(event): #Above function for graphtext5
            graphtext5.delete('1.0', 'end')
            return None

        def msclick6(event): #Above function for graphtext6
            graphtext6.delete('1.0', 'end')
            return None

        def msclick7(event): #Above function for graphtext7
            graphtext7.delete('1.0', 'end')
            return None

        def msclick8(event): #Above function for graphtext8
            graphtext8.delete('1.0', 'end')
            return None

        def msclick9(event): #Above function for graphtext9
            graphtext9.delete('1.0', 'end')
            return None

        xyvar = tk.IntVar() #This variable is for radio button value
        xyvar.set(1)

        backbutton = ttk.Button(self, text = 'Back', style = 'btn.TButton', command = lambda: controller.show_frame(ChoicePage)) #This button takes us to the previous page
        backbutton.grid(row = 0, column = 2, padx = 10, pady = 20, sticky = 'e')

        label = tk.Label(self, text = 'Graphs', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title Label
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        histbutton = ttk.Button(self, text = 'History', style = 'btn.TButton', command = lambda: controller.show_frame(HistPage)) #This button takes us to the usage history page
        histbutton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')

        graphopslf = tk.LabelFrame(self, text = 'Graph Operations:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains all the stuff to be used for taking inputs for graphs
        graphopslf.grid(row = 1, column = 0, padx = 5, pady = 10)

        graphlabel1 = tk.Label(graphopslf, text = 'Graph 1:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Label for first input field
        graphlabel1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')

        graphtext1 = tk.Text(graphopslf, font = LargeFont, height = 1.3, width = 18) #This field takes input for X axis
        graphtext1.grid(row = 1, column = 0, ipady = 1, padx = 5, pady = 7)
        graphtext1.insert(tk.END, 'Enter X Coordinates')
        graphtext1.bind('<Button-1>', msclick1)

        graphtext2 = tk.Text(graphopslf, font = LargeFont, height = 1.3, width = 18) #This field takes input for Y axis
        graphtext2.grid(row = 2, column = 0, ipady = 1, padx = 5, pady = 7)     
        graphtext2.insert(tk.END, 'Enter Y Coordinates')
        graphtext2.bind('<Button-1>', msclick2)       

        plotbtn = ttk.Button(graphopslf, text = 'Line Plot', style = 'btn.TButton', command = lambda: plotLG()) #This button plots line graph
        plotbtn.grid(row = 3, column = 0, padx = 5, pady = 6, sticky = 'w')
        plotbtn.config(width = 8)

        scatterbtn = ttk.Button(graphopslf, text = 'Scatter', style = 'btn.TButton', command = lambda: plotSC()) #This button plots scatter plot
        scatterbtn.grid(row = 3, column = 0, padx = 5, pady = 6, sticky = 'e')
        scatterbtn.config(width = 8)

        barbtn = ttk.Button(graphopslf, text = 'Bar Plot', style = 'btn.TButton', command = lambda: plotBG()) #This button plots bar graph
        barbtn.grid(row = 4, column = 0, padx = 5, pady = 6, sticky = 'e')
        barbtn.config(width = 8)

        histobtn = ttk.Button(graphopslf, text = 'Histogram', style = 'btn.TButton', command = lambda: plotHG()) #This button plots histogram
        histobtn.grid(row = 4, column = 0, padx = 5, pady = 6, sticky = 'w')
        histobtn.config(width = 8)

        resetbtn = ttk.Button(graphopslf, text = 'Reset', style = 'btn.TButton', command = lambda: reset()) #This button resets all the fields in graphopslf label frame
        resetbtn.grid(row = 0, column = 0, padx = 5, pady = 4, sticky = 'e')
        resetbtn.config(width = 6)

        graphlabel2 = tk.Label(graphopslf, text = 'Graph 2:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Label for second input field
        graphlabel2.grid(row = 5, column = 0, padx = 5, pady = 5)

        graphtext3 = tk.Text(graphopslf, font = LargeFont, height = 1.3, width = 18) #This field takes input for pie chart and AUTC
        graphtext3.grid(row = 6, column = 0, ipady = 1, padx = 5, pady = 7)
        graphtext3.insert(tk.END, 'Enter Data')
        graphtext3.bind('<Button-1>', msclick3)

        graphtext4 = tk.Text(graphopslf, font = LargeFont, height = 1.3, width = 18) #This field takes input for pie chart and AUTC
        graphtext4.grid(row = 7, column = 0, ipady = 1, padx = 5, pady = 7)     
        graphtext4.insert(tk.END, 'Enter Data')
        graphtext4.bind('<Button-1>', msclick4)

        xradio = ttk.Radiobutton(graphopslf, text = 'X', style = 'btn.TRadiobutton', variable = xyvar, value = 1) #This radio button plots AUTC from X axis
        xradio.grid(row = 5, column = 0, padx = 5, pady = 4, sticky = 'w')

        yradio = ttk.Radiobutton(graphopslf, text = 'Y', style = 'btn.TRadiobutton', variable = xyvar, value = 2) #This radio button plots AUTC from Y axis
        yradio.grid(row = 5, column = 0, padx = 5, pady = 4, sticky = 'e')

        autcbtn = ttk.Button(graphopslf, text = 'AUTC', style = 'btn.TButton', command = lambda: plotAUTC()) #This button plots AUTC
        autcbtn.grid(row = 8, column = 0, padx = 5, pady = 6, sticky = 'e')
        autcbtn.config(width = 8)

        piebtn = ttk.Button(graphopslf, text = 'Pie Chart', style = 'btn.TButton', command = lambda: plotPC()) #This button plots pie chart
        piebtn.grid(row = 8, column = 0, padx = 5, pady = 6, sticky = 'w')
        piebtn.config(width = 8)

        limitlf = tk.LabelFrame(self, text = 'Axis Customization:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame takes input for customizing axis limits and labels
        limitlf.grid(row = 1, column = 2, padx = 5, pady = 10)

        graphlabel3 = tk.Label(limitlf, text = 'Axis Ticks:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Label for axis tick input field
        graphlabel3.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')

        graphtext5 = tk.Text(limitlf, font = LargeFont, height = 1.3, width = 18) #This field takes input for X axis ticks
        graphtext5.grid(row = 1, column = 0, ipady = 1, padx = 5, pady = 7)
        graphtext5.insert(tk.END, 'Enter X Axis Ticks')
        graphtext5.bind('<Button-1>', msclick5)

        graphtext6 = tk.Text(limitlf, font = LargeFont, height = 1.3, width = 18) #This field takes input for Y axis ticks
        graphtext6.grid(row = 2, column = 0, ipady = 1, padx = 5, pady = 7)     
        graphtext6.insert(tk.END, 'Enter Y Axis Ticks')
        graphtext6.bind('<Button-1>', msclick6)       

        graphlabel4 = tk.Label(limitlf, text = 'Axis Labels:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Label for axis label input field
        graphlabel4.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'w')

        graphtext7 = tk.Text(limitlf, font = LargeFont, height = 1.3, width = 18) #This field takes input for X axis label
        graphtext7.grid(row = 4, column = 0, ipady = 1, padx = 5, pady = 7)
        graphtext7.insert(tk.END, 'Enter X Axis Label')
        graphtext7.bind('<Button-1>', msclick7)

        graphtext8 = tk.Text(limitlf, font = LargeFont, height = 1.3, width = 18) #This field takes input for Y axis label
        graphtext8.grid(row = 5, column = 0, ipady = 1, padx = 5, pady = 7)     
        graphtext8.insert(tk.END, 'Enter Y Axis Label')
        graphtext8.bind('<Button-1>', msclick8)

        graphlabel5 = tk.Label(limitlf, text = 'Graph title:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Label for graph title input field
        graphlabel5.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = 'w')

        graphtext9 = tk.Text(limitlf, font = LargeFont, height = 1.3, width = 18) #This field takes input for graph title
        graphtext9.grid(row = 7, column = 0, ipady = 1, padx = 5, pady = 7)     
        graphtext9.insert(tk.END, 'Enter Graph Title')
        graphtext9.bind('<Button-1>', msclick9)

        resetaxisbtn = ttk.Button(limitlf, text = 'Reset', style = 'btn.TButton', command = lambda: resetAxis()) #This button resets all the fields in limitlf label frame
        resetaxisbtn.grid(row = 0, column = 0, padx = 5, pady = 4, sticky = 'e')
        resetaxisbtn.config(width = 6)

        graphresetbtn = ttk.Button(limitlf, text = 'Reset Graph', style = 'btn.TButton', command = lambda: resetGraph()) #This button resets the graph
        graphresetbtn.grid(row = 8, column = 0, padx = 10, pady = 12)

        plotlf = tk.LabelFrame(self, text = 'Graph:', font = LabelFont, fg = '#00adb5', bg = '#393e46', width = 120, height = 50) #This label frame contains the plotted graph
        plotlf.grid(row = 1, column = 1, padx = 5, pady = 10)

        f = Figure(figsize = (6.93, 3.3), dpi = 100) #This is default graph when graph page is opened or reset
        a = f.add_subplot(111)
        a.plot([0], [0])
        
        a.set_facecolor('#222831') #Graph colours
        f.patch.set_facecolor('#222831')
        a.tick_params(axis='x', colors='#00adb5', which = 'both')
        a.tick_params(axis='y', colors='#00adb5', which = 'both')
        a.spines['bottom'].set_color('#eeeeee')
        a.spines['left'].set_color('#eeeeee')
        a.spines['top'].set_visible(False) #Hides top and right axis
        a.spines['right'].set_visible(False)

        canvas = FigureCanvasTkAgg(f, plotlf)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)

class ConverterPage(tk.Frame): #This class is for Converter page

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831')

        def convertMass(): #This function is for mass conversion
            try:
                global uHist
                global uStatement

                massqty = float(massvar.get()) #Acquisition of required values and parameters
                cnvfrom = masscombo1.get()
                cnvto = masscombo2.get()

                if cnvfrom == 'Kilograms': #Conversions happen in this loop nest                    
                    if cnvto == 'Kilograms':
                        massansvar.set(round((massqty), prec))                    
                    elif cnvto == 'Grams':
                        massansvar.set(round((massqty * 1000), prec))
                    elif cnvto == 'Pounds':
                        massansvar.set(round((massqty * 2.20462), prec))
                    elif cnvto == 'Ounces':
                        massansvar.set(round((massqty * 35.274), prec))

                elif cnvfrom == 'Grams':                    
                    if cnvto == 'Kilograms':
                        massansvar.set(round((massqty / 1000), prec))                    
                    elif cnvto == 'Grams':
                        massansvar.set(round((massqty), prec))
                    elif cnvto == 'Pounds':
                        massansvar.set(round((massqty * 0.00220462), prec))
                    elif cnvto == 'Ounces':
                        massansvar.set(round((massqty * 0.035274), prec))

                elif cnvfrom == 'Pounds':                    
                    if cnvto == 'Kilograms':
                        massansvar.set(round((massqty * 0.453592), prec))                    
                    elif cnvto == 'Grams':
                        massansvar.set(round((massqty * 453.592), prec))
                    elif cnvto == 'Pounds':
                        massansvar.set(round((massqty), prec))
                    elif cnvto == 'Ounces':
                        massansvar.set(round((massqty * 16), prec))

                elif cnvfrom == 'Ounces':                    
                    if cnvto == 'Kilograms':
                        massansvar.set(round((massqty * 0.0283495), prec))                    
                    elif cnvto == 'Grams':
                        massansvar.set(round((massqty * 28.3495), prec))
                    elif cnvto == 'Pounds':
                        massansvar.set(round((massqty / 16), prec))
                    elif cnvto == 'Ounces':
                        massansvar.set(round((massqty), prec))

                uStatement = str('You converted ' + str(massqty) + ' ' + str(cnvfrom) + ' to ' + massansvar.get() + ' ' + str(cnvto) + '\n') #Usage history statement
                uHist.append(uStatement)

            except:
                massvar.set('ERROR')
                massansvar.set('ERROR')
                masscombo1.current(0)
                masscombo2.current(0)

        def convertLen(): #This function is for length conversion
            try:
                global uHist
                global uStatement

                lenqty = float(lenvar.get()) #Acquisition of required values and parameters
                cnvfrom = lencombo1.get()
                cnvto = lencombo2.get()

                if cnvfrom == 'Kilometres': #Conversions happen in this loop nest                    
                    if cnvto == 'Kilometres':
                        lenansvar.set(round((lenqty), prec))                    
                    elif cnvto == 'Metres':
                        lenansvar.set(round((lenqty * 1000), prec))
                    elif cnvto == 'Miles':
                        lenansvar.set(round((lenqty * 0.621371), prec))
                    elif cnvto == 'Yards':
                        lenansvar.set(round((lenqty * 1093.61), prec))
                    elif cnvto == 'Feet':
                        lenansvar.set(round((lenqty * 3280.84), prec))
                    elif cnvto == 'Inches':
                        lenansvar.set(round((lenqty * 39370.1), prec))
                
                elif cnvfrom == 'Metres':                     
                    if cnvto == 'Kilometres':
                        lenansvar.set(round((lenqty / 1000), prec))                    
                    elif cnvto == 'Metres':
                        lenansvar.set(round((lenqty), prec))
                    elif cnvto == 'Miles':
                        lenansvar.set(round((lenqty * 0.000621371), prec))
                    elif cnvto == 'Yards':
                        lenansvar.set(round((lenqty * 1.09361), prec))
                    elif cnvto == 'Feet':
                        lenansvar.set(round((lenqty * 3.28084), prec))
                    elif cnvto == 'Inches':
                        lenansvar.set(round((lenqty * 39.3701), prec))

                elif cnvfrom == 'Miles':                     
                    if cnvto == 'Kilometres':
                        lenansvar.set(round((lenqty * 1.60934), prec))                    
                    elif cnvto == 'Metres':
                        lenansvar.set(round((lenqty), prec))
                    elif cnvto == 'Miles':
                        lenansvar.set(round((lenqty * 1609.34), prec))
                    elif cnvto == 'Yards':
                        lenansvar.set(round((lenqty * 1760), prec))
                    elif cnvto == 'Feet':
                        lenansvar.set(round((lenqty * 5280), prec))
                    elif cnvto == 'Inches':
                        lenansvar.set(round((lenqty * 63360), prec))     

                elif cnvfrom == 'Yards':                     
                    if cnvto == 'Kilometres':
                        lenansvar.set(round((lenqty * 0.0009144), prec))                    
                    elif cnvto == 'Metres':
                        lenansvar.set(round((lenqty * 0.9144), prec))
                    elif cnvto == 'Miles':
                        lenansvar.set(round((lenqty / 1760), prec))
                    elif cnvto == 'Yards':
                        lenansvar.set(round((lenqty), prec))
                    elif cnvto == 'Feet':
                        lenansvar.set(round((lenqty * 3), prec))
                    elif cnvto == 'Inches':
                        lenansvar.set(round((lenqty * 36), prec))

                elif cnvfrom == 'Feet':                     
                    if cnvto == 'Kilometres':
                        lenansvar.set(round((lenqty * 0.0003048), prec))                    
                    elif cnvto == 'Metres':
                        lenansvar.set(round((lenqty * 0.3048), prec))
                    elif cnvto == 'Miles':
                        lenansvar.set(round((lenqty * 0.000189394), prec))
                    elif cnvto == 'Yards':
                        lenansvar.set(round((lenqty / 3), prec))
                    elif cnvto == 'Feet':
                        lenansvar.set(round((lenqty), prec))
                    elif cnvto == 'Inches':
                        lenansvar.set(round((lenqty * 12), prec))

                elif cnvfrom == 'Inches':                     
                    if cnvto == 'Kilometres':
                        lenansvar.set(round((lenqty / 39370), prec))                    
                    elif cnvto == 'Metres':
                        lenansvar.set(round((lenqty * 0.0254), prec))
                    elif cnvto == 'Miles':
                        lenansvar.set(round((lenqty / 63360), prec))
                    elif cnvto == 'Yards':
                        lenansvar.set(round((lenqty / 36), prec))
                    elif cnvto == 'Feet':
                        lenansvar.set(round((lenqty / 12), prec))
                    elif cnvto == 'Inches':
                        lenansvar.set(round((lenqty), prec))

                uStatement = str('You converted ' + str(lenqty) + ' ' + str(cnvfrom) + ' to ' + lenansvar.get() + ' ' + str(cnvto) + '\n') #Usage history statement
                uHist.append(uStatement)

            except:
                lenvar.set('ERROR')
                lenansvar.set('ERROR')
                lencombo1.current(0)
                lencombo2.current(0)

        def convertTemp(): #This function is for temperature conversion
            try:
                global uHist
                global uStatement

                tempqty = float(tempvar.get()) #Acquisition of required values and parameters
                cnvfrom = tempcombo1.get()
                cnvto = tempcombo2.get()

                if cnvfrom == 'Celsius': #Conversions happen in this loop nest                    
                    if cnvto == 'Celsius':
                        tempansvar.set(round((tempqty), prec))                    
                    elif cnvto == 'Fahrenheit':
                        tempansvar.set(round(((tempqty * (9 / 5)) + 32), prec))
                    elif cnvto == 'Kelvin':
                        tempansvar.set(round((tempqty + 273.15), prec))
                
                elif cnvfrom == 'Fahrenheit':                     
                    if cnvto == 'Celsius':
                        tempansvar.set(round(((tempqty - 32) * (5 / 9)), prec))                    
                    elif cnvto == 'Fahrenheit':
                        tempansvar.set(round((tempqty), prec))
                    elif cnvto == 'Kelvin':
                        tempansvar.set(round((((tempqty - 32) * (5 / 9) + 273.15)), prec))

                elif cnvfrom == 'Kelvin':                     
                    if cnvto == 'Celsius':
                        tempansvar.set(round((tempqty - 273.15), prec))                    
                    elif cnvto == 'Fahrenheit':
                        tempansvar.set(round((((tempqty - 273.15) * (9 / 5)) + 32), prec))
                    elif cnvto == 'Kelvin':
                        tempansvar.set(round((tempqty), prec))    

                uStatement = str('You converted ' + str(tempqty) + ' ' + str(cnvfrom) + ' to ' + tempansvar.get() + ' ' + str(cnvto) + '\n') #Usage history statement
                uHist.append(uStatement)

            except:
                tempvar.set('ERROR')
                tempansvar.set('ERROR')
                tempcombo1.current(0)
                tempcombo2.current(0)

        def convertFluid(): #This function is for fluid volume conversion
            try:
                global uHist
                global uStatement

                fluidqty = float(fluidvar.get()) #Acquisition of required values and parameters
                cnvfrom = fluidcombo1.get()
                cnvto = fluidcombo2.get()

                if cnvfrom == 'Litres': #Conversions happen in this loop nest                    
                    if cnvto == 'Litres':
                        fluidansvar.set(round((fluidqty), prec))                    
                    elif cnvto == 'Mililitres':
                        fluidansvar.set(round((fluidqty * 1000), prec))
                    elif cnvto == 'US Gallons':
                        fluidansvar.set(round((fluidqty * 0.264172), prec))
                    elif cnvto == 'US Fl. Oz':
                        fluidansvar.set(round((fluidqty * 33.814), prec))
                    elif cnvto == 'IMP Gallons':
                        fluidansvar.set(round((fluidqty * 0.219969), prec))
                    elif cnvto == 'IMP Fl. Oz':
                        fluidansvar.set(round((fluidqty * 35.1951), prec))
                
                elif cnvfrom == 'Mililitres':                     
                    if cnvto == 'Litres':
                        fluidansvar.set(round((fluidqty / 1000), prec))                    
                    elif cnvto == 'Mililitres':
                        fluidansvar.set(round((fluidqty), prec))
                    elif cnvto == 'US Gallons':
                        fluidansvar.set(round((fluidqty * 0.000264172), prec))
                    elif cnvto == 'US Fl. Oz':
                        fluidansvar.set(round((fluidqty * 0.033814), prec))
                    elif cnvto == 'IMP Gallons':
                        fluidansvar.set(round((fluidqty * 0.000219969), prec))
                    elif cnvto == 'IMP Fl. Oz':
                        fluidansvar.set(round((fluidqty * 0.0351951), prec))

                elif cnvfrom == 'US Gallons':                     
                    if cnvto == 'Litres':
                        fluidansvar.set(round((fluidqty * 3.78541), prec))                    
                    elif cnvto == 'Mililitres':
                        fluidansvar.set(round((fluidqty * 3785.41), prec))
                    elif cnvto == 'US Gallons':
                        fluidansvar.set(round((fluidqty), prec))
                    elif cnvto == 'US Fl. Oz':
                        fluidansvar.set(round((fluidqty * 128), prec))
                    elif cnvto == 'IMP Gallons':
                        fluidansvar.set(round((fluidqty * 0.832674), prec))
                    elif cnvto == 'IMP Fl. Oz':
                        fluidansvar.set(round((fluidqty * 133.228), prec))    

                elif cnvfrom == 'US Fl. Oz':                     
                    if cnvto == 'Litres':
                        fluidansvar.set(round((fluidqty * 0.0295735), prec))                    
                    elif cnvto == 'Mililitres':
                        fluidansvar.set(round((fluidqty * 29.5735), prec))
                    elif cnvto == 'US Gallons':
                        fluidansvar.set(round((fluidqty / 128), prec))
                    elif cnvto == 'US Fl. Oz':
                        fluidansvar.set(round((fluidqty), prec))
                    elif cnvto == 'IMP Gallons':
                        fluidansvar.set(round((fluidqty / 153.722), prec))
                    elif cnvto == 'IMP Fl. Oz':
                        fluidansvar.set(round((fluidqty * 1.04084), prec))

                elif cnvfrom == 'IMP Gallons':                     
                    if cnvto == 'Litres':
                        fluidansvar.set(round((fluidqty * 4.54609), prec))                    
                    elif cnvto == 'Mililitres':
                        fluidansvar.set(round((fluidqty * 4546.09), prec))
                    elif cnvto == 'US Gallons':
                        fluidansvar.set(round((fluidqty * 1.20095), prec))
                    elif cnvto == 'US Fl. Oz':
                        fluidansvar.set(round((fluidqty * 153.722), prec))
                    elif cnvto == 'IMP Gallons':
                        fluidansvar.set(round((fluidqty), prec))
                    elif cnvto == 'IMP Fl. Oz':
                        fluidansvar.set(round((fluidqty * 160), prec))

                elif cnvfrom == 'IMP Fl. Oz':                     
                    if cnvto == 'Litres':
                        fluidansvar.set(round((fluidqty * 0.0284131), prec))                    
                    elif cnvto == 'Mililitres':
                        fluidansvar.set(round((fluidqty * 28.41310000012815), prec))
                    elif cnvto == 'US Gallons':
                        fluidansvar.set(round((fluidqty / 133), prec))
                    elif cnvto == 'US Fl. Oz':
                        fluidansvar.set(round((fluidqty * 0.96076120843406853655), prec))
                    elif cnvto == 'IMP Gallons':
                        fluidansvar.set(round((fluidqty / 160), prec))
                    elif cnvto == 'IMP Fl. Oz':
                        fluidansvar.set(round((fluidqty), prec))

                uStatement = str('You converted ' + str(fluidqty) + ' ' + str(cnvfrom) + ' to ' + fluidansvar.get() + ' ' + str(cnvto) + '\n') #Usage history statement
                uHist.append(uStatement)

            except:
                fluidvar.set('ERROR')
                fluidansvar.set('ERROR')
                fluidcombo1.current(0)
                fluidcombo2.current(0)

        def convertEnergy(): #This function is for energy conversion
            try:
                global uHist
                global uStatement

                energyqty = float(energyvar.get()) #Acquisition of required values and parameters
                cnvfrom = energycombo1.get()
                cnvto = energycombo2.get()

                if cnvfrom == 'Joules': #Conversions happen in this loop nest                    
                    if cnvto == 'Joules':
                        energyansvar.set(round((energyqty), prec))                    
                    elif cnvto == 'Calories':
                        energyansvar.set(round((energyqty * 0.239006), prec))
                    elif cnvto == 'E. Volts':
                        energyansvar.set(round((energyqty / (1.6 * (10 ** -19))), prec))
                    elif cnvto == 'BTUs':
                        energyansvar.set(round((energyqty * 0.000947817), prec))
                    elif cnvto == 'Ft. Pounds':
                        energyansvar.set(round((energyqty * 0.737562), prec))
                
                elif cnvfrom == 'Calories':                   
                    if cnvto == 'Joules':
                        energyansvar.set(round((energyqty * 4.184), prec))                    
                    elif cnvto == 'Calories':
                        energyansvar.set(round((energyqty), prec))
                    elif cnvto == 'E. Volts':
                        energyansvar.set(round(((energyqty * 4.184) / (1.6 * (10 ** -19))), prec))
                    elif cnvto == 'BTUs':
                        energyansvar.set(round((energyqty * 0.00396567), prec))
                    elif cnvto == 'Ft. Pounds':
                        energyansvar.set(round((energyqty * 3.08596), prec))

                elif cnvfrom == 'E. Volts':                   
                    if cnvto == 'Joules':
                        energyansvar.set(round((energyqty * (1.6 * (10 ** -19))), prec))                    
                    elif cnvto == 'Calories':
                        energyansvar.set(round(((energyqty * (1.6 * (10 ** -19))) * 0.239006), prec))
                    elif cnvto == 'E. Volts':
                        energyansvar.set(round((energyqty), prec))
                    elif cnvto == 'BTUs':
                        energyansvar.set(round(((energyqty * (1.6 * (10 ** -19))) * 0.000947817), prec))
                    elif cnvto == 'Ft. Pounds':
                        energyansvar.set(round(((energyqty * (1.6 * (10 ** -19))) * 0.737562), prec))

                elif cnvfrom == 'BTUs':                   
                    if cnvto == 'Joules':
                        energyansvar.set(round((energyqty * 1055.06), prec))                    
                    elif cnvto == 'Calories':
                        energyansvar.set(round((energyqty * 252.164), prec))
                    elif cnvto == 'E. Volts':
                        energyansvar.set(round(((energyqty * 1055.06) / (1.6 * (10 ** -19))), prec))
                    elif cnvto == 'BTUs':
                        energyansvar.set(round((energyqty), prec))
                    elif cnvto == 'Ft. Pounds':
                        energyansvar.set(round((energyqty * 778.169), prec))

                elif cnvfrom == 'Ft. Pounds':                   
                    if cnvto == 'Joules':
                        energyansvar.set(round((energyqty * 1.35582), prec))                    
                    elif cnvto == 'Calories':
                        energyansvar.set(round((energyqty * 0.324048), prec))
                    elif cnvto == 'E. Volts':
                        energyansvar.set(round(((energyqty * 1.35582) / (1.6 * (10 ** -19))) , prec))
                    elif cnvto == 'BTUs':
                        energyansvar.set(round((energyqty * 0.00128507), prec))
                    elif cnvto == 'Ft. Pounds':
                        energyansvar.set(round((energyqty), prec))

                uStatement = str('You converted ' + str(energyqty) + ' ' + str(cnvfrom) + ' to ' + energyansvar.get() + ' ' + str(cnvto) + '\n') #Usage history statement
                uHist.append(uStatement)

            except:
                energyvar.set('ERROR')
                energyansvar.set('ERROR')
                energycombo1.current(0)
                energycombo2.current(0)

        def convertCurr(): #This function is for currency conversion
            try:
                global uHist
                global uStatement

                currqty = float(currvar.get()) #Acquisition of required values and parameters
                cnvfrom = currcombo1.get()
                cnvto = currcombo2.get()

                api_key = apivar.get() #Acquisition of API key
                
                if cnvto == 'BTC': #Workaround for invalid call when converting traditional currency to bitcoin
                    base_url = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
                    main_url = base_url + "&from_currency=" + cnvto + "&to_currency=" + cnvfrom + "&apikey=" + api_key 

                    req_ob = requests.get(main_url)
                    result = req_ob.json()

                    rate = float(result["Realtime Currency Exchange Rate"] ['5. Exchange Rate'])
                    curransvar.set(round((currqty / rate), prec))
                
                else:
                    base_url = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
                    main_url = base_url + "&from_currency=" + cnvfrom + "&to_currency=" + cnvto + "&apikey=" + api_key 

                    req_ob = requests.get(main_url)
                    result = req_ob.json()

                    rate = float(result["Realtime Currency Exchange Rate"] ['5. Exchange Rate'])
                    curransvar.set(round((currqty * rate), prec))

                uStatement = str('You converted ' + str(currqty) + ' ' + str(cnvfrom) + ' to ' + curransvar.get() + ' ' + str(cnvto) + '\n') #Usage history statement
                uHist.append(uStatement)                

            except:
                apivar.set('ERROR')
                currvar.set('ERROR')
                curransvar.set('ERROR')
                currcombo1.current(0)
                currcombo2.current(0)

        def getKey(): #This function lets user get API key
            try:

                url = 'https://www.alphavantage.co/support/' 

                webbrowser.open_new(url) #Opens url in new tab
            
            except:
                apivar.set('ERROR')
                currvar.set('ERROR')
                curransvar.set('ERROR')
                currcombo1.current(0)
                currcombo2.current(0)

        def resetMass(): #This function resets mass converter
            massfield.delete(0, 'end')
            massvar.set('Enter Mass')
            massansfield.delete(0, 'end')
            massansvar.set('Answer Here')
            masscombo1.current(0)
            masscombo2.current(0)

        def resetLen(): #This function resets length converter
            lenfield.delete(0, 'end')
            lenvar.set('Enter Length')
            lenansfield.delete(0, 'end')
            lenansvar.set('Answer Here')
            lencombo1.current(0)
            lencombo2.current(0)

        def resetTemp(): #This function resets temperature converter
            tempfield.delete(0, 'end')
            tempvar.set('Enter Temperature')
            tempansfield.delete(0, 'end')
            tempansvar.set('Answer Here')
            tempcombo1.current(0)
            tempcombo2.current(0)

        def resetFluid(): #This function resets fluid volume converter
            fluidfield.delete(0, 'end')
            fluidvar.set('Enter Volume')
            fluidansfield.delete(0, 'end')
            fluidansvar.set('Answer Here')
            fluidcombo1.current(0)
            fluidcombo2.current(0)

        def resetEnergy(): #This function resets energy converter
            energyfield.delete(0, 'end')
            energyvar.set('Enter Energy')
            energyansfield.delete(0, 'end')
            energyansvar.set('Answer Here')
            energycombo1.current(0)
            energycombo2.current(0)

        def resetCurr(): #This function resets currency converter
            currfield.delete(0, 'end')
            currvar.set('Enter Amount')
            curransfield.delete(0, 'end')
            curransvar.set('Answer Here')
            currcombo1.current(0)
            currcombo2.current(0)

        def msclick1(event): #This function is to empty massfield upon mouse click
            massfield.delete(0, 'end')
            return None

        def msclick2(event): #Above function for lenfield
            lenfield.delete(0, 'end')
            return None

        def msclick3(event): #Above function for tempfield
            tempfield.delete(0, 'end')
            return None

        def msclick4(event): #Above function for fluidfield
            fluidfield.delete(0, 'end')
            return None

        def msclick5(event): #Above function for energyfield
            energyfield.delete(0, 'end')
            return None

        def msclick6(event): #Above function for apifield
            apifield.delete(0, 'end')
            return None

        def msclick7(event): #Above function for currfield
            currfield.delete(0, 'end')
            return None

        massvar = tk.StringVar() #These variables are the text variables for all the Entry fields
        massvar.set('Enter Mass')
        massansvar = tk.StringVar()
        massansvar.set('Answer Here')
        lenvar = tk.StringVar()
        lenvar.set('Enter Length')
        lenansvar = tk.StringVar()
        lenansvar.set('Answer Here')
        tempvar = tk.StringVar()
        tempvar.set('Enter Temperature')
        tempansvar = tk.StringVar()
        tempansvar.set('Answer Here')
        fluidvar = tk.StringVar()
        fluidvar.set('Enter Volume')
        fluidansvar = tk.StringVar()
        fluidansvar.set('Answer Here')
        energyvar = tk.StringVar()
        energyvar.set('Enter Energy')
        energyansvar = tk.StringVar()
        energyansvar.set('Answer Here')
        apivar = tk.StringVar()
        apivar.set('Enter API Key Here')
        currvar = tk.StringVar()
        currvar.set('Enter Amount')
        curransvar = tk.StringVar()
        curransvar.set('Answer Here')

        backbutton = ttk.Button(self, text = 'Back', style = 'btn.TButton', command = lambda: controller.show_frame(ChoicePage)) #This button takes us to the previous page
        backbutton.grid(row = 0, column = 2, padx = 10, pady = 20, sticky = 'e')

        histbutton = ttk.Button(self, text = 'History', style = 'btn.TButton', command = lambda: controller.show_frame(HistPage)) #This button takes us to the usage history page
        histbutton.grid(row = 0, column = 0, padx = 10, pady = 20, sticky = 'w')

        label = tk.Label(self, text = 'Converter', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title label
        label.grid(row = 0, column = 1, pady = 10)

        leftlf = tk.LabelFrame(self, text = 'Mass, Length & Temperature:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains all the stuff to be used for taking inputs for graphs
        leftlf.grid(row = 1, column = 0, padx = 10, pady = 10)

        masslabel = tk.Label(leftlf, text = 'Mass:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Mass label
        masslabel.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'w')

        massfield = tk.Entry(leftlf, width = 14, textvariable = massvar, font = LargeFont) #This entry field takes mass input
        massfield.grid(row = 1, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)
        massfield.bind('<Button-1>', msclick1)

        s = ttk.Style() #Style for combo boxes
        s.map('TCombobox', fieldbackground = [('readonly','white')])
        s.map('TCombobox', selectbackground = [('readonly', 'white')])
        s.map('TCombobox', selectforeground = [('readonly', 'black')])

        masscombo1 = ttk.Combobox(leftlf, width = 9, font = LargeFont, values = ['From...', 'Kilograms', 'Grams', 'Pounds', 'Ounces'], state = 'readonly') #Mass combo boxes
        masscombo1.current(0)        
        masscombo1.grid(row = 1, column = 1, ipadx = 1, ipady = 3, padx = 5, pady = 5) 

        masscombo2 = ttk.Combobox(leftlf, width = 9, font = LargeFont, values = ['To...', 'Kilograms', 'Grams', 'Pounds', 'Ounces'], state = 'readonly') 
        masscombo2.current(0)        
        masscombo2.grid(row = 1, column = 2, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        massansfield = tk.Entry(leftlf, width = 14, textvariable = massansvar, font = LargeFont, state = 'readonly') #Answer is displayed here
        massansfield.grid(row = 2, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        resetmassbtn = ttk.Button(leftlf, text = 'Reset', style = 'btn.TButton', command = lambda: resetMass()) #This button resets mass
        resetmassbtn.grid(row = 1, column = 3, padx = 5, pady = 5)
        resetmassbtn.config(width = 7)

        massbtn = ttk.Button(leftlf, text = 'Convert', style = 'btn.TButton', command = lambda: convertMass()) #This button converts mass
        massbtn.grid(row = 2, column = 3, padx = 5, pady = 5)
        massbtn.config(width = 7)

        lenlabel = tk.Label(leftlf, text = 'Length:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Length label
        lenlabel.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'w')

        lenfield = tk.Entry(leftlf, width = 14, textvariable = lenvar, font = LargeFont) #This entry field takes length input
        lenfield.grid(row = 4, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)
        lenfield.bind('<Button-1>', msclick2)

        lencombo1 = ttk.Combobox(leftlf, width = 9, font = LargeFont, values = ['From...', 'Kilometres', 'Metres', 'Miles', 'Yards', 'Feet', 'Inches'], state = 'readonly') #Length combo boxes
        lencombo1.current(0)        
        lencombo1.grid(row = 4, column = 1, ipadx = 1, ipady = 3, padx = 5, pady = 5) 

        lencombo2 = ttk.Combobox(leftlf, width = 9, font = LargeFont, values = ['To...', 'Kilometres', 'Metres', 'Miles', 'Yards', 'Feet', 'Inches'], state = 'readonly') 
        lencombo2.current(0)        
        lencombo2.grid(row = 4, column = 2, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        lenansfield = tk.Entry(leftlf, width = 14, textvariable = lenansvar, font = LargeFont, state = 'readonly') #Answer is displayed here
        lenansfield.grid(row = 5, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        resetlenbtn = ttk.Button(leftlf, text = 'Reset', style = 'btn.TButton', command = lambda: resetLen()) #This button resets length
        resetlenbtn.grid(row = 4, column = 3, padx = 5, pady = 5)
        resetlenbtn.config(width = 7)

        lenbtn = ttk.Button(leftlf, text = 'Convert', style = 'btn.TButton', command = lambda: convertLen()) #This button converts length
        lenbtn.grid(row = 5, column = 3, padx = 5, pady = 5)
        lenbtn.config(width = 7)      

        templabel = tk.Label(leftlf, text = 'Temperature:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Temperature label
        templabel.grid(row = 6, column = 0, padx = 10, pady = 5, sticky = 'w')

        tempfield = tk.Entry(leftlf, width = 14, textvariable = tempvar, font = LargeFont) #This entry field takes temperature input
        tempfield.grid(row = 7, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)
        tempfield.bind('<Button-1>', msclick3)

        tempcombo1 = ttk.Combobox(leftlf, width = 9, font = LargeFont, values = ['From...', 'Celsius', 'Fahrenheit', 'Kelvin'], state = 'readonly') #Temperature combo boxes
        tempcombo1.current(0)        
        tempcombo1.grid(row = 7, column = 1, ipadx = 1, ipady = 3, padx = 5, pady = 5) 

        tempcombo2 = ttk.Combobox(leftlf, width = 9, font = LargeFont, values = ['To...', 'Celsius', 'Fahrenheit', 'Kelvin'], state = 'readonly') 
        tempcombo2.current(0)        
        tempcombo2.grid(row = 7, column = 2, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        tempansfield = tk.Entry(leftlf, width = 14, textvariable = tempansvar, font = LargeFont, state = 'readonly') #Answer is displayed here
        tempansfield.grid(row = 8, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        resettempbtn = ttk.Button(leftlf, text = 'Reset', style = 'btn.TButton', command = lambda: resetTemp()) #This button resets temperature
        resettempbtn.grid(row = 7, column = 3, padx = 5, pady = 5)
        resettempbtn.config(width = 7)

        tempbtn = ttk.Button(leftlf, text = 'Convert', style = 'btn.TButton', command = lambda: convertTemp()) #This button converts temperature
        tempbtn.grid(row = 8, column = 3, padx = 5, pady = 5)
        tempbtn.config(width = 7)

        rightlf = tk.LabelFrame(self, text = 'Fluids, Energy & Currency:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #Placeholder label
        rightlf.grid(row = 1, column = 2, padx = 10, pady = 10)

        fluidlabel = tk.Label(rightlf, text = 'Fluid Volume:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Fluid label
        fluidlabel.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'w')        

        fluidfield = tk.Entry(rightlf, width = 14, textvariable = fluidvar, font = LargeFont) #This entry field takes fluid input
        fluidfield.grid(row = 1, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)
        fluidfield.bind('<Button-1>', msclick4)

        fluidcombo1 = ttk.Combobox(rightlf, width = 9, font = LargeFont, values = ['From...', 'Litres', 'Mililitres', 'US Gallons', 'US Fl. Oz', 'IMP Gallons', 'IMP Fl. Oz'], state = 'readonly') #Fluid combo boxes
        fluidcombo1.current(0)        
        fluidcombo1.grid(row = 1, column = 1, ipadx = 1, ipady = 3, padx = 5, pady = 5) 

        fluidcombo2 = ttk.Combobox(rightlf, width = 9, font = LargeFont, values = ['To...', 'Litres', 'Mililitres', 'US Gallons', 'US Fl. Oz', 'IMP Gallons', 'IMP Fl. Oz'], state = 'readonly') 
        fluidcombo2.current(0)        
        fluidcombo2.grid(row = 1, column = 2, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        fluidansfield = tk.Entry(rightlf, width = 14, textvariable = fluidansvar, font = LargeFont, state = 'readonly') #Answer is displayed here
        fluidansfield.grid(row = 2, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        resetfluidbtn = ttk.Button(rightlf, text = 'Reset', style = 'btn.TButton', command = lambda: resetFluid()) #This button resets fluid volume
        resetfluidbtn.grid(row = 1, column = 3, padx = 5, pady = 5)
        resetfluidbtn.config(width = 7)

        fluidbtn = ttk.Button(rightlf, text = 'Convert', style = 'btn.TButton', command = lambda: convertFluid()) #This button converts fluid volume
        fluidbtn.grid(row = 2, column = 3, padx = 5, pady = 5)
        fluidbtn.config(width = 7)

        energylabel = tk.Label(rightlf, text = 'Energy:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Energy label
        energylabel.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'w')        

        energyfield = tk.Entry(rightlf, width = 14, textvariable = energyvar, font = LargeFont) #This entry field takes energy input
        energyfield.grid(row = 4, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)
        energyfield.bind('<Button-1>', msclick5)

        energycombo1 = ttk.Combobox(rightlf, width = 9, font = LargeFont, values = ['From...', 'Joules', 'Calories', 'E. Volts', 'BTUs', 'Ft. Pounds'], state = 'readonly') #Energy combo boxes
        energycombo1.current(0)        
        energycombo1.grid(row = 4, column = 1, ipadx = 1, ipady = 3, padx = 5, pady = 5) 

        energycombo2 = ttk.Combobox(rightlf, width = 9, font = LargeFont, values = ['To...', 'Joules', 'Calories', 'E. Volts', 'BTUs', 'Ft. Pounds'], state = 'readonly') 
        energycombo2.current(0)        
        energycombo2.grid(row = 4, column = 2, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        energyansfield = tk.Entry(rightlf, width = 14, textvariable = energyansvar, font = LargeFont, state = 'readonly') #Answer is displayed here
        energyansfield.grid(row = 5, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        resetenergybtn = ttk.Button(rightlf, text = 'Reset', style = 'btn.TButton', command = lambda: resetEnergy()) #This button resets energy
        resetenergybtn.grid(row = 4, column = 3, padx = 5, pady = 5)
        resetenergybtn.config(width = 7)

        energybtn = ttk.Button(rightlf, text = 'Convert', style = 'btn.TButton', command = lambda: convertEnergy()) #This button converts energy
        energybtn.grid(row = 5, column = 3, padx = 5, pady = 5)
        energybtn.config(width = 7)

        currlabel = tk.Label(rightlf, text = 'Currency:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Currency label
        currlabel.grid(row = 6, column = 0, padx = 10, pady = 5, sticky = 'w')        

        apifield = tk.Entry(rightlf, width = 23, textvariable = apivar, font = LargeFont) #This entry field takes API input
        apifield.grid(row = 6, column = 1, columnspan = 2, ipadx = 1, ipady = 3, padx = 5, pady = 5, sticky = 'e')
        apifield.bind('<Button-1>', msclick6)

        currfield = tk.Entry(rightlf, width = 14, textvariable = currvar, font = LargeFont) #This entry field takes currency input
        currfield.grid(row = 7, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)
        currfield.bind('<Button-1>', msclick7)

        currcombo1 = ttk.Combobox(rightlf, width = 9, font = LargeFont, values = ['From...', 'USD', 'CAD', 'GBP', 'EUR', 'RUB', 'ZAR', 'INR', 'JPY', 'HKD', 'CNY', 'AUD', 'NZD', 'BTC'], state = 'readonly') #Currency combo boxes
        currcombo1.current(0)        
        currcombo1.grid(row = 7, column = 1, ipadx = 1, ipady = 3, padx = 5, pady = 5) 

        currcombo2 = ttk.Combobox(rightlf, width = 9, font = LargeFont, values = ['To...', 'USD', 'CAD', 'GBP', 'EUR', 'RUB', 'ZAR', 'INR', 'JPY', 'HKD', 'CNY', 'AUD', 'NZD', 'BTC'], state = 'readonly') 
        currcombo2.current(0)        
        currcombo2.grid(row = 7, column = 2, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        curransfield = tk.Entry(rightlf, width = 14, textvariable = curransvar, font = LargeFont, state = 'readonly') #Answer is displayed here
        curransfield.grid(row = 8, column = 0, ipadx = 1, ipady = 3, padx = 5, pady = 5)

        apibtn = ttk.Button(rightlf, text = 'Get Key', style = 'btn.TButton', command = lambda: getKey()) #This button redirects to alpha vantage website to get API key
        apibtn.grid(row = 6, column = 3, padx = 5, pady = 5)
        apibtn.config(width = 7)

        resetcurrbtn = ttk.Button(rightlf, text = 'Reset', style = 'btn.TButton', command = lambda: resetCurr()) #This button resets currency
        resetcurrbtn.grid(row = 7, column = 3, padx = 5, pady = 5)
        resetcurrbtn.config(width = 7)

        currbtn = ttk.Button(rightlf, text = 'Convert', style = 'btn.TButton', command = lambda: convertCurr()) #This button converts currency
        currbtn.grid(row = 8, column = 3, padx = 5, pady = 5)
        currbtn.config(width = 7)

class ComplexPage(tk.Frame): #This class is for the Complex & Equations page

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831')

        def compArithPhase(): #This function calculates phase
            try:
                global uHist
                global uStatement

                real = float(realfield.get()) #Acquisition of required values
                imag = float(imagfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                phase = round((cmath.phase(z)), prec) #Phase is calculated in radians

                comparithansvar.set(phase) #Phase is displayed

                uStatement = str('You calculated phase of ' + realfield.get() + ' + ' + imagfield.get() + 'i, which is ' + comparithansfield.get() +' radians' + '\n') #Usage history statement
                uHist.append(uStatement)
            
            except:
                realvar.set('ERROR')
                imagvar.set('ERROR')
                comparithansvar.set('ERROR')

        def compArithModulus(): #This function calculates modulus
            try:
                global uHist
                global uStatement

                real = float(realfield.get()) #Acquisition of required values
                imag = float(imagfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                mod = round((abs(z)), prec) #Modulus is calculated 

                comparithansvar.set(mod) #Modulus is displayed

                uStatement = str('You calculated modulus of ' + realfield.get() + ' + ' + imagfield.get() + 'i, which is ' + comparithansfield.get() + '\n') #Usage history statement
                uHist.append(uStatement)
            
            except:
                realvar.set('ERROR')
                imagvar.set('ERROR')
                comparithansvar.set('ERROR')

        def compArithLoge(): #This function calculates natural log
            try:
                global uHist
                global uStatement

                real = float(realfield.get()) #Acquisition of required values
                imag = float(imagfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                loge = np.around((cmath.log(z, evar)), prec) #Natural log is calculated 

                comparithansvar.set(loge) #Natural log is displayed

                uStatement = str('You calculated natural log of ' + realfield.get() + ' + ' + imagfield.get() + 'i, which is ' + comparithansfield.get() + '\n') #Usage history statement
                uHist.append(uStatement)
            
            except:
                realvar.set('ERROR')
                imagvar.set('ERROR')
                comparithansvar.set('ERROR')

        def compArithLogx(): #This function calculates log base x
            try:
                global uHist
                global uStatement

                real = float(realfield.get()) #Acquisition of required values
                imag = float(imagfield.get())
                base = float(logbasefield.get())
                z = complex(real, imag) #User input is converted into python complex number

                logx = np.around((cmath.log(z, base)), prec) #Log base x is calculated 

                comparithansvar.set(logx) #Log base x is displayed

                uStatement = str('You calculated log base ' + logbasefield.get() + ' of ' + realfield.get() + ' + ' + imagfield.get() + 'i, which is ' + comparithansfield.get() + '\n') #Usage history statement
                uHist.append(uStatement)
            
            except:
                realvar.set('ERROR')
                imagvar.set('ERROR')
                logbasevar.set('ERROR')
                comparithansvar.set('ERROR')

        def compTrigSin(): #This function calculates sin
            try:
                global uHist
                global uStatement

                real = float(realtrigfield.get()) #Acquisition of required values
                imag = float(imagtrigfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                ans = np.around(cmath.sin(z), prec)
                
                comptrigansvar.set(ans)

                uStatement = str('You calculated sine of ' + realtrigfield.get() + ' + ' + imagtrigfield.get() + 'i, which is ' + comptrigansfield.get() + '\n')
                uHist.append(uStatement)

            except:
                realtrigvar.set('ERROR')
                imagtrigvar.set('ERROR')
                comptrigansvar.set('ERROR')                                 

        def compTrigAsin(): #This function calculates arcsin
            try:
                global uHist
                global uStatement

                real = float(realtrigfield.get()) #Acquisition of required values
                imag = float(imagtrigfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                ans = np.around(cmath.asin(z), prec)
                
                comptrigansvar.set(ans)

                uStatement = str('You calculated arcsine of ' + realtrigfield.get() + ' + ' + imagtrigfield.get() + 'i, which is ' + comptrigansfield.get() + '\n')
                uHist.append(uStatement)

            except:
                realtrigvar.set('ERROR')
                imagtrigvar.set('ERROR')
                comptrigansvar.set('ERROR')   

        def compTrigCos(): #This function calculates cos
            try:
                global uHist
                global uStatement

                real = float(realtrigfield.get()) #Acquisition of required values
                imag = float(imagtrigfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                ans = np.around(cmath.cos(z), prec)
                
                comptrigansvar.set(ans)

                uStatement = str('You calculated cosine of ' + realtrigfield.get() + ' + ' + imagtrigfield.get() + 'i, which is ' + comptrigansfield.get() + '\n')
                uHist.append(uStatement)

            except:
                realtrigvar.set('ERROR')
                imagtrigvar.set('ERROR')
                comptrigansvar.set('ERROR')                                 

        def compTrigAcos(): #This function calculates arccos
            try:
                global uHist
                global uStatement

                real = float(realtrigfield.get()) #Acquisition of required values
                imag = float(imagtrigfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                ans = np.around(cmath.acos(z), prec)
                
                comptrigansvar.set(ans)

                uStatement = str('You calculated arccosine of ' + realtrigfield.get() + ' + ' + imagtrigfield.get() + 'i, which is ' + comptrigansfield.get() + '\n')
                uHist.append(uStatement)

            except:
                realtrigvar.set('ERROR')
                imagtrigvar.set('ERROR')
                comptrigansvar.set('ERROR') 

        def compTrigTan(): #This function calculates tan
            try:
                global uHist
                global uStatement

                real = float(realtrigfield.get()) #Acquisition of required values
                imag = float(imagtrigfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                ans = np.around(cmath.tan(z), prec)
                
                comptrigansvar.set(ans)

                uStatement = str('You calculated tangent of ' + realtrigfield.get() + ' + ' + imagtrigfield.get() + 'i, which is ' + comptrigansfield.get() + '\n')
                uHist.append(uStatement)

            except:
                realtrigvar.set('ERROR')
                imagtrigvar.set('ERROR')
                comptrigansvar.set('ERROR')                                 

        def compTrigAtan(): #This function calculates arctan
            try:
                global uHist
                global uStatement

                real = float(realtrigfield.get()) #Acquisition of required values
                imag = float(imagtrigfield.get())
                z = complex(real, imag) #User input is converted into python complex number

                ans = np.around(cmath.atan(z), prec)
                
                comptrigansvar.set(ans)

                uStatement = str('You calculated arctangent of ' + realtrigfield.get() + ' + ' + imagtrigfield.get() + 'i, which is ' + comptrigansfield.get() + '\n')
                uHist.append(uStatement)

            except:
                realtrigvar.set('ERROR')
                imagtrigvar.set('ERROR')
                comptrigansvar.set('ERROR') 

        def resetCompArith(): #This function resets complex arithmetic
            realfield.delete(0, 'end')
            realvar.set('Enter Real Part')
            imagfield.delete(0, 'end')
            imagvar.set('Enter Imaginary Part')
            comparithansfield.delete(0, 'end')
            comparithansvar.set('Answer Here')

        def resetCompTrig(): #This function resets complex trigonometry
            realtrigfield.delete(0, 'end')
            realtrigvar.set('Enter Real Part')
            imagtrigfield.delete(0, 'end')
            imagtrigvar.set('Enter Imaginary Part')
            comptrigansfield.delete(0, 'end')
            comptrigansvar.set('Answer Here')

        def solveEquations(): #This function solves user's equations
            try:
                global uHist
                global uStatement

                varcount = varcombo.get() #Number of variables and thus equations is taken

                if varcount == '1': #In case of 1 variable
                    var1 = Symbol(varfield1.get()) #Taking equation variable

                    eqn1 = eqnfield1.get() #Taking equation

                    ans = solve((eqn1), (var1), dict = True) #Solving equation

                    eqnansvar1.set(round(ans[0][var1], prec)) #Displaying output

                    uStatement = str('You solved ' + varcount + ' equation ' + eqn1 + ' where ' + varfield1.get() + ' = ' + eqnansfield1.get() + '\n') #Usage history statement
                    uHist.append(uStatement)

                    ans.clear() #Clearing ans dictionary for next operation

                elif varcount == '2': #In case of 2 variables
                    var1 = Symbol(varfield1.get()) #Taking equation variables
                    var2 = Symbol(varfield2.get())

                    eqn1 = eqnfield1.get() #Taking equations
                    eqn2 = eqnfield2.get()

                    ans = solve((eqn1, eqn2), (var1, var2), dict = True) #Solving equations

                    eqnansvar1.set(round(ans[0][var1], prec)) #Displaying output
                    eqnansvar2.set(round(ans[0][var2], prec))

                    uStatement = str('You solved ' + varcount + ' equations ' + eqn1 + ', ' + eqn2 + ' where ' + varfield1.get() + ' = ' + eqnansfield1.get() + ', ' + varfield2.get() + ' = ' + eqnansfield2.get() + '\n') #Usage history statement
                    uHist.append(uStatement)

                    ans.clear()

                elif varcount == '3': #In case of 3 variables
                    var1 = Symbol(varfield1.get()) #Taking equation variables
                    var2 = Symbol(varfield2.get())
                    var3 = Symbol(varfield3.get())

                    eqn1 = eqnfield1.get() #Taking equations
                    eqn2 = eqnfield2.get()
                    eqn3 = eqnfield3.get()

                    ans = solve((eqn1, eqn2, eqn3), (var1, var2, var3), dict = True) #Solving equations

                    eqnansvar1.set(round(ans[0][var1], prec)) #Displaying output
                    eqnansvar2.set(round(ans[0][var2], prec))
                    eqnansvar3.set(round(ans[0][var3], prec))

                    uStatement = str('You solved ' + varcount + ' equations ' + eqn1 + ', ' + eqn2 + ' where ' + varfield1.get() + ' = ' + eqnansfield1.get() + ', ' + varfield2.get() + ' = ' + eqnansfield2.get() + ', ' + varfield3.get() + ' = ' + eqnansfield3.get() + '\n') #Usage history statement
                    uHist.append(uStatement)

                    ans.clear()

                elif varcount == '4': #In case of 4 variables
                    var1 = Symbol(varfield1.get()) #Taking equation variables
                    var2 = Symbol(varfield2.get())
                    var3 = Symbol(varfield3.get())
                    var4 = Symbol(varfield4.get())

                    eqn1 = eqnfield1.get() #Taking equations
                    eqn2 = eqnfield2.get()
                    eqn3 = eqnfield3.get()
                    eqn4 = eqnfield4.get()

                    ans = solve((eqn1, eqn2, eqn3, eqn4), (var1, var2, var3, var4), dict = True) #Solving equations

                    eqnansvar1.set(round(ans[0][var1], prec)) #Displaying output
                    eqnansvar2.set(round(ans[0][var2], prec))
                    eqnansvar3.set(round(ans[0][var3], prec))
                    eqnansvar4.set(round(ans[0][var4], prec))

                    uStatement = str('You solved ' + varcount + ' equations ' + eqn1 + ', ' + eqn2 + ' where ' + varfield1.get() + ' = ' + eqnansfield1.get() + ', ' + varfield2.get() + ' = ' + eqnansfield2.get() + ', ' + varfield3.get() + ' = ' + eqnansfield3.get() + ', ' + varfield4.get() + ' = ' + eqnansfield4.get() + '\n') #Usage history statement
                    uHist.append(uStatement)

                    ans.clear()

            except:
                eqnansvar1.set('ERROR')
                eqnansvar2.set('ERROR')
                eqnansvar3.set('ERROR')
                eqnansvar4.set('ERROR')

        def resetEquations(): #This function resets equation solver
            varfield1.delete(0, 'end')        
            eqnvar1.set('Enter 1st Variable')        
            varfield2.delete(0, 'end')        
            eqnvar2.set('Enter 2nd Variable')       
            varfield3.delete(0, 'end')        
            eqnvar3.set('Enter 3rd Variable')        
            varfield4.delete(0, 'end')        
            eqnvar4.set('Enter 4th Variable')
            eqnfield1.delete(0, 'end')
            eqn1.set('Enter 1st Equation')
            eqnfield2.delete(0, 'end')
            eqn2.set('Enter 2nd Equation')
            eqnfield3.delete(0, 'end')
            eqn3.set('Enter 3rd Equation')
            eqnfield4.delete(0, 'end')
            eqn4.set('Enter 4th Equation')
            eqnansfield1.delete(0, 'end')
            eqnansvar1.set('1st Variable Value')
            eqnansfield2.delete(0, 'end')
            eqnansvar2.set('2nd Variable Value')
            eqnansfield3.delete(0, 'end')
            eqnansvar3.set('3rd Variable Value')
            eqnansfield4.delete(0, 'end')
            eqnansvar4.set('4th Variable Value')
            varcombo.current(0)

        def msclick1(event): #This function is to empty realfield upon mouse click
            realfield.delete(0, 'end')
            return None

        def msclick2(event): #Above function for imagfield
            imagfield.delete(0, 'end')
            return None

        def msclick3(event): #Above function for varfield1
            varfield1.delete(0, 'end')
            return None

        def msclick4(event): #Above function for varfield2
            varfield2.delete(0, 'end')
            return None

        def msclick5(event): #Above function for varfield3
            varfield3.delete(0, 'end')
            return None

        def msclick6(event): #Above function for varfield4
            varfield4.delete(0, 'end')
            return None

        def msclick7(event): #Above function for eqnfield1
            eqnfield1.delete(0, 'end')
            return None

        def msclick8(event): #Above function for eqnfield2
            eqnfield2.delete(0, 'end')
            return None

        def msclick9(event): #Above function for eqnfield3
            eqnfield3.delete(0, 'end')
            return None

        def msclick10(event): #Above function for eqnfield4
            eqnfield4.delete(0, 'end')
            return None

        def msclick11(event): #Above function for logbasefield
            logbasefield.delete(0, 'end')
            return None

        def msclick12(event): #Above function for realtrigfield
            realtrigfield.delete(0, 'end')
            return None

        def msclick13(event): #Above function for imagtrigfield
            imagtrigfield.delete(0, 'end')
            return None

        realvar = tk.StringVar() #These variables are the text variables for all the Entry fields
        realvar.set('Enter Real Part')
        imagvar = tk.StringVar()
        imagvar.set('Enter Imaginary Part')
        logbasevar = tk.StringVar()
        logbasevar.set('Enter Log Base')
        comparithansvar = tk.StringVar()
        comparithansvar.set('Answer Here')
        realtrigvar = tk.StringVar() 
        realtrigvar.set('Enter Real Part')
        imagtrigvar = tk.StringVar()
        imagtrigvar.set('Enter Imaginary Part')
        comptrigansvar = tk.StringVar()
        comptrigansvar.set('Answer Here')
        eqnvar1 = tk.StringVar()
        eqnvar1.set('Enter 1st Variable')
        eqnvar2 = tk.StringVar()
        eqnvar2.set('Enter 2nd Variable')
        eqnvar3 = tk.StringVar()
        eqnvar3.set('Enter 3rd Variable')
        eqnvar4 = tk.StringVar()
        eqnvar4.set('Enter 4th Variable')
        eqn1 = tk.StringVar()
        eqn1.set('Enter 1st Equation')
        eqn2 = tk.StringVar()
        eqn2.set('Enter 2nd Equation')
        eqn3 = tk.StringVar()
        eqn3.set('Enter 3rd Equation')
        eqn4 = tk.StringVar()
        eqn4.set('Enter 4th Equation')
        eqnansvar1 = tk.StringVar()
        eqnansvar1.set('1st Variable Value')
        eqnansvar2 = tk.StringVar()
        eqnansvar2.set('2nd Variable Value')
        eqnansvar3 = tk.StringVar()
        eqnansvar3.set('3rd Variable Value')
        eqnansvar4 = tk.StringVar()
        eqnansvar4.set('4th Variable Value')

        label1 = tk.Label(self, text = 'Complex No.s &', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title Label
        label1.grid(row = 0, column = 1, padx = 0, pady = 0)

        label2 = tk.Label(self, text = 'Equations', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title Label
        label2.grid(row = 1, column = 1, padx = 0, pady = 0, sticky = 'n')

        backbutton = ttk.Button(self, text = 'Back', style = 'btn.TButton', command = lambda: controller.show_frame(ChoicePage)) #This button takes us to the previous page
        backbutton.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = 'e')

        histbutton = ttk.Button(self, text = 'History', style = 'btn.TButton', command = lambda: controller.show_frame(HistPage)) #This button takes us to the usage history page
        histbutton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')

        complf = tk.LabelFrame(self, text = 'Complex Numbers:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains complex operations
        complf.grid(row = 1, column = 0, padx = 10, pady = 10)

        complabel = tk.Label(complf, text = 'Complex Arithmetic:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Label for complex arithmetic
        complabel.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')

        realfield = tk.Entry(complf, font = LargeFont, width = 17, textvariable = realvar) #This field takes real part of complex number
        realfield.grid(row = 1, column = 0, ipadx = 1, ipady = 3, padx = 1.5, pady = 7.5)
        realfield.bind('<Button-1>', msclick1)

        imagfield = tk.Entry(complf, font = LargeFont, width = 17, textvariable = imagvar) #This field takes imaginary part of complex number
        imagfield.grid(row = 1, column = 1, ipadx = 1, ipady = 3, padx = 1.5, pady = 7.5)
        imagfield.bind('<Button-1>', msclick2)

        logbasefield = tk.Entry(complf, font = LargeFont, width = 17, textvariable = logbasevar) #This field takes custom base of log
        logbasefield.grid(row = 0, column = 1, ipadx = 1, ipady = 3, padx = 1.5, pady = 7.5)
        logbasefield.bind('<Button-1>', msclick11)

        comparithansfield = tk.Entry(complf, font = LargeFont, width = 17, textvariable = comparithansvar, state = 'readonly') #This field shows complex arithmetic output
        comparithansfield.grid(row = 2, column = 0, ipadx = 1, ipady = 3, padx = 2.5, pady = 7.5)

        resetcomparithbtn = ttk.Button(complf, text = 'Reset', style = 'btn.TButton', command = lambda: resetCompArith()) #This button resets complex arithmetic
        resetcomparithbtn.grid(row = 0, column = 2, padx = 5, pady = 5)
        resetcomparithbtn.config(width = 8)

        phasebtn = ttk.Button(complf, text = 'Phase', style = 'btn.TButton', command = lambda: compArithPhase()) #This button is for phase calculation
        phasebtn.grid(row = 1, column = 2, padx = 5, pady = 5)
        phasebtn.config(width = 8)

        absbtn = ttk.Button(complf, text = 'Modulus', style = 'btn.TButton', command = lambda: compArithModulus()) #This button is for modulus calculation
        absbtn.grid(row = 2, column = 2, padx = 5, pady = 5)
        absbtn.config(width = 8)

        logebtn = ttk.Button(complf, text = 'Log (e)', style = 'btn.TButton', command = lambda: compArithLoge()) #This button is for natural log calculation
        logebtn.grid(row = 2, column = 1, padx = 2, pady = 5, sticky = 'w')
        logebtn.config(width = 8)

        logxbtn = ttk.Button(complf, text = 'Log (x)', style = 'btn.TButton', command = lambda: compArithLogx()) #This button is for log base x calculation
        logxbtn.grid(row = 2, column = 1, padx = 2, pady = 5, sticky = 'e')
        logxbtn.config(width = 8)

        comptriglabel = tk.Label(complf, text = 'Trigonometry:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Label for complex trigonometry
        comptriglabel.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'w')

        realtrigfield = tk.Entry(complf, font = LargeFont, width = 17, textvariable = realtrigvar) #This field takes real part of complex number
        realtrigfield.grid(row = 4, column = 0, ipadx = 1, ipady = 3, padx = 1.5, pady = 7.5)
        realtrigfield.bind('<Button-1>', msclick12)

        imagtrigfield = tk.Entry(complf, font = LargeFont, width = 17, textvariable = imagtrigvar) #This field takes imaginary part of complex number
        imagtrigfield.grid(row = 4, column = 1, ipadx = 1, ipady = 3, padx = 1.5, pady = 7.5)
        imagtrigfield.bind('<Button-1>', msclick13)

        comptrigansfield = tk.Entry(complf, font = LargeFont, width = 17, textvariable = comptrigansvar, state = 'readonly') #This field shows complex trigonometry output
        comptrigansfield.grid(row = 5, column = 0, ipadx = 1, ipady = 3, padx = 2.5, pady = 7.5)

        resetcomptrigbtn = ttk.Button(complf, text = 'Reset', style = 'btn.TButton', command = lambda: resetCompTrig()) #This button resets complex trigonometry
        resetcomptrigbtn.grid(row = 4, column = 2, padx = 5, pady = 5)
        resetcomptrigbtn.config(width = 8)

        sinbtn = ttk.Button(complf, text = 'Sin', style = 'btn.TButton', command = lambda: compTrigSin()) #This button is for sin calculation
        sinbtn.grid(row = 5, column = 1, padx = 2, pady = 5, sticky = 'w')
        sinbtn.config(width = 8)

        arcsinbtn = ttk.Button(complf, text = 'Arcsin', style = 'btn.TButton', command = lambda: compTrigAsin()) #This button is for arcsin calculation
        arcsinbtn.grid(row = 5, column = 1, padx = 2, pady = 5, sticky = 'e')
        arcsinbtn.config(width = 8)

        cosbtn = ttk.Button(complf, text = 'Cos', style = 'btn.TButton', command = lambda: compTrigCos()) #This button is for cos calculation
        cosbtn.grid(row = 6, column = 0, padx = 6, pady = 5, sticky = 'w')
        cosbtn.config(width = 8)

        arccosbtn = ttk.Button(complf, text = 'Arccos', style = 'btn.TButton', command = lambda: compTrigAcos()) #This button is for arccos calculation
        arccosbtn.grid(row = 6, column = 0, padx = 6, pady = 5, sticky = 'e')
        arccosbtn.config(width = 8)

        tanbtn = ttk.Button(complf, text = 'Tan', style = 'btn.TButton', command = lambda: compTrigTan()) #This button is for tan calculation
        tanbtn.grid(row = 6, column = 1, padx = 2, pady = 5, sticky = 'w')
        tanbtn.config(width = 8)

        arctanbtn = ttk.Button(complf, text = 'Arctan', style = 'btn.TButton', command = lambda: compTrigAtan()) #This button is for arctan calculation
        arctanbtn.grid(row = 6, column = 1, padx = 2, pady = 5, sticky = 'e')
        arctanbtn.config(width = 8)

        eqnlf = tk.LabelFrame(self, text = 'Equation Solver:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains equation solver
        eqnlf.grid(row = 1, column = 2, padx = 10, pady = 10)

        varlabel = tk.Label(eqnlf, text = 'Variables:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Variable input label
        varlabel.grid(row = 0, column = 0, padx = 3, pady = 1, sticky = 'w')   

        s = ttk.Style() #Style for combo box
        s.map('TCombobox', fieldbackground = [('readonly','white')])
        s.map('TCombobox', selectbackground = [('readonly', 'white')])
        s.map('TCombobox', selectforeground = [('readonly', 'black')])

        varcombo = ttk.Combobox(eqnlf, width = 23, font = LargeFont, values = ['How Many Variables?', '1', '2', '3', '4'], state = 'readonly') #Combo box to select number of variables
        varcombo.current(0)        
        varcombo.grid(row = 0, column = 1, columnspan = 3, ipadx = 1, ipady = 3, padx = 3, pady = 1) 

        varfield1 = tk.Entry(eqnlf, font = LargeFont, width = 16, textvariable = eqnvar1) #These entry fields take the equation variables from user
        varfield1.grid(row = 1, column = 0, ipadx = 1, ipady = 3, padx = 3, pady = 3)
        varfield1.bind('<Button-1>', msclick3)

        varfield2 = tk.Entry(eqnlf, font = LargeFont, width = 16, textvariable = eqnvar2) 
        varfield2.grid(row = 1, column = 1, ipadx = 1, ipady = 3, padx = 3, pady = 3)
        varfield2.bind('<Button-1>', msclick4)

        varfield3 = tk.Entry(eqnlf, font = LargeFont, width = 16, textvariable = eqnvar3) 
        varfield3.grid(row = 2, column = 0, ipadx = 1, ipady = 3, padx = 3, pady = 3)
        varfield3.bind('<Button-1>', msclick5)

        varfield4 = tk.Entry(eqnlf, font = LargeFont, width = 16, textvariable = eqnvar4) 
        varfield4.grid(row = 2, column = 1, ipadx = 1, ipady = 3, padx = 3, pady = 3)
        varfield4.bind('<Button-1>', msclick6)

        eqnlabel = tk.Label(eqnlf, text = 'Equations:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Equation input label
        eqnlabel.grid(row = 3, column = 0, padx = 3, pady = 1, sticky = 'w')   

        eqnfield1 = tk.Entry(eqnlf, font = LargeFont, width = 33, textvariable = eqn1) #These entry fields take the equations from user
        eqnfield1.grid(row = 4, column = 0, ipadx = 1, ipady = 3, columnspan = 3, padx = 3, pady = 3)
        eqnfield1.bind('<Button-1>', msclick7)

        eqnfield2 = tk.Entry(eqnlf, font = LargeFont, width = 33, textvariable = eqn2) 
        eqnfield2.grid(row = 5, column = 0, ipadx = 1, ipady = 3, columnspan = 3, padx = 3, pady = 3)
        eqnfield2.bind('<Button-1>', msclick8)

        eqnfield3 = tk.Entry(eqnlf, font = LargeFont, width = 33, textvariable = eqn3) 
        eqnfield3.grid(row = 6, column = 0, ipadx = 1, ipady = 3, columnspan = 3, padx = 3, pady = 3)
        eqnfield3.bind('<Button-1>', msclick9)

        eqnfield4 = tk.Entry(eqnlf, font = LargeFont, width = 33, textvariable = eqn4) 
        eqnfield4.grid(row = 7, column = 0, ipadx = 1, ipady = 3, columnspan = 3, padx = 3, pady = 3)
        eqnfield4.bind('<Button-1>', msclick10)

        reseteqnbtn = ttk.Button(eqnlf, text = 'Reset', style = 'btn.TButton', command = lambda: resetEquations()) #This button resets equation solver
        reseteqnbtn.grid(row = 3, column = 3, padx = 3, pady = 1)
        reseteqnbtn.config(width = 8)

        eqnanslabel = tk.Label(eqnlf, text = 'Answers:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Answer output label
        eqnanslabel.grid(row = 8, column = 0, padx = 3, pady = 1, sticky = 'w')

        eqnansfield1 = tk.Entry(eqnlf, font = LargeFont, width = 16, textvariable = eqnansvar1, state = 'readonly') #These fields display the values of the variables as answer
        eqnansfield1.grid(row = 9, column = 0, ipadx = 1, ipady = 3, padx = 3, pady = 3)

        eqnansfield2 = tk.Entry(eqnlf, font = LargeFont, width = 16, textvariable = eqnansvar2, state = 'readonly') 
        eqnansfield2.grid(row = 9, column = 1, ipadx = 1, ipady = 3, padx = 3, pady = 3)

        eqnansfield3 = tk.Entry(eqnlf, font = LargeFont, width = 16, textvariable = eqnansvar3, state = 'readonly') 
        eqnansfield3.grid(row = 10, column = 0, ipadx = 1, ipady = 3, padx = 3, pady = 3)

        eqnansfield4 = tk.Entry(eqnlf, font = LargeFont, width = 16, textvariable = eqnansvar4, state = 'readonly') 
        eqnansfield4.grid(row = 10, column = 1, ipadx = 1, ipady = 3, padx = 3, pady = 3)

        eqnbtn = ttk.Button(eqnlf, text = 'Solve', style = 'btn.TButton', command = lambda: solveEquations()) #This button solves user's equations
        eqnbtn.grid(row = 8, column = 3, padx = 3, pady = 1)
        eqnbtn.config(width = 8)

class HistPage(tk.Frame): #This class is for the History page

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831')

        label = tk.Label(self, text = 'Usage History', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title label
        label.grid(row = 0, column = 1, padx = 350, pady = 10, sticky = 'nsew')

        def showHist(): #This function is to print usage history in text field
            try:
                global uHist
                
                n = len(uHist)
                element = ''
                for i in reversed(range(n)):
                    element = str(element + uHist[i] + '\n')
                history.insert(tk.END, element)            
            except:
                print("\nSomething went wrong!")

        def clrpage(): #This function is to clear the contents on usage history text field
            history.delete('1.0', 'end')

        def clrhist(): #This function is to delete the usage history
            global uHist
            uHist.clear()

        history = tk.Text(self, font = LargeFont, fg = '#00adb5', bg = '#393e46', height = 20, width = 80)
        history.grid(row = 1, column = 1, padx = 40, pady = 10)

        dispbutton = ttk.Button(self, text = 'Show', style = 'btn.TButton', command = lambda: showHist()) #This button displays usage history
        dispbutton.grid(row = 0, column = 0, padx = 10, sticky = 'w')

        clrtextbtn = ttk.Button(self, text = 'Clear Page', style = 'btn.TButton', command = lambda: clrpage()) #This button clears the history page
        clrtextbtn.grid(row = 1, column = 2, padx = 10, sticky = 'e')

        clrhistbtn = ttk.Button(self, text = 'Clear History', style = 'btn.TButton', command = lambda: clrhist()) #This button deletes usage history
        clrhistbtn.grid(row = 1, column = 2, padx = 10, sticky = 'ne')

        choicebutton = ttk.Button(self, text = 'Choices', style = 'btn.TButton', command = lambda: controller.show_frame(ChoicePage)) #This button takes us to the choices page
        choicebutton.grid(row = 0, column = 2, padx = 10, sticky = 'e')        
                        
root = Calculator()

icon = Image.open(r'Images\calcicon.png') #This is to make the calculator icon utilizing PIL's modules
icon = icon.resize((64, 64), Image.ANTIALIAS) #Resize icon to desirable size
icon = ImageTk.PhotoImage(icon) #Make the icon file readable
root.iconphoto(False, icon)

menubar = tk.Menu(root)
root.config(menu = menubar)

def ariHelp(): #This function defines the help menu for arithmetic page
    arihelpmenu = tk.Toplevel(root, bg = '#222831')
    arihelpmenu.title('Arithmetic Help')
    arihelpmenu.geometry('1000x700')
    
    label = tk.Label(arihelpmenu, text = 'How to use Arithmetic Page', font = TitleFont, fg = '#00adb5', bg = '#222831') #Text to be displayed in the page
    label.grid(row = 0, column = 0, padx = 10, pady = 10)

    helplabel1 = tk.Label(arihelpmenu, text = '- The Arithmetic Page is divided into 2 sections, the traditional calculator and the special calculator.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel1.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel2 = tk.Label(arihelpmenu, text = '- On the left side, you can use the traditional calculator by using the buttons to input values, much like every other calculator.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel2.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel3 = tk.Label(arihelpmenu, text = '- On the right side, the special calculator deals with modulus, absolute and percentage calculation.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel3.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel4 = tk.Label(arihelpmenu, text = '- You can enter the values in the respective fields, and then pressing the respective buttons.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel4.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel5 = tk.Label(arihelpmenu, text = '- The answers will be displayed in the respective answer fields.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel5.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')

    ariimg = Image.open(r'Images\ariss.png') #This is to process ariss utilizing PIL's modules
    ariimg = ariimg.resize((1000, 460), Image.ANTIALIAS)
    ariimg = ImageTk.PhotoImage(ariimg)
    
    panel = tk.Label(arihelpmenu, image = ariimg) #This is to display processed ariss as a label
    panel.photo = ariimg
    panel.grid(row = 6) 

    helpicon = Image.open(r'Images\helpicon.png') #This is to make the help icon utilizing PIL's modules
    helpicon = helpicon.resize((64, 64), Image.ANTIALIAS) #Resize icon to desirable size
    helpicon = ImageTk.PhotoImage(helpicon) #Make the icon file readable
    arihelpmenu.iconphoto(False, helpicon)

def numpyHelp(): #This function defines the help menu for matrices page
    numpyhelpmenu = tk.Toplevel(root, bg = '#222831')
    numpyhelpmenu.title('Matrices & More Help')
    numpyhelpmenu.geometry('1000x700')
    
    label = tk.Label(numpyhelpmenu, text = 'How to use Matrices & More Page', font = TitleFont, fg = '#00adb5', bg = '#222831') #Text to be displayed in the page
    label.grid(row = 0, column = 0, padx = 10, pady = 10)

    helplabel1 = tk.Label(numpyhelpmenu, text = '- The Matrices & More Page is divided into 2 sections, matrix operations and trig + log section.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel1.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel2 = tk.Label(numpyhelpmenu, text = '- On the left side, the matrix operations are present.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel2.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel3 = tk.Label(numpyhelpmenu, text = '- Instructions for how to use it are provided in screenshot.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel3.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel4 = tk.Label(numpyhelpmenu, text = '- On the right side, there is trig and log section. For trig you can select degree or radian with radio buttons.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel4.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel5 = tk.Label(numpyhelpmenu, text = '- Enter inputs in respective fields and press button for operation. Answer will show in field.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel5.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')

    numpyimg = Image.open(r'Images\numpyss.png') #This is to process numpyss utilizing PIL's modules
    numpyimg = numpyimg.resize((1000, 460), Image.ANTIALIAS)
    numpyimg = ImageTk.PhotoImage(numpyimg)
    
    panel = tk.Label(numpyhelpmenu, image = numpyimg) 
    panel.photo = numpyimg
    panel.grid(row = 6)

    helpicon = Image.open(r'Images\helpicon.png') #This is to make the help icon utilizing PIL's modules
    helpicon = helpicon.resize((64, 64), Image.ANTIALIAS) #Resize icon to desirable size
    helpicon = ImageTk.PhotoImage(helpicon) #Make the icon file readable
    numpyhelpmenu.iconphoto(False, helpicon)

def matplotlibHelp(): #This function defines the help menu for graphs page
    matplotlibhelpmenu = tk.Toplevel(root, bg = '#222831')
    matplotlibhelpmenu.title('Graphs Help')
    matplotlibhelpmenu.geometry('1000x700')
    
    label = tk.Label(matplotlibhelpmenu, text = 'How to use Graphs Page', font = TitleFont, fg = '#00adb5', bg = '#222831') #Text to be displayed in the page
    label.grid(row = 0, column = 0, padx = 10, pady = 10)

    helplabel1 = tk.Label(matplotlibhelpmenu, text = '- The Graphs page takes data on the left side, labels and co-ord limits on the right side and plots the graph in the middle.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel1.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel2 = tk.Label(matplotlibhelpmenu, text = '- The first two input fields take input for line, bar, histogram and scatter plots. The other 2 fields are for pie chart.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel2.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel3 = tk.Label(matplotlibhelpmenu, text = '- Enter all X and Y coordinates sequentially with a space in the respective fields.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel3.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel4 = tk.Label(matplotlibhelpmenu, text = '- Enter labels in first field and data in second field with spaces for pie chart. Instructions for AUTC are in screenshot.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel4.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel5 = tk.Label(matplotlibhelpmenu, text = '- Enter coordinate limits of each axis, labels and graph title on the right. ', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel5.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')

    matplotlibimg = Image.open(r'Images\matplotlibss.png') #This is to process matplotlibss utilizing PIL's modules
    matplotlibimg = matplotlibimg.resize((1000, 460), Image.ANTIALIAS)
    matplotlibimg = ImageTk.PhotoImage(matplotlibimg)
    
    panel = tk.Label(matplotlibhelpmenu, image = matplotlibimg) 
    panel.photo = matplotlibimg
    panel.grid(row = 6)

    helpicon = Image.open(r'Images\helpicon.png') #This is to make the help icon utilizing PIL's modules
    helpicon = helpicon.resize((64, 64), Image.ANTIALIAS) #Resize icon to desirable size
    helpicon = ImageTk.PhotoImage(helpicon) #Make the icon file readable
    matplotlibhelpmenu.iconphoto(False, helpicon)

def converterHelp(): #This function defines the help menu for converter page
    converterhelpmenu = tk.Toplevel(root, bg = '#222831')
    converterhelpmenu.title('Graphs Help')
    converterhelpmenu.geometry('1000x700')
    
    label = tk.Label(converterhelpmenu, text = 'How to use Converter Page', font = TitleFont, fg = '#00adb5', bg = '#222831') #Text to be displayed in the page
    label.grid(row = 0, column = 0, padx = 10, pady = 10)

    helplabel1 = tk.Label(converterhelpmenu, text = '- The Converter page currently has 6 types of conversions.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel1.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel2 = tk.Label(converterhelpmenu, text = '- Enter numerical value of the quantity to be converted in the designated field.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel2.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel3 = tk.Label(converterhelpmenu, text = '- Select the original and desired unit using the drop down menu and press "Convert".', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel3.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel4 = tk.Label(converterhelpmenu, text = '- Converted value appears in answer field.', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel4.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'w')

    helplabel5 = tk.Label(converterhelpmenu, text = '- You need to get API Key for live currency converter. Click on "Get API Key" button and follow the webpage instructions. ', font = LabelFont, fg = '#00adb5', bg = '#222831')
    helplabel5.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')

    converterimg = Image.open(r'Images\converterss.png') #This is to process converterss utilizing PIL's modules
    
    converterimg = converterimg.resize((1000, 460), Image.ANTIALIAS)
    converterimg = ImageTk.PhotoImage(converterimg)
    
    panel = tk.Label(converterhelpmenu, image = converterimg) 
    panel.photo = converterimg
    panel.grid(row = 6)

    helpicon = Image.open(r'Images\helpicon.png') #This is to make the help icon utilizing PIL's modules
    helpicon = helpicon.resize((64, 64), Image.ANTIALIAS) #Resize icon to desirable size
    helpicon = ImageTk.PhotoImage(helpicon) #Make the icon file readable
    converterhelpmenu.iconphoto(False, helpicon)

helpmenu = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'Help', menu = helpmenu)
helpmenu.add_command(label = 'Arithmetic', command = lambda: ariHelp())
helpmenu.add_command(label = 'Matrices & More', command = lambda: numpyHelp())
helpmenu.add_command(label = 'Graphs', command = lambda: matplotlibHelp())
helpmenu.add_command(label = 'Converter', command = lambda: converterHelp())

root.mainloop()

