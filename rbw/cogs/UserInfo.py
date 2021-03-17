import asyncio

import discord
from discord.ext import commands, tasks
import json
from var import signature, colorcode, command_usage

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["ui", "useri", "info", "uinfo","infouser"])
    async def userinfo(self, ctx, member: discord.Member = None):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        with open("json/strikes.json", "r") as f:
            strikes = json.load(f)
        if member is None:
            member = ctx.message.author
        else:
            pass
        memberID = str(member.id)
        try:
            embed = discord.Embed(title=f"Userinfo of {member}", description=f"All Gameinfos about {member}", color=colorcode)
            embed.add_field(name="Name:", value=f"`{elo[memberID]['name']}`", inline=False)
            embed.add_field(name="Wins:", value=f"`{elo[memberID]['wins']}`")
            embed.add_field(name="Losses:", value=f"`{elo[memberID]['losses']}`")
            embed.add_field(name="Win-Lose-Ratio:", value=f"`{elo[memberID]['wlr']}%`")
            embed.add_field(name="Elo:", value=f"`{elo[memberID]['elo']}`")
            embed.add_field(name="MVP:", value=f"`{elo[memberID]['mvp']}`")
            if memberID in strikes:
                embed.add_field(name="Strikes:", value=f"`{strikes[memberID]['strikes']}`")
            else:
                embed.add_field(name="Strikes:", value=f"`0`")
            embed.set_footer(text=signature)
            embed.set_thumbnail(url=member.avatar_url)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(50)
            await ctx.message.delete()
            await x.delete()
        except KeyError:
            error = discord.Embed(title=f"{member} is not Registered", description="Use =register `ign` in #register", color=colorcode)
            x = await ctx.send(embed=error)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")



    @userinfo.command()
    async def wins(self, ctx, member: discord.member = None):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        if member is None:
            member = ctx.message.author
        else:
            pass
        memberID = str(member.id)
        try:
            embed = discord.Embed(title=f"Wins of {member}", description=None, color=colorcode)
            embed.add_field(name="Wins:", value=f"`{elo[memberID]['wins']}`")
            embed.set_footer(text=signature)
            embed.set_thumbnail(url=member.avatar_url)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(50)
            await ctx.message.delete()
            await x.delete()

        except KeyError:
            error = discord.Embed(title=f"{member} is not Registered", description="Use =register `ign` in #register", color=colorcode)
            x = await ctx.send(embed=error)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @userinfo.command()
    async def losses(self, ctx, member: discord.member = None):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        if member is None:
            member = ctx.message.author
        else:
            pass
        memberID = str(member.id)
        try:
            embed = discord.Embed(title=f"Losses of {member}", description=None,
                                  color=colorcode)
            embed.add_field(name="Losses:", value=f"`{elo[memberID]['losses']}`")
            embed.set_footer(text=signature)
            embed.set_thumbnail(url=member.avatar_url)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(50)
            await ctx.message.delete()
            await x.delete()

        except KeyError:
            error = discord.Embed(title=f"{member} is not Registered", description="Use =register `ign` in #register", color=colorcode)
            x = await ctx.send(embed=error)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @userinfo.command()
    async def name(self, ctx, member: discord.member = None):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        if member is None:
            member = ctx.message.author
        else:
            pass
        memberID = str(member.id)
        try:
            embed = discord.Embed(title=f"Name of {member}", description=None,
                                  color=colorcode)
            embed.add_field(name="Name:", value=f"`{elo[memberID]['name']}`", inline=False)
            embed.set_footer(text=signature)
            embed.set_thumbnail(url=member.avatar_url)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(50)
            await ctx.message.delete()
            await x.delete()

        except KeyError:
            error = discord.Embed(title=f"{member} is not Registered", description="Use =register `ign` in #register", color=colorcode)
            x = await ctx.send(embed=error)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @userinfo.command()
    async def wlr(self, ctx, member: discord.member = None):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        if member is None:
            member = ctx.message.author
        else:
            pass
        memberID = str(member.id)
        try:
            embed = discord.Embed(title=f"Win/Loss/Ratio of {member}", description=None,
                                  color=colorcode)
            embed.add_field(name="Win-Lose-Ratio:", value=f"`{elo[memberID]['wlr']}%`")
            embed.set_footer(text=signature)
            embed.set_thumbnail(url=member.avatar_url)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(50)
            await ctx.message.delete()
            await x.delete()

        except KeyError:
            error = discord.Embed(title=f"{member} is not Registered", description="Use =register `ign` in #register", color=colorcode)
            x = await ctx.send(embed=error)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @userinfo.command()
    async def elo(self, ctx, member: discord.member = None):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        if member is None:
            member = ctx.message.author
        else:
            pass
        memberID = str(member.id)
        try:
            embed = discord.Embed(title=f"Elo of {member}", description=None,
                                  color=colorcode)
            embed.add_field(name="Elo:", value=f"`{elo[memberID]['elo']}`")
            embed.set_footer(text=signature)
            embed.set_thumbnail(url=member.avatar_url)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(50)
            await ctx.message.delete()
            await x.delete()
        

        except KeyError:
            error = discord.Embed(title=f"{member} is not Registered", description="Use =register `ign` in #register", color=colorcode)
            x = await ctx.send(embed=error)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @userinfo.command()
    async def mvp(self, ctx, member: discord.member = None):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        if member is None:
            member = ctx.message.author
        else:
            pass
        memberID = str(member.id)
        try:
            embed = discord.Embed(title=f"MVP's of {member}", description=None,
                                  color=colorcode)
            embed.add_field(name="MVP:", value=f"`{elo[memberID]['mvp']}`")
            embed.set_footer(text=signature)
            embed.set_thumbnail(url=member.avatar_url)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(50)
            await ctx.message.delete()
            await x.delete()

        except KeyError:
            error = discord.Embed(title=f"{member} is not Registered", description="Use =register `ign` in #register", color=colorcode)
            x = await ctx.send(embed=error)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @userinfo.command()
    @commands.has_role("Staff")
    async def strikes(self, ctx, member: discord.member = None):
        with open("json/strikes.json", "r") as f:
            strikes = json.load(f)
        if member is None:
            member = ctx.message.author
        else:
            pass
        memberID = str(member.id)
        try:
            embed = discord.Embed(title=f"Strikes of {member}", description=None,
                                  color=colorcode)
            if memberID in strikes:
                embed.add_field(name="Strikes:", value=f"`{strikes[memberID]['strikes']}`")
            else:
                embed.add_field(name="Strikes:", value=f"`0`")
            embed.set_footer(text=signature)
            embed.set_thumbnail(url=member.avatar_url)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(50)
            await ctx.message.delete()
            await x.delete()

        except KeyError:
            error = discord.Embed(title=f"{member} is not Registered", description="Use =register `ign` in #register", color=colorcode)
            x = await ctx.send(embed=error)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

def setup(bot):
    bot.add_cog(UserInfo(bot))