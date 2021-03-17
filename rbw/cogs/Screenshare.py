import asyncio

import discord
from discord.ext import commands
from var import signature, colorcode, getting_ssed, waiting_to_ss, command_usage


class Screenshare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["screenshare"])
    async def ss(self, ctx, member : discord.Member, *, reason):
        channel = self.bot.get_channel(waiting_to_ss)

        embed = discord.Embed(title="Screenshare Request sent successfully", description=f"Your Screenshare Request against  {member.name} has been sent to the Staff",color=colorcode)
        embed.add_field(name="Name:", value=f"{member.name}", inline=False)
        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        embed.add_field(name="Member ID", value=f"{member.id}",inline=False)
        embed.set_footer(text=signature)
        x = await ctx.send(embed=embed)




        embed = discord.Embed(title="Screenshare Request ", description=f"{ctx.author.name} has issued a Screenshare Request against {member.name}",color=colorcode)
        embed.add_field(name="Name:", value=f"{member.name}", inline=False)
        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        embed.add_field(name="Member ID", value=f"{member.id}",inline=False)
        embed.set_footer(text=signature)
        await channel.send(embed=embed)

        await asyncio.sleep(5)
        await x.delete()
        await ctx.message.delete()

        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")


    @commands.command()
    @commands.has_role("Staff")
    async def freeze(self, ctx, member : discord.Member, *, reason):
        embed = discord.Embed(title=None, description=f"Froze {member.name} and pinged them!", color=colorcode)
        await ctx.send(embed=embed)

        channel = self.bot.get_channel(getting_ssed)

        embed = discord.Embed(title="Being Screenshared", description=f"{member.name} is being ss'ed for {reason}",color=colorcode)
        embed.add_field(name="⚠️If you log out you will be banned⚠️", value="** **", inline=False)
        embed.set_footer(text=signature)
        await channel.send(member.mention)
        await channel.send(embed=embed)

        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")


def setup(bot):
    bot.add_cog(Screenshare(bot))
