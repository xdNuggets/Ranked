import discord
from discord.ext import commands
import json
from var import signature, colorcode, command_usage
import asyncio


class Scoring(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["em"])
    @commands.has_role("Staff")
    async def elomodify(self, ctx, member : discord.Member, amount = 0):
        with open("json/elo.json", "r") as f:
            elo = json.load(f)

        member_id = str(member.id)

        elo[member_id]['elo'] += amount

        embed=discord.Embed(title=None, description=f"{member.name} now has {elo[member_id]['elo']} elo!", color=colorcode)
        embed.set_footer(text=signature)
        await ctx.send(embed=embed)
        await member.edit(nick=f"[{elo[member_id]['elo']}] {elo[member_id]['name']}")

        with open("json/elo.json", "w") as f:
            json.dump(elo, f, indent=4)
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")


def setup(bot):
    bot.add_cog(Scoring(bot))