from datetime import datetime
import nextcord
from nextcord.ext import commands
import helper
import constants
import databaseHandler
import json

import roleHandler

USER_MESSAGE_COUNTER = {

}

    

def getSocialCredit( user:nextcord.Member):
    return databaseHandler.getUserValue(user, "socialCredit")

def getRank( user:nextcord.Member) ->str:
    return databaseHandler.getUserValue(user, "rank")



class socialCreditHandler(commands.Cog):
    def __init__(self, client):
        self.client:commands.Bot = client

    async def updateSocialCredit(guild:nextcord.Guild, user:nextcord.Member, amountToIncrementBy):
        """INCREMENTS SOCIAL CREDIT. TO SET SOCIAL CREDIT, user setSocialCredit"""
        databaseHandler.incrementUserValue(user, "socialCredit", amountToIncrementBy)
        return await socialCreditHandler.updateTitle(guild, user)

    async def setSocialCredit(guild:nextcord.Guild, user:nextcord.Member, amountTOincrementBY):
        databaseHandler.updateUserValue(user, "socialCredit", 0)
        return await socialCreditHandler.updateTitle(guild, user)

    async def getRoleUpdateMessage(user:nextcord.Member) -> nextcord.Embed:
        all_ranks = constants.RANK_ROLES.keys()
        newRank = getRank(user)
        desc = constants.RANK_ROLES[newRank]["desc"]
        embed = nextcord.Embed(title = f"{user.display_name}'s rank has been updated to {newRank}", description=f"```{desc}```")
        r, g, b = constants.RANK_ROLES[newRank]["color"]
        embed.color = nextcord.Color.from_rgb(r, g, b)
        embed.timestamp = datetime.now()
        return embed
        
    async def updateTitle(guild:nextcord.Guild, user:nextcord.Member):
        all_ranks = list(constants.RANK_ROLES.keys())
        currentSocialCredit = getSocialCredit( user)
        currentRank = getRank(user)
        newRank:str = currentRank
        for rank in all_ranks:
            if currentSocialCredit >= constants.RANK_ROLES[rank]["minSocialCredit"]:
                newRank = rank
            else:
                break
        if currentRank != newRank:
            if not await roleHandler.hasRoleByName(guild, newRank):
                await roleHandler.createRankRole(guild, roleName=newRank)
            if await roleHandler.hasRoleByName(guild, currentRank):
                await roleHandler.removeRankRole(guild, user, currentRank)
            await roleHandler.addRoleByName(guild, newRank, user)
            databaseHandler.updateUserValue(user, "rank", newRank)
            return await socialCreditHandler.getRoleUpdateMessage(user)




    @commands.command(name = "awardMember", aliases = ["awardmember", "awardperson"], help = "Awards a member the specified amount of social credit")
    @commands.has_permissions(administrator = True)
    async def awardMember(self, ctx, user:nextcord.Member, amountOfSocialCredit:int):
        rankUpEmbed = await socialCreditHandler.updateSocialCredit(user.guild, user, amountOfSocialCredit)
        embed = nextcord.Embed(
            title = f"{user.display_name} has been awarded {amountOfSocialCredit} social credit!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{user.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed)
        if rankUpEmbed:
            await ctx.channel.send(embed=rankUpEmbed)


    @commands.command(name = "awardRole", aliases = ["awardRank", "awardrank", "awardrole"], help = "Awards all members who have the specified role the specified amount of social credit")
    @commands.has_permissions(administrator = True)
    async def awardRole(self, ctx, role:nextcord.Role, amountOfSocialCredit:int):
        async for member in ctx.guild.fetch_members(limit=None):
            if role in member.roles:
                rankUpEmbed = await socialCreditHandler.updateSocialCredit(member.guild, member, amountOfSocialCredit)

        embed = nextcord.Embed(
            title = f"Members of {role.name} have been awarded {amountOfSocialCredit} social credit!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{role.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed  )
        if rankUpEmbed:
            await ctx.channel.send(embed=rankUpEmbed)


    @commands.command(name = "profile", help = "displays the persons profile")
    async def profile(self, ctx, p:nextcord.Member = None):
        if not p:
            p = ctx.author
        
        points = getSocialCredit(p)

        embed = nextcord.Embed(title = f"{p.display_name}'s profile!", color = nextcord.Color.green())
        embed.add_field(name = "social credit:", value = f"```{points} social Credit```")
        embed.add_field(name="Rank", value="```"+databaseHandler.getUserValue(p, "rank")+"```")
        embed.set_author(name = p.display_name, icon_url=p.avatar)
        embed.set_thumbnail(url = constants.SPINNING_COIN_GIF)
        r, g, b = constants.RANK_ROLES[getRank(p)]["color"]
        embed.color = nextcord.Color.from_rgb(r, g, b)
        embed.timestamp = ctx.message.created_at
        await ctx.channel.send(embed = embed)





    @commands.command(name = "leaderboard", aliases = ["lb"],help = "displays top social credit holders")
    async def leaderboard(self, ctx, limit:int=10):
        with open(constants.USER_DATABASE_PATH, "r") as read:
            dictionary = json.load(read)
            sortedIdDictionary = {k:v for k, v in sorted(dictionary["users"].items(), key=lambda item:-item[1]["socialCredit"])}
        i=1
        embed = nextcord.Embed(title = "Social Credit Leaderboard", color = ctx.author.color)
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        embed.timestamp = ctx.message.created_at
        rankings = sortedIdDictionary.keys()
        for x in rankings:
            temp = ctx.guild.get_member(int(x)).display_name
            tempSC = sortedIdDictionary[x]["socialCredit"]
            embed.add_field(name = f"{i}: {temp}", value = f"`{tempSC} Social credit`", inline = False) 
            i+=1
            if i > limit:
                break

        await ctx.channel.send(embed=embed)


    @commands.command(name = "resetSocialCredit", help = "resets ALL social credit to 0")
    @commands.has_permissions(administrator = True)
    async def resetSocialCredit(self, ctx):
        embed=nextcord.Embed(
                title = "Are you sure?", 
                description="reply with `yes` to confirm", 
                color= nextcord.Color.red(), 
                )
        embed.set_thumbnail(url = constants.ERROR_EXCLAMATION_ICON)
        embed.timestamp = ctx.message.created_at
        prompt = await ctx.channel.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "yes"
        
        confirm = await self.client.wait_for('message', check=check, timeout=10)
        if confirm:
            rankings = databaseHandler.getDictionary()
            guild:nextcord.Guild = ctx.guild
            async for member in guild.fetch_members(limit=None):
                await socialCreditHandler.setSocialCredit(ctx.guild, member, 0)
            
            


            embed=nextcord.Embed(
                title = f"{ctx.author.display_name} has reset social credit!", 
                description = "@here", color = nextcord.Color.blue(), 
                )
            embed.set_thumbnail(url = constants.ERROR_EXCLAMATION_ICON)
            embed.timestamp =ctx.message.created_at
            await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message:nextcord.Message):
        dictKey = str(message.author.id)

        await helper.handleBadWords(message)
        if dictKey in USER_MESSAGE_COUNTER.keys():
            USER_MESSAGE_COUNTER[dictKey] +=1
            if USER_MESSAGE_COUNTER[dictKey] == 10:
                databaseHandler.incrementUserValue(message.author, "socialCredit", 1)
                rankUpEmbed = await socialCreditHandler.updateTitle(message.guild, message.author)
                USER_MESSAGE_COUNTER[dictKey] = 0
                if rankUpEmbed:
                    await message.channel.send(embed=rankUpEmbed)
        else:
            USER_MESSAGE_COUNTER[dictKey] = 1



    


def setup(client):
    client.add_cog(socialCreditHandler(client))