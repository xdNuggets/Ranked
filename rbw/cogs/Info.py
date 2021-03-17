import discord
from discord.ext import commands, tasks
from var import signature, colorcode, command_usage
import asyncio

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(description="Check the ranking system")
    async def ranks(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/723167534697938957/812230689789050900/20210219_132400.jpg")
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")


    @commands.command(description="Credits for the Bot")
    async def credits(self, ctx):
        embed = discord.Embed(title="Credits", description="Thanks to these people for making this bot possible", color=colorcode)
        embed.add_field(name="Developers", value="GozZzer#1245 & Nuggets#0007", inline=False)
        embed.add_field(name="Inspiration", value="ImSeventy's bot, Ranked_bot", inline=False)
        embed.add_field(name="Thanks to Mad & Roie for:", value="helping me with code!", inline=False)
        embed.set_footer(text=signature)
        await ctx.send(embed=embed)
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(title="Not the normal support command", description=None, color=colorcode)
        embed.add_field(name="Support Nuggets", value="https://paypal.me/NuggetsIsCute")
        embed.add_field(name="Support GozZzer", value="https://paypal.me/GozZzer")
        embed.set_footer(text=signature)
        await ctx.send(embed=embed)
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command()
    async def didiask(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        else:
            pass
        x = await ctx.send(f"{member.mention}\nhttps://cdn.discordapp.com/attachments/820650889638576148/820662903598350376/did_i_ask.mp4 ")
        await asyncio.sleep(100)
        await ctx.message.delete()
        await x.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command()
    @commands.has_role("Staff")
    async def id(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        else:
            pass
        await ctx.send(f"ID of {member.mention}: {member.id}")
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command()
    @commands.has_role("Staff")
    async def name(self, ctx, member : discord.Member = None):
        member_id = member.id
        if member_id is None:
            member_id = ctx.message.author.id
        else:
            pass
        member_name = await ctx.guild.fetch_member(member_id)
        await ctx.send(f'Name of {member}: {member_name.mention}')
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

def setup(bot):
    bot.add_cog(Info(bot))