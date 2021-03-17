import asyncio

import discord
from discord.ext import commands, tasks
import json
from var import signature, colorcode, command_usage

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["leaderboard"])
    async def lb(self, ctx):
        with open("json/elo.json", "r") as f:
            elo =json.load(f)
        top_wins = sorted(elo, key=lambda k: elo[k]["wins"], reverse=True)[:10]
        embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard", description="This is the leaderboard for wins",color=colorcode)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        for member in top_wins:
            membername = ctx.guild.get_member(int(member))
            if membername is None:
                pass
            else:
                # print(type(member))
                embed.add_field(name=membername, value=f"`{elo[member]['wins']}`Wins", inline=False)
        

        


        embed.set_footer(text=signature)
        x = await ctx.send(embed=embed)
        await asyncio.sleep(50)
        await x.delete()
        await ctx.message.delete()

        command_channel = self.bot.get_channel(command_usage)
        await command_channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")


    @lb.command()
    async def wlr(self, ctx):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        '''top_w = sorted(elo, key=lambda k: elo[k]["wins"], reverse=True)
        print(top_w)
        top_l = sorted(elo, key=lambda k: elo[k]["losses"], reverse=True)
        print(top_l)
        top_wins = sorted(elo, key=lambda k: elo[k]["wins"] / elo[k]["losses"], reverse=True)[:10]'''
        embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard", description="This is the leaderboard for Win Loss Ratio",color=colorcode)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        top_wlr = sorted(elo, key=lambda k: elo[k]["wlr"], reverse=True)

        for member in top_wlr:
            membername = ctx.guild.get_member(int(member))
            if membername is None:
                pass
            else:
                embed.add_field(name=f"{membername}", value=f"`{elo[member]['wlr']}%` ({elo[member]['wins']} wins, {elo[member]['losses']} losses)", inline=False)
        
        embed.set_footer(text=signature)
        x = await ctx.send(embed=embed)
        await asyncio.sleep(50)
        await x.delete()
        await ctx.message.delete()
        with open("json/elo.json", "w") as f:
            json.dump(elo, f, indent=4)
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @lb.command()
    async def elo(self, ctx):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)
        top_wins = sorted(elo, key=lambda k: elo[k]["elo"], reverse=True)[:10]
        embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard", description="This is the leaderboard for Elo", color=colorcode)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        for member in top_wins:
            membername = ctx.guild.get_member(int(member))
            # print(type(member))
            embed.add_field(name=f"{membername}", value=f"`{elo[member]['elo']}` elo", inline=False)
        
        embed.set_footer(text=signature)
        x = await ctx.send(embed=embed)
        await asyncio.sleep(50)
        await x.delete()
        await ctx.message.delete()

        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")


def setup(bot):
    bot.add_cog(Leaderboard(bot))