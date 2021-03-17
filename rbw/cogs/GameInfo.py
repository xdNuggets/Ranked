import asyncio
import discord
from discord.ext import commands, tasks
import json
from var import signature, colorcode, command_usage


class GameInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["gi", "gamei", "ginfo"])
    async def gameinfo(self, ctx, gamenumber: int = None):
        if gamenumber is not None:
            with open('json/teams.json', "r") as f:
                teams = json.load(f)
            with open('json/elo.json', "r") as f:
                elo = json.load(f)

            num = 0
            gamelist = []
            for games in teams:
                try:
                    gamelist.append(int(teams[games]["number"]))
                    if teams[games]["number"] == gamenumber:
                        num = games
                except:
                    pass
            if gamenumber in gamelist:
                embed = discord.Embed(title=f"Gameinfo of Game #{gamenumber}", description="Infos about the game.", color=colorcode)
                win_team = []
                lose_team = []
                for user in teams[num]["Winners"][2:]:
                    win_team.append(user)
                for user in teams[num]["Losers"][2:]:
                    lose_team.append(user)
                mvp = teams[num]["MVP"]
                if teams[num]["Winners"][0] == "Team 1":
                    win_cap = teams[num]["Captain1"]
                    lose_cap = teams[num]["Captain2"]
                else:
                    win_cap = teams[num]["Captain2"]
                    lose_cap = teams[num]["Captain1"]


                win_cap = elo[str(win_cap)]["name"]
                lose_cap = elo[str(lose_cap)]["name"]
                win_names = ''
                lose_names = ''
                i = 1
                for name in win_team:
                    win_names = f'{win_names}\n Player{i}: {name}'
                    i += 1
                i = 1
                for name in lose_team:
                    lose_names = f'{lose_names}\n Player{i}: {name}'
                    i += 1

                embed.add_field(name="Winner:", value=f'**{teams[num]["Winners"][0]}**\n\nCaptain: {win_cap}{win_names}', inline=True)
                embed.add_field(name="Loser:", value=f'**{teams[num]["Losers"][0]}**\n\nCaptain: {lose_cap}{lose_names}', inline=True)
                embed.add_field(name="MVP:", value=mvp, inline=False)
                embed.set_footer(text=signature)
                await ctx.send(embed=embed)
            else:
                error_embed = discord.Embed(title=f'There is no game #{gamenumber}!',
                                            description=f'Game #{gamenumber} has not been played so far.',
                                            color=colorcode)
                error = await ctx.channel.send(embed=error_embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error.delete()

        else:
            error_missing_embed = discord.Embed(title='Usage of **=gameinfo**',
                                                description='This is how to use the **=gameinfo Command**',
                                                color=colorcode)
            error_missing_embed.add_field(name='Usage:', value="=gameinfo `Gamenumber`",
                                          inline=False)
            error_missing = await ctx.channel.send(embed=error_missing_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missing.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @gameinfo.command()
    async def winner(self, ctx, gamenumber: int = None):
        if gamenumber is not None:
            with open('json/teams.json', "r") as f:
                teams = json.load(f)
            with open('json/elo.json', "r") as f:
                elo = json.load(f)

            num = 0
            gamelist = []
            for games in teams:
                try:
                    gamelist.append(int(teams[games]["number"]))
                    if teams[games]["number"] == gamenumber:
                        num = games
                except:
                    pass
            if gamenumber in gamelist:
                embed = discord.Embed(title=f"Winner of Game #{gamenumber}", description=None,
                                      color=colorcode)
                win_team = []
                for user in teams[num]["Winners"][2:]:
                    win_team.append(user)
                if teams[num]["Winners"][0] == "Team 1":
                    win_cap = teams[num]["Captain1"]
                else:
                    win_cap = teams[num]["Captain2"]

                win_cap = elo[str(win_cap)]["name"]
                win_names = ''
                i = 1
                for name in win_team:
                    win_names = f'{win_names}\n Player{i}: {name}'
                    i += 1

                embed.add_field(name="Winner:",
                                value=f'**{teams[num]["Winners"][0]}**\n\nCaptain: {win_cap}{win_names}', inline=True)
                await ctx.send(embed=embed)
            else:
                error_embed = discord.Embed(title=f'There is no game #{gamenumber}!',
                                            description=f'Game #{gamenumber} has not been played so far.',
                                            color=colorcode)
                error = await ctx.channel.send(embed=error_embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error.delete()
        else:
            error_missing_embed = discord.Embed(title='Usage of **=gameinfo winner**',
                                                description='This is how to use the **=gameinfo winner Command**',
                                                color=colorcode)
            error_missing_embed.add_field(name='Usage:', value="=gameinfo winner `Gamenumber`",
                                          inline=False)
            error_missing = await ctx.channel.send(embed=error_missing_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missing.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @gameinfo.command()
    async def loser(self, ctx, gamenumber: int = None):
        if gamenumber is not None:
            with open('json/teams.json', "r") as f:
                teams = json.load(f)
            with open('json/elo.json', "r") as f:
                elo = json.load(f)

            num = 0
            gamelist = []
            for games in teams:
                try:
                    gamelist.append(int(teams[games]["number"]))
                    if teams[games]["number"] == gamenumber:
                        num = games
                except:
                    pass
            if gamenumber in gamelist:
                embed = discord.Embed(title=f"Winner of Game #{gamenumber}", description=None,
                                      color=colorcode)
                lose_team = []
                for user in teams[num]["Losers"][2:]:
                    lose_team.append(user)
                if teams[num]["Losers"][0] == "Team 1":
                    lose_cap = teams[num]["Captain1"]
                else:
                    lose_cap = teams[num]["Captain2"]

                lose_cap = elo[str(lose_cap)]["name"]
                lose_names = ''
                i = 1
                for name in lose_team:
                    lose_names = f'{lose_names}\n Player{i}: {name}'
                    i += 1

                embed.add_field(name="Winner:",
                                value=f'**{teams[num]["Losers"][0]}**\n\nCaptain: {lose_cap}{lose_names}', inline=True)
                await ctx.send(embed=embed)
            else:
                error_embed = discord.Embed(title=f'There is no game #{gamenumber}!',
                                            description=f'Game #{gamenumber} has not been played so far.',
                                            color=colorcode)
                error = await ctx.channel.send(embed=error_embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error.delete()
        else:
            error_missing_embed = discord.Embed(title='Usage of **=gameinfo loser**',
                                                description='This is how to use the **=gameinfo loser Command**',
                                                color=colorcode)
            error_missing_embed.add_field(name='Usage:', value="=gameinfo loser `Gamenumber`",
                                          inline=False)
            error_missing = await ctx.channel.send(embed=error_missing_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missing.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @gameinfo.command()
    async def mvp(self, ctx, gamenumber: int = None):
        if gamenumber is not None:
            with open('json/teams.json', "r") as f:
                teams = json.load(f)

            num = 0
            gamelist = []
            for games in teams:
                try:
                    gamelist.append(int(teams[games]["number"]))
                    if teams[games]["number"] == gamenumber:
                        num = games
                except:
                    pass
            if gamenumber in gamelist:
                embed = discord.Embed(title=f"Gameinfo of Game #{gamenumber}", description=None, color=colorcode)
                mvp = teams[num]["MVP"]
                embed.add_field(name="MVP:", value=mvp, inline=False)
                await ctx.send(embed=embed)
            else:
                error_embed = discord.Embed(title=f'There is no game #{gamenumber}!',
                                            description=f'Game #{gamenumber} has not been played so far.',
                                            color=colorcode)
                error = await ctx.channel.send(embed=error_embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error.delete()
        else:
            error_missing_embed = discord.Embed(title='Usage of **=gameinfo mvp**',
                                                description='This is how to use the **=gameinfo mvp Command**',
                                                color=colorcode)
            error_missing_embed.add_field(name='Usage:', value="=gameinfo mvp `Gamenumber`",
                                          inline=False)
            error_missing = await ctx.channel.send(embed=error_missing_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missing.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

def setup(bot):
    bot.add_cog(GameInfo(bot))