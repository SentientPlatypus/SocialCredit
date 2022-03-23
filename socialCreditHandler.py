import nextcord
from nextcord.ext import commands
import helper
import constants
import databaseHandler
import json

def updateSocialCredit(user:nextcord.Member, amount):
    databaseHandler.incrementUserValue(user, "socialCredit", amount)

def getSocialCredit(user:nextcord.Member):
    return databaseHandler.getUserValue(user, "socialCredit")


class socialCreditHandler(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command(name = "awardMember", help = "Awards a member the specified amount of social credit")
    @commands.has_permissions(administrator = True)
    async def awardMember(self, ctx, user:nextcord.Member, amountOfSocialCredit:int):
        updateSocialCredit(user, amountOfSocialCredit)

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
                updateSocialCredit(member, amountOfSocialCredit)

        embed = nextcord.Embed(
            title = f"Members of {role.name} have been awarded {amountOfSocialCredit} social credit!",
            color = nextcord.Color.gold()
            )
        embed.timestamp = ctx.message.created_at
        embed.add_field(name = "Awarded by:", value = f"{ctx.author.mention}")
        embed.add_field(name = "Awarded to:", value = f"{role.mention}")
        embed.set_thumbnail(url=constants.SPINNING_COIN_GIF)
        await ctx.channel.send(embed=embed)

    @commands.command(name = "profile", help = "displays the persons social credit")
    async def profile(self, ctx, p:nextcord.Member = None):
        if not p:
            p = ctx.author
        
        points = getSocialCredit(p)

        embed = nextcord.Embed(title = f"{p.display_name}'s social credit!", color = nextcord.Color.green())
        embed.add_field(name = "social credit:", value = f"```{points} social Credit```")
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
        print(rankings)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x).display_name
                tempSC = sortedIdDictionary[x]["socialCredit"]
                embed.add_field(name = f"{i}: {temp}", value = f"social credit: `{tempSC}BP`", inline = False) 
                i+=1
                if i > limit:
                    break
            except:
                pass
        await ctx.channel.send(embed=embed)


    @commands.command(name = "resetSocialCredit", help = "resets ALL social credit to 0")
    @commands.has_permissions(administrator = True)
    async def resetBozuPoints(self, ctx):
        embed=nextcord.Embed(
                title = "Are you sure?", 
                description="reply with `yes` to confirm", 
                color= nextcord.Color.red(), 
                )
        embed.set_thumbnail(url = constants.EXCLAMATION_MARK_IMG)
        embed.timestamp = ctx.message.created_at
        prompt = await ctx.channel.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "yes"
        
        confirm = await self.client.wait_for('message', check=check, timeout=10)
        if confirm:
            rankings = pointDB.find().sort("bozuPoints",-1)
            for x in rankings:
                pointDB.update_one({"id":x["id"]}, {"$set":{"bozuPoints":0}})
            embed=nextcord.Embed(
                title = f"{ctx.author.display_name} has reset social credit!", 
                description = "@here", color = nextcord.Color.blue(), 
                )
            embed.set_thumbnail(url = constants.EXCLAMATION_MARK_IMG)
            embed.timestamp =ctx.message.created_at
            await ctx.channel.send(embed=embed)



    


def setup(client):
    client.add_cog(socialCreditHandler(client))