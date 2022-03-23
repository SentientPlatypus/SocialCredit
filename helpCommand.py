
from typing import Optional
import helper
from nextcord import Embed, member
from nextcord.ext import commands
from nextcord.ext.commands import Cog, command
import nextcord
from nextcord.utils import get
import asyncio
#python pagekite.py 5000 scp16tsundere.pagekite.me

class HelpMenu():
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=5)
    
    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title="Help",
                      description="SCP help!",
                      color=self.ctx.author.color)
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        
        return embed
    
    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((entry.brief or "No description", helper.syntax(entry)))

        return await self.write_page(menu, fields)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`",
                        description=helper.syntax(command),
                        color=ctx.author.color)
        embed.add_field(name="Command description", value=command.help)
        await ctx.send(embed=embed)

    @command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):

        if cmd is None:
            leave=False
            pgnum=1
            while leave==False:
                embed = nextcord.Embed(title = "Help", description = "Use `!help <command>` for extended information on a command.", color =nextcord.Color.from_rgb(255, 192, 203))
                if pgnum==1:
                    embed.add_field(name="Bot", value="> `info`,`help`",inline=False)
                    embed.add_field(name = "General", value = "> `userinfo`, `serverinfo`")
                    embed.add_field(name = "SocialCredit 💬", value = "> `profile`, `awardMember`, `awardRole`, `leaderBoard`")
                embed.set_footer(text="navigate with reactions")
                try:
                    await msg.edit(embed=embed)
                    await msg.remove_reaction(emoji=rawreaction, member=ctx.author)
                except:
                    msg= await ctx.send(embed = embed)
                    await msg.add_reaction("⬅️") 
                    await msg.add_reaction("➡️")
                try:
                    def check(reaction, user):
                        return user==ctx.author and str(reaction.emoji) in ["➡️","⬅️"] and reaction.message == msg
                    confirm = await self.bot.wait_for('reaction_add',check=check, timeout = 60)
                    try:
                        if confirm:
                            rawreaction = str(confirm[0])
                            if rawreaction=="➡️":
                                pgnum+=1
                                if pgnum>1:
                                    pgnum=1
                            elif rawreaction=="⬅️":
                                pgnum-=1
                                if pgnum<1:
                                    pgnum=1
                    except:
                        pass
                except asyncio.TimeoutError:
                    break
        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send("That command does not exist.")


def setup(bot):
    bot.add_cog(Help(bot))