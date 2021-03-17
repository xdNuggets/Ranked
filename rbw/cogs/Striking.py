import asyncio

import discord
from discord.ext import commands
import json
from var import signature, colorcode, strikes_channel, command_usage


class Striking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Strike a person!")
    async def strike(self, ctx, member: discord.Member=None, *, reason=None):
        if member is not None or reason is not None:
            if member == ctx.author:
                await ctx.send("You cannot strike yourself!")

            else:
                embed = discord.Embed(title="Strike placed!",
                                      description="You have successfully placed a strike against a player!",
                                      color=colorcode)
                embed.add_field(name=f"Name: {member.name}", value="**    **", inline=False)
                embed.add_field(name=f"Reason: {reason}", value="**      **", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

                channel = self.bot.get_channel(strikes_channel)
                embed = discord.Embed(title="Strike placed!",
                                      description=f"{ctx.author.name} has successfully placed a strike against {member.name}!",
                                      color=colorcode)
                embed.add_field(name=f"Name: {member.name}", value="**    **", inline=False)
                embed.add_field(name=f"Reason: {reason}", value="**      **", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await channel.send(embed=embed)
        else:
            error_missingarg_embed = discord.Embed(title='Usage of **=strike**',
                                                 description='This is how to use the **=strike Command**',
                                                 color=colorcode)
            error_missingarg_embed.add_field(name='Usage:', value="=strike `Player` `Reason`")
            error_missingarg = await ctx.channel.send(embed=error_missingarg_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missingarg.delete()


    @commands.command(aliases=["as"])
    @commands.has_role("Staff")
    async def addstrike(self, ctx, member: discord.Member):
        if member is not None:
            with open("json/strikes.json", "r") as f:
                strikes = json.load(f)
            with open("json/elo.json", "r") as o:
                elo = json.load(o)

            roleobject = discord.utils.get(ctx.message.guild.roles, name="Banned")
            embed = discord.Embed(title=f"Strike saved on {member.name}'s account", color=colorcode)
            embed2 = discord.Embed(title=f"Successfully striked {member.name}", color=colorcode)
            embed2.add_field(name="Banned", value="Due to having too many strikes, I automatically banned them")
            embed2.add_field(name="Elo cleared",
                             value="Due to having too many strikes I have automatically cleared their elo")
            embed.set_footer(text=signature)

            member_id = str(member.id)

            if member_id in strikes:
                strikes[member_id]["strikes"] += 1
            else:
                await createUser(self, strikes, member_id)
                strikes[member_id]["strikes"] += 1
            if strikes[member_id]["strikes"] > 4:
                elo[member_id]['elo'] = 0
                await member.add_roles(roleobject)
                await member.edit(nick=f"[{elo[member_id]['elo']}] {elo[member_id]['name']}")
                await ctx.send(embed=embed2)
            else:
                await ctx.send(embed=embed)

            with open("json/strikes.json", "w") as f:
                json.dump(strikes, f, indent=4)

            with open("json/elo.json", "w") as o:
                json.dump(elo, o, indent=4)
        else:
            error_missingarg_embed = discord.Embed(title='Usage of **=addstrike**',
                                                 description='This is how to use the **=addstrike Command**',
                                                 color=colorcode)
            error_missingarg_embed.add_field(name='Usage:', value="=addstrike `Player`")
            error_missingarg = await ctx.channel.send(embed=error_missingarg_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missingarg.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command(aliases=["rs"])
    async def removestrike(self, ctx, member: discord.Member):
        if member is not None:
            with open("json/strikes.json", "r") as f:
                strikes = json.load(f)

            member_id = str(member.id)

            if member_id in strikes:
                strikes[member_id]["strikes"] -= 1

            embed = discord.Embed(title="Removed Strike", description=f"Successfully removed strike from {member.name}",
                                  color=colorcode)
            embed.add_field(name=f"{member.name} now has:", value=f"{strikes[member_id]['strikes']} strikes")
            embed.set_footer(text=signature)

            await ctx.send(embed=embed)

            with open("json/strikes.json", "w") as f:
                json.dump(strikes, f, indent=4)
        else:
            error_missingarg_embed = discord.Embed(title='Usage of **=removestrike**',
                                                 description='This is how to use the **=removestrike Command**',
                                                 color=colorcode)
            error_missingarg_embed.add_field(name='Usage:', value="=removestrike `Player`")
            error_missingarg = await ctx.channel.send(embed=error_missingarg_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missingarg.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")


async def createUser(self, users, userID):
    newUser = {
        "strikes": 0
    }

    users[userID] = newUser


def setup(bot):
    bot.add_cog(Striking(bot))
