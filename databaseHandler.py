from nextcord.ext import commands
import os
import nextcord
from sympy import python, true
import constants as constants
import helper as helper
import json



def getDictionary(path:str = constants.USER_DATABASE_PATH) ->dict:
    """Returns python dictionary from JSON file at path"""
    with open(path, "r") as read:
        return json.load(read)

def updateDatabase(newDictionary:dict, path:str = constants.USER_DATABASE_PATH):
    with open(path, "w") as File:
        json.dump(newDictionary, fp=File, indent=4)

def checkMember(user:nextcord.Member) ->None:
    """Checks a member if its present in the database, and if not, adds it. JSON DOES NOT TAKE INTEGER KEYS."""

    id = str(user.id)
    allUsersDict = getDictionary()
    if id in allUsersDict["users"].keys():
        userDict = allUsersDict["users"][id]
        if userDict["needsUpdate"]:
            for key in constants.USER_DATABASE_DEFAULTS:
                if key not in userDict.keys():
                    userDict[key] = constants.USER_DATABASE_DEFAULTS[key]
            userDict["needsUpdate"] = False
            updateDatabase(allUsersDict)
    else:
        newUserDictionary = constants.USER_DATABASE_DEFAULTS
        newUserDictionary["needsUpdate"] = False
        allUsersDict["users"][id] = newUserDictionary
        updateDatabase(allUsersDict)

def checkMemberById(id:str):
    """Make sure the id is a string. JSON keys cant be integers!"""
    allUsersDict = getDictionary()
    if id in allUsersDict["users"].keys():
        userDict = allUsersDict["users"][id]
        if userDict["needsUpdate"]:
            for key in constants.USER_DATABASE_DEFAULTS:
                if key not in userDict.keys():
                    userDict[key] = constants.USER_DATABASE_DEFAULTS[key]
            userDict["needsUpdate"] = False
            updateDatabase(allUsersDict)
    else:
        newUserDictionary = constants.USER_DATABASE_DEFAULTS
        newUserDictionary["needsUpdate"] = False
        allUsersDict["users"][id] = newUserDictionary
        updateDatabase(allUsersDict)

def checkGuild(guild:nextcord.Guild) ->None:
    """Checks a guild if its present in the database, and if not, adds it. JSON DOES NOT TAKE INTEGER KEYS."""
    id = str(guild.id)
    allGuildsDict = getDictionary(path=constants.GUILD_DATABASE_PATH)
    if id in allGuildsDict["guilds"].keys():
        guildDict = allGuildsDict["guilds"][id]
        if guildDict["needsUpdate"]:
            for key in constants.GUILD_DATABASE_DEFAULTS:
                if key not in guildDict.keys():
                    guildDict[key] = constants.GUILD_DATABASE_DEFAULTS[key]
            guildDict["needsUpdate"] = False
            updateDatabase(allGuildsDict, constants.GUILD_DATABASE_PATH)
    else:
        newGuildDictionary = constants.GUILD_DATABASE_DEFAULTS
        newGuildDictionary["needsUpdate"] = False
        allGuildsDict["guilds"][id] = newGuildDictionary
        updateDatabase(allGuildsDict, constants.GUILD_DATABASE_PATH)


def getPrefix(guild:nextcord.Guild) ->str:
    id = str(guild.id)
    allGuildsDict = getDictionary(constants.GUILD_DATABASE_PATH)
    return allGuildsDict["guilds"][id]["prefix"]

def updateUserValue(user:nextcord.user, key:str, newValue) ->None:
    id = str(user.id)
    allUsersDictionary = getDictionary()
    allUsersDictionary["users"][id][key] = newValue
    updateDatabase(allUsersDictionary)

def getUserValue(user:nextcord.user, key:str):
    id = str(user.id)
    allUsersDictionary = getDictionary()
    return allUsersDictionary["users"][id][key]

def incrementUserValue(user:nextcord.user, key:str, amountToIncrement:int):
    updateUserValue(user, key, getUserValue(user, key) + amountToIncrement)

def updateGuildValue(guild:nextcord.Guild, key:str, newValue) ->None:
    id = str(guild.id)
    allGuildsDictionary = getDictionary(constants.GUILD_DATABASE_PATH)
    allGuildsDictionary["guilds"][id][key] = newValue
    updateDatabase(allGuildsDictionary, constants.GUILD_DATABASE_PATH)

def getGuildValue(guild:nextcord.Guild, key:str):
    id = str(guild.id)
    allGuildsDictionary = getDictionary(constants.GUILD_DATABASE_PATH)
    return allGuildsDictionary["guilds"][id][key]

def incrementGuildValue(user:nextcord.user, key:str, amountToIncrement:int):
    updateGuildValue(user, key, getGuildValue(user, key) + amountToIncrement)


class databseHandler(commands.Cog):
    def __init__(self, client):
        self.client:commands.Bot = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        checkGuild(guild)
        for member in guild.members:
            checkMember(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        checkMember(member)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            checkGuild(guild)
            for member in guild.members:
                checkMember(member)
        print(constants.DB_CHECK_READY_PRINT)

    @commands.command()
    @commands.is_owner()
    async def setUpdateTrueForUsers(self, ctx):
        allUsersDictionary = getDictionary(constants.USER_DATABASE_PATH)
        for key in allUsersDictionary["users"]:
            allUsersDictionary["users"][key]["needsUpdate"] = True
        updateDatabase(allUsersDictionary, constants.USER_DATABASE_PATH)
        for key in allUsersDictionary["users"]:
            checkMemberById(key)
        print("done")



def setup(client):
    client.add_cog(databseHandler(client))