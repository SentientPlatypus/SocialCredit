from typing import List
import nextcord
from nextcord.ext import commands
import helper
import constants


async def hasRoleByName(guild:nextcord.Guild, roleName:str) -> bool:
    allRoles = await guild.fetch_roles()
    for role in allRoles:
        if role.name.lower() == roleName.lower():
            return True
    return False

async def getRoleByName(guild:nextcord.Guild, roleName:str) -> nextcord.Role:
    allRoles = await guild.fetch_roles()
    for role in allRoles:
        if role.name.lower() == roleName.lower():
            return role
    return None

async def addRoleByName(guild:nextcord.Guild, roleName:str, user:nextcord.Member):
    allRolesInGuild:List[nextcord.Role] = await guild.fetch_roles()
    await user.add_roles(*[await getRoleByName(guild, roleName)])


async def hasChannel(guild:nextcord.Guild, channelName:str) ->bool:
    allChannels = await guild.fetch_channels()
    for channel in allChannels:
        if channel.name.lower() == channelName.lower():
            return True
    return False

async def getChannel(guild:nextcord.Guild, channelName:str):
    allChannels = await guild.fetch_channels()
    for channel in allChannels:
        if channel.name.lower() == channelName.lower():
            return channel
    return channel

async def peopleWhoHaveRole(guild:nextcord.Guild, role:nextcord.Role) ->List[nextcord.Member]:
    roleOwners = []
    async for member in guild.fetch_members(limit = None):
        if role in member.roles:
            roleOwners.append(member)
    return roleOwners


async def createRankRole(guild:nextcord.Guild, roleName:str) ->None:
    r, g, b = constants.RANK_ROLES[roleName]["color"]
    guild.create_role(name=roleName, color=nextcord.Color.from_rgb(r, g, b))


class roleHandler(commands.Cog):
    def __init__(self, client):
        self.client:commands.Bot = client




def setup(client):
    client.add_cog(roleHandler(client))