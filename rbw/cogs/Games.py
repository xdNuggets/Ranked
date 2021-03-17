import discord
from discord.ext import commands
import asyncio
import json
import random
from var import signature, colorcode, scoring_channel, scoring_role, command_usage


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open("json/elo.json", "r") as o:
            elo = json.load(o)
        with open("json/teams.json", "r") as t:
            teams = json.load(t)

        print("hi")

        if before.channel is None and after.channel is not None:
            y = len(member.voice.channel.members)
            if y == after.channel.user_limit:
                teams["num"] += 1
                name = teams["num"]
                print("ok this works")
                await member.guild.create_category(f'Game #{name}')
                category = discord.utils.get(member.guild.categories, name=f'Game #{name}')
                text_channel = await category.create_text_channel(name=name)
                team1_voice = await category.create_voice_channel(name='Team 1')
                team2_voice = await category.create_voice_channel(name='Team 2')
                print("how about now")
                channelID = text_channel.id
                await createUser(self, channelID, teams)
                teams[channelID]["ppt"] = after.channel.user_limit / 2

                teams[channelID]["vc1"] = team1_voice.id
                teams[channelID]["vc2"] = team2_voice.id
                teams[channelID]["category"] = category.id
                teams[channelID]["number"] = name

                response1 = random.choice(after.channel.members)
                response2 = random.choice(after.channel.members)
                while response2 == response1:
                    response2 = random.choice(after.channel.members)

                elocaptain1 = response1.id
                elocaptain2 = response2.id

                teams[channelID]["Captain1"] = elocaptain1
                teams[channelID]["Captain2"] = elocaptain2

                embed = discord.Embed(title=f"Game #{name}", description="Player Infos", color=colorcode)
                embed.add_field(name="Captain 1:",
                                value=f'{elo[str(elocaptain1)]["name"]}\nElo: `{elo[str(elocaptain1)]["elo"]}`',
                                inline=False)
                embed.add_field(name="Captain 2:",
                                value=f'{elo[str(elocaptain2)]["name"]}\nElo: `{elo[str(elocaptain2)]["elo"]}`',
                                inline=False)

                embed.set_footer(text=signature)

                memberlist = ''

                for member in after.channel.members:
                    if member == response1:
                        pass
                    elif member == response2:
                        pass
                    else:
                        member_id = str(member.id)
                        memberlist = f'{memberlist}**{elo[member_id]["name"]}** (Elo: `{elo[member_id]["elo"]}`)\n'
                    await category.set_permissions(member, view_channel=True, send_messages=True, attach_files=True,
                                                   speak=True)
                await category.set_permissions(member.guild.default_role, send_messages=False, view_channel=False)
                teams[channelID]["memberlist"] = memberlist
                embed.add_field(name='Players:', value=memberlist)
                await text_channel.send(' '.join([m.mention for m in after.channel.members]))
                embed.add_field(name="Team 1:", value=f'**{elo[str(elocaptain1)]["name"]}**', inline=False)
                embed.add_field(name="Team 2:", value=f'**{elo[str(elocaptain2)]["name"]}**', inline=False)
                msg = await text_channel.send(embed=embed)
                teams[channelID]["embed"] = msg.id

                with open("json/teams.json", "w") as t:
                    json.dump(teams, t, indent=4)

    @commands.command(aliases=["p"])
    @commands.has_role("Registered")
    async def pick(self, ctx, member: discord.Member = None):
        if member is None:
            error_nomember_embed = discord.Embed(title='Usage of **=pick**',
                                                 description='This is how to use the **=pick Command**',
                                                 color=colorcode)
            error_nomember_embed.add_field(name='Usage:', value="=pick `Player`")
            error_nomember_embed.set_footer(text=signature)
            error_nomember = await ctx.channel.send(embed=error_nomember_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_nomember.delete()
        else:
            with open("json/teams.json", "r") as f:
                teams = json.load(f)
            with open("json/elo.json", "r") as o:
                elo = json.load(o)
            name = teams["num"]
            member_id = member.id
            channel_members = []
            try:
                channel_members = ctx.author.voice.channel.members
            except AttributeError:
                error_embed = discord.Embed(title="You are not in a VoiceChannel",
                                                     description=None,
                                                     color=colorcode)
                error = await ctx.channel.send(embed=error_embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error.delete()

            channelID = ctx.channel.id
            author = ctx.author.id
            msg = await ctx.channel.fetch_message(teams[str(channelID)]["embed"])

            member_name = elo[str(member_id)]["name"]

            ppt = teams[str(channelID)]["ppt"]

            memberlist = teams[str(channelID)]["memberlist"]

            players = memberlist.split("\n")
            list_stars = []
            list_names = []
            removed = 0

            for i in players:
                u = i.split(" ")
                list_stars.append(u[0])

            for i in list_stars:
                w = ''
                for p in i:
                    if p == "*":
                        pass
                    else:
                        w += p
                list_names.append(w)

            for i in list_names:
                if i == member_name:
                    removed = list_names.index(i)
                elif i == '':
                    del list_names[list_names.index(i)]
                else:
                    pass

            del players[removed]

            memberlist = '\n'.join(players)

            teams[str(channelID)]["memberlist"] = memberlist

            picker = teams[str(channelID)]["picker"]

            team1_id = teams[str(channelID)]["Team1"]
            team2_id = teams[str(channelID)]["Team2"]

            Captain1 = teams[str(channelID)]["Captain1"]
            Captain2 = teams[str(channelID)]["Captain2"]

            Captain1_name = await ctx.guild.fetch_member(Captain1)
            Captain2_name = await ctx.guild.fetch_member(Captain2)

            team1_name_ = f'**{elo[str(Captain1)]["name"]}**'
            team2_name_ = f'**{elo[str(Captain2)]["name"]}**'

            if member == Captain1_name or member == Captain2_name:
                error_captain_embed = discord.Embed(title="U cant pick a Captain", description=None, color=colorcode)
                error_captain = await ctx.channel.send(embed=error_captain_embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error_captain.delete()
            else:
                if author == Captain1:
                    if picker == 1:
                        teams[str(channelID)]["picker"] = 2
                        if len(team1_id) + 1 < ppt:
                            for i in channel_members:
                                if i.id == member_id:
                                    teams[str(channelID)]["Team1"].append(member_id)
                                    with open("teams.json", "w") as f:
                                        json.dump(teams, f, indent=4)
                                    with open("teams.json", "r") as f:
                                        teams = json.load(f)
                                    team1_id = teams[str(channelID)]["Team1"]
                                    team2_id = teams[str(channelID)]["Team2"]
                                    team1_name = []
                                    team2_name = []
                                    for i in team1_id:
                                        team1_name.append(elo[str(i)]["name"])
                                    for i in team2_id:
                                        team2_name.append(elo[str(i)]["name"])
                                    for i in team1_name:
                                        team1_name_ = f'{team1_name_}\n{i}'
                                    for i in team2_name:
                                        team2_name_ = f'{team2_name_}\n{i}'
                                    new_embed = discord.Embed(title=f"Game #{name}",
                                                              description="Please pick your teammates",
                                                              color=colorcode)
                                    new_embed.add_field(name="Captain 1:",
                                                        value=f'{elo[str(Captain1)]["name"]}\nElo: `{elo[str(Captain1)]["elo"]}`',
                                                        inline=False)
                                    new_embed.add_field(name="Captain 2:",
                                                        value=f'{elo[str(Captain2)]["name"]}\nElo: `{elo[str(Captain2)]["elo"]}`',
                                                        inline=False)
                                    if memberlist == '':
                                        pass
                                    else:
                                        new_embed.add_field(name='Players:', value=memberlist)
                                    new_embed.add_field(name="Team 1:", value=team1_name_, inline=False)
                                    new_embed.add_field(name="Team 2:", value=team2_name_, inline=False)
                                    new_embed.set_footer(text=signature)
                                    await msg.edit(embed=new_embed)
                                else:
                                    pass
                        elif len(team1_id) + 1 == ppt:
                            error_playerlimit_embed = discord.Embed(title="There are no players left!",
                                                                    description=None,
                                                                    color=colorcode)
                            error_playerlimit = await ctx.channel.send(embed=error_playerlimit_embed)
                            await asyncio.sleep(10)
                            await ctx.message.delete()
                            await error_playerlimit.delete()
                    else:
                        error_captain2_embed = discord.Embed(title="Captain 2 has to pick", description=None,
                                                             color=colorcode)
                        error_captain2 = await ctx.channel.send(embed=error_captain2_embed)
                        await asyncio.sleep(10)
                        await ctx.message.delete()
                        await error_captain2.delete()
                elif author == Captain2:
                    if picker == 2:
                        teams[str(channelID)]["picker"] = 1
                        if len(team2_id) + 1 < ppt:
                            for i in channel_members:
                                if i.id == member_id:
                                    teams[str(channelID)]["Team2"].append(member_id)
                                    with open("teams.json", "w") as f:
                                        json.dump(teams, f, indent=4)
                                    with open("teams.json", "r") as f:
                                        teams = json.load(f)
                                    team1_id = teams[str(channelID)]["Team1"]
                                    team2_id = teams[str(channelID)]["Team2"]
                                    team1_name = []
                                    team2_name = []
                                    for i in team1_id:
                                        team1_name.append(elo[str(i)]["name"])
                                    for i in team2_id:
                                        team2_name.append(elo[str(i)]["name"])
                                    for i in team1_name:
                                        team1_name_ = f'{team1_name_}\n{i}'
                                    for i in team2_name:
                                        team2_name_ = f'{team2_name_}\n{i}'
                                    new_embed = discord.Embed(title=f"Game #{name}",
                                                              description="Please pick your teammates",
                                                              color=colorcode)
                                    new_embed.add_field(name="Captain 1:",
                                                        value=f'{elo[str(Captain1)]["name"]}\nElo: `{elo[str(Captain1)]["elo"]}`',
                                                        inline=False)
                                    new_embed.add_field(name="Captain 2:",
                                                        value=f'{elo[str(Captain2)]["name"]}\nElo: `{elo[str(Captain2)]["elo"]}`',
                                                        inline=False)
                                    if memberlist == '':
                                        vc1 = teams[str(channelID)]["vc1"]
                                        vc2 = teams[str(channelID)]["vc2"]

                                        vchannel1 = self.bot.get_channel(vc1)
                                        vchannel2 = self.bot.get_channel(vc2)

                                        cap1 = await ctx.guild.fetch_member(Captain1)
                                        cap2 = await ctx.guild.fetch_member(Captain2)

                                        await cap1.move_to(vchannel1)
                                        await cap2.move_to(vchannel2)
                                        for user in team1_id:
                                            user = await ctx.guild.fetch_member(user)
                                            await user.move_to(vchannel1)
                                        for user in team2_id:
                                            user = await ctx.guild.fetch_member(user)
                                            await user.move_to(vchannel2)
                                    else:
                                        new_embed.add_field(name='Players:', value=memberlist)
                                    new_embed.add_field(name="Team 1:", value=team1_name_, inline=False)
                                    new_embed.add_field(name="Team 2:", value=team2_name_, inline=False)
                                    new_embed.set_footer(text=signature)
                                    await msg.edit(embed=new_embed)
                                else:
                                    pass
                        elif len(team2_id) + 1 == ppt:
                            error_playerlimit_embed = discord.Embed(title="There are no players left!",
                                                                    description=None,
                                                                    color=colorcode)
                            error_playerlimit = await ctx.channel.send(embed=error_playerlimit_embed)
                            await asyncio.sleep(10)
                            await ctx.message.delete()

                            await error_playerlimit.delete()
                    else:
                        error_captain1_embed = discord.Embed(title="Captain 1 has to pick", description=None,
                                                             color=colorcode)
                        error_captain1 = await ctx.channel.send(embed=error_captain1_embed)
                        await asyncio.sleep(10)
                        await ctx.message.delete()
                        await error_captain1.delete()
                else:
                    error_nocaptain_embed = discord.Embed(title="You are not allowed to pick Players", description=None,
                                                          color=colorcode)
                    error_captain = await ctx.channel.send(embed=error_nocaptain_embed)
                    await asyncio.sleep(10)
                    await error_captain.delete()

                with open("json/teams.json", "w") as f:
                    json.dump(teams, f, indent=4)
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command()
    @commands.has_role("Registered")
    async def submit(self, ctx):
        try:
            attachment = ctx.message.attachments[0]

            with open("json/teams.json", "r") as f:
                teams = json.load(f)
            channelName = ctx.channel.name
            channelID = ctx.channel.id
            category = self.bot.get_channel(teams[str(channelID)]["category"])

            for attachment in ctx.message.attachments:
                score_channel = self.bot.get_channel(818794834210062346)
                embed = discord.Embed(title=None, description=f"Game #{channelName} Submitted by {ctx.author.name}",
                                      color=colorcode)
                embed.set_image(url=attachment.url)
                embed.set_footer(text=signature)
                await score_channel.send(embed=embed)

            for channel in category.voice_channels:
                await channel.delete()
            for channel in category.text_channels:
                await channel.delete()
            await category.delete()
            element = teams[id]
            del element['embed']
            del element['memberlist']
            del element['picker']
            del element['ppt']
            del element['vc1']
            del element['vc2']
            del element['category']
            with open("json/teams.json", "w") as t:
                json.dump(teams, t, indent=4)
        except IndexError:
            error_missingarg_embed = discord.Embed(title='Usage of **=submit**',
                                                   description='This is how to use the **=submit Command**',
                                                   color=colorcode)
            error_missingarg_embed.add_field(name='Usage:', value="=submit `attachment`")
            error_missingarg_embed.set_footer(text=signature)
            error_missingarg = await ctx.channel.send(embed=error_missingarg_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missingarg.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")

    @commands.command(aliases=["game", "sc"])
    @commands.has_role("Staff")
    async def score(self, ctx, gamenumber: int = None, winning_team: int = None, mvp: discord.Member=None):
        role = discord.utils.get(ctx.guild.roles, id=scoring_role)
        if ctx.channel.id == scoring_channel:
            if role in ctx.author.roles:
                if gamenumber is None or winning_team is None or mvp is None:
                        error_missing_embed = discord.Embed(title='Usage of **=score**',
                                                            description='This is how to use the **=score Command**',
                                                            color=colorcode)
                        error_missing_embed.add_field(name='Usage:', value="=score `Gamenumber` `WinnerTeam` `mvp`",
                                                      inline=False)
                        error_missing_embed.add_field(name='Example:', value="=score `1` `2` `not_Nuggets`",
                                                      inline=False)
                        error_missing_embed.set_footer(text=signature)
                        error_missing = await ctx.channel.send(embed=error_missing_embed)
                        await asyncio.sleep(10)
                        await ctx.message.delete()
                        await error_missing.delete()
                else:
                    if winning_team > 2:
                        error_high_embed = discord.Embed(title='Only Team 1 or Team 2 can win**',
                                                        description=None,
                                                        color=colorcode)
                        error_high = await ctx.channel.send(embed=error_high_embed)
                        await asyncio.sleep(10)
                        await ctx.message.delete()
                        await error_high.delete()
                    else:
                        submit_embed = discord.Embed(title=f'Game #{gamenumber} submitted!',
                                                     description=f'Game submitted by {ctx.author}', color=colorcode)

                        with open("json/teams.json", "r") as f:
                            teams = json.load(f)
                        with open("json/elo.json", "r") as t:
                            elo = json.load(t)
                        id = ''
                        for games in teams:
                            try:
                                if teams[games]["number"] == gamenumber:
                                    id = games
                            except TypeError:
                                pass
                            else:
                                pass
                        add_elo_list = []
                        remove_elo_list = []

                        if winning_team == 1:
                            add_elo_list.append(teams[id]["Captain1"])
                            remove_elo_list.append(teams[id]["Captain2"])
                            teams[id]["Winners"].append("Team 1")
                            teams[id]["Winners"].append(elo[str(teams[id]["Captain1"])]["name"])
                            for i in teams[id]["Team1"]:
                                teams[id]["Winners"].append(elo[str(i)]["name"])

                            teams[id]["Losers"].append("Team 2")
                            teams[id]["Losers"].append(elo[str(teams[id]["Captain2"])]["name"])
                            for i in teams[id]["Team2"]:
                                teams[id]["Losers"].append(elo[str(i)]["name"])
                            cap1 = await ctx.guild.fetch_member(teams[id]["Captain1"])
                            winner_namelist = f'{cap1.mention}\n'
                            for user in teams[id]["Team1"]:
                                add_elo_list.append(str(user))
                                user = await ctx.guild.fetch_member(user)
                                winner_namelist = f'{winner_namelist}{user.mention}\n'
                            cap2 = await ctx.guild.fetch_member(teams[id]["Captain2"])
                            loser_namelist = f'{cap2.mention}\n'
                            for user in teams[id]["Team2"]:
                                remove_elo_list.append(str(user))
                                user = await ctx.guild.fetch_member(user)
                                loser_namelist = f'{loser_namelist}{user.mention}\n'
                            submit_embed.add_field(name='Winners:', value=f"**Team 1**\n{winner_namelist}")
                            submit_embed.add_field(name="Losers:", value=f"**Team 2**\n{loser_namelist}")

                        elif winning_team == 2:
                            add_elo_list.append(teams[id]["Captain2"])
                            remove_elo_list.append(teams[id]["Captain1"])
                            teams[id]["Winners"].append("Team 2")
                            teams[id]["Winners"].append(elo[str(teams[id]["Captain2"])]["name"])
                            for i in teams[id]["Team2"]:
                                teams[id]["Winners"].append(elo[str(i)]["name"])
                            teams[id]["Losers"].append("Team 1")
                            teams[id]["Losers"].append(elo[str(teams[id]["Captain1"])]["name"])
                            for i in teams[id]["Team1"]:
                                teams[id]["Losers"].append(elo[str(i)]["name"])
                            cap2 = await ctx.guild.fetch_member(teams[id]["Captain2"])
                            winner_namelist = f'{cap2.mention}\n'
                            for user in teams[id]["Team2"]:
                                add_elo_list.append(str(user))
                                user = await ctx.guild.fetch_member(user)
                                winner_namelist = f'{winner_namelist}{user.mention}\n'
                            cap1 = await ctx.guild.fetch_member(teams[id]["Captain1"])
                            loser_namelist = f'{cap1.mention}\n'
                            for user in teams[id]["Team1"]:
                                remove_elo_list.append(str(user))
                                user = await ctx.guild.fetch_member(user)
                                loser_namelist = f'{loser_namelist}{user.mention}\n'
                            submit_embed.add_field(name='Winners:', value=f"**Team 2**\n{winner_namelist}")
                            submit_embed.add_field(name="Losers:", value=f"**Team 1**\n{loser_namelist}")
                        teams[id]["MVP"] = elo[str(mvp.id)]["name"]
                        submit_embed.add_field(name="MVP:", value=f'{mvp.mention}', inline=False)
                        await ctx.channel.send(embed=submit_embed)

                        # Modify Elo
                        all_list = []
                        for u in add_elo_list:
                            all_list.append(await ctx.guild.fetch_member(u))
                            u = str(u)
                            elo[u]['elo'] += elo[u]['win']
                            teams[id]["add"].append(elo[u]['win'])
                        for u in remove_elo_list:
                            all_list.append(await ctx.guild.fetch_member(u))
                            u = str(u)
                            elo[u]['elo'] += elo[u]['lose']
                            teams[id]["removed"].append(elo[u]['lose'])
                            
                        elo[str(mvp.id)]['elo'] += elo[str(mvp.id)]['mvp']
                        teams[id]["add"].append(elo[str(mvp.id)]['mvp'])

                        for member in all_list:
                            await member.edit(nick=f"[{elo[str(member.id)]['elo']}] {elo[str(member.id)]['name']}")



                        with open("json/elo.json", "w") as x:
                            json.dump(elo, x, indent=4)

                        with open("json/teams.json", "w") as x:
                            json.dump(teams, x, indent=4)
            else:
                error_missing_permissions_embed = discord.Embed(title='You dont have permissions to submit a Game',
                                                                description=None,
                                                                color=colorcode)
                error_missing_permissions = await ctx.channel.send(embed=error_missing_permissions_embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error_missing_permissions.delete()
        else:
            await asyncio.sleep(2)
            await ctx.message.delete()
        

    @commands.command()
    @commands.has_role("Staff")
    async def undogame(self, ctx, gamenumber: int = None):
        role = discord.utils.get(ctx.guild.roles, id=scoring_role)
        if role in ctx.author.roles:
            if ctx.channel.id == scoring_channel:
                if gamenumber is None:
                    error_missing_embed = discord.Embed(title='Usage of **=undogame**',
                                                            description='This is how to use the **=undogame Command**',
                                                            color=colorcode)
                    error_missing_embed.add_field(name='Usage:', value="=undogame `Gamenumber`",
                                                    inline=False)
                    error_missing = await ctx.channel.send(embed=error_missing_embed)
                    await asyncio.sleep(10)
                    await ctx.message.delete()
                    await error_missing.delete()
                else:
                    with open('json/teams.json', "r") as f:
                        teams = json.load(f)
                    with open('json/elo.json', "r") as o:
                        elo = json.load(o)

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
                        try:
                            game = teams[num]
                            cap1 = game["Captain1"]
                            cap2 = game["Captain2"]
                            team1 = game["Team1"]
                            team2 = game["Team2"]

                            add_list = game["add"]
                            rem_list = game["removed"]

                            if game["Winners"][0] == "Team 1":
                                elo[str(cap1)]["elo"] -= add_list[0]
                                elo[str(cap1)]["wins"] -= 1
                                elo[str(cap2)]["elo"] -= rem_list[0]
                                elo[str(cap2)]["losses"] -= 1
                                i = 1
                                for mem in team1:
                                    elo[str(mem)]["elo"] -= add_list[i]
                                    elo[str(mem)]["wins"] -= 1
                                i += 1
                                b = 1
                                for mem in team2:
                                    elo[str(mem)]["elo"] -= rem_list[b]
                                    elo[str(mem)]["losses"] -= 1
                                b += 1
                            else:
                                elo[str(cap2)]["elo"] -= add_list[0]
                                elo[str(cap2)]["wins"] -= 1
                                elo[str(cap1)]["elo"] -= rem_list[0]
                                elo[str(cap1)]["losses"] -= 1
                                i = 1
                                for mem in team1:
                                    elo[str(mem)]["elo"] -= rem_list[i]
                                    elo[str(mem)]["losses"] -= 1
                                i += 1
                                b = 1
                                for mem in team2:
                                    elo[str(mem)]["elo"] -= add_list[b]
                                    elo[str(mem)]["wins"] -= 1
                                b += 1
                            mvp = ""
                            for users in elo:
                                try:
                                    if elo[users]["name"] == game["MVP"]:
                                        mvp = users
                                except TypeError:
                                    pass
                                else:
                                    pass
                            elo[mvp]["elo"] -= elo[mvp]["mvp"]
                            game["add"] = []
                            game["removed"] = []
                            game["Winners"] = []
                            game["Losers"] = []
                            game["MVP"] = ""

                            embed = discord.Embed(title=f"Game #{gamenumber} has been undone!", description=None,
                                                  color=colorcode)
                            x = await ctx.channel.send(embed=embed)
                            await asyncio.sleep(10)
                            await ctx.message.delete()
                            await x.delete()

                            with open("json/teams.json", "w") as t:
                                json.dump(teams, t, indent=4)
                            with open("json/elo.json", "w") as f:
                                json.dump(elo, f, indent=4)


                        except:
                            error_embed = discord.Embed(title=f'There is no game #{gamenumber} submitted!',
                                                        description='You can only undo a game when it is submitted.',
                                                        color=colorcode)
                            error = await ctx.channel.send(embed=error_embed)
                            await asyncio.sleep(10)
                            await ctx.message.delete()
                            await error.delete()

                    else:
                        error_embed = discord.Embed(title=f'There is no game #{gamenumber}!',
                                                    description=f'Game #{gamenumber} has not been played so far.',
                                                    color=colorcode)
                        error = await ctx.channel.send(embed=error_embed)
                        await asyncio.sleep(10)
                        await ctx.message.delete()
                        await error.delete()
                    
            else:
                error_missing_permissions_embed = discord.Embed(title='This command can`t be used in this channel!',
                                                                description=None,
                                                                color=colorcode)
                error_missing_permissions = await ctx.channel.send(embed=error_missing_permissions_embed)
                await asyncio.sleep(10)
                await ctx.message.delete()
                await error_missing_permissions.delete()
        else:
            error_missing_permissions_embed = discord.Embed(title='You dont have permissions to undo a Game',
                                                                description=None,
                                                                color=colorcode)
            error_missing_permissions = await ctx.channel.send(embed=error_missing_permissions_embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await error_missing_permissions.delete()
        channel = self.bot.get_channel(command_usage)
        await channel.send(f"{ctx.author.name} used {ctx.command.name} in {ctx.channel}")



async def createUser(self, channelID, teams):
    newUser = {
        "number": "",
        "Captain1": "",
        "Captain2": "",
        "Team1": [],
        "Team2": [],
        "embed": "",
        "memberlist": "",
        "MVP": "",
        "picker": 1,
        "Winners": [],
        "Losers": [],
        "ppt": "",
        "vc1": "",
        "vc2": "",
        "category": "",
        "add": [],
        "remove": []
    }

    teams[channelID] = newUser



def setup(bot):
    bot.add_cog(Games(bot))
