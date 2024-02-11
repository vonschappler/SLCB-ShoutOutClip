import os
import ttk
import Tkinter as tk
import ShoutOutClip_About
import ShoutOutClip_Overlay
import ShoutOutClip_Script
import ShoutOutClip_Manager
import ShoutOutClip_Theme
import ShoutOutClip_Functions as fn

global scriptName, version, icoFile
scriptName = fn.dbLogger.scriptName
version = fn.dbLogger.version
icoFile = os.path.realpath(os.path.join(os.path.dirname(__file__), "assets/icon.ico"))

#
#   Dashboard Settings
#
def Init():
    global root, style, mainInt
    root = tk.Tk()
    screenW = root.winfo_screenwidth()
    screenH = root.winfo_screenheight()
    windowW = int(root.winfo_screenwidth()/2)
    windowH = int(root.winfo_screenheight()/2)
    centerX = int(screenW/2 - windowW/2)
    centerY = int(screenH/2 - windowH/2)
    geometry = str(windowW) + 'x' + str(windowH) + "+" + str(centerX) + "+" + str(centerY)
    root.geometry(geometry)
    root.resizable(False, False)
    root.columnconfigure(0, weight=2)
    root.rowconfigure(0, weight=2)
    root.configure(bg=ShoutOutClip_Theme.darkGray)
    root.iconbitmap(icoFile)
    root.bind_all('<FocusOut>', lambda e, root=root: fn.unselect(root))
    root.bind_all('<Button-1>', lambda e: 'break')
    style=ShoutOutClip_Theme.CreateStyle()
    style.theme_use('vonSchappler')  
    ShoutOutClip_Theme.AddRootOptions(root)
    statusBarPanel = ttk.Frame(root, takefocus=0)
    statusBarPanel.grid(column=0, row=2, sticky=tk.W+tk.E, columnspan=3)
    statusBarPanel.columnconfigure(0, weight=10)
    statusBarPanel.columnconfigure(1, weight=1)
    statusBarLeft = ttk.Label(statusBarPanel, text=' Script Settings: ', anchor=tk.W, relief=tk.GROOVE, justify=tk.RIGHT, style='status.TLabel', takefocus=0)
    statusBarLeft.grid(column=0, row=0, sticky=tk.W+tk.E, columnspan=2)
    statusBarLeft.grid_propagate(False)
    statusBarRigtText = ' {script} {version} '.format(script=scriptName, version=version)
    root.title(statusBarRigtText)
    statusBarRight = ttk.Label(statusBarPanel, text=statusBarRigtText, anchor=tk.E, relief=tk.GROOVE, justify=tk.RIGHT, style='status.TLabel', takefocus=0)
    statusBarRight.grid(column=2, row=0, sticky=tk.W+tk.E, ipadx=10)
    statusBarRight.grid_propagate(False)
    mainInt = ttk.Notebook(root, takefocus=0)
    mainInt.grid(column=0, row=0, sticky=tk.W+tk.E+tk.N+tk.S, columnspan=3)
    mainInt.bind('<<NotebookTabChanged>>', lambda e, tabbed=mainInt, bar=statusBarLeft: fn.changeTabStatus(tabbed, bar))
    mainInt.add(ShoutOutClip_Script.createTab(mainInt), text='Script Settings')
    mainInt.add(ShoutOutClip_Overlay.createTab(mainInt), text='Overlay Settings')
    mainInt.add(ShoutOutClip_Manager.createTab(mainInt), text='Manage Casters')
    mainInt.add(ShoutOutClip_About.createTab(mainInt), text='About')
    root.bind_all('<FocusIn>', lambda e, root=root, textZones=[ShoutOutClip_Script.tabHelpText, ShoutOutClip_Overlay.tabHelpText, ShoutOutClip_Manager.tabHelpText] : fn.changeHelp(e, root, textZones))
    msg = '[{time}] (SUC) - {scriptName} {version} dashboard was started with success!'.format(time=fn.dbLogger.getTime(), scriptName=scriptName, version=version)
    fn.printLog(msg)
    return

Init()

# Final styling for tabs
style.configure('TNotebook.Tab', width=root.winfo_screenwidth() / len(mainInt.tabs()))

root.mainloop()
fn.dbLogger.logEnd()