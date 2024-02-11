import ttk
import Tkinter as tk
import tkFont
import ShoutOutClip_Functions as fn

global readSettings, animOptions, fontOptions, tabHelpText, myFrame, overlaySettingsTab, reg

animOptions =['Drop','Fade', 'Fade up', 'Fade down', 'Fade left', 'Fade right', 'Fly up', 'Fly down', 'Fly left', 'Fly right', 'Horizontal Flip', 'Scale', 'Slide down', 'Slide up', 'Slide left', 'Slide right', 'Swing up', 'Swing down', 'Swing left', 'Swing right', 'Vertical Flip', 'Zoom']
readSettings = fn.readJson(fn.overlaySettingsFile)

def createTab(mainInt):
    global tab, fontOptions, variables
    tab = ttk.Frame(mainInt)
    tab.pack()
    fontOptions = []
    for f in tkFont.families():
        fontOptions.append(f)
    fontOptions.sort()
    createVariables()
    configureTab(tab)
    configureCanvas(tab)
    addHelp(tab)
    addButtons(tab)
    return tab

def createVariables():
    global variables, readSettings
    variables = []
    if readSettings == None:
        msg = '[{time}] (WAR) - The required file "{file}" could not be found. A default file will be created instead.'
        msg += 'If this message is displayed too frequently, please contact the developer.'
        msg = msg.format(time=fn.dbLogger.getTime(), file=fn.overlaySettingsFile)
        fn.printLog(msg)
        defData = {
            "animation": "Drop",
            "bottomBgColor": "#ffffff",
            "bottomTextColor": "#1b1c1d",
            "clipInfoBgColor": "#1b1c1d",
            "clipInfoDivider": "#16b2ab",
            "clipInfoTextColor": "#ffffff",
            "clipZoneBorder": "#16b2ab",
            "displayClip": True,
            "displayClipInfo": True,
            "imgBgColor": "#1b1c1d",
            "showClipBorder": True,
            "textFont": "Arial",
            "topBgColor": "#16b2ab",
            "topTextColor": "#ffffff",
            "volume": 50
        }
        fn.createFile(defData, fn.overlaySettingsFile)
        settings = defData
    else:
        settings = readSettings
    
    animation = tk.StringVar(value=settings['animation'])
    bottomBgColor = tk.StringVar(value=settings['bottomBgColor'])
    bottomTextColor = tk.StringVar(value=settings['bottomTextColor'])
    clipInfoBgColor = tk.StringVar(value=settings['clipInfoBgColor'])
    clipInfoDivider = tk.StringVar(value=settings['clipInfoDivider'])
    clipInfoTextColor = tk.StringVar(value=settings['clipInfoTextColor'])
    clipZoneBorder = tk.StringVar(value=settings['clipZoneBorder'])
    displayClip = tk.BooleanVar(value=settings['displayClip'])
    displayClipInfo = tk.BooleanVar(value=settings['displayClipInfo'])
    imgBgColor = tk.StringVar(value=settings['imgBgColor'])
    showClipBorder = tk.BooleanVar(value=settings['showClipBorder'])
    textFont = tk.StringVar(value=settings['textFont'])
    topBgColor = tk.StringVar(value=settings['topBgColor'])
    topTextColor = tk.StringVar(value=settings['topTextColor'])
    volume = tk.IntVar(value=settings['volume'])
    
    variables.append(textFont)
    variables.append(animation)
    variables.append(volume)
    variables.append(displayClip)
    variables.append(displayClipInfo)
    variables.append(topTextColor)
    variables.append(topBgColor)
    variables.append(bottomTextColor)
    variables.append(bottomBgColor)
    variables.append(imgBgColor)
    variables.append(showClipBorder)
    variables.append(clipZoneBorder)
    variables.append(clipInfoDivider)
    variables.append(clipInfoTextColor)
    variables.append(clipInfoBgColor)
    return variables

def configureTab(tab):
    tab.columnconfigure(0, weight=30)
    tab.columnconfigure(1, weight=2)
    tab.columnconfigure(2, weight=0)
    tab.columnconfigure(3, weight=2)
    tab.columnconfigure(4, weight=2)
    tab.rowconfigure(0, weight=10)
    tab.rowconfigure(1, weight=0)
    return

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
    addOverlayPlayground(frame)
    ttk.Separator(frame,orient='horizontal').grid(row=1, column=0 , sticky=tk.W+tk.E, pady=5)
    addOverlaySettings(frame)
    return frame

def addOverlayPlayground(canvas):
    playgroundFrame = tk.Frame(canvas, width=canvas.winfo_width(), takefocus=0)
    playgroundFrame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E+tk.W)
    playgroundFrame.columnconfigure(0, weight=1)
    overlayOpen = ttk.Button(playgroundFrame, text='Overlay Playground', name='openOverlayPreview')
    overlayOpen.grid(row=0, column=0, sticky=tk.E+tk.W, pady=5)
    overlayOpen.configure(command=fn.openOverlay)
    overlayOpen.focus_set()
    return playgroundFrame

def addOverlaySettings(canvas):
    global variables, clipVolumeLabel
    frame = tk.Frame(canvas, takefocus=0, width=canvas.winfo_width())
    frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E+tk.W)
    frame.columnconfigure(0, weight=1)
    
    generalSettings = ttk.Labelframe(frame, text=' General Settings: ', takefocus=0)
    generalSettings.grid(row=0, column=0, pady=5, sticky=tk.W + tk.E)
    generalSettings.config(border=1, relief=tk.SOLID)
    generalSettings.columnconfigure(0, weight=0)
    generalSettings.columnconfigure(1, weight=0)
    generalSettings.columnconfigure(2, weight=1)
    generalSettings.config(border=1, relief=tk.SOLID)
    
    ttk.Label(generalSettings, text='Overlay font: ').grid(row=0, column=0,sticky=tk.E+tk.W, pady=5)
    overlayFontSelector = ttk.Combobox(generalSettings, values=fontOptions, state='readonly', name='overlayFont', textvariable=variables[0])
    overlayFontSelector.set(variables[0].get())
    overlayFontSelector.grid(row=0, column=1, sticky=tk.E + tk.W, pady=5, columnspan=2, ipady=2)
    
    ttk.Label(generalSettings, text='Animation style: ').grid(row=1, column=0,sticky=tk.E+tk.W, pady=5)
    overlayAnimSelector = ttk.Combobox(generalSettings, values=animOptions, state='readonly', name='overlayAnimation', textvariable=variables[1])
    overlayAnimSelector.set(variables[1].get())
    overlayAnimSelector.grid(row=1, column=1, sticky=tk.E + tk.W, pady=5, columnspan=2, ipady=2)
    
    ttk.Label(generalSettings, text='Clip volume: ').grid(row=2, column=0, sticky=tk.E+tk.W, pady=[5, 5])
    clipVolumeLabel = ttk.Label(generalSettings, text='{vol}%'.format(vol=variables[2].get()), anchor=tk.E)
    clipVolumeLabel.grid(row=2, column=1, pady=[5, 5], padx=[10, 5], sticky=tk.W)
    clipVolumeSetter = ttk.Scale(generalSettings, variable=variables[2], from_=0, to=100, name='clipVolumeSetter')
    clipVolumeSetter.configure(command=lambda e, label=clipVolumeLabel, var=variables[2]: fn.setVolume(label, var))
    clipVolumeSetter.grid(row=2, column=2, sticky=tk.E+tk.W, ipadx=5, ipady=5, pady=[5, 5])
    
    displayClipCheck = ttk.Checkbutton(generalSettings, text="Display clip video with shoutout?", variable=variables[3], onvalue=True, offvalue=False, name='displayClip')
    displayClipCheck.grid(row=3, column=0, columnspan=3, sticky=tk.E+tk.W, pady=5)
    
    displayInfoCheck = ttk.Checkbutton(generalSettings, text="Display clip information when the clip is displayed on shoutouts?", variable=variables[4], onvalue=True, offvalue=False, name='displayInfo')
    displayInfoCheck.grid(row=4, column=0, columnspan=3, sticky=tk.E + tk.W, pady=5)
    
    visualSettings = ttk.LabelFrame(frame, text=' Overlay Visual Style Settings: ', takefocus=0)
    visualSettings.grid(row=5, column=0, pady=5, sticky=tk.W + tk.E, columnspan=3)
    visualSettings.config(border=1, relief=tk.SOLID)
    
    ttk.Label(visualSettings, text="Top text color: ", takefocus=0).grid(row=0, column=0, sticky=tk.W+tk.E, pady=5)
    topTextColorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='topTextColor', textvariable=variables[5])
    topTextColorEntry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=0, column=2, pady=5, padx=10)
    overlayTopTextColorBtn = ttk.Button(visualSettings, text='Select text color...', command=lambda var=variables[5]: fn.colorPicker(var), takefocus=0)
    overlayTopTextColorBtn.grid(row=0, column=3, sticky=tk.W+tk.E, pady=5)
    
    ttk.Label(visualSettings, text="Top back color: ", takefocus=0).grid(row=1, column=0, sticky=tk.W+tk.E, pady=5)
    topBgColorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='topBackgroundColor', textvariable=variables[6])
    topBgColorEntry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=1, column=2, pady=5, padx=10)
    overlayTopBgColorBtn = ttk.Button(visualSettings, text='Select back color...', command=lambda var=variables[6]: fn.colorPicker(var), takefocus=0)
    overlayTopBgColorBtn.grid(row=1, column=3, sticky=tk.W+tk.E, pady=5)
    
    ttk.Label(visualSettings, text="Bottom text color: ", takefocus=0).grid(row=2, column=0, sticky=tk.W+tk.E, pady=5)
    bottomTextcolorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='bottomTextColor', textvariable=variables[7])
    bottomTextcolorEntry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=2, column=2, pady=5, padx=10)
    overlayBottomTextColorBtn = ttk.Button(visualSettings, text='Select text color...', command=lambda var=variables[7]: fn.colorPicker(var), takefocus=0)
    overlayBottomTextColorBtn.grid(row=2, column=3, sticky=tk.W+tk.E, pady=5)
    
    ttk.Label(visualSettings, text="Bottom back color: ", takefocus=0).grid(row=3, column=0, sticky=tk.W+tk.E, pady=5)
    bottomBgColorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='bottomBackgroundColor', textvariable=variables[8])
    bottomBgColorEntry.grid(row=3, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=3, column=2, pady=5, padx=10)
    overlayBottomBgColorBtn = ttk.Button(visualSettings, text='Select back color...', command=lambda var=variables[8]: fn.colorPicker(var), takefocus=0)
    overlayBottomBgColorBtn.grid(row=3, column=3, sticky=tk.W+tk.E, pady=5)
    
    ttk.Label(visualSettings, text="Images back color: ", takefocus=0).grid(row=4, column=0, sticky=tk.W+tk.E, pady=5)
    imagesBgColorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='imagesBackgroundColor', textvariable=variables[9])
    imagesBgColorEntry.grid(row=4, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=4, column=2, pady=5, padx=10)
    overlayImagesBgColorBtn = ttk.Button(visualSettings, text='Select back color...', command=lambda var=variables[9]: fn.colorPicker(var), takefocus=0)
    overlayImagesBgColorBtn.grid(row=4, column=3, sticky=tk.W+tk.E, pady=5)
    
    ttk.Separator(visualSettings,orient='horizontal').grid(row=5, column=0 , sticky=tk.W+tk.E, pady=10, columnspan=4)
    
    displayClipBorderCheck = ttk.Checkbutton(visualSettings, text="Display border around Clip?", variable=variables[10], onvalue=True, offvalue=False, name='displayClipBorder')
    displayClipBorderCheck.grid(row=6, column=0, columnspan=4, sticky=tk.E + tk.W, pady=5)
    
    ttk.Label(visualSettings, text="Clip border color: ", takefocus=0).grid(row=7, column=0, sticky=tk.W+tk.E, pady=5)
    clipBorderColorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='clipBorderColor', textvariable=variables[11])
    clipBorderColorEntry.grid(row=7, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=7, column=2, pady=5, padx=10)
    clipBorderColorBtn = ttk.Button(visualSettings, text='Select border color...', command=lambda var=variables[11]: fn.colorPicker(var), takefocus=0)
    clipBorderColorBtn.grid(row=7, column=3, sticky=tk.W+tk.E, pady=5)
    
    ttk.Label(visualSettings, text="Information divider color: ", takefocus=0).grid(row=8, column=0, sticky=tk.W+tk.E, pady=5)
    clipDividerColorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='clipDividerColor', textvariable=variables[12])
    clipDividerColorEntry.grid(row=8, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=8, column=2, pady=5, padx=10)
    clipDividerColorBtn = ttk.Button(visualSettings, text='Select divider color...', command=lambda var=variables[12]: fn.colorPicker(var), takefocus=0)
    clipDividerColorBtn.grid(row=8, column=3, sticky=tk.W+tk.E, pady=5)
    
    ttk.Label(visualSettings, text="Information text color: ", takefocus=0).grid(row=9, column=0, sticky=tk.W+tk.E, pady=5)
    clipInfoTextColorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='clipInfoTextColor', textvariable=variables[13])
    clipInfoTextColorEntry.grid(row=9, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=9, column=2, pady=5, padx=10)
    clipInfoTextColorBtn = ttk.Button(visualSettings, text='Select text color...', command=lambda var=variables[13]: fn.colorPicker(var), takefocus=0)
    clipInfoTextColorBtn.grid(row=9, column=3, sticky=tk.W+tk.E, pady=5)
    
    ttk.Label(visualSettings, text="Information back color: ", takefocus=0).grid(row=10, column=0, sticky=tk.W+tk.E, pady=5)
    clipInfoBgColorEntry = ttk.Entry(visualSettings, font=('Calibri', 12), name='clipInfoBgColor', textvariable=variables[14])
    clipInfoBgColorEntry.grid(row=10, column=1, sticky=tk.W+tk.E, pady=5, ipady=2)
    ttk.Label(visualSettings, text="or", takefocus=0).grid(row=10, column=2, pady=5, padx=10)
    clipInfoBgColorBtn = ttk.Button(visualSettings, text='Select back color...', command=lambda var=variables[14]: fn.colorPicker(var), takefocus=0)
    clipInfoBgColorBtn.grid(row=10, column=3, sticky=tk.W+tk.E, pady=5)
    return frame


def addButtons(frame):
    restoreBckBtn = ttk.Button(frame, text='Restore backup', name='restore')
    restoreBckBtn.grid(column=1, row=1, columnspan=2, sticky=tk.E+tk.W, padx=[10,5], pady=[0,10])
    restoreBckBtn.config(command=lambda file=fn.overlaySettingsFile, cb=setSettings: fn.restoreBackup(file, cb))

    createBckBtn = ttk.Button(frame, text='Create backup', name='create')
    createBckBtn.grid(column=3, row=1, sticky=tk.E+tk.W, padx=[5,5], pady=[0,10])
    createBckBtn.config(command=lambda file=fn.overlaySettingsFile: fn.createBackup(file))
    
    saveBtn = ttk.Button(frame, text='Save settings', name='save')
    saveBtn.grid(column=4, row=1, sticky=tk.E+tk.W, padx=[5,10], pady=[0,10])
    saveBtn.config(command= lambda file=fn.overlaySettingsFile, cb1=getSettings, variables=variables, cb2=setSettings : fn.saveFile(file, cb1, cb2, variables))
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
    global clipVolumeLabel
    restSettings = fn.readJson(fn.overlaySettingsFile)
    variables[0].set(value=restSettings['textFont'])
    variables[1].set(value=restSettings['animation'])
    variables[2].set(value=restSettings['volume'])
    variables[3].set(value=restSettings['displayClip'])
    variables[4].set(value=restSettings['displayClipInfo'])
    variables[5].set(value=restSettings['topTextColor'])
    variables[6].set(value=restSettings['topBgColor'])
    variables[7].set(value=restSettings['bottomTextColor'])
    variables[8].set(value=restSettings['bottomBgColor'])
    variables[9].set(value=restSettings['imgBgColor'])
    variables[10].set(value=restSettings['showClipBorder'])
    variables[11].set(value=restSettings['clipZoneBorder'])
    variables[12].set(value=restSettings['clipInfoDivider'])
    variables[13].set(value=restSettings['clipInfoTextColor'])
    variables[14].set(value=restSettings['clipInfoBgColor'])
    clipVolumeLabel['text'] = '{vol:.0f}%'.format(vol=variables[2].get())
    return

def getSettings(variablesArray):
    settingsData = {
        "textFont": variablesArray[0].get(),
        "animation": variablesArray[1].get(),
        "volume": variablesArray[2].get(),
        "displayClip": variablesArray[3].get(),
        "displayClipInfo": variablesArray[4].get(),
        "topTextColor": variablesArray[5].get(),
        "topBgColor": variablesArray[6].get(),
        "bottomTextColor": variablesArray[7].get(),
        "bottomBgColor": variablesArray[8].get(),
        "imgBgColor": variablesArray[9].get(),
        "showClipBorder": variablesArray[10].get(),
        "clipZoneBorder": variablesArray[11].get(),
        "clipInfoDivider": variablesArray[12].get(),
        "clipInfoTextColor": variablesArray[13].get(),
        "clipInfoBgColor": variablesArray[14].get(),
    }
    return settingsData