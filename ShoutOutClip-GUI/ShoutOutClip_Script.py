import ttk
import Tkinter as tk
import ShoutOutClip_Functions as fn

global chatOptions, readSettings

chatOptions = ['Announcement (/announce)', 'Action (/me)', 'Chat']
readSettings = fn.readJson(fn.scriptSettingsFile)

def createTab(mainInt):
    global tab
    tab = ttk.Frame(mainInt)
    tab.pack()
    createVariables()
    configureTab(tab)
    configureCanvas(tab)
    addHelp(tab)
    addButtons(tab)
    return tab

def configureTab(tab):
    tab.columnconfigure(0, weight=30)
    tab.columnconfigure(1, weight=2)
    tab.columnconfigure(2, weight=0)
    tab.columnconfigure(3, weight=2)
    tab.columnconfigure(4, weight=2)
    tab.rowconfigure(0, weight=10)
    tab.rowconfigure(1, weight=0)
    return

def createVariables():
    global variables, readSettings
    variables = []
    if readSettings == None:
        msg = '[{time}] (WAR) - The required file "{file}" could not be found. A default file will be created instead.'
        msg += 'If this message is displayed too frequently, please contact the developer.'
        msg = msg.format(time=fn.dbLogger.getTime(), file=fn.scriptSettingsFile)
        fn.printLog(msg)
        defData = {
            "saveRaider": False, 
            "shoutCaster": True, 
            "shoutMessage": "(Featured streamer ad) - Let's show some love to {caster} , which was last saw playing {game} on {url} !", 
            "shoutMode": "Announcement (/announce)", 
            "shoutOnJoin": False, 
            "shoutRaider": True, 
            "shoutRaiderCount": 1, 
            "shoutRaiderMessage": "(Fellow raider ad) - We just got raided by {caster} with {viewercount} viewers! They were playing {game} with their community at {url} ! It's hype time!"
        }
        fn.createFile(defData, fn.scriptSettingsFile)
        settings = defData
    else:
        settings = readSettings
        
    shoutCaster = tk.BooleanVar(value=settings['shoutCaster'])
    shoutOnJoin = tk.BooleanVar(value=settings['shoutOnJoin'])
    shoutMessage = tk.StringVar(value=settings['shoutMessage'])
    shoutMode = tk.StringVar(value=settings['shoutMode'])
    shoutRaider = tk.BooleanVar(value=settings['shoutRaider'])
    shoutRaiderCount = tk.IntVar(value=settings['shoutRaiderCount'])
    shoutRaiderMessage = tk.StringVar(value=settings['shoutRaiderMessage'])
    saveRaider = tk.BooleanVar(value=settings['saveRaider'])
    
    variables.append(shoutCaster)
    variables.append(shoutOnJoin)
    variables.append(shoutMessage)
    variables.append(shoutMode)
    variables.append(shoutRaider)
    variables.append(shoutRaiderCount)
    variables.append(shoutRaiderMessage)
    variables.append(saveRaider)
    return variables


def configureCanvas(tab):
    global frame
    canvas = tk.Canvas(tab, takefocus=0, highlightthickness=0)
    canvas.grid(column=0, row=0, sticky=tk.W+tk.N+tk.S+tk.E, padx=[10,0], pady=10, columnspan=2)
    frame = addComponents(canvas)
    canvas.create_window((0,0), window=frame, anchor=tk.N+tk.E)
    scrollY = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
    scrollY.grid(row=0, column=2, padx=[0,0], sticky=tk.N+tk.S+tk.W, pady=[10,10])
    canvas['yscrollcommand'] = scrollY.set
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))
    canvas.yview_moveto(0)
    return

def addComponents(place):
    frame = tk.Frame(place, width=place.winfo_width())
    addGeneralSettings(frame)
    addRaiderSettings(frame)
    addScriptLogsSettings(frame)
    return frame

def addGeneralSettings(canvas):
    global chatOptions
    frame = tk.Frame(canvas, takefocus=0, width=canvas.winfo_width())
    frame.grid(row=0, column=0, padx=10, pady=[0,10], sticky=tk.E+tk.W)
    frame.columnconfigure(0, weight=1)
    
    generalSettings = ttk.LabelFrame(frame, text=' General Settings: ', takefocus=0)
    generalSettings.grid(row=0, column=0, pady=5, sticky=tk.W + tk.E)
    generalSettings.config(border=1, relief=tk.SOLID)
    generalSettings.columnconfigure(0, weight=0)
    generalSettings.columnconfigure(1, weight=1)
    
    shoutCasterCheck = ttk.Checkbutton(generalSettings, text="Auto shoutout saved casters?", variable=variables[0], onvalue=True, offvalue=False, name='shoutCaster')
    shoutCasterCheck.grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W, pady=5)
    shoutCasterCheck.focus_set()
    
    shoutOnJoinCheck = ttk.Checkbutton(generalSettings, text="Auto shoutout casters when they join the channel?                               ", variable=variables[1], onvalue=True, offvalue=False, name='shoutOnJoin')
    shoutOnJoinCheck.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W, pady=5)
    
    ttk.Label(generalSettings, text='Message to be sent by default on shoutouts:').grid(row=2, column=0, sticky=tk.E+tk.W, pady=5, columnspan=2)
    shoutMessageEntry = ttk.Entry(generalSettings, font=('Calibri', 12), name='shoutMessage', textvariable=variables[2])
    shoutMessageEntry.grid(row=3, column=0, sticky=tk.E+tk.W, pady=5, columnspan=2, ipady=2)
    
    ttk.Label(generalSettings, text='Shoutout message method:').grid(row=4, column=0, sticky=tk.E+tk.W, pady=5)
    shoutModeSelector = ttk.Combobox(generalSettings, values=chatOptions, state='readonly', name='shoutMode', textvariable=variables[3])
    shoutModeSelector.set(variables[3].get())
    shoutModeSelector.grid(row=4, column=1, sticky=tk.E+tk.W, pady=5, padx=[10, 0], ipady=2)
    
    return frame

def addRaiderSettings(canvas):
    global variables
    frame = tk.Frame(canvas, takefocus=0, width=canvas.winfo_width())
    frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E+tk.W)
    frame.columnconfigure(0, weight=1)
    
    raiderSettings = ttk.LabelFrame(frame, text=' Raider Settings: ', takefocus=0)
    raiderSettings.grid(row=0, column=0, pady=5, sticky=tk.W + tk.E)
    raiderSettings.config(border=1, relief=tk.SOLID)
    raiderSettings.columnconfigure(0, weight=0)
    raiderSettings.columnconfigure(1, weight=1)
    
    shoutRaiderCheck = ttk.Checkbutton(raiderSettings, text="Send shoutout on chat when raided?", variable=variables[4], onvalue=True, offvalue=False, name='shoutRaider')
    shoutRaiderCheck.grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W, pady=5)
    
    ttk.Label(raiderSettings, text='Minimum viewer to trigger shoutout on raids:').grid(row=1, column=0)
    shoutRaiderCountEntry = ttk.Entry(raiderSettings, font=('Calibri', 12), name='shoutRaiderCount', textvariable=variables[5])
    shoutRaiderCountEntry.grid(row=1, column=1, pady=5, padx=[10,0], sticky=tk.E+tk.W, ipady=2)
    
    ttk.Label(raiderSettings, text='Message to be sent on raider shoutouts:').grid(row=2, column=0, sticky=tk.E+tk.W, pady=5, columnspan=2)
    shoutRaiderMessageEntry = ttk.Entry(raiderSettings, font=('Calibri', 12), name='shoutRaiderMessage', textvariable=variables[6])
    shoutRaiderMessageEntry.grid(row=3, column=0, sticky=tk.E+tk.W, pady=5, columnspan=2, ipady=2)
    
    saveRaiderCheck = ttk.Checkbutton(raiderSettings, text="Save raider to the casters database if not already saved?           ", variable=variables[7], onvalue=True, offvalue=False, name='saveRaider')
    saveRaiderCheck.grid(row=4, column=0, sticky=tk.E+tk.W, columnspan=2)
    
    return frame

def addScriptLogsSettings(canvas):
    frame = ttk.Labelframe(canvas, text=" Logs Controller: ", takefocus=0)
    frame.grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S, padx=10, pady=10)
    frame.config(border=1, relief=tk.SOLID)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=10)

    openDashboardLogs = ttk.Button(frame, text='Open Dashboard Logs Folder', name='logDashOpen')
    openDashboardLogs.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S, padx=[0, 5], pady=5)
    openDashboardLogs.configure(command=fn.openDashboardLogs)

    deleteDashboardLogs = ttk.Button(frame, text='Delete Dashboard Logs', name="logDashDelete")
    deleteDashboardLogs.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S, padx=[5, 0], pady=5)
    deleteDashboardLogs.configure(command=fn.deleteDashboardLogs)

    ttk.Separator(frame).grid(row=1, column=0,columnspan=2, sticky=tk.E+tk.W, pady=5)

    openScriptLogs = ttk.Button(frame, text='Open Script Logs Folder', name='logScriptOpen')
    openScriptLogs.grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S, padx=[0, 5], pady=5)
    openScriptLogs.configure(command=fn.openScriptLogs)

    deleteScriptLogs = ttk.Button(frame, text='Delete Script Logs', name='logScriptDelete')
    deleteScriptLogs.grid(row=2, column=1, sticky=tk.E+tk.W+tk.N+tk.S, padx=[5, 0], pady=5)
    deleteScriptLogs.configure(command=fn.deleteScriptLogs)

    ttk.Separator(frame).grid(row=3, column=0,columnspan=2, sticky=tk.E+tk.W, pady=5)

    deleteAllLogs = ttk.Button(frame, text='Delete All Log files', name='logDeleteAll')
    deleteAllLogs.grid(row=4, column=0, sticky=tk.E+tk.W+tk.N+tk.S, pady=[5, 10], columnspan=2)
    deleteAllLogs.configure(command=fn.deleteAllLogs)
    return

def addButtons(frame):
    restoreBckBtn = ttk.Button(frame, text='Restore backup', name='restore')
    restoreBckBtn.grid(column=1, row=1, columnspan=2, sticky=tk.E+tk.W, padx=[10,5], pady=[0,10])
    restoreBckBtn.config(command=lambda file=fn.scriptSettingsFile, cb=setSettings: fn.restoreBackup(file, cb))

    createBckBtn = ttk.Button(frame, text='Create backup', name='create')
    createBckBtn.grid(column=3, row=1, sticky=tk.E+tk.W, padx=[5,5], pady=[0,10])
    createBckBtn.config(command=lambda file=fn.scriptSettingsFile: fn.createBackup(file))
    
    saveBtn = ttk.Button(frame, text='Save settings', name='save')
    saveBtn.grid(column=4, row=1, sticky=tk.E+tk.W, padx=[5,10], pady=[0,10])
    saveBtn.config(command= lambda file=fn.scriptSettingsFile, cb1=getSettings, variables=variables, cb2=setSettings : fn.saveFile(file, cb1, cb2, variables))
    return

def addHelp(tab):
    global tabHelpText
    tabHelpFrame = ttk.Labelframe(tab, text=' Quick Help: ', takefocus=0)
    tabHelpFrame.grid(row=0, column=3, sticky=tk.E+tk.W+tk.N+tk.S, padx=10, pady=10, columnspan=2)
    tabHelpText = tk.Text(tabHelpFrame, width=1, height=1, wrap=tk.WORD, takefocus=0)
    tabHelpText.pack(fill=tk.BOTH, expand=tk.YES, pady=[5,10])
    tabHelpFrame.columnconfigure(0, weight=10)
    tabHelpFrame.rowconfigure(0, weight=1)
    tabHelpText.grid(column=0, row=0, sticky=tk.W+tk.E+tk.N+tk.S, pady=5)
    scrollY = ttk.Scrollbar(tabHelpFrame, orient=tk.VERTICAL, command=tabHelpText.yview)
    scrollY.grid(column=1, row=0, sticky=tk.E+tk.N+tk.S)
    tabHelpText['yscrollcommand'] = scrollY.set
    return tabHelpText

def setSettings():
    restSettings = fn.readJson(fn.scriptSettingsFile)
    variables[0].set(value=restSettings['shoutCaster'])
    variables[1].set(value=restSettings['shoutOnJoin'])
    variables[2].set(value=restSettings['shoutMessage'])
    variables[3].set(value=restSettings['shoutMode'])
    variables[4].set(value=restSettings['shoutRaider'])
    variables[5].set(value=restSettings['shoutRaiderCount'])
    variables[6].set(value=restSettings['shoutRaiderMessage'])
    variables[7].set(value=restSettings['saveRaider'])
    return

def getSettings(variablesArray):
    settingsData = {
        "shoutCaster": variablesArray[0].get(),
        "shoutOnJoin": variablesArray[1].get(),
        "shoutMessage": variablesArray[2].get(),
        "shoutMode": variablesArray[3].get(),
        "shoutRaider": variablesArray[4].get(),
        "shoutRaiderCount": variablesArray[5].get(),
        "shoutRaiderMessage": variablesArray[6].get(),
        "saveRaider": variablesArray[7].get(),
    }
    fn.updateDefaultMessage(settingsData['shoutMessage'].encode('utf-8'))
    return settingsData