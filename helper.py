import nextcord
import constants
from pymongo import MongoClient
import gspread
import pandas as pd



def getNumMembers(client):
    membersz=0
    for x in client.guilds:
        membersz+=len(x.members)+1
    return membersz

async def updatePresence(client):
    await client.change_presence(
        status=nextcord.Status.online, 
        activity=nextcord.Game(
            name = "%shelp %s users"%(
                constants.CMD_PREFIX, getNumMembers(client)
                )
            )
        )


def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"```{cmd_and_aliases} {params}```"