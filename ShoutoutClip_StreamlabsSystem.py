#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import os
import codecs
import json
import clr
import re
sys.path.append(os.path.join(os.path.dirname(__file__), 'ShoutOutClip-Classes'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ShoutOutClip-Database'))
clr.AddReference('IronPython.SQLite.dll')
clr.AddReference('IronPython.Modules.dll')
from collections import deque
from random import randint
from ShoutOutClip_DatabaseClass import Database as db
from ShoutOutClip_LoggerClass import Logger as log

global scriptLogger, startMsg, streamer, clipAPI, gameAPI, casterLastGameAPI, lastGameImage, casterAvatar, wasRaided, viewerCount, raiderName
scriptLogger = log('script')
streamer = ''
clipAPI = 'https://twitchapi.teklynk.com/getuserclips.php?channel={streamer}&limit=10&dateRange=365'
gameAPI = 'https://twitchapi.teklynk.com/getgame.php?id={game_id}'
casterLastGameAPI = 'https://decapi.me/twitch/game/{streamer}'
lastGameImage = 'https://static-cdn.jtvnw.net/ttv-boxart/{lastGame}-144x192.jpg'
casterAvatar = 'https://decapi.me/twitch/avatar/{streamer}'
wasRaided = False
viewerCount = None
raiderName = None

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = scriptLogger.scriptName
Website = "https://rebrand.ly/vonWebsite"
Description = "Displays a shoutout overlay with a random clip from the shouted user"
Creator = "von_Schappler"
Version = scriptLogger.version

#---------------------------------------
# Variables
#---------------------------------------
global dbSettingsFile, scriptSettingsFile, overlaySettingsFile, guiFile 

dbSettingsFile = os.path.realpath(os.path.join(os.path.dirname(
    __file__), './ShoutOutClip-Classes/ShoutOutClip_dbSettings.json'))
scriptSettingsFile = os.path.realpath(os.path.join(
    os.path.dirname(__file__), './ShoutOutClip_ScriptSettings.json'))
overlaySettingsFile = os.path.realpath(os.path.join(os.path.dirname(__file__), './ShoutOutClip_OverlaySettings.json'))
guiFile = os.path.realpath(os.path.join(os.path.dirname(__file__), './ShoutOutClip-GUI/ShoutOutClip_App.py'))
fixObs = os.path.realpath(os.path.join(os.path.dirname(__file__), './FixObs.css'))

#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    global shoutOutQ, streamer, castersDBList, scriptSettings, overlaySettings, allowedCasters, alreadyShout
    try:
        streamer = Parent.GetChannelName()
        castersDb = db(dbSettingsFile, scriptSettingsFile)
        startMsg = castersDb.createTable()
        printLog(startMsg)
        shoutOutQ = deque()
        allowedCasters = []
        alreadyShout = []
        castersDBList = castersDb.getAllowedCasters()[0]
        for item in castersDBList:
            allowedCasters.append(item[0].lower())
        with codecs.open(scriptSettingsFile, mode='r+', encoding='utf-8-sig') as f:
            scriptSettings = json.loads(f.read())
        with codecs.open(overlaySettingsFile, mode='r+', encoding='utf-8-sig') as f:
            overlaySettings = json.loads(f.read())
        msg = '({script} - {version}) - Started with success!'
        msg = msg.format(script=ScriptName, version=Version)
    except Exception as e:
        msg = '({script} - {version}) - Unable to start script...'
        msg += '({script} - {version}) - Error message: {err}'
        msg = msg.format(script=ScriptName, version=Version, err=e)
    SendInfo('action (/me)', msg)
    return

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings():
    global scriptLogger
    scriptLogger.logEnd()
    Init()
    return

#---------------------------------------
#	Script is going to be unloaded
#---------------------------------------
def Unload():
    global scriptLogger
    scriptLogger.logEnd()
    return

#---------------------------------------
#	Script is enabled or disabled on UI
#---------------------------------------
def ScriptToggled(state):
    global isEnabled
    if state:
        status = 'enabled'
        isEnabled = True
    else:
        status = 'disabled'
        Init()
        isEnabled = False
    msg = '@{streamer}, ({script} - {version}) is {status}...'
    msg = msg.format(streamer=streamer, script=ScriptName, version=Version, status=status)
    SendInfo('action (/me)', msg)
    return isEnabled

#---------------------------------------
# Execute data and process messages
#---------------------------------------
def Execute(data):
    global alreadyShout, allowedCasters, wasRaided
    if data.IsChatMessage() and isEnabled:
        user = data.User
        if (user not in alreadyShout) and (user in allowedCasters) and (not scriptSettings['shoutOnJoin']):
            RunCommand('shout {caster}'.format(caster=user), user)
    if (data.IsRawData() and data.IsFromTwitch() and Parent.IsLive()) and isEnabled:
        rawData = data.RawData
        raiderData = CheckRaider(rawData)
        if (raiderData[0] and scriptSettings['shoutRaider']):
            RunCommand('shout {caster}'.format(caster=raiderData[1]), raiderData[1])
            if ((raiderData[1] not in castersDBList) or (raiderData[1].lower() not in castersDBList) and scriptSettings['saveRaider']):
                castersDBList.addCaster(raiderData[1].lower(), 'DEFAULT')
    return

#---------------------------------------
# Tick
#---------------------------------------
def Tick():
    global allowedCasters, shoutOutQ, castersDBList, alreadyShout, wasRaided, viewerCount
    if isEnabled:
        currentViewers = Parent.GetViewerList()
        for viewer in currentViewers:
            if (viewer.lower() not in alreadyShout) and (viewer.lower() in allowedCasters) and (scriptSettings['shoutOnJoin']):
                RunCommand('shout {caster}'.format(caster=viewer.lower()), viewer.lower())
    if len(shoutOutQ) > 0 and not Parent.IsOnCooldown(ScriptName, 'shout'):
        clipInfo = shoutOutQ[0]['clipInfo']
        caster = shoutOutQ[0]['casterName'].lower()
        casterName = shoutOutQ[0]['casterName']
        lastGame = shoutOutQ[0]['casterInfo']['lastGame']
        url = shoutOutQ[0]['casterInfo']['url']
        if (clipInfo == None or overlaySettings['displayClip'] == False):
            duration = 10
        else: 
            duration =  shoutOutQ[0]['clipInfo']['duration']
        duration += 5
        Parent.AddCooldown(ScriptName, 'shout', duration)
        Parent.BroadcastWsEvent('EVENT_SHOUTOUT', json.dumps(shoutOutQ[0], ensure_ascii=False))
        if (wasRaided and scriptSettings['shoutRaider']):
            shoutMessage = shoutOutQ[0]['shoutMessage']
            viewercount = viewerCount
        else:
            if (caster in allowedCasters):
                pos = allowedCasters.index(caster)
                shoutMessage = castersDBList[pos][1]
                viewercount = None
            else:
                shoutMessage = castersDBList[0][1]
                viewercount = None
        shoutMessage = shoutMessage.format(caster=casterName, game=lastGame, url=url, viewercount = viewercount)
        SendInfo(scriptSettings['shoutMode'], shoutMessage)
        wasRaided = False
        viewercount = None
        shoutOutQ.popleft()
    return

#---------------------------------------
# Parse
#---------------------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    if '$shoutout' in parseString:
        regex = re.search(r'\$shoutout\((.*)\)', parseString)
        if regex:
            RunCommand(regex.group(1), username)
            return parseString.replace(regex.group(0), '')
    return parseString

#---------------------------------------
# Functions
#---------------------------------------
def RunCommand(command, user):
    cmdOptions = ['shout_clip', 'shout', 'gui', 'restart', 'test']
    args = command.split(' ')
    toDo = args[0].lower()
    if toDo in cmdOptions:
        if toDo == cmdOptions[0] or toDo == cmdOptions[1]:
            if (toDo == cmdOptions[1]):
                overlaySettings['displayClip'] = False
            try:
                caster = RemovePound(args[1])
                ShoutOut(caster)
                Parent.SendStreamMessage('/shoutout {caster}'.format(caster=caster))
            except:
                msg = '({script} - {version}) - Unable to send a shoutout - the command needs a valid Twitch handle in order to emit a shoutout'
                msg = msg.format(script=ScriptName, version=Version)
                SendInfo('action (/me)', msg)
        if toDo == cmdOptions[1]:
            OpenGUI()
        if toDo == cmdOptions[2]:
            ReloadSettings()
        if toDo == cmdOptions[3]:
            TestRaider()
    return

def printLog(msg):
    global scriptLogger
    scriptLogger.logWrite(msg)
    return

def SendInfo(mode, message):
    modeOpts = ['Announcement (/announce)', 'Action (/me)', 'Chat']
    if mode.lower() == modeOpts[0].lower():
        slashCommand = '/announce '
    if mode.lower() == modeOpts[1].lower():
        slashCommand = '/me : '
    if mode.lower() == modeOpts[2].lower():
        slashCommand = ''
    msg = '{slashCommand} {message}'
    msg = msg.format(slashCommand=slashCommand, message=message)
    Parent.SendStreamMessage(msg)
    return

def GetClipInfo(caster):
    global clipAPI, gameAPI
    clipURL = clipAPI.format(streamer=caster)
    jsonClipsData = json.loads(Parent.GetRequest(clipURL, {}))
    clipsData = json.loads(jsonClipsData['response'])
    clipsList = clipsData['data']
    if len(clipsList) == 0:
        clipInfo = None
        return clipInfo
    selectedClipIndex = randint(0, len(clipsList))
    selectedClip = clipsList[selectedClipIndex]
    gameURL= gameAPI.format(game_id=selectedClip['game_id'])
    jsonGameData = json.loads(Parent.GetRequest(gameURL, {}))
    gameData = json.loads(jsonGameData['response'])
    gameName = gameData['data'][0]['name']
    clipTitle = selectedClip['title']
    clipInfo = {
        'duration': selectedClip['duration'],
        'url': selectedClip['clip_url'],
        'game': gameName,
        'title': clipTitle
    }
    return clipInfo
    
def GetCasterInfo(caster):
    global casterLastGameAPI, lastGameImage, casterAvatar
    noUser = 'User not found: {streamer}'
    noUser = noUser.format(streamer=caster)
    casterLastGameURL = casterLastGameAPI.format(streamer=caster)
    jsonLastGameData = json.loads(Parent.GetRequest(casterLastGameURL, {}))
    if (jsonLastGameData['response'] == noUser):
        msg = '({script} - {version}) - Unable to send a shoutout to {streamer} - it seems their username was entered incorrectly'
        msg = msg.format(script=ScriptName, version=Version, streamer=caster)
        SendInfo('action (/me)', msg)
        return None
    lastGame = jsonLastGameData["response"]
    gameImage = lastGameImage.format(lastGame=lastGame)
    avatar = json.loads(Parent.GetRequest(casterAvatar.format(streamer=caster), {}))['response']
    url = "https://www.twitch.tv/{caster}".format(caster=caster)
    casterInfo = {
        "lastGame": lastGame,
        "gameImage": gameImage,
        "avatar": avatar,
        "url": url
    }
    return casterInfo

def RemovePound(caster):
    if caster[0] == '@':
        caster = caster[1:]
    else:
        caster = caster
    return caster.lower()

def ShoutOut(caster):
    global shoutOutQ, alreadyShout
    displayName = Parent.GetDisplayName(caster)
    casterInfo = GetCasterInfo(caster)
    if (casterInfo !=None):
        clipInfo =  GetClipInfo(caster)
    else:
        return
    shoutMessage = ''
    if wasRaided:
        shoutMessage = scriptSettings['shoutRaiderMessage']
    payload = {
        "casterName": displayName,
        "casterInfo": casterInfo,
        "clipInfo": clipInfo,
        "overlaySettings": overlaySettings,
        "shoutMessage": shoutMessage
    }
    shoutOutQ.append(payload)
    alreadyShout.append(caster)
    return

def TestRaider():
    global shoutQ, scriptSettings
    minRaiders = scriptSettings['shoutRaiderCount']
    data = "@msg-id=raid;msg-param-displayName="+ Parent.GetChannelName() +";msg-param-viewerCount=" + str(Parent.GetRandom(minRaiders, minRaiders + 100)) + "; :tmi.twitch.tv USERNOTICE #" + Parent.GetChannelName()
    raiderData = CheckRaider(data)
    if (raiderData[0]):
        RunCommand('shout {caster}'.format(caster=raiderData[1]), raiderData[1])
    return
    
def CheckRaider(data):
    global raiderName, wasRaided, userNotice, reUserNotice, viewerCount
    reUserNotice = re.compile(r"(?:^(?:@(?P<irctags>[^\ ]*)\ )?:tmi\.twitch\.tv\ USERNOTICE)")
    userNotice = reUserNotice.search(data)
    if userNotice:
        tags = dict(re.findall(r"([^=]+)=([^;]*)(?:;|$)", userNotice.group("irctags")))
        id = tags['msg-id']
        if (id == 'raid'):
            displayName = tags['msg-param-displayName']
            viewerCount = tags['msg-param-viewerCount']
            if int(viewerCount) >= scriptSettings['shoutRaiderCount']:
                raiderName = displayName
            wasRaided = True
    else:
        wasRaided = False
    return [wasRaided, raiderName, viewerCount]

#---------------------------------------
# SetDefaults Custom User Interface Button
#---------------------------------------
def OpenReadMe():
    ReadMe = 'https://github.com/vonschappler/SLCB-ShoutOutClip#readme'
    os.startfile(ReadMe)
    return

def OpenUserGuide():
    Guide = 'https://github.com/vonschappler/SLCB-ShouOutClip/wiki/User-Guide'
    os.startfile(Guide)
    return

def OpenGUI():
    global guiFile
    command = 'python \"{file}"'.format(file=guiFile)
    os.system(command)
    return

def OpenDiscord():
    Discord = "http://rebrand.ly/vonDiscord"
    os.startfile(Discord)
    return

def OpenReleases():
    Release = "https://github.com/vonschappler/SLCB-ShoutOutClip/releases"
    os.startfile(Release)
    return

def OpenDonation():
    PayPal = 'https://rebrand.ly/vonPayPal'
    os.startfile(PayPal)
    return

def OpenTwitch():
    Twitch = "http://rebrand.ly/vonTwitch"
    os.startfile(Twitch)
    return

def OpenSite():
    os.startfile(Website)
    return

def OpenFixObs():
    os.startfile(fixObs)
    return

def TestOverlay():
    caster = Parent.GetChannelName()
    RunCommand('shout {caster}'.format(caster=caster), caster)
    return