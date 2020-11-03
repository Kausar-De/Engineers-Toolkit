import tkinter as tk #For GUI
import tkinter.ttk as ttk #For styling
from PIL import ImageTk, Image #For image processing
import numpy as np #For matrix operations
import math #For math expressions

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

        tk.Tk.wm_title(self, 'Scientific Calculator') #Program title
        
        container = tk.Frame(self) #Code for main container
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {} #Code for accomodating different frames in which code will run

        for F in (StartPage, ChoicePage, ArithPage, HistPage): #Iterates through the different pages. Different page names will be added here as they are created
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
        precvar.set('Enter Precision')

        label1 = tk.Label(self, text = 'Welcome to the Calculator!', font = TitleFont, fg = '#00adb5', bg = '#222831') #These labels are for displaying the title text
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

        precifield = tk.Entry(precilf, textvariable = precvar, font = LargeFont) #This entry field displays user input and output
        precifield.grid(row = 1, column = 0, ipadx = 0.1, ipady = 3, padx = 10, pady = 10)
        precifield.bind('<Button-1>', msclick)

        precibutton = ttk.Button(precilf, text = 'SET', style = 'btn.TButton', command = lambda: setPreci())
        precibutton.grid(row = 2, column = 0, padx = 10, pady = 10)
                                
class ChoicePage(tk.Frame): #This class is for the second page, where user can choose which part of calculator to use

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg = '#222831')

        choiceslf = tk.LabelFrame(self, bg = '#222831', borderwidth = 0, highlightthickness = 0) #This label enables positioning buttons centrally
        choiceslf.grid(row = 1, column = 0, padx = 360, pady = 100)

        label = tk.Label(self, text = 'So, what are we doing?', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title label
        label.grid(row = 0, column = 0, padx = 150, pady = 10, sticky = 'nsew') 

        arithbutton = ttk.Button(choiceslf, text = 'Arithmetic', style = 'btn.TButton', command = lambda: controller.show_frame(ArithPage)) #Button to take us to arithmetic operations (PLANNED)
        arithbutton.grid(row = 0, column = 0, padx = 10, pady = 20)

        numpybutton = ttk.Button(choiceslf, text = 'Matrices & More', style = 'btn.TButton') #Button to take us to numpy operations (PLANNED)
        numpybutton.grid(row = 0, column = 1, padx = 10, pady = 20)

        graphbutton = ttk.Button(choiceslf, text = 'Graphs', style = 'btn.TButton') #Button to take us to matplotlib operations (PLANNED)
        graphbutton.grid(row = 1, column = 0, padx = 10, pady = 20)

        docsbutton = ttk.Button(choiceslf, text = 'Useful Formulae', style = 'btn.TButton') #Button to take us to documentations page (PLANNED)
        docsbutton.grid(row = 1, column = 1, padx = 10, pady = 20)

        backbutton = ttk.Button(choiceslf, text = 'Back', style = 'btn.TButton', command = lambda: controller.show_frame(StartPage)) #This button takes us to the previous page
        backbutton.grid(row = 0, column = 2, padx = 10, pady = 20)

        histbutton = ttk.Button(choiceslf, text = 'History', style = 'btn.TButton', command = lambda: controller.show_frame(HistPage)) #This button takes us to the usage history page (PLANNED)
        histbutton.grid(row = 1, column = 2, padx = 10, pady = 10)

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

        def clr(): #This function is for behaviour of CLEAR button for arithmetic
            global expression
            expression = ''
            equation.set('Enter your Input')

        def clrmod(): #This function is for behaviour of CLEAR button for modulus
            mod1var.set('Enter Dividend')
            mod2var.set('Enter Divisor')
            modansvar.set('Answer shows here')

        def clrabs(): #This function is for behaviour of CLEAR button for absolute value
            absvar.set('Enter your input')
            absansvar.set('Answer shows here')

        def clrperc(): #This function is for behaviour of CLEAR button for percentage
            perc1var.set('Enter Part')
            perc2var.set('Enter Whole')
            percansvar.set('Answer shows here')
            
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
        modansvar.set('Answer shows here')
        absansvar = tk.StringVar()
        absansvar.set('Answer shows here')
        perc1var = tk.StringVar()
        perc1var.set('Enter Part')
        perc2var = tk.StringVar()
        perc2var.set('Enter Whole')
        percansvar = tk.StringVar()
        percansvar.set('Answer shows here')        

        label = tk.Label(self, text = 'Arithmetic', font = TitleFont, fg = '#00adb5', bg = '#222831') #Title Label
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        arilf = tk.LabelFrame(self, text = 'Arithmetic:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains all the stuff for simple arithmetic
        arilf.grid(row = 1, column = 0, padx = 10, pady = 10)

        inputfield = tk.Entry(arilf, textvariable = equation, font = LargeFont, state = 'disabled') #This entry field displays user input and output
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

        btng = ttk.Button(arilf, text = 'g', style = 'btn.TButton', command = lambda: click(9.8))
        btng.grid(row = 2, column = 0, padx = 10, pady = 10)

        btnphi = ttk.Button(arilf, text = '\u03C6', style = 'btn.TButton', command = lambda: click(round(phivar, prec)))
        btnphi.grid(row = 1, column = 1, padx = 10, pady = 10)

        btnclr = ttk.Button(arilf, text = 'Clear', style = 'btn.TButton', command = lambda: clr()) #Button to clear inputfield
        btnclr.grid(row = 0, column = 3, padx = 10, pady = 10)
        
        modabslf = tk.LabelFrame(self, text = 'Modulus & Absolute:', font = LabelFont, fg = '#00adb5', bg = '#393e46') #This label frame contains everything else
        modabslf.grid(row = 1, column = 2, padx = 10, pady = 10)

        modlabel = tk.Label(modabslf, text = 'Modulus:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Modulus Label
        modlabel.grid(row = 0, column = 0, padx = 10, pady = 7.5, sticky = 'w')

        perclabel = tk.Label(modabslf, text = 'Percentage:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Percentage Label
        perclabel.grid(row = 5, column = 0, padx = 10, pady = 7.5, sticky = 'w')

        abslabel = tk.Label(modabslf, text = 'Absolute value:', font = LabelFont, fg = '#00adb5', bg = '#222831') #Absolute Value Label
        abslabel.grid(row = 3, column = 0, padx = 10, pady = 7.5, sticky = 'w')

        modfield1 = tk.Entry(modabslf, textvariable = mod1var) #This entry field is for dividend in modulus
        modfield1.grid(row = 1, column = 0, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)
        modfield1.bind('<Button-1>', msclick1)

        modfield2 = tk.Entry(modabslf, textvariable = mod2var) #This entry field is for divisor in modulus
        modfield2.grid(row = 1, column = 1, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)
        modfield2.bind('<Button-1>', msclick2)

        modansfield = tk.Entry(modabslf, textvariable = modansvar, state = 'disabled') #This entry field is for displaying modulus answer
        modansfield.grid(row = 2, column = 0, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)

        percfield1 = tk.Entry(modabslf, textvariable = perc1var) #This entry field is for part in percentage
        percfield1.grid(row = 6, column = 0, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)
        percfield1.bind('<Button-1>', msclick4)

        percfield2 = tk.Entry(modabslf, textvariable = perc2var) #This entry field is for whole in percentage
        percfield2.grid(row = 6, column = 1, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)
        percfield2.bind('<Button-1>', msclick5)

        percansfield = tk.Entry(modabslf, textvariable = percansvar, state = 'disabled') #This entry field is for displaying percentage answer
        percansfield.grid(row = 7, column = 0, ipadx = 1, ipady = 3, padx = 10, pady = 7.5)

        absfield = tk.Entry(modabslf, textvariable = absvar) #This entry field is for absolute value
        absfield.grid(row = 4, column = 0, ipadx = 1, padx = 10, ipady = 3, pady = 7.5)
        absfield.bind('<Button-1>', msclick3)

        absansfield = tk.Entry(modabslf, textvariable = absansvar, state = 'disabled') #This entry field is for displaying absolute answer
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

icon = Image.open(r'calcicon.png') #This is to make the calculator icon utilizing PIL's modules
icon = icon.resize((64, 64), Image.ANTIALIAS) #Resize icon to desi#00adb5 size
icon = ImageTk.PhotoImage(icon) #Make the icon file readable
root.iconphoto(False, icon)

root.mainloop()
