import sqlite3
import json
import codecs
import os
from collections import OrderedDict as od
from ShoutOutClip_LoggerClass import Logger as log

global databaseLog, table, cCaster, cMessage, cAllow, saveRaider, shoutMessage
databaseLog = log('dashboard')

class Database():
    def __init__(self, dbSettingsFile=None, scriptSettingsFile=None):
        self.startMsg = '[{time}] (INF) - Starting database...'
        dbFile = dbSettingsFile
        scriptFile = scriptSettingsFile
        try:
            with codecs.open(dbSettingsFile, encoding='utf-8-sig', mode='r') as f:
                self.dbSettings = json.load(f, encoding='utf-8', object_pairs_hook=od)
                self.startMsg += '\n[{time}] (SUC) - Required asset "{dbFile}" found!'
            self.dbFolder = self.dbSettings['dbFolder']
            self.dbFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '../{folder}')).format(folder=self.dbFolder)
            self.dbFileName = self.dbSettings['dbFileName']
            self.dbColumns = self.dbSettings['dbColumns']
            self.dbTable = self.dbSettings['dbTable']
            e = None
        except Exception as e:
            self.startMsg += '\n[{time}] (WAR) - Unabled to find one or more required assets or the required files are not in the right format. The script is creating a new set of configuration files...'
            self.startMsg += '\n[{time}] (ERR) - System message: {err}'
            self.dbFolder = 'ShoutOutClip-Database'
            self.dbFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '../{folder}')).format(folder=self.dbFolder)
            self.dbFileName = "ShoutOutClip_Database.sqlite"
            self.dbColumns = ['caster', 'customMessage', 'allow']
            self.dbTable = 'castersSettings'
            with codecs.open(os.path.realpath(os.path.join(os.path.dirname(__file__), 'ShoutOutClip_dbSettings.json')), mode='w+', encoding='utf-8-sig') as f:
                settings = {
                    'dbColumns': self.dbColumns,
                    'dbFileName': self.dbFileName,
                    'dbFolder': self.dbFolder,
                    'dbTable': self.dbTable
                }
                json.dump(settings, f, ensure_ascii=False, indent=2)
                self.startMsg += '\n[{time}] (SUC) - Required missing assets created with success!'
            pass
        try:
            with codecs.open(scriptSettingsFile, encoding='utf-8-sig', mode='r') as f:
                self.scriptSettings = json.load(f, encoding='utf-8', object_pairs_hook=od)
                self.startMsg += '\n[{time}] (SUC) - Required asset "{scriptFile}" found!'
            self.saveRaider = self.scriptSettings['saveRaider']
            self.shoutMessage = self.scriptSettings['shoutMessage']
        except Exception as e:
            self.startMsg += '\n[{time}] (WAR) - Unabled to find one or more required assets or the required files are not in the right format. The script is creating a new set of configuration files...'
            self.startMsg += '\n[{time}] (ERR) - System message: {err}'
            self.saveRaider = False
            self.shoutMessage = '[Fellow streamer AD] - Let\'s show some love to {caster} , which was last saw playing {game} on {url} !'
            pass
        self.dbFile = os.path.join(self.dbFilePath, self.dbFileName)
        self.startMsg += '\n[{time}] (SUC) - Database initialized with success!'
        self.startMsg = self.startMsg.format(time=databaseLog.getTime(), err=e, dbFile=dbFile, scriptFile=scriptFile)
        return 
    
    def dbConns(self):
        self.conn = sqlite3.connect(self.dbFile)
        return self.conn
        
    def createTable(self):
        global table, cCaster, cMessage, cAllow, autoAddRadier, shoutMessage
        table = self.dbTable
        cCaster = self.dbColumns[0]
        cMessage = self.dbColumns[1]
        cAllow = self.dbColumns[2]
        autoAddRadier = self.saveRaider
        shoutMessage = self.shoutMessage
        msg = self.startMsg
        msg += '\n[{time}] (INF) - Starting connection with the casters database...'
        conn = self.dbConns()
        cursor = conn.cursor()
        try:
            createQ = 'create table if not exists {table} (id integer primary key autoincrement, {col0} text not null unique, {col1} text default "{shoutMessage}", {col2} boolean not null default 1)'
            createQ = createQ.format(table=table, col0=cCaster, col1=cMessage, shoutMessage=self.shoutMessage, col2=cAllow)
            addIndexQ = 'create unique index if not exists {col0} on {table} ({col0})'
            addIndexQ = addIndexQ.format(col0=cCaster, table=table)
            addDefaultCasterQ = 'insert into {table} ({col0}) values ("any")'
            addDefaultCasterQ = addDefaultCasterQ.format(table=table, col0=cCaster)
            cursor.execute(createQ)
            cursor.execute(addIndexQ)
            try:
                cursor.execute(addDefaultCasterQ)
            except:
                pass
            msg += '\n[{time}] (SUC) - Database connection created with success!'
            e = None
        except Exception as e:
            msg += '\n[{time}] (ERR) - An error occurred while trying to connect to the database...'
            msg += '\n[{time}] (ERR) - System message: {err}'
        msg = msg.format(time=databaseLog.getTime(), err=e)
        conn.commit()
        conn.close()
        return msg
    
    def addCaster(self, *args):
        global table, cCaster, cMessage, casterToAdd, casterMsg
        conn = self.dbConns()
        cursor = conn.cursor()
        addCasterQ = 'insert into {table} ({col0}, {col1}) values ("{casterToAdd}", "{casterMsg}")'
        if args and len(args[1]) > 0:
            casterToAdd = args[0]
            casterMsg = args[1]
        elif args and args[1] == 'DEFAULT':
            casterToAdd = args[0]
            casterMsg = self.shoutMessage
        elif args and len(args[1]) == 0:
            casterToAdd = args[0]
            casterMsg = ''
        msg = '[{time}] (INF) - Adding {caster} with message "{message}" to the database...'
        addCasterQ = addCasterQ.format(table=table, col0=cCaster, col1=cMessage, casterToAdd=casterToAdd, casterMsg=casterMsg).decode('utf-8')
        try:
            cursor.execute(addCasterQ)
            msg +='\n[{time}] (SUC) - Caster added with success!'
            e = None
        except Exception as e:
            if not args or (len(args[0]) == 0):
                msg = '[{time}] (ERR) - Unable to add caster to the database...'
                casterToAdd = None
                casterMsg = None
                e = 'Required information is missing or in wrong format.'
            else:
                msg += '\n[{time}] (ERR) - An error occurred when trying to add {caster} to the database...'
                casterToAdd = args[0]
                casterMsg = None
            msg +='\n[{time}] (ERR) - System error: {err}'
            pass
        msg = msg.format(time=databaseLog.getTime(), caster=casterToAdd, message=casterMsg, err=e)
        conn.commit()
        conn.close()
        return msg
    
    def getCaster(self, caster):
        global table, cCaster, cMessage, cAllow
        conn = self.dbConns()
        cursor = conn.cursor()
        getCasterQ = 'select * from {table} where {col0}="{caster}"'
        getCasterQ = getCasterQ.format(col0=cCaster, table=table, caster=caster)
        msg = '[{time}] (INF) - Feching "{caster}" information on the database...'
        try:
            result = cursor.execute(getCasterQ).fetchone()
            msg += '\n[{time}] (SUC) - "{caster}" information fetched with success!'
            e = None
        except Exception as e:
            result = None
            msg += '\n[{time}] (ERR) - An error occurred when trying to fetch "{caster}"...'
            msg += '\n[{time}] (ERR) - System message: {err}'
        msg = msg.format(time=databaseLog.getTime(), err=e, caster=caster)
        conn.close()
        return [result, msg]
    
    def getCasters(self):
        global table, cCaster, cMessage, cAllow
        conn = self.dbConns()
        cursor = conn.cursor()
        getCastersQ = 'select {col0}, {col1}, {col2} from {table}'
        getCastersQ = getCastersQ.format(col0=cCaster, col1=cMessage, col2=cAllow, table=table)
        msg = '[{time}] (INF) - Fetching list of casters...'
        try:
            result = cursor.execute(getCastersQ).fetchall()
            msg += '\n[{time}] (SUC) - List of casters fetched with success!'
            e = None
        except Exception as e:
            result = None
            msg += '\n[{time}] (ERR) - An error occurred when trying to fetch the list of casters...'
            msg += '\n[{time}] (ERR) - System message: {err}'
        msg = msg.format(time=databaseLog.getTime(), err=e)
        conn.close()
        return [result, msg]
    
    def getAllowedCasters(self):
        global table, cCaster, cMessage, cAllow
        conn = self.dbConns()
        cursor = conn.cursor()
        getAllowedCastersQ = 'select {col0}, {col1} from {table} where {col2}=1'
        getAllowedCastersQ = getAllowedCastersQ.format(col0=cCaster, col1=cMessage, table=table, col2=cAllow).decode('utf-8')
        msg = '[{time}] (INF) - Fetching list of allowed casters...'
        try:
            queryResult = cursor.execute(getAllowedCastersQ).fetchall()
            result = []
            for item in queryResult:
                result.append([item[0], item[1]])
            msg += '\n[{time}] (SUC) - List of allowed casters fetched with success!'
            e = None
        except Exception as e:
            result = None
            msg += '\n[{time}] (ERR) - An error occurred when trying to fetch the list of allowed casters...'
            msg += '\n[{time}] (ERR) - System message: {err}'
        msg = msg.format(time=databaseLog.getTime(), err=e)
        conn.close()
        return [result, msg]
    
    def updateCaster(self, caster, values):
        global table, cCaster, cMessage, cAllow, allowed
        allowed = None
        conn = self.dbConns()
        cursor = conn.cursor()
        getCasterQ = 'select * from {table} where {col0}="{caster}"'
        getCasterQ = getCasterQ.format(table=table, col0=cCaster, caster=caster)
        foundCaster = cursor.execute(getCasterQ).fetchone()
        if foundCaster and len(values) == 3:
            casterId = foundCaster[0]
        msg = '[{time}] (INF) - Fecthing information from {caster} for update...'
        try:
            if values[2] == False:
                newAllow = 0
            elif values[2] == True:
                newAllow = 1
            editCasterQ = 'update {table} set {col0}="{newCaster}", {col1}="{newMessage}", {col2}={newAllow} where id={casterId}'
            editCasterQ = editCasterQ.format(table=table, col0=cCaster, newCaster=values[0], col1=cMessage, newMessage=values[1], col2=cAllow, newAllow=newAllow, casterId=casterId).decode('utf-8')
            cursor.execute(editCasterQ)
            msg += '\n[{time}] (SUC) - Caster "{caster}" updated with success!'
            msg += '\n[{time}] (INF) - New Twitch handle: "{newCaster}"'
            msg += '\n[{time}] (INF) - New caster message: "{newMessage}"'
            if values[2] == 0:
                allowed = 'No'
            elif values[2] == 1:
                allowed = 'Yes'
            msg += '\n[{time}] (INF) - Automatic shoutout status: "{allowed}"'
            e = None
        except Exception as e:
            if len(values) != 3:
                e = 'Missing information to edit "{caster}"'.format(caster=caster)
            msg += '\n[{time}] (ERR) - An error occurred when trying to update "{caster}" information...'
            msg += '\n[{time}] (ERR) - System message: {err}'
            pass
        msg = msg.format(time=databaseLog.getTime(), caster=caster, newCaster=values[0], newMessage = values[1], allowed=allowed, err=e)
        conn.commit()
        conn.close()
        return msg
    
    def deleteCaster(self, caster):
        global table, cCaster
        conn = self.dbConns()
        cursor = conn.cursor()
        getCasterQ = 'select id from {table} where {col0}="{caster}"'
        getCasterQ = getCasterQ.format(table=table, col0=cCaster, caster=caster)
        foundCaster = cursor.execute(getCasterQ).fetchone()
        if foundCaster:
            casterId = foundCaster[0]
        msg = '[{time}] (INF) - Fecthing {caster} for deletion from database...'
        try:
            deleteCasterQ = 'delete from {table} where id="{casterId}"'
            deleteCasterQ = deleteCasterQ.format(table=table, casterId=casterId)
            cursor.execute(deleteCasterQ)
            msg +='\n[{time}] (SUC) - "{caster}" successfull deleted!'
            e = None
        except Exception as e:
            if not foundCaster:
                e = 'No caster found with the search parameter {caster}'.format(caster=caster)
            msg += '\n[{time}] (ERR) - An error occurred when trying to delete {caster} from the database...'
            msg += '\n[{time}] (ERR) - System message: {err}'
        conn.commit()
        conn.close()
        msg = msg.format(time=databaseLog.getTime(), caster=caster, err=e)
        return msg
    