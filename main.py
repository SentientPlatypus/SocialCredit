from nextcord.ext import commands
import os
import sys
import nextcord
import datetime
import math
import traceback
import asyncio
##-------------HELPERS-------------------------------
import constants
import helper

##--------------WEBSERV-------------------------------
from keep_alive import keep_alive

##-------------COGS-----------------------------------
import helpCommand
import databaseHandler
import socialCreditHandler
import roleHandler

print("we out")

async def determinePrefix(bot, message):
    guild = message.guild
    if guild:
        databaseHandler.getPrefix(guild.id)
client = commands.Bot(command_prefix="!", intents =nextcord.Intents.all(), status=nextcord.Status.online)




##------------INITIALIZING COGS----------------------
roleHandlerCog = [roleHandler]
for i in range(len(roleHandlerCog)):
    roleHandlerCog[i].setup(client)

databaseHandlerCog = [databaseHandler]
for i in range(len(databaseHandlerCog)):
    databaseHandlerCog[i].setup(client)

helpCommandCog = [helpCommand]
for i in range(len(helpCommandCog)):
    helpCommandCog[i].setup(client)

socialCreditHandlerCog = [socialCreditHandler]
for i in range(len(socialCreditHandlerCog)):
    socialCreditHandlerCog[i].setup(client)




@client.command(name = "info", help = "Gives information about me!")
async def info(ctx):
    embed=nextcord.Embed(title="Peoples repubilc of IHS Information", color=nextcord.Color.purple())
    embed.description= "Current persons in the republic:%g"%(len(client.guilds))
    embed.set_footer(text="by Gene")

    embed.set_thumbnail(url=client.user.avatar)
    await ctx.channel.send(embed=embed)


@client.command(name = "ranks", aliases=["ranking", "rankinginfo", "rankingInfo", "rank"], help = "Gives information about the ranking system")
async def ranks(ctx):
    embed=nextcord.Embed(title="The Ranking system", color=nextcord.Color.purple())
    embed.description= "Your rank is determined by your current social credit score."
    for rankName in constants.RANK_ROLES.keys():
        requiredSocialCredit = constants.RANK_ROLES[rankName]["minSocialCredit"]
        embed.add_field(name = rankName, value= f"```Social credit required: {requiredSocialCredit}```")

    embed.add_field(name = "How does social credit work?", value="```Social credit can be obtained by sending chat messages (+1 social credit / 10 messages), or it can be awarded by admins. (see !awardMember & !awardRole)```")
    embed.set_footer(text="by Gene")

    embed.set_thumbnail(url=client.user.avatar)
    await ctx.channel.send(embed=embed)

@client.command(name = "userinfo", help = "returns User's info", aliases=["ui"])
@commands.guild_only()
@commands.cooldown(1, 4, commands.BucketType.user)
async def userinfo(ctx, user:nextcord.Member = None):
    if not user:
        user = ctx.author
    try:
        playinggame = user.activity.title
    except:
        playinggame = None
    embed = nextcord.Embed(title = f"User info for {user.display_name}", color = nextcord.Color.blue())
    embed.description = f"displays the information about {user.mention}"
    embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar)

    server = ctx.message.guild
    embed.add_field(name = "Social credit", value=databaseHandler.getUserValue(user, "socialCredit"))
    embed.set_author(name=user.name, icon_url=user.display_avatar)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Discriminator", value=user.discriminator)
    embed.add_field(name="Bot", value=str(user.bot))
    embed.add_field(name="Created", value=user.created_at.strftime("%d %b %Y %H:%M"))
    embed.add_field(name="Joined", value=user.joined_at.strftime("%d %b %Y %H:%M"))
    embed.add_field(name="Playing", value=playinggame)
    embed.add_field(name="Status", value=user.status)
    embed.add_field(name="Color", value=str(user.color))

    try:
        roles = [x.name for x in user.roles if x.name != "@everyone"]

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                        if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"
        embed.add_field(name="Roles", value=roles)
    except:
        pass
    embed.timestamp = ctx.message.created_at

    await ctx.reply(embed=embed)

@client.command(name = "serverinfo", help = "returns server's info", aliases=["si"])
@commands.guild_only()
@commands.cooldown(1, 4, commands.BucketType.user)
async def serverinfo(ctx):
    """Display Server Info"""
    server = ctx.guild
    verif = server.verification_level

    online = len([m.status for m in server.members
                    if m.status == nextcord.Status.online or
                    m.status == nextcord.Status.idle])

    embed = nextcord.Embed(color=0xDEADBF)
    embed.add_field(name="Name", value=f"**{server.name}**\n({server.id})")
    embed.add_field(name="Owner", value=server.owner)
    embed.add_field(name="Online (Cached)", value=f"**{online}/{server.member_count}**")
    embed.add_field(name="Created at", value=server.created_at.strftime("%d %b %Y %H:%M"))
    embed.add_field(name="Channels", value=f"Text Channels: **{len(server.text_channels)}**\n"
    f"Voice Channels: **{len(server.voice_channels)}**\n"
    f"Categories: **{len(server.categories)}**\n"
    f"AFK Channel: **{server.afk_channel}**")
    embed.add_field(name="Roles", value=str(len(server.roles)))
    embed.add_field(name="Emojis", value=f"{len(server.emojis)}/100")
    embed.add_field(name="Region", value=str(server.region).title())
    embed.add_field(name="Security", value=f"Verification Level: **{verif}**\n"
    f"Content Filter: **{server.explicit_content_filter}**")

    try:
        embed.set_thumbnail(icon=server.icon)
    except:
        pass

    await ctx.send(embed=embed)




@client.command(name = "poll", help = "initializes a poll", aliases=["polls"])
async def poll(ctx, title, *l):
    await ctx.message.delete()
    if len(l)>=11:
        embed = nextcord.Embed(title = "Do a better job at making options.", description = "This isnt a Third world election.", color = ctx.author.color)
        await ctx.send(embed = embed)
    closed = False
    while closed == False:
        l = list(l)
        title = str(title)
        options = [' '+ x  for x in l]
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
        optionsfinal = []
        for x in range(len(options)):
            optionsfinal.append(reactions[x]+options[x])
        optionsfinal = [x + "\n\n" for x in optionsfinal]
        embed = nextcord.Embed(title = "%s"%(title), description = "%s\n\n\n"%("".join(optionsfinal)), color = ctx.author.color)
        embed.set_author(name= ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.timestamp = ctx.message.created_at
        try:
            if suggestions == True:
                embed.set_footer(text = "suggestions are open! use the ➕ to add a suggestion!")
        except:
            embed.set_footer(text = "%s hasnt opened suggestions to this poll."%(ctx.author.display_name))
        try:
            await msg.edit(embed=embed)
        except:
            msg = await ctx.send(embed = embed)
        for x in range(len(l)):
            await msg.add_reaction(reactions[x])
        await msg.add_reaction("➕")
        await msg.add_reaction("🚪")

        try:
            if suggestions== True:
                def check2(reaction, user):
                    return str(reaction.emoji) in ["➕", "🚪"] and reaction.message==msg
                confirm2 = await client.wait_for('reaction_add', check=check2)
                if confirm2:
                    if str(confirm2[0]) == "➕":
                        doodle = await ctx.channel.send(embed=nextcord.Embed(title = "Type your suggestion!", color = ctx.author.color))
                        def check3(m):
                            return m.channel == ctx.channel
                        confirm3 = await client.wait_for('message', check=check3)
                        await doodle.delete()
                        await confirm3.delete()
                        l.append("%s"%(confirm3.content))
                if str(confirm2[0]) == "🚪":
                    if str(confirm2[1]) == str(ctx.author):
                        embed.set_footer(text="This poll is closed!")
                        await msg.edit(embed=embed)
                        closed = True
                        break
        except:
            def check(reaction,user):
                return user==ctx.author and str(reaction.emoji) in ["➕", "🚪"] and reaction.message==msg
            confirm = await client.wait_for('reaction_add', check=check)
            if confirm:
                if str(confirm[0]) == "➕":
                    embed.set_footer(text = "suggestions are open! use the ➕ to add a suggestion!")
                    await msg.edit(embed=embed)
                    suggestions = True
                
                if str(confirm[0]) == "🚪":
                    embed.set_footer(text="This poll is closed!")
                    await msg.edit(embed=embed)
                    closed = True
                    break

























@client.event
async def on_command_error(ctx, error):
    prefix = databaseHandler.getPrefix(ctx.guild)
    commandThatFailed = ctx.command
    embed = nextcord.Embed()
    embed.timestamp = ctx.message.created_at
    embed.set_author(icon_url=client.user.avatar, name="Command Error")
    embed.set_thumbnail(url=constants.ERROR_EXCLAMATION_ICON)
    embed.color=nextcord.Color.red()
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Retry in %s"%(datetime.timedelta(seconds=math.floor(error.retry_after)))
        embed.title = "Still On Cooldown!"
        embed.description = "```%s```"%(msg)
    elif isinstance(error, commands.CommandNotFound):
        embed.title = "Command not found!!"
        embed.description = f"```That command does not exist! see {prefix}help```"
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.title = "Missing Argument!"
        embed.description = "Syntax: %s"%(helper.syntax(commandThatFailed))
        embed.set_footer(text = 'Make Sure to add "quotation marks" around a parameter that has a space!')
    elif isinstance(error, commands.BadArgument):
        embed.title="Bad Argument"
        embed.description="```%s```"%(str(error))
    elif isinstance(error, asyncio.TimeoutError):
        embed.title = "Timeout"
        embed.description= "```you took too long for that interaction, dummy.```"
    elif isinstance(error, commands.MissingPermissions):
        embed.title = "Missing Permissions"
        embed.description= "```You dont have le perms```"
    else:
        print("failed")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return
    await ctx.channel.send(embed=embed)




@client.event
async def on_ready():
    print(constants.FINAL_READY_PRINT)
    await helper.updatePresence(client)

@client.event
async def on_member_join(member):
    await helper.updatePresence(client)

@client.event
async def on_guild_join(member):
    await helper.updatePresence(client)


keep_alive()
client.run(constants.BOT_TOKEN)
