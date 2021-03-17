import discord
from discord.ext import commands
import json
from var import signature, colorcode, command_usage
import asyncio


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx, ign):
        with open("elo.json", "r") as f:
            users = json.load(f)

        member_id = str(ctx.author.id)

        if member_id in users:
            embed = discord.Embed(title="Already Registered",
                                  description="You are already registered! If you want to "
                                              "change your name please use =rename",
                                  color=colorcode)
            embed.set_footer(text=signature)
            error = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error.delete()
        else:
            await createNewUser(self, users, member_id)
            users[str(ctx.author.id)]['name'] = ign
            with open('elo.json', 'w') as f:
                json.dump(users, f, indent=4)

            role = discord.utils.get(ctx.message.guild.roles, name="Registered")
            member = ctx.author

            channel = self.bot.get_channel(813469418683498557)
            if channel == ctx.channel:
                embed = discord.Embed(title="Registered!", description=f'✅ You registered under the name: {ign}',
                                      color=colorcode)
                embed.set_footer(text=signature)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await member.add_roles(role)
                await ctx.author.edit(nick=f"[0] {ign}")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Wrong Channel!,",
                                      description="Please use this command in the #register channel!")
                embed.set_footer(text=signature)
                error = await ctx.send(embed=embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command()
    async def rename(self, ctx, newnick):
        with open("elo.json", "r") as f:
            users = json.load(f)
        member_id = str(ctx.author.id)

        if member_id in users:
            pass
        else:
            embed = discord.Embed(title="Already registered",
                                  description="You are not registered! Please register in #register")
            await ctx.send(embed=embed)

        users[str(ctx.author.id)]['name'] = newnick

        with open("json/elo.json", "w") as f:
            json.dump(users, f, indent=4)

        embed = discord.Embed(title="Renamed!", description=f'✅ You renamed yourself to: {newnick}', color=colorcode)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=signature)
        await ctx.author.edit(nick=f"[{users[member_id]['elo']}] {newnick}")
        await ctx.send(embed=embed)
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command()
    @commands.has_role("Staff")
    async def forceregister(self, ctx, member: discord.Member, ign):
        with open("elo.json", "r") as f:
            users = json.load(f)
        member_id = str(member.id)

        if member_id in users:
            embed = discord.Embed(title=None, description="This person is already registered!")
            embed.set_footer(text=signature)
            await ctx.send(embed=embed)
        else:
            await createNewUser(self, users, member_id)
            users[str(member.id)]['name'] = ign
            with open('elo.json', 'w') as f:
                json.dump(users, f, indent=4)
        role = discord.utils.get(ctx.message.guild.roles, name="Registered")

        channel = self.bot.get_channel(813469418683498557)
        if channel == ctx.channel:
            embed = discord.Embed(title="Registered!",
                                  description=f'✅ {ctx.author.name} registered {member.name} under the name: {ign}',
                                  color=colorcode)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await member.add_roles(role)
            await member.edit(nick=f"[0] {ign}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Wrong Channel!",
                                  description="Please use this command in the #register channel!")
            embed.set_footer(text=signature)
            error = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command()
    @commands.has_role("Staff")
    async def renameuser(self, ctx, member: discord.Member, ign):
        with open("elo.json", "r") as f:
            elo = json.load(f)

        member_id = str(member.id)

        elo[str(member_id)]['name'] = ign
        with open('json/elo.json', 'w') as f:
            json.dump(elo, f, indent=4)

        embed = discord.Embed(title="Renamed User!",
                              description=f'✅ {ctx.author.name} renamed {member.name} to the name: {ign}',
                              color=colorcode)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=signature)
        await member.edit(nick=f"[{elo[member_id]['elo']}] {ign}")
        await ctx.send(embed=embed)
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")



    @commands.command()
    async def ban(self, ctx, member : discord.Member = None):
        if member is None:
            embed = discord.Embed(title=None, description="No User was mentioned. Please mention a user!", color=colorcode)
        else:
            role = discord.utils.get(ctx.message.guild.roles, name="Banned")
            embed = discord.Embed(title="Banned User!", description=None, color=colorcode)
            embed.set_footer(text=signature)
            await member.add_roles(role)
            await ctx.send(embed=embed)

    @commands.command()
    async def unban(self, ctx, member : discord.Member = None):
        if member is None:
            embed = discord.Embed(title=None, description="No User was mentioned. Please mention a user!", color=colorcode)
        else:
            role = discord.utils.get(ctx.message.guild.roles, name="Banned")
            embed = discord.Embed(title="Unbanned User!", description=None, color=colorcode)
            embed.set_footer(text=signature)
            await member.remove_roles(role)
            await ctx.send(embed=embed)


async def createNewUser(self, users, userID):
    newUser = {
        "name": "",
        "elo": 0,
        "rank": "coal",
        "win": 35,
        "lose": 0,
        "mvp": 10,
        "wins": 0,
        "losses": 0,
        "played": 0,
        "wlr": 0
    }

    users[userID] = newUser


def setup(bot):
    bot.add_cog(User(bot))
