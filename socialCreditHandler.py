import nextcord
from nextcord.ext import commands
import helper
import constants
import databaseHandler
import json

import roleHandler

    

    

def getSocialCredit( user:nextcord.Member):
    return databaseHandler.getUserValue(user, "socialCredit")

def getRank( user:nextcord.Member):
    return databaseHandler.getUserValue(user, "rank")

class socialCreditHandler(commands.Cog):
    def __init__(self, client):
        self.client:commands.Bot = client

    async def updateSocialCredit(guild:nextcord.Guild, user:nextcord.Member, amount):
        databaseHandler.incrementUserValue(user, "socialCredit", amount)
        await socialCreditHandler.updateTitle(guild, user)


    async def updateTitle(guild:nextcord.Guild, user:nextcord.Member):
        all_ranks = list(constants.RANK_ROLES.keys())
        currentSocialCredit = getSocialCredit( user)
        currentRank = getRank( user)
        rankIndex = 0;
        if currentSocialCredit > 100:
            rankIndex +=1
        if currentSocialCredit > 1000:
            rankIndex +=1
        if currentSocialCredit > 10000:
            rankIndex +=1
        if currentSocialCredit > 25000:
            rankIndex +=1

        if list(all_ranks).index(currentRank) != rankIndex:
            newRole:str = all_ranks[rankIndex]
            if not await roleHandler.hasRoleByName(guild, newRole):
                await roleHandler.createRankRole(guild, roleName=newRole)
            await roleHandler.addRoleByName(guild, newRole, user)




    @commands.command(name = "awardMember", help = "Awards a member the specified amount of social credit")
    @commands.has_permissions(administrator = True)
    async def awardMember(self, ctx, user:nextcord.Member, amountOfSocialCredit:int):
        await socialCreditHandler.updateSocialCredit(user.guild, user, amountOfSocialCredit)

        embed = nextcord.Embed(
            title = f"{user.display_name} has been awarded {amountOfSocialCredit} social credit!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{user.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed)

    @commands.command(name = "awardRole", help = "Awards all members who have the specified role the specified amount of social credit")
    @commands.has_permissions(administrator = True)
    async def awardRole(self, ctx, role:nextcord.Role, amountOfSocialCredit:int):
        async for member in ctx.guild.fetch_members(limit=None):
            if role in member.roles:
                await socialCreditHandler.updateSocialCredit(member.guild, member, amountOfSocialCredit)

        embed = nextcord.Embed(
            title = f"Members of {role.name} have been awarded {amountOfSocialCredit} social credit!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{role.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed)

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
        embed.timestamp = ctx.message.created_at
        await ctx.channel.send(embed = embed)





    @commands.command(name = "leaderboard", help = "displays top social credit holders")
    async def leaderboard(self, ctx, limit:int=10):
        with open(constants.USER_DATABASE_PATH, "r") as read:
            dictionary = json.load(read)
            sortedIdDictionary = {k:v for k, v in sorted(dictionary["users"].items(), key=lambda item:item[1]["socialCredit"])}
        i=1
        embed = nextcord.Embed(title = "Social Credit Leaderboard", color = ctx.author.color)
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        embed.timestamp = ctx.message.created_at
        rankings = sortedIdDictionary.keys()
        for x in rankings:
            temp = ctx.guild.get_member(int(x)).display_name
            tempSC = sortedIdDictionary[x]["socialCredit"]
            embed.add_field(name = f"{i}: {temp}", value = f"social credit: `{tempSC}SocialCredit`", inline = False) 
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
            for x in rankings["users"].keys():
                databaseHandler.updateUserValue(ctx.guild.get_member(int(x)), "socialCredit", 0)
            embed=nextcord.Embed(
                title = f"{ctx.author.display_name} has reset social credit!", 
                description = "@here", color = nextcord.Color.blue(), 
                )
            embed.set_thumbnail(url = constants.ERROR_EXCLAMATION_ICON)
            embed.timestamp =ctx.message.created_at
            await ctx.channel.send(embed=embed)



    


def setup(client):
    client.add_cog(socialCreditHandler(client))