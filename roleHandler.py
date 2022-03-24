import nextcord
from nextcord.ext import commands
import helper
import constants
cluster = helper.getMongo()
pointDB = cluster["discord"]["bozuPoints"]


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

async def peopleWhoHaveRole(guild:nextcord.Guild, role:nextcord.Role):
    roleOwners = []
    async for member in guild.fetch_members(limit = None):
        if role in member.roles:
            roleOwners.append(member)
    return roleOwners

def lookup(guild:nextcord.Guild,member:nextcord.Member, returnedData,
        roleNameColHead:str = "Team Number", 
        locationColHead:str = "Team Location", 
        LevelColHead:str = "Team Skill Level",
        member1ColHead:str = "Member 1 Discord Username", 
        member2ColHead:str= "Member 2 Discord Username", 
        member3ColHead:str= "Member 3 Discord Username", 
        member4ColHead:str= "Member 4 Discord Username", 
        member5ColHead:str= "Member 5 Discord Username", 
):
    row = next(
        x for x in returnedData 
        if guild.get_member_named(x[member1ColHead]) == member
        or guild.get_member_named(x[member2ColHead]) == member
        or guild.get_member_named(x[member3ColHead]) == member
        or guild.get_member_named(x[member4ColHead]) == member
        or guild.get_member_named(x[member5ColHead]) == member
    )
    return {
        "location": row[locationColHead],
        "level" : row[LevelColHead],
        "group" : f"group-{row[roleNameColHead]}"
    }


class roleHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "sortBySpreadsheet", help = "will manage member roles and group chats based on the spreadsheet. rishi, dont mind the parameters, they have default values. just call !sortBySpreadsheet. ")
    @commands.has_permissions(administrator= True)
    async def sortBySpreadsheet(self, ctx,
        spreadSheetName:str = "CodeBozu Fellowship 2 Teams",
        roleNameColHead:str = "Team Number", 
        locationColHead:str = "Team Location", 
        LevelColHead:str = "Team Skill Level",
        member1ColHead:str = "Member 1 Discord Username", 
        member2ColHead:str= "Member 2 Discord Username", 
        member3ColHead:str= "Member 3 Discord Username", 
        member4ColHead:str= "Member 4 Discord Username", 
        member5ColHead:str= "Member 5 Discord Username", 
    ):
        embed=nextcord.Embed(
                title = "Are you sure?", 
                description="reply with `yes` to confirm", 
                color= nextcord.Color.red(), 
                )
        embed.set_thumbnail(url = constants.EXCLAMATION_MARK_IMG)
        embed.add_field(
            name = "This command will:",
            value="""
            1. Manage roles and chats based on the spreadsheet
            2. assume members are only on one team
            3. only sort people who have a valid username (with or without discriminator) 
            4. ONLY WORK IF GROUP ROLES ARENT THE HIGHEST ROLES A MEMBER HAS. (fellowship role must be higher)
            """
        )
        embed.add_field(
            name = "NOTE:",
            value="""
            Bozu will determine if a row is valid if it has
            -A team location
            -A team level
            -Has a non empty cell for the first member
            """
        )
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text="Rishi yo ass better be careful before executing this one")
        prompt = await ctx.channel.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "yes"
        
        confirm = await self.client.wait_for('message', check=check, timeout=10)
        await ctx.trigger_typing()
        if confirm:
            groupChatCategory = await getChannel(ctx.guild, constants.DEFAULT_GROUP_CHAT_CATEGORY) if await hasChannel(ctx.guild, constants.DEFAULT_GROUP_CHAT_CATEGORY) else await ctx.guild.create_category(constants.DEFAULT_GROUP_CHAT_CATEGORY)
            groupChatCategory2 = await getChannel(ctx.guild, constants.DEFAULT_GROUP_CHAT_CATEGORY2) if await hasChannel(ctx.guild, constants.DEFAULT_GROUP_CHAT_CATEGORY2) else await ctx.guild.create_category(constants.DEFAULT_GROUP_CHAT_CATEGORY2)
            groupChatCategory3 = await getChannel(ctx.guild, constants.DEFAULT_GROUP_CHAT_CATEGORY3) if await hasChannel(ctx.guild, constants.DEFAULT_GROUP_CHAT_CATEGORY3) else await ctx.guild.create_category(constants.DEFAULT_GROUP_CHAT_CATEGORY3)


            recievedData = helper.getSpreadSheetData(r"C:\Users\trexx\Documents\PYTHON CODE LOL\CODEBOZU\bozuBot\bot-env\credentials.json", spreadSheetName)
            for row in recievedData:
                print(row)
                location = row[locationColHead]
                level = row[LevelColHead]

                m1 = ctx.guild.get_member_named(row[member1ColHead]) if row[member1ColHead] != "" else None
                m2 = ctx.guild.get_member_named(row[member2ColHead]) if row[member2ColHead] != "" else None
                m3 = ctx.guild.get_member_named(row[member3ColHead]) if row[member3ColHead] != "" else None
                m4 = ctx.guild.get_member_named(row[member4ColHead]) if row[member4ColHead] != "" else None
                m5 = ctx.guild.get_member_named(row[member5ColHead]) if row[member5ColHead] != "" else None
                roleName = f"group-{row[roleNameColHead]}"
                if location != "" and level != "" and m1 != "":
                    
                    locationRole = await getRoleByName(ctx.guild, location) if await hasRoleByName(ctx.guild, location) else await ctx.guild.create_role(name = location)
                    levelRole = await getRoleByName(ctx.guild, level) if await hasRoleByName(ctx.guild, level) else await ctx.guild.create_role(name = level)
                    createdRole = await getRoleByName(ctx.guild, roleName) if await hasRoleByName(ctx.guild, roleName) else await ctx.guild.create_role(name = roleName)
                    
                    for memberObj in [m1,m2,m3,m4, m5]:
                        if not memberObj:
                            continue
                        await memberObj.add_roles(*[createdRole, locationRole, levelRole])
                        print("MADE IT HERE")

                    otherPeopleWhoHaveRole = [m for m in await peopleWhoHaveRole(ctx.guild, createdRole) if m not in [m1,m2,m3,m4,m5]]
                    
                    for other in otherPeopleWhoHaveRole:
                        toRemove = []
                        otherData = lookup(
                            ctx.guild, other, recievedData, roleNameColHead,locationColHead,
                            LevelColHead, member1ColHead, member2ColHead, member3ColHead, member4ColHead
                        )
                        if otherData["group"] != createdRole.name:
                            toRemove.append(createdRole)
                        if otherData["location"] != locationRole.name:
                            toRemove.append(locationRole)
                        if otherData["level"] != levelRole.name:
                            toRemove.append(levelRole)

                        for role in toRemove:
                            try:
                                await other.remove_roles(role)
                            except:
                                pass

                    overwrites = {
                        ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                        createdRole: nextcord.PermissionOverwrite(read_messages = True)
                    }
                    if not await hasChannel(ctx.guild, roleName):
                        try:
                            await ctx.guild.create_text_channel(roleName, overwrites = overwrites, category= groupChatCategory)
                        except:
                            try:
                                await ctx.guild.create_text_channel(roleName, overwrites = overwrites, category= groupChatCategory2)
                            except:
                                try:
                                    await ctx.guild.create_text_channel(roleName, overwrites = overwrites, category= groupChatCategory3)
                                except:
                                    pass
            embed = nextcord.Embed(title = "Hopefully that worked LMAO", color = nextcord.Color.yellow())
            embed.set_image(url=constants.PRAYING_CHEEMS_IMG)
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(roleHandler(client))