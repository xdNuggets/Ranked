import discord
from discord.ext import commands, tasks
from help_command import MinimalEmbedPaginatorHelp
import asyncio
import os
import json
from var import token, signature, prefix, colorcode, welcome_channel
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=MinimalEmbedPaginatorHelp(), intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}\nID: {bot.user.id}')
    print('------')
    bot.loop.create_task(status_task())
    has_elo.start() 
    bot.guild = bot.get_guild(675669569603502091)


async def status_task():
    while True:
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="the sounds of sweats", status=discord.Status.online))
        await asyncio.sleep(6)
        await bot.change_presence(
            activity=discord.Streaming(name="Ranked Bedwars", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", status=discord.Status.online))
        await asyncio.sleep(10)
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="unbendables videos", status=discord.Status.dnd))
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Nuggets code me", status=discord.Status.idle))
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Game(name="Ranked Bedwars", status=discord.Status.dnd))
        await asyncio.sleep(5)
        # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="a Ranked Bedwars Game"))
        # await asyncio.sleep(5)





for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(welcome_channel)
    member_count = len([m for m in channel.guild.members if not m.bot])
    embed = discord.Embed(title=f"Welcome to {channel.guild.name}, {member.name}! You are the  Member **#{member_count}**.",
                          description="Please register to play Ranked Bedwars!\nEx: =register not_Nuggets",
                          color=colorcode)
    embed.set_footer(text=signature)
    await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    try:
        if hasattr(ctx.command, 'on_error'):
            return
        else:
            embed = discord.Embed(title=None, description=f"`{ctx.command.qualifed_name} {ctx.command.signature}` \n{error}", colour=colorcode)
            embed.set_author(name=f"Error  in {ctx.command}")
            embed.set_footer(text=signature)
            x = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await x.delete()
    except:
        embed = discord.Embed(title = f"Error in {ctx.command}", description=f"{error}", colour=colorcode)
        embed.set_footer(text=signature)
        x = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await x.delete()



@tasks.loop(seconds=10)
async def has_elo():
    with open("json/elo.json", "r") as f:
        elo = json.load(f)

    for member_id in elo:
        member = await bot.guild.fetch_member(member_id)
        if 200 <= elo[member_id]["elo"] < 400:
            removerole = bot.guild.get_role(749621588676182036)
            await member.remove_roles(removerole)
            role = bot.guild.get_role(749621862996246549)
            await member.add_roles(role)
            elo[member_id]['rank'] = "iron"
            elo[member_id]['lose'] = -15
        elif 400 <= elo[member_id]["elo"] < 600:
            removerole = bot.guild.get_role(749621862996246549)
            await member.remove_roles(removerole)
            role = bot.guild.get_role(749621940452458635)
            await member.add_roles(role)
            elo[member_id]['rank'] = "gold"
            elo[member_id]['win'] = 25
            elo[member_id]['lose'] = -20
        elif 600 <= elo[member_id]["elo"] < 800:
            removerole = bot.guild.get_role(749621940452458635)
            await member.remove_roles(removerole)
            role = bot.guild.get_role(749621855937232967)
            await member.add_roles(role)
            elo[member_id]['rank'] = "diamond"
            elo[member_id]['win'] = 20
            elo[member_id]['lose'] = -20
        elif 800 <= elo[member_id]["elo"] < 1000:
            removerole = bot.guild.get_role(749621855937232967)
            await member.remove_roles(removerole)
            role = bot.guild.get_role(749622230123806798)
            await member.add_roles(role)
            elo[member_id]['rank'] = "emerald"
            elo[member_id]['mvp'] = 5
            elo[member_id]['lose'] = -25
            elo[member_id]['win'] = 20
        elif 1000 <= elo[member_id]["elo"] < 1200:
            removerole = bot.guild.get_role(749622230123806798)
            await member.remove_roles(removerole)
            role = bot.guild.get_role(749622841783222302)
            await member.add_roles(role)
            elo[member_id]['rank'] = "sapphire"
            elo[member_id]['lose'] = -25
            elo[member_id]['win'] = 15
            elo[member_id]['mvp'] = 5
        elif 1200 <= elo[member_id]["elo"] < 1400:
            removerole = bot.guild.get_role(749622841783222302)
            await member.remove_roles(removerole)
            role = bot.guild.get_role(749622960020652173)
            await member.add_roles(role)
            elo[member_id]['rank'] = "ruby"
            elo[member_id]['lose'] = -30
            elo[member_id]['mvp'] = 5
            elo[member_id]['win'] = 10
        elif 1400 <= elo[member_id]["elo"] < 1600:
            removerole = bot.guild.get_role(749622960020652173)
            await member.remove_roles(removerole)
            role = bot.guild.get_role(749623068653256724)
            await member.add_roles(role)
            elo[member_id]['rank'] = "obsidian"
            elo[member_id]['lose'] = -35
            elo[member_id]['mvp'] = 5
            elo[member_id]['win'] = 10
        elif elo[member_id]['elo'] >= 1600:
            removerole = bot.guild.get_role(749623068653256724)
            await member.remove_roles(removerole)
            role = bot.guild.get_role(749624155611201536)
            await member.add_roles(role)
            elo[member_id]['rank'] = "champion"
            elo[member_id]['win'] = 35
            elo[member_id]['mvp'] = 5
            elo[member_id]['lose'] = -45
        if elo[member_id]["wins"] == 0 and elo[member_id]["losses"] == 0:
            elo[member_id]["wlr"] = 0
        elif elo[member_id]["wins"] == 0:
            elo[member_id]["wlr"] = 0
        elif elo[member_id]["losses"] == 0:
            elo[member_id]["wlr"] = 100
        else:
            wlr = round((elo[member_id]["wins"] / (elo[member_id]["wins"] + elo[member_id]["losses"])) * 100, 0)
            if wlr == -0.0:
                wlr = 0.0
            else:
                pass
            elo[member_id]["wlr"] = wlr
    with open("json/elo.json", "w") as f:
        json.dump(elo, f, indent=4)




bot.run(token)
