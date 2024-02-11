import json
import codecs
import os
import sys
import Tkinter as tk
import tkColorChooser as color
import ShoutOutClip_Theme
sys.path.append(os.path.join(
    os.path.dirname(__file__), '../ShoutOutClip-Classes'))
from shutil import copy
from ShoutOutClip_DatabaseClass import Database as db
from ShoutOutClip_LoggerClass import Logger as log

global dbLogger, dbSettingsFile, scriptSettingsFile, castersDB, helpFile, helpText
dbLogger = log('dashboard')
dbLogger.logInit()
dbSettingsFile = os.path.realpath(os.path.join(os.path.dirname(
    __file__), '../ShoutOutClip-Classes/ShoutOutClip_dbSettings.json'))
scriptSettingsFile = os.path.realpath(os.path.join(
    os.path.dirname(__file__), '../ShoutOutClip_ScriptSettings.json'))
overlaySettingsFile = os.path.realpath(os.path.join(os.path.dirname(__file__), '../ShoutOutClip_OverlaySettings.json'))
helpFile = os.path.realpath(os.path.join(
    os.path.dirname(__file__), 'assets/ShoutOutClip_Help.json'))

def printLog(msg):
    print(msg)
    if dbLogger:
        dbLogger.logWrite(msg)
    return

def initDb():
    global castersDB
    castersDB = db(dbSettingsFile, scriptSettingsFile)
    startDBMsg = castersDB.createTable()
    printLog(startDBMsg)
    return castersDB

def createFile(data, file):
    global dbLogger
    try:
        with codecs.open(file, mode='w+', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True, encoding='utf-8')
        msg = '[{time}] (SUC) - Required file "{file}" created with success!'
        e = None
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to create required file "{file}" ...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(time=dbLogger.getTime(), file=file, err=e)
    printLog(msg)
    return

def saveFile(filename, cb1, cb2, variables):
    global dbLogger, castersDB, scriptSettingsFile
    data = cb1(variables)
    try:
        with codecs.open(filename, mode='w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        msg = '[{time}] (SUC) - New information saved to  file "{file}" '
        e = None
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to save file "{file}" ...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(time=dbLogger.getTime(), file=filename, err=e)
    printLog(msg)
    cb2()
    return castersDB

def createBackup(fileName):
    global dbLogger
    backFileName = '{file}.bk'.format(file=fileName)
    try:
        copy(fileName, backFileName)
        msg = '[{time}] (SUC) - Saved backup of "{file}" to {backup}'
        e = None
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to create backup of file "{file}" ...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(file=fileName, backup=backFileName, err=e, time=dbLogger.getTime())
    printLog(msg)
    return

def restoreBackup(fileName, cb):
    global dbLogger, castersDB, scriptSettingsFile
    backFileName = '{file}.bk'.format(file=fileName)
    try:
        copy(backFileName, fileName)
        msg = '[{time}] (SUC) - Previously saved backup of "{file}" using "{backup}" restored'
        cb()
        e = None
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to restore backup of file "{file}" ...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(time=dbLogger.getTime(), file=fileName, err=e, backup=backFileName)
    printLog(msg)
    return castersDB

def readJson(jsonFile):
    global dbLogger
    try:
        with codecs.open(jsonFile, mode='r', encoding='utf-8-sig') as f:
            jsonData = json.load(f)
        msg = '[{time}] (SUC) - Required file "{file}" loaded with success!'
        e = None
    except Exception as e:
        jsonData = None
        msg = '[{time}] (ERR) - Unable to load the required file "{file}"...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(time=dbLogger.getTime(), file=jsonFile, err=e)
    printLog(msg)
    return jsonData

def changeTabStatus(tab, bar, *args):
    global dbLogger
    tabIndex = tab.index(tab.select())
    barText = ' {text}'
    barText = barText.format(text=tab.tab(tabIndex, 'text'))
    bar.configure(text=barText)
    msg = '[{time}] (INF) - Now displaying {tab}...'
    msg = msg.format(time=dbLogger.getTime(), tab=barText)
    printLog(msg)
    return

def openDashboardLogs():
    folder = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '../ShoutOutClip-Logs/Dashboard'))
    os.startfile(folder)
    return

def deleteDashboardLogs():
    dbLogger.folderLogDelete('dashboard')
    return

def openScriptLogs():
    folder = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '../ShoutOutClip-Logs/Script'))
    os.startfile(folder)
    return

def deleteScriptLogs():
    dbLogger.folderLogDelete('script')
    return

def openLogs():
    folder = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '../ShoutOutClip-Logs'))
    os.startfile(folder)
    return

def deleteAllLogs():
    deleteDashboardLogs()
    deleteScriptLogs()
    return

def setVolume(label, var, *args):
    label['text'] = '{:.0f}%'.format(var.get())
    return var.get()

def getCasters(db):
    results = db.getCasters()
    if len(results[0]) > 0:
        list = results[0]
    else:
        list = []
    msg = results[1]
    printLog(msg)
    return list

def addOne(db, cb1, mode, data, cb2):
    data = cb1(data)
    msg = db.addCaster(data[0], data[1])
    printLog(msg)
    cb2(mode)
    return

def updateDefaultMessage(message):
    global castersDB
    msg = castersDB.updateCaster('any', ['any', message, 1])
    printLog(msg)
    return castersDB

    
def updateOne(db, cb1, mode, data, cb2):
    data = cb1(data)
    msg = db.updateCaster(data[0], data[1:])
    printLog(msg)
    cb2(mode)
    return

def deleteOne(db, cb1, mode, data, cb2):
    data = cb1(data)
    msg = db.deleteCaster(data[0])
    printLog(msg)
    cb2(mode)
    return

def unselect(root, *args):
    widget = root.tk_focusPrev()
    widget.selection_clear()
    return

def dbDisconnect():
    castersDB.conn.close()
    return

helpText = readJson(helpFile)

def changeHelp(e, root, textZones, *args):
    try:
        widget = root.focus_get()
        if widget:
            key = widget.winfo_name()
        for textZone in textZones:
            textZone.config(state='normal')
            textZone.delete('0.0', tk.END)
            textZone.insert(tk.END, helpText[key])
            textZone.config(state='disabled', selectbackground=ShoutOutClip_Theme.darkGray, selectforeground=ShoutOutClip_Theme.darkWhite, cursor='arrow',takefocus=0)
    except Exception as e:
        if e.args[0] != 'popdown':
            text = "Quick help for this field was not found. Please contact the developer"
            textZone.config(state='normal')
            textZone.delete('0.0', tk.END)
            textZone.insert(tk.END, text)
            textZone.config(state='disabled', selectbackground=ShoutOutClip_Theme.darkGray, selectforeground=ShoutOutClip_Theme.darkWhite, cursor='arrow',takefocus=0)
        else:
            pass
        pass
    return

def openOverlay():
    global logs
    overlayFile = os.path.realpath(os.path.join(os.path.dirname(__file__), 'assets/previewOverlay/index.html'))
    try:
        os.startfile(overlayFile)
        msg = '[{time}] (INF) - Opening overlay playground...'
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to open overlay playground...'
        msg += '\n[{time}] (ERR) - System message {err}.'.format(time=dbLogger.getTime(), err=e)
    printLog(msg)
    return

def setVolume(label, var, *args):
    label['text'] = '{:.0f}%'.format(var.get())
    return var.get()

def colorPicker(colorVar):
    myColor = color.askcolor()
    colorVar.set(myColor[1])
    return 
