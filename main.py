from tkinter import *
from tkinter.ttk import *
from tkinter import font,colorchooser,filedialog,messagebox
import os
import tempfile
from datetime import datetime

#CREATING THE FUNCTIONS
#declaring global variables
FileUrl=''
fontSize=12
fontStyle='Calibri'

#function for new file
def NewFile(event=None):
    global FileUrl
    NewOption=messagebox.askyesnocancel('Warning','Do you want to save this file?')
    if NewOption is True:
        SaveFile()
        FileUrl=''
        TextArea.delete(0.0,END)
        root.title('New File')
    elif NewOption is False:
        FileUrl=''
        TextArea.delete(0.0,END)
        root.title('New File')
    else:
        pass

#function for opening a file
def OpenFile(event=None):
    global FileUrl
    FileUrl=filedialog.askopenfilename(initialdir=os.getcwd,title='Select File',filetypes=(('Text File','txt'),('All Files','*.*')))
    if FileUrl!='':
        OpenedFile=open(FileUrl,'r')
        TextArea.insert(0.0,OpenedFile.read())
        root.title(os.path.basename(FileUrl))

#function for save command
def SaveFile(event=None):
    if FileUrl=='':
        NewFileUrl=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text Files','txt'),('All Files','*.*')))
        if NewFileUrl is not None:
            text=TextArea.get(0.0,END)
            NewFileUrl.write(text)
            NewFileUrl.close()
        else:
            pass
    else:
        text=TextArea.get(0.0,END)
        CurrentFile=open(FileUrl,'w')
        CurrentFile.write(text)

#function for save as command
def SaveAsFile(event=None):
    NewFileUrl=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text Files','txt'),('All Files','*.*')))
    if NewFileUrl!='':
        text=TextArea.get(0.0,END)
        NewFileUrl.write(text)
        NewFileUrl.close()
        if FileUrl!='':
            os.remove(FileUrl)
    else: 
        pass

#function for print command
def PrintFile(event=None):
    file=tempfile.mktemp('.txt')
    open(file,'w').write(TextArea.get(0.0,END))
    os.startfile(file,'print')

#function to exit file
def ExitFile(event=None):
    SaveOption=messagebox.askyesnocancel('Warning','Do you want to save this file?')
    if SaveOption is True:
        SaveFile()
        root.destroy()
    elif SaveOption is False:
        root.destroy()
    else:
        pass    

#function for cut operation
def CutText():
    TextArea.event_generate('<Control x>')  #this function can also be defined directly in command of cut using lambda keyword

#function for copy operation
def CopyText():
    TextArea.event_generate('<Control c>')

#function for paste operation
def PasteText():
    TextArea.event_generate('<Control v>')

#function for clear operation 
def ClearText():
    TextArea.delete(0.0,END)

#function to find text
def FindText():
    #Functions for find and replace frame
    #Find fucntion
    def FindWord():
        TextArea.tag_remove('FindTag',0.0,END)
        word=FindEntry.get()
        StartIndex='1.0'
        if word!='':
            while True:
                StartIndex=TextArea.search(word,StartIndex,stopindex=END)
                if not StartIndex:
                    break
                EndIndex=f'{StartIndex}+{len(word)}c'
                TextArea.tag_add('FindTag',StartIndex,EndIndex)
                TextArea.tag_config('FindTag',background='yellow')
                StartIndex=EndIndex

    #function to make the highlighted text normal after closing find window
    def TextNormal():
        TextArea.tag_remove('FindTag',0.0,END)
        FindRoot.destroy()

    #Replace function
    def ReplaceWord():
        WordFind=FindEntry.get()
        WordReplace=ReplaceEntry.get()
        text=TextArea.get(0.0,END)
        text=text.replace(WordFind,WordReplace)
        TextArea.delete(0.0,END)
        TextArea.insert(INSERT,text)

    #GUI
    #Creating a find window
    FindRoot=Toplevel()
    FindRoot.title('Find')
    FindRoot.geometry('500x250+370+230')
    FindRoot.resizable(0,0)
    
    #creating a frame on the window
    FindFrame=LabelFrame(FindRoot,text='Find/replace')
    FindFrame.pack(padx=100,pady=50)
    
    #creating labels on frame
    FindLabel=Label(FindFrame,text='Find')
    FindLabel.grid(row=0,column=0,padx=5,pady=5)
    ReplaceLabel=Label(FindFrame,text='Replace')
    ReplaceLabel.grid(row=1,column=0,padx=5,pady=5)

    #creating entry fields for the labels
    FindEntry=Entry(FindFrame)
    FindEntry.grid(row=0,column=1,padx=5,pady=5)
    ReplaceEntry=Entry(FindFrame)
    ReplaceEntry.grid(row=1,column=1,padx=5,pady=5)

    #creating buttons on the frame
    FindButton=Button(FindFrame,text='Find',command=FindWord)
    FindButton.grid(row=2,column=0,padx=25,pady=15)
    ReplaceButton=Button(FindFrame,text='Replace',command=ReplaceWord)
    ReplaceButton.grid(row=2,column=1,padx=25,pady=15)

    FindRoot.protocol('WM_DELETE_WINDOW',TextNormal)
    FindRoot.mainloop()

#function to show date and time
def showDateTime(event=None):
    DateTime=datetime.now()
    DateTime=DateTime.strftime('%A %B %d, %Y %I:%M:%S %p')
    TextArea.insert(1.0,DateTime+'\n')

#function to show/hide toolbar
def ShowToolBarFunc():
    if showToolBar.get()==False:
        toolBar.pack_forget()
    if showToolBar.get()==True:
        TextArea.pack_forget()
        toolBar.pack(fill=X)
        TextArea.pack(fill=BOTH,expand=1)

#function to show/hide status bar
def ShowStatusBarFunc():
    if showStatusBar.get()==False:
        StatusBar.pack_forget()
    if showStatusBar.get()==True:
        StatusBar.pack()

#function to change theme
def ChangeTheme(BGColor,FGColor):
    TextArea.config(bg=BGColor,fg=FGColor)

#fucntion for changing font style
def FontStyleChange(event):
    global fontStyle
    fontStyle=FontChoice.get()
    TextArea.config(font=(fontStyle,fontSize))

#function for changing font size 
def FontSizeChange(event):
    global fontSize
    fontSize=FontSizeChoice.get()
    TextArea.config(font=(fontStyle,fontSize))

#funtion for making the text bold
def BoldText():
    TextProperty=font.Font(font=TextArea['font']).actual()    #gets all the properties of the font in the textarea
    if TextProperty['weight']=='normal' and TextProperty['slant']=='roman' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'bold'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='italic' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'bold','italic'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='italic' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'bold','italic','underline'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='roman' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'bold','underline'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='roman' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'normal'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='italic' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'normal','italic'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='italic' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'normal','italic','underline'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='roman' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'normal','underline'))
    

#function for making the text italic  
def ItalicText():
    TextProperty=font.Font(font=TextArea['font']).actual()
    if TextProperty['weight']=='normal' and TextProperty['slant']=='roman' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'italic'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='italic' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'roman'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='italic' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'roman','underline'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='roman' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'italic','underline'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='roman' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'bold','italic'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='italic' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'bold','roman'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='italic' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'bold','roman','underline'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='roman' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'bold','italic','underline'))

#function for underlining the text
def UnderlineText():
    TextProperty=font.Font(font=TextArea['font']).actual()
    if TextProperty['weight']=='normal' and TextProperty['slant']=='roman' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'underline'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='italic' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'italic','underline'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='italic' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'italic'))
    if TextProperty['weight']=='normal' and TextProperty['slant']=='roman' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='roman' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'bold','underline'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='italic' and TextProperty['underline']==False:
        TextArea.config(font=(fontStyle,fontSize,'bold','italic','underline'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='italic' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'bold','italic'))
    if TextProperty['weight']=='bold' and TextProperty['slant']=='roman' and TextProperty['underline']==True:
        TextArea.config(font=(fontStyle,fontSize,'bold'))

#function for changing the font colour
def fontColorChange():
    fontColor=colorchooser.askcolor()
    TextArea.config(fg=fontColor[1])

#function for left align
def LeftAlign():
    text=TextArea.get(0.0,END)
    TextArea.tag_config('left',justify=LEFT)
    TextArea.delete(0.0,END)
    TextArea.insert(INSERT,text,'left')

#function for center align
def CenterAlign():
    text=TextArea.get(0.0,END)
    TextArea.tag_config('center',justify=CENTER)
    TextArea.delete(0.0,END)
    TextArea.insert(INSERT,text,'center')

#function for right align
def RightAlign():
    text=TextArea.get(0.0,END)
    TextArea.tag_config('right',justify=RIGHT)
    TextArea.delete(0.0,END)
    TextArea.insert(INSERT,text,'right')

#function for displaying no. of words and characters in status bar
def StatusBarFunction(event):
        if TextArea.edit_modified():
            chars=len(TextArea.get(0.0,'end-1c'))
            words=len(TextArea.get(0.0,END).split())
            StatusBar.config(text=f'Characters: {chars}  Words: {words}')
            TextArea.edit_modified(False)

#-----------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------#

#creating an object of Tk class to make the GUI
root=Tk()   
root.title('Text Editor by ADITI MITTAL')  #title of the window
root.geometry('1200x600+15+15')     #sets the size of the window    +10+10: distance from x and y axis resp. 

#CREATING THE MENUBAR
menubar=Menu(root)
root.config(menu=menubar)

# CREATING  AND ADDING SUBMENUS
#FILE MENU
filemenu=Menu(menubar,tearoff=False)    #tearoff helps in creating a detachable menu, value 0/False means no detachable menu
menubar.add_cascade(label='File',menu=filemenu)

#icons for file menu commands
NewIcon=PhotoImage(file='new.png')
OpenIcon=PhotoImage(file='open.png')
SaveIcon=PhotoImage(file='save.png')
SaveAsIcon=PhotoImage(file='save_as.png')
PrintIcon=PhotoImage(file='print.png')
ExitIcon=PhotoImage(file='exit.png')

#adding file menu commands 
filemenu.add_command(label='New', accelerator='Ctrl+N',image=NewIcon,compound=LEFT,command= NewFile)
filemenu.add_command(label='Open',accelerator='Ctrl+O',image=OpenIcon,compound=LEFT,command= OpenFile)
filemenu.add_command(label='Save',accelerator='Ctrl+S',image=SaveIcon,compound=LEFT,command= SaveFile)
filemenu.add_command(label='Save As',accelerator='Ctrl+Alt+S',image=SaveAsIcon,compound=LEFT,command= SaveAsFile)
filemenu.add_command(label='Print',accelerator='Ctrl+P',image=PrintIcon,compound=LEFT,command= PrintFile)
filemenu.add_separator()
filemenu.add_command(label='Exit',accelerator='Ctrl+Q',image=ExitIcon,compound=LEFT,command= ExitFile)

#binding the window with the shortcuts
root.bind('<Control-n>',NewFile)
root.bind('<Control-o>',OpenFile)
root.bind('<Control-s>',SaveFile)
root.bind('<Control-Alt-s>',SaveAsFile)
root.bind('<Control-p>',PrintFile)
root.bind('<Control-q>',ExitFile)

#-----------------------------------------------------------------------------------------------#

#EDIT MENU
editmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Edit',menu=editmenu)

#icons for edit menu commands 
UndoIcon=PhotoImage(file='undo.png')
RedoIcon=PhotoImage(file='redo.png')
CutIcon=PhotoImage(file='cut.png')
CopyIcon=PhotoImage(file='copy.png')
PasteIcon=PhotoImage(file='paste.png')
SelectAllIcon=PhotoImage(file='select_all.png')
ClearIcon=PhotoImage(file='clear_all.png')
FindIcon=PhotoImage(file='find.png')
DateTimeIcon=PhotoImage(file='date_time.png')

#adding edit menu commands
editmenu.add_command(label='Undo',accelerator='Ctrl+Z',image=UndoIcon,compound=LEFT,command=lambda: TextArea.event_generate('<Control z>'))
editmenu.add_command(label='Redo',accelerator='Ctrl+Y',image=RedoIcon,compound=LEFT,command=lambda: TextArea.event_generate('<Control y>'))
editmenu.add_separator()
editmenu.add_command(label='Cut',accelerator='Ctrl+X',image=CutIcon,compound=LEFT,command=CutText)
editmenu.add_command(label='Copy',accelerator='Ctrl+C',image=CopyIcon,compound=LEFT,command=CopyText)
editmenu.add_command(label='Paste',accelerator='Ctrl+V',image=PasteIcon,compound=LEFT,command=PasteText)
editmenu.add_command(label='Select All',accelerator='Ctrl+A',image=SelectAllIcon,compound=LEFT,command=lambda: TextArea.event_generate('<Control a>'))
editmenu.add_command(label='Clear',accelerator='Ctrl+Alt+X',image=ClearIcon,compound=LEFT,command=ClearText)
editmenu.add_separator()
editmenu.add_command(label='Find',accelerator='Ctrl+F',image=FindIcon,compound=LEFT,command=FindText)
editmenu.add_command(label='Time/Date',accelerator='Fn+D',image=DateTimeIcon,compound=LEFT,command=showDateTime)

#binding date time function to shortcut
root.bind('<F5>',showDateTime)

#-----------------------------------------------------------------------------------------------#

#VIEW MENU
viewmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='View',menu=viewmenu)

#icons for view menu
ToolbarIcon=PhotoImage(file='tool_bar.png')
StatusbarIcon=PhotoImage(file='status_bar.png')

#defining view variables
showToolBar=BooleanVar()
showStatusBar=BooleanVar()
showToolBar.set(True)
showStatusBar.set(True)

#adding view menu commands: the checkbuttons
viewmenu.add_checkbutton(label='Tool Bar',variable=showToolBar,onvalue=True,offvalue=False,image=ToolbarIcon,compound=LEFT,command=ShowToolBarFunc)
viewmenu.add_checkbutton(label='Status Bar',variable=showStatusBar,onvalue=True,offvalue=False,image=StatusbarIcon,compound=LEFT,command=ShowStatusBarFunc)

#-----------------------------------------------------------------------------------------------#

#THEMES MENU
themesmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Themes',menu=themesmenu)

#icons for theme menu
LightDefaultIcon=PhotoImage(file='light_default.png')
LightPlusIcon=PhotoImage(file='light_plus.png')
DarkIcon=PhotoImage(file='dark.png')
PinkIcon=PhotoImage(file='pink.png')
NightBlueIcon=PhotoImage(file='night_blue.png')
OrangeIcon=PhotoImage(file='orange.png')

#defining themes variable
ThemeChoice=StringVar()

#adding themes commands: the radiobuttons
themesmenu.add_radiobutton(label='Light Default',variable=ThemeChoice,image=LightDefaultIcon,compound=LEFT,command=lambda: ChangeTheme('white','black'))
themesmenu.add_radiobutton(label='Light Plus',variable=ThemeChoice,image=LightPlusIcon,compound=LEFT, command=lambda: ChangeTheme('#d6d6d4','black'))
themesmenu.add_radiobutton(label='Dark',variable=ThemeChoice,image=DarkIcon,compound=LEFT, command=lambda: ChangeTheme('black','white'))
themesmenu.add_radiobutton(label='Pink',variable=ThemeChoice,image=PinkIcon,compound=LEFT, command=lambda: ChangeTheme('pink','#001285'))
themesmenu.add_radiobutton(label='Night Blue',variable=ThemeChoice,image=NightBlueIcon,compound=LEFT, command=lambda: ChangeTheme('#191970','#f0b1ed'))
themesmenu.add_radiobutton(label='Orange',variable=ThemeChoice,image=OrangeIcon,compound=LEFT, command=lambda: ChangeTheme('#ffb861','black'))

#-----------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------#

# CREATING TOOLBAR
toolBar=Label(root)
toolBar.pack(side=TOP,fill=X)

#CREATING FONT COMBOBOX
#tuple for all fonts: font family
FontFamily=font.families()

#defining fonts variable
FontChoice=StringVar()

#adding font options
FontScrollBox=Combobox(toolBar,values=FontFamily,state='readonly',textvariable=FontChoice,width=25)
FontScrollBox.current(FontFamily.index('Calibri'))
FontScrollBox.grid(row=0,column=0,padx=5)

#BINDING THE COMBOBOX WITH FONT STYLE CHANGE FUNCTION
FontScrollBox.bind('<<ComboboxSelected>>',FontStyleChange)

#-----------------------------------------------------------------------------------------------#

#CREATING FONT SIZE COMBOBOX
#defining font size variable
FontSizeChoice=IntVar()

#adding font size options
FontSizeBox=Combobox(toolBar,values=tuple(range(8,81,2)),textvariable=FontSizeChoice,width=18,state='readonly')
FontSizeBox.current(2)
FontSizeBox.grid(row=0,column=1,padx=5)

#BINDING THE COMBOBOX WITH FONT SIZE CHANGE FUNCTION
FontSizeBox.bind('<<ComboboxSelected>>',FontSizeChange)

#-----------------------------------------------------------------------------------------------#

#CREATING BUTTONS ON TOOLBAR
#bold button
BoldButtonIcon=PhotoImage(file='bold.png')
BoldButton=Button(toolBar,image=BoldButtonIcon,command=BoldText)
BoldButton.grid(row=0,column=2,padx=5)

#italics button
ItalicsButtonIcon=PhotoImage(file='italic.png')
ItalicsButton=Button(toolBar,image=ItalicsButtonIcon,command=ItalicText)
ItalicsButton.grid(row=0,column=3,padx=5)

#underline button
UnderlineButtonIcon=PhotoImage(file='underline.png')
UnderlineButton=Button(toolBar,image=UnderlineButtonIcon,command=UnderlineText)
UnderlineButton.grid(row=0, column=4, padx=5)

#font colour button
FontColourIcon=PhotoImage(file='font_color.png')
FontColourButton=Button(toolBar,image=FontColourIcon,command=fontColorChange)
FontColourButton.grid(row=0,column=5,padx=5)

#left align button
LeftAlignIcon=PhotoImage(file='left.png')
LeftAlignButton=Button(toolBar,image=LeftAlignIcon,command=LeftAlign)
LeftAlignButton.grid(row=0,column=6,padx=5)

#center align button
CenterAlignIcon=PhotoImage(file='center.png')
CenterAlignButton=Button(toolBar,image=CenterAlignIcon,command=CenterAlign)
CenterAlignButton.grid(row=0,column=7)

#right align button
RightAlignIcon=PhotoImage(file='right.png')
RightAlignButton=Button(toolBar,image=RightAlignIcon,command=RightAlign)
RightAlignButton.grid(row=0,column=8,padx=5)

#-----------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------#

#CREATING TEXT AREA
#Adding a scrollbar on the right
ScrollBar=Scrollbar(root)
ScrollBar.pack(side=RIGHT,fill=Y)

#Adding the text area
TextArea=Text(root,yscrollcommand=ScrollBar.set,font=('Calibri',12),undo=True)    #setting the scrollbar along with the text area
TextArea.pack(fill=BOTH,expand=True)
ScrollBar.config(command=TextArea.yview)    #adding functionality to the scrollbar to scroll along with the text

#Adding the status bar
StatusBar=Label(root,text='Status Bar')
StatusBar.pack(side=BOTTOM)
TextArea.bind('<<Modified>>',StatusBarFunction)

#-----------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------#

root.mainloop()     #holds the window