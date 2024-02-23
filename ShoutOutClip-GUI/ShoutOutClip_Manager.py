import ttk
import Tkinter as tk
import ShoutOutClip_Functions as fn

global enableOptions, db, castersList, castersData
db = fn.initDb()
castersList = []
castersData = fn.getCasters(db)
for data in castersData:
    castersList.append(data[0])
castersList.sort()
enableOptions = ['Temporarily Disabled', 'Enabled']

def createTab(mainInt):
    global tab
    tab = ttk.Frame(mainInt)
    tab.pack()
    createVariables()
    configureTab(tab)
    configureCanvas(tab)
    addHelp(tab)
    return tab

def configureTab(tab):
    tab.columnconfigure(0, weight=5)
    tab.columnconfigure(1, weight=0)
    tab.columnconfigure(2, weight=3)
    tab.rowconfigure(0, weight=10)
    return

def createVariables():
    global variables
    variables = []
    addCaster = tk.StringVar(value='')
    addMessage = tk.StringVar(value='DEFAULT')
    edtCasterSelect = tk.StringVar(value='')
    edtCasterName = tk.StringVar(value='')
    edtCasterMessage = tk.StringVar(value='')
    edtCasterAllow = tk.BooleanVar(value=False)
    edtCasterAllowSelect = tk.StringVar(value='')
    
    variables.append(addCaster)
    variables.append(addMessage)
    variables.append(edtCasterSelect)
    variables.append(edtCasterName)
    variables.append(edtCasterMessage)
    variables.append(edtCasterAllow)
    variables.append(edtCasterAllowSelect)
    return variables

def configureCanvas(tab):
    global frame
    canvas = tk.Canvas(tab, takefocus=0, highlightthickness=0)
    canvas.grid(column=0, row=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=[10,0], pady=10)
    frame = addComponents(canvas)
    canvas.create_window((0,0), window=frame, anchor=tk.N+tk.E)
    scrollY = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
    scrollY.grid(row=0, column=1, padx=[5,0], sticky=tk.N+tk.S+tk.W, pady=[10,10])
    canvas['yscrollcommand'] = scrollY.set
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))
    canvas.yview_moveto(0)
    return

def addComponents(place):
    frame = tk.Frame(place)
    addCaster(frame)
    edtCaster(frame)
    return frame

def addCaster(canvas):
    frame = tk.Frame(canvas, takefocus=0)
    frame.grid(row=1, column=0, pady=[0,10], padx=5, sticky=tk.W+tk.E)

    casterAdd = ttk.LabelFrame(frame, text=' Add new caster: ', width=0)
    casterAdd.grid(row=0, column=0, pady=5, sticky=tk.W+tk.E)
    casterAdd.config(border=1, relief=tk.SOLID)
    casterAdd.columnconfigure(0, weight=0)
    casterAdd.columnconfigure(1, weight=1)
    casterAdd.columnconfigure(2, weight=1)

    ttk.Label(casterAdd, text='Caster\'s Twitch username:').grid(row=0, column=0, sticky=tk.E+tk.W, pady=5)
    casterUsernameEntry = ttk.Entry(casterAdd, font=('Calibri', 12), name='casterName', textvar=variables[0])
    casterUsernameEntry.grid(row=0, column=1, sticky=tk.E+tk.W, pady=5, padx=[10,0], columnspan=2, ipady=2)
    casterUsernameEntry.focus_set()
    
    ttk.Label(casterAdd, text='Caster\'s custom message:                                                ').grid(row=1, column=0, sticky=tk.E+tk.W, pady=5, columnspan=2)
    casterMessageEntry = ttk.Entry(casterAdd, font=('Calibri', 12), name='casterMessage', textvar=variables[1])
    casterMessageEntry.grid(row=2, column=0, columnspan=3, sticky=tk.E+tk.W, pady=5, ipady=2)

    saveCasterBtn = ttk.Button(casterAdd, text='Save caster', name='addCaster')
    saveCasterBtn.grid(row=3, column=1, pady=[5,0], sticky=tk.W+tk.E, padx=[0,5])
    saveCasterBtn.configure(command=lambda db=db, cb1=getNewData, var=variables, mode='save', cb2=updateList: fn.addOne(db, cb1, mode, var, cb2))

    cancelCasterBtn = ttk.Button(casterAdd, text='Discard Changes', name='cancelCaster')
    cancelCasterBtn.grid(row=3, column=2 , pady=[10,5], sticky=tk.W+tk.E, padx=[5,5])
    cancelCasterBtn.configure(command=cancelSave)
    return frame

def edtCaster(canvas):
    global casterSelector, casterShoutEnableSelector, casterEdit
    frame = tk.Frame(canvas, takefocus=0)
    frame.grid(row=2, column=0, padx=5, pady=[0,10], sticky=tk.E+tk.W)
    frame.columnconfigure(0, weight=1)
    
    casterEdit = ttk.LabelFrame(frame, text=' Edit caster: ')
    casterEdit.grid(row=0, column=0, pady=5, sticky=tk.W+tk.E)
    casterEdit.config(border=1, relief=tk.SOLID)
    casterEdit.columnconfigure(0, weight=0)
    casterEdit.columnconfigure(1, weight=1)
    
    ttk.Label(casterEdit, text='Select a caster to edit:').grid(row=0, column=0, pady=5, sticky=tk.E + tk.W)
    casterSelector = ttk.Combobox(casterEdit, values=castersList[1:], state='readonly', name='casterSelector', textvar=variables[2])
    casterSelector.bind('<<ComboboxSelected>>', lambda e, frame=casterEdit: changeText(frame))
    casterSelector.grid(row=0, column=1, sticky=tk.E+tk.W, pady=5, padx=[10, 0], columnspan=2, ipady=2)
    
    ttk.Label(casterEdit, text='Caster\'s Twitch username:').grid(row=1, column=0, sticky=tk.E+tk.W, pady=5)
    casterUsernameEntry = ttk.Entry(casterEdit, font=('Calibri', 12), name='editCasterName', textvar=variables[3])
    casterUsernameEntry.grid(row=1, column=1, sticky=tk.E+tk.W, pady=5, padx=[10,0], columnspan=2, ipady=2)
    
    ttk.Label(casterEdit, text='Caster\'s custom message:').grid(row=2, column=0, sticky=tk.E+tk.W, pady=5, columnspan=2)
    casterMessageEntry = ttk.Entry(casterEdit, font=('Calibri', 12), name='casterMessage', textvar=variables[4])
    casterMessageEntry.grid(row=3, column=0, columnspan=3, sticky=tk.E+tk.W, pady=5, ipady=2)
    
    ttk.Label(casterEdit, text='Automatic shoutout caster?').grid(row=4, column=0, pady=5)
    casterShoutEnableSelector = ttk.Combobox(casterEdit, values=enableOptions, state='readonly', name='casterShoutEnable', textvar=variables[6])
    casterShoutEnableSelector.grid(row=4, column=1, sticky=tk.E+tk.W, pady=5, padx=[10, 0], columnspan=2, ipady=2)
    
    saveChangesBtn = ttk.Button(casterEdit, text='Save changes', name='saveCaster')
    saveChangesBtn.grid(row=5, column=0, pady=[5,0], sticky=tk.W+tk.E, padx=[0,5])
    saveChangesBtn.configure(command=lambda db=db, cb1=getUpdateData, var=variables, mode='edit', cb2=updateList: fn.updateOne(db, cb1, mode, var, cb2))

    cancelEditBtn = ttk.Button(casterEdit, text='Discard Changes', name='discardCaster')
    cancelEditBtn.grid(row=5, column=1 , pady=[10,5], sticky=tk.W+tk.E, padx=[5,5])
    cancelEditBtn.configure(command=lambda frame=casterEdit: cancelEdit(frame))
    
    deleteSingleBtn = ttk.Button(casterEdit, text='Delete caster', name='deleteCaster')
    deleteSingleBtn.grid(row=5, column=2 , pady=[5,0], sticky=tk.W+tk.E, padx=[5,0])
    deleteSingleBtn.configure(command=lambda db=db, cb1=getUpdateData, var=variables, mode='edit', cb2=updateList: fn.deleteOne(db, cb1, mode, var, cb2))
    return frame

def addHelp(tab):
    global tabHelpText
    tabHelpFrame = ttk.Labelframe(tab, text=' Quick Help: ', takefocus=0)
    tabHelpFrame.grid(row=0, column=2, sticky=tk.E+tk.W+tk.N+tk.S, padx=10, pady=10)
    tabHelpText = tk.Text(tabHelpFrame, width=1, height=1, wrap=tk.WORD, takefocus=0)
    tabHelpText.pack(fill=tk.BOTH, expand=tk.YES, pady=[5,10])
    tabHelpFrame.columnconfigure(0, weight=10)
    tabHelpFrame.rowconfigure(0, weight=1)
    tabHelpText.grid(column=0, row=0, sticky=tk.W+tk.E+tk.N+tk.S, pady=5)
    scrollY = ttk.Scrollbar(tabHelpFrame, orient=tk.VERTICAL, command=tabHelpText.yview)
    scrollY.grid(column=1, row=0, sticky=tk.E+tk.N+tk.S)
    tabHelpText['yscrollcommand'] = scrollY.set
    return tabHelpText

def cancelSave():
    global variables
    variables[0].set("")
    variables[1].set("DEFAULT")
    return

def updateList(mode):
    global variables, castersList, casterSelector, castersData, casterEdit
    if mode == 'save':
        cancelSave()
    elif mode == 'edit':
        frame = casterEdit
        cancelEdit(frame)
    castersData = fn.getCasters(db)
    castersList = []
    for data in castersData:
        castersList.append(data[0])
    castersList.sort()
    casterSelector.config(values=castersList[1:])
    return castersData

def cancelEdit(frame):
    global casterShoutEnableSelector, variables
    frame['text'] = ' Edit caster: '
    variables[2].set("")
    variables[3].set("")
    variables[4].set("")
    variables[5].set(False)
    variables[6].set("")
    return

def changeText(frame):
    global casterSelector, casterShoutEnableSelector, variables
    frame['text'] = ' Editing caster options for {caster}: '.format(caster=variables[2].get())
    caster = fn.getCaster(db, variables[2].get())
    variables[3].set(caster[1])
    variables[4].set(caster[2])
    variables[5].set(caster[3])
    casterSelector.set(variables[3].get())
    casterShoutEnableSelector.set(enableOptions[variables[5].get()])
    return caster

def getNewData(var):
    data = [var[0].get(), var[1].get().encode('utf-8')]
    return data

def getUpdateData(var):
    global current, casterShoutEnableSelector
    var[5].set(casterShoutEnableSelector.current())
    data = [var[2].get(), var[3].get(), var[4].get().encode(encoding='utf-8'), var[5].get()]
    return data
