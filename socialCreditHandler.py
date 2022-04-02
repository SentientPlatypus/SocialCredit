import asyncio
from datetime import datetime
from socket import timeout
from tabnanny import check
from turtle import color
from matplotlib.pyplot import text
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


    @commands.command(name = "hail", aliases = ["hailrepublic", "hailRepublic", "dailyBonus"], help = "daily bonus social credit when you hail the republic")
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def dailyBonus(self, ctx):
        rankUpEmbed = await socialCreditHandler.updateSocialCredit(ctx.guild, ctx.author, constants.DAILY_BONUS_REWARD)
        embed = nextcord.Embed(
            title = f"{ctx.author.display_name} has hailed the Peoples Republic of IHS and has been awarded {constants.DAILY_BONUS_REWARD} social credit!",
            color = nextcord.Color.gold(),
            description= "```All hail the Peoples Republic of IHS!```"
            )
        embed.timestamp = ctx.message.created_at
        embed.set_thumbnail(url=constants.FLAG_IMG)
        await ctx.channel.send(embed=embed)
        if rankUpEmbed:
            await ctx.channel.send(embed=rankUpEmbed)


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



    @commands.command(name = "shame", aliases = ["stone", "accuse"],help = "shame someone if they deserve it")
    async def shame(self, ctx, member:nextcord.Member, *, reason):
        msg:nextcord.Message = ctx.message
        sender:nextcord.Member = ctx.author
        em = nextcord.Embed(title = f"{sender.display_name} shames {member.display_name}!", description=f"Reason: ```{reason}```", color=nextcord.Color.red())
        em.add_field(name = f"Does {member.display_name} deserve to be punished?", value="````You decide. React with ✅ if you support the punishment. React with ❌ if you dont.```")
        em.set_footer(text=f"Action will be taken at {constants.MINIMUM_SHAME_VOTES} votes.")
        em.timestamp = msg.created_at
        punishEmbed:nextcord.Message = await ctx.channel.send(embed=em)
        await punishEmbed.add_reaction("✅")
        await punishEmbed.add_reaction("❌")
        punishVotes = 1
        supportVotes = 1
        while punishVotes < constants.MINIMUM_SHAME_VOTES and supportVotes < constants.MINIMUM_SHAME_VOTES:
            def check2(reaction:nextcord.Reaction, user:nextcord.Member):
                return str(reaction.emoji) in ["✅", "❌"] and reaction.message == punishEmbed
            confirm = await self.client.wait_for("reaction_add", check=check2)
            if confirm:
                punishEmbed = await ctx.channel.fetch_message(punishEmbed.id)
                punishVotes = 1 + punishEmbed.reactions[0].count
                supportVotes = 1 + punishEmbed.reactions[1].count

        if punishVotes > supportVotes:
            em = nextcord.Embed(title = f"The people have spoken!", description=f"Reason: ```Since there were more votes to punish, {member.display_name} will be penalized {constants.SHAME_PENALTY} social credit for endangering the republic```", color=nextcord.Color.red())
            em.timestamp = msg.created_at
            await socialCreditHandler.updateSocialCredit(ctx.guild, member, -constants.SHAME_PENALTY)
            try:
                await punishEmbed.reply(embed=em)
            except:
                await ctx.channel.send(embed=em)
        else:
            em = nextcord.Embed(title = f"The people have spoken!", description=f"Reason: ```Since there were more votes to support, {sender.display_name} will be penalized {constants.SHAME_PENALTY} social credit for being a jerk.```", color=nextcord.Color.red())
            em.timestamp = msg.created_at
            await socialCreditHandler.updateSocialCredit(ctx.guild, sender, -constants.SHAME_PENALTY)
            try:
                await punishEmbed.reply(embed=em)
            except:
                await ctx.channel.send(embed=em)

        


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
            try:
                temp = ctx.guild.get_member(int(x)).display_name
                tempSC = sortedIdDictionary[x]["socialCredit"]
                embed.add_field(name = f"{i}: {temp}", value = f"`{tempSC} Social credit`", inline = False) 
                i+=1
                if i > limit:
                    break
            except:
                pass

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


    @commands.command(name = "trivia", help = f"a gamble. If you get it right, you will recieve {constants.TRIVIA_REWARD} otherwise, you get {constants.TRIVIA_PENALTY}")
    async def trivia(self, ctx):
        questionObj:helper.TriviaQuestion = helper.getTriviaQuestion()
        questionEmbed = nextcord.Embed(title = f"{questionObj.question}", description = questionObj.optionStr, color=nextcord.Color.yellow())
        questionEmbed.set_footer(text = f"You have {constants.TRIVIA_TIME_LIMIT} seconds to answer.")
        questionMsg:nextcord.Message = await ctx.channel.send(embed=questionEmbed)
        reactionOptions = questionObj.optionDict.keys()
        for reaction in reactionOptions:
            await questionMsg.add_reaction(reaction)

        def check(reaction:nextcord.Reaction, user):
            return str(reaction.emoji) in reactionOptions and reaction.message == questionMsg and user == ctx.author
        
        try:
            confirm = self.client.wait_for("reaction_add", check=check)
            rawReaction = str(confirm[0])
            isCorrect = questionObj.optionDict[rawReaction] == questionObj.correctAnswer

            if isCorrect:
                em = nextcord.Embed(title = f"Correct Answer!", description = f"{ctx.author.display_name} will be rewarded {constants.TRIVIA_REWARD} social credit", color=nextcord.Color.green())
                em.timestamp = datetime.now()
                await ctx.channel.send(embed=em)
                await socialCreditHandler.updateSocialCredit(ctx.guild, ctx.author, constants.TRIVIA_REWARD)
            else:
                em = nextcord.Embed(title = f"Incorrect Answer!", description = f"{ctx.author.display_name} will be penalized {constants.TRIVIA_PENALTY} social credit", color=nextcord.Color.red())
                em.timestamp = datetime.now()
                await ctx.channel.send(embed=em)
                await socialCreditHandler.updateSocialCredit(ctx.guild, ctx.author, -constants.TRIVIA_REWARD)





        except asyncio.TimeoutError:
            timeOut = nextcord.Embed(title = f"You took too long to answer.", description = f"{ctx.author.mention} will be penalized {constants.TRIVIA_PENALTY} social credit", color=nextcord.Color.red())
            timeOut.timestamp = datetime.now()
            await ctx.channel.send(embed=timeout)




    @commands.Cog.listener()
    async def on_message(self, message:nextcord.Message):
        dictKey = str(message.author.id)

        if isinstance(message.channel, nextcord.channel.DMChannel):
            return
        await helper.handleBadWords(message)
        if dictKey in USER_MESSAGE_COUNTER.keys():
            USER_MESSAGE_COUNTER[dictKey] +=1
            if USER_MESSAGE_COUNTER[dictKey] == 4:
                databaseHandler.incrementUserValue(message.author, "socialCredit", 1)
                rankUpEmbed = await socialCreditHandler.updateTitle(message.guild, message.author)
                USER_MESSAGE_COUNTER[dictKey] = 0
                if rankUpEmbed:
                    await message.channel.send(embed=rankUpEmbed)
        else:
            USER_MESSAGE_COUNTER[dictKey] = 0

    




    


def setup(client):
    client.add_cog(socialCreditHandler(client))