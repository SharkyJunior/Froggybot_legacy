import os
import os.path
import pickle
import random
import datetime
import operator
import asyncio
import time

from discord.utils import get
from random import randint as ri
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, CommandOnCooldown, MissingRequiredArgument, MissingRole, MissingPermissions

TOKEN = 'ODM3MzIwODIxMDAwODk2NTYy.YIq1yA.tyHW7JqeFuCk449E-a5n0Gs-j68'
PREFIX = '#'
ROULETTE_MULTIPLIER = 1.2
GUILD_ID = 836887040364511283
DAILY_LIMIT = 2400
DAILY_MULTIPLIER = 0.4
WORK_LIMIT = 100
ENTER_ROLE = "Адекватный чел"
SLOTS_OPTIONS = [":watch:", ":bulb:", ":yo_yo:", ":paperclip:", ":cd:", ":dvd:", ":mag_right:", ":amphora:", ":ringed_planet:", ":gem:", ":rugby_football:", ":nut_and_bolt:", ":lemon:", ":package:", ":crystal_ball:", ":cherries:", ":video_game:", ":tickets:"]

intents = discord.Intents.default()
intents.members = True
activity = discord.Game(name='#help')
bot = commands.Bot(command_prefix=PREFIX, activity=activity, intents=intents)
bot.remove_command('help')

data_filename = 'data.pickle'

@bot.command()
@commands.has_permissions(administrator=True)
async def load(message, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
@commands.has_permissions(administrator=True)
async def unload(message, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
@commands.has_permissions(administrator=True)
async def reload(message, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')


async def change_status():
    await bot.wait_until_ready()
    statuses = ['#help', f'on {len(bot.guilds)} servers', 'slots', 'with coins', 'dice', 'on v0.2', 'the ban hammer']

    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity=discord.Game(name=status))

        await asyncio.sleep(15)



class Data:
    def __init__(self, wallet, bank, isPlayingRoulette, lastRouletteBet, lastRoulettePrize, lastMessage, isPlayingHL, DicesPlayed, RoulettesPlayed, SlotsPlayed, HighLowsPlayed, MoneyWon, MoneyLost, RobAttempts, TimesRobbed, DailyRewardsCollected, WorksCollected, SuccessfulRobberies, TimesSuccessfullyRobbed, MoneyWoninDice, MoneyLostinDice, MoneyWoninSlots, MoneyLostinSlots, MoneyWoninHighLow, MoneyLostinHighLow, MoneyWoninRoulette, MoneyLostinRoulette, TotalRobberyProfit, TotalGamesPlayed, MoneyGotfromDailyRewards, MoneyGotfromWorkPayments):
        self.wallet = wallet
        self.bank = bank
        self.isPlayingRoulette = isPlayingRoulette
        self.lastRouletteBet = lastRouletteBet
        self.lastRoulettePrize = lastRoulettePrize
        self.lastMessage = lastMessage
        self.isPlayingHL = isPlayingHL

        #info
        self.DicesPlayed = DicesPlayed
        self.RoulettesPlayed = RoulettesPlayed
        self.SlotsPlayed = SlotsPlayed
        self.HighLowsPlayed = HighLowsPlayed
        self.RobAttempts = RobAttempts
        self.SuccessfulRobberies = SuccessfulRobberies
        self.TimesRobbed = TimesRobbed
        self.TimesSuccessfullyRobbed = TimesSuccessfullyRobbed
        self.TotalRobberyProfit = TotalRobberyProfit
        self.DailyRewardsCollected = DailyRewardsCollected
        self.WorksCollected = WorksCollected
        self.TotalGamesPlayed = TotalGamesPlayed

        #money info
        self.MoneyWon = MoneyWon
        self.MoneyLost = MoneyLost
        self.MoneyWoninDice = MoneyWoninDice
        self.MoneyLostinDice = MoneyLostinDice
        self.MoneyWoninSlots = MoneyWoninSlots
        self.MoneyLostinSlots = MoneyLostinSlots
        self.MoneyWoninHighLow = MoneyWoninHighLow
        self.MoneyLostinHighLow = MoneyLostinHighLow
        self.MoneyWoninRoulette = MoneyWoninRoulette
        self.MoneyLostinRoulette = MoneyLostinRoulette
        self.MoneyGotfromDailyRewards = MoneyGotfromDailyRewards
        self.MoneyGotfromWorkPayments = MoneyGotfromWorkPayments

@bot.event
async def on_ready():
    print('Zhababot is logged in as {0.user}'.format(bot))

@bot.command()
async def test(ctx):
    print(to_sec('10m'))
    print(to_sec('1h'))
    print(to_sec('1d'))

@bot.command()
async def server_info(ctx):
    await ctx.channel.send(":x: Nothing made here yet! :no_good:")
    server_info = ctx.guild

@bot.command(aliases=['user-info'])
async def user_info(ctx, mode="full", member: discord.Member=None):
    if member is None:
        md = load_member_data(ctx.author.id)
        info_owner = ctx.author.display_name
        user_age = time.time() - ctx.message.author.created_at.timestamp()
    else:
        md = load_member_data(member.id)
        info_owner = member.display_name
        user_age = time.time() - member.created_at.timestamp()

    print(user_age)
    em = discord.Embed(title=f':ledger: {info_owner}', colour=discord.Color.from_rgb(255, 211, 0))
    if mode == "full":
        em.add_field(name='Money stats',       value=f"Money total won = {md.MoneyWon}:coin:\n\
                                                       Money total lost = {md.MoneyLost}:coin:\n\
                                                       Money in wallet = {md.wallet}:coin:\n\
                                                       Money on bank account = {md.bank}:coin:\n\
                                                       Money won in Dice = {md.MoneyWoninDice}:coin:\n\
                                                       Money lost in Dice = {md.MoneyLostinDice}:coin:\n\
                                                       Money won in Roulette = {md.MoneyWoninRoulette}:coin:\n\
                                                       Money lost in Roulette = {md.MoneyLostinRoulette}:coin:\n\
                                                       Money won in Slots = {md.MoneyWoninSlots}:coin:\n\
                                                       Money lost in Slots = {md.MoneyLostinSlots}:coin:\n\
                                                       Money won in HighLow = {md.MoneyWoninHighLow}:coin:\n\
                                                       Money lost in HighLow = {md.MoneyLostinHighLow}:coin:")
        em.add_field(name='Games played',      value=f"Total games played = {md.TotalGamesPlayed}\n\
                                                       Dice = {md.DicesPlayed}\n\
                                                       Roulette = {md.RoulettesPlayed}\n\
                                                       Slots = {md.SlotsPlayed}\n\
                                                       HighLow = {md.HighLowsPlayed}")
        em.add_field(name='Rewards collected', value=f"Daily rewards = {md.DailyRewardsCollected}\n\
                                                       Total money collected from daily rewards = {md.MoneyGotfromDailyRewards}:coin:\n\
                                                       Work payments = {md.WorksCollected}\n\
                                                       Total money collected from work = {md.MoneyGotfromWorkPayments}:coin:")
        em.add_field(name='Robbery',           value=f"Total robbery profit = {md.TotalRobberyProfit}:coin:\n\
                                                       Rob attempts = {md.RobAttempts}\n\
                                                       Successful robberies = {md.SuccessfulRobberies}\n\
                                                       The amount of times you were tried to get robbed = {md.TimesRobbed}\n\
                                                       The amount of times you were succesfully robbed = {md.TimesSuccessfullyRobbed}")
        em.add_field(name='General info',      value=f"The account age = {int(user_age//31536000)}y {int(user_age//86400)}d {int(user_age//3600)}h {int(user_age//60)}m")
    elif mode == "money" or mode == "m":
        em.add_field(name='Money',             value=f"Money total won = {md.MoneyWon}:coin:\n\
                                                       Money total lost = {md.MoneyLost}:coin:\n\
                                                       Money in wallet = {md.wallet}:coin:\n\
                                                       Money on bank account = {md.bank}:coin:\n\
                                                       Money won in Dice = {md.MoneyWoninDice}:coin:\n\
                                                       Money lost in Dice = {md.MoneyLostinDice}:coin:\n\
                                                       Money won in Roulette = {md.MoneyWoninRoulette}:coin:\n\
                                                       Money lost in Roulette = {md.MoneyLostinRoulette}:coin:\n\
                                                       Money won in Slots = {md.MoneyWoninSlots}:coin:\n\
                                                       Money lost in Slots = {md.MoneyLostinSlots}:coin:\n\
                                                       Money won in HighLow = {md.MoneyWoninHighLow}:coin:\n\
                                                       Money lost in HighLow = {md.MoneyLostinHighLow}:coin:")
    elif mode == "games" or mode == "g":
        em.add_field(name='Games played',      value=f"Total games played = {md.TotalGamesPlayed}\n\
                                                       Dice = {md.DicesPlayed}\n\
                                                       Roulette = {md.RoulettesPlayed}\n\
                                                       Slots = {md.SlotsPlayed}\n\
                                                       HighLow = {md.HighLowsPlayed}")
    elif mode == "rewards" or mode == "rd":
        em.add_field(name='Rewards collected', value=f"Daily rewards = {md.DailyRewardsCollected}\n\
                                                       Total money collected from daily rewards = {md.MoneyGotfromDailyRewards}:coin:\n\
                                                       Work payments = {md.WorksCollected}\n\
                                                       Total money collected from work = {md.MoneyGotfromWorkPayments}:coin:")
    elif mode == "robbery" or mode == "r":
        em.add_field(name='Robbery',           value=f"Total robbery profit = {md.TotalRobberyProfit}:coin:\n\
                                                       Rob attempts = {md.RobAttempts}\n\
                                                       Successful robberies = {md.SuccessfulRobberies}\n\
                                                       The amount of times you were tried to get robbed = {md.TimesRobbed}\n\
                                                       The amount of times you were succesfully robbed = {md.TimesSuccessfullyRobbed}")
    else:
        await ctx.channel.send(":x: No such a mode check `#help user_info` for the syntax")
        return

    await ctx.channel.send(embed=em)





@bot.command(aliases=['gstart','gs','giveaway-start'])
@commands.has_permissions(manage_messages=True)
async def giveaway_start(message, time, winners, channel : discord.TextChannel = None, *, prize = ''):
    time = to_sec(time)
    if time != "Error" and channel != None and prize != '':
        endtime = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
        embed = discord.Embed(title=":tada: Giveaway!", description=f'**{prize}**\nReact with :tada: to enter!', color=message.author.color, timestamp=endtime)
        embed.add_field(name="Host", value=message.author.mention)
        embed.add_field(name="Time remaining", value=f'{time//86400}d {time%86400//3600}h {time%86400%3600//60}m {time%60}s')
        embed.set_footer(text=f"Ends at ")

        msg = await channel.send(embed=embed)
        await msg.add_reaction("🎉")
        print(time)
        while time > 0:
            await asyncio.sleep(10)
            time -= 10
            em = discord.Embed(title=":tada: Giveaway!", description=f'**{prize}**\nReact with :tada: to enter!',
                                  color=message.author.color, timestamp=endtime)
            em.add_field(name="Host", value=message.author.mention)
            em.add_field(name="Time remaining",
                            value=f'{time // 86400}d {time % 86400 // 3600}h {time % 86400 % 3600 // 60}m {time % 60}s')
            em.set_footer(text=f"Ends at ")
            await msg.edit(embed=em)

        endmsg = await channel.fetch_message(msg.id)

        users = await endmsg.reactions[0].users().flatten()
        users.pop(users.index(bot.user))
        print(users)
        winusers = []
        for i in range(int(winners)):
            win = random.choice(users)
            users.pop(users.index(win))
            winusers.append(win)
        winusers_mention = []
        for user in winusers:
            winusers_mention.append(user.mention)

        winusers_str = ', '.join(winusers_mention)
        em = discord.Embed(title=":tada: Giveaway has ended!", description=f'**{prize}**',
                           color=message.author.color, timestamp=endtime)
        em.add_field(name="Host", value=message.author.mention)
        em.add_field(name="Winners",
                     value=winusers_str)
        em.set_footer(text=f"Ended at ")
        await msg.edit(embed=em)

        for user in winusers:
            print(user)
            dm = await user.create_dm()
            em = discord.Embed(title=":tada: You have won the giveaway!", description=f'**{prize}**',
                               color=message.author.color, timestamp=endtime)
            em.add_field(name="Giveaway",
                         value=msg.jump_url)
            em.set_footer(text=f"Ended at ")
            await dm.send(embed=em)
    else:
        if time == "Error":
            await message.channel.send(
            "**:x: I can not understand this amount of time, check `#help giveaway_start` for syntax.**")
        elif prize == '':
            await message.channel.send(
                "**:x: Please enter something to giveaway.**")
        else:
            await message.channel.send(
                "**:x: I can not understand this, check `#help gstart` for syntax.**")

@bot.command(aliases=['gsetup', 'giveaway-setup'])
@commands.has_permissions(manage_messages=True)
async def giveaway_setup(message):
    def check(m):
        return m.author == message.author and m.channel == message.channel

    await message.channel.send(":tada: Ok, now let's setup your giveaway!")
    await asyncio.sleep(0.5)
    await message.channel.send(":tada: First, what **channel** should the giveaway be hosted in?\n\n`Please mention a channel in this server`")

    msg = await bot.wait_for('message', check=check)

    while True:
        try:
            channel_id = int(msg.content[2:-1])
            break
        except:
            await message.channel.send(f":x: Sorry, I could not understand this channel, please type it like this: {message.channel.mention}")
            msg = await bot.wait_for('message', check=check)
    print(channel_id)
    channel = bot.get_channel(channel_id)
    await message.channel.send(f":tada: Sweet! The giveaway will be hosted in {channel.mention}.")
    await asyncio.sleep(0.5)
    await message.channel.send(":tada: **How long** will the giveaway stay?\n\n`Please type the amount of time (s|m|h|d)`")

    msg = await bot.wait_for('message', check=check)

    time = to_sec(msg.content)

    while time == "Error":
        await message.channel.send(
            f":x: Sorry, I could not understand this amount of time, please type it like this: `10m`, `3h`, `2d`")
        msg = await bot.wait_for('message', check=check)
        print(msg.content)
        time = to_sec(msg.content)

    if msg.content[-1] == 's':
        await message.channel.send(f":tada: Nice! The giveaway will last for **{msg.content[:-1]} seconds**.")
    elif msg.content[-1] == 'm':
        await message.channel.send(f":tada: Nice! The giveaway will last for **{msg.content[:-1]} minutes**.")
    elif msg.content[-1] == 'h':
        await message.channel.send(f":tada: Nice! The giveaway will last for **{msg.content[:-1]} hours**.")
    elif msg.content[-1] == 'd':
        await message.channel.send(f":tada: Nice! The giveaway will last for **{msg.content[:-1]} days**.")

    await asyncio.sleep(0.5)
    await message.channel.send(
        ":tada: **How many** winners will be in your giveaway?\n\n`Please type the amount of winners`")

    msg = await bot.wait_for('message', check=check)

    while True:
        try:
            winners = int(msg.content)
            if winners > 0:
                break
            else:
                await message.channel.send(":x: Please write a **valid** number")
        except:
            await message.channel.send(
                f":x: Sorry, I could not understand this amount of winners, please type an **integer**")
            msg = await bot.wait_for('message', check=check)

    if winners == 1:
        await message.channel.send(f':tada: Neat! There will be only **{winners} winner**')
    else:
        await message.channel.send(f':tada: Neat! There will be **{winners} winners**')

    await asyncio.sleep(0.5)
    await message.channel.send(
        ":tada: And last question, what are you giveawaying?\n\n`Please type the prize`")

    msg = await bot.wait_for('message', check=check)

    prize = msg.content

    await asyncio.sleep(0.5)
    await message.channel.send(
        f":tada: Started giveaway of `{prize}` in {channel.mention}!")

    endtime = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
    embed = discord.Embed(title=":tada: Giveaway!", description=f'**{prize}**\nReact with :tada: to enter!',
                          color=message.author.color, timestamp=endtime)
    embed.add_field(name="Host", value=message.author.mention)
    embed.add_field(name="Time remaining",
                    value=f'{time // 86400}d {time % 86400 // 3600}h {time % 86400 % 3600 // 60}m {time % 60}s')
    embed.set_footer(text=f"Ends at ")

    msg = await channel.send(embed=embed)
    await msg.add_reaction("🎉")
    print(time)
    while time > 0:
        await asyncio.sleep(5)
        time -= 5
        print(time)
        print('edited')
        em = discord.Embed(title=":tada: Giveaway!", description=f'**{prize}**\nReact with :tada: to enter!',
                           color=message.author.color, timestamp=endtime)
        em.add_field(name="Host", value=message.author.mention)
        em.add_field(name="Time remaining",
                     value=f'{time // 86400}d {time % 86400 // 3600}h {time % 86400 % 3600 // 60}m {time % 60}s')
        em.set_footer(text=f"Ends at ")
        await msg.edit(embed=em)

    endmsg = await channel.fetch_message(msg.id)

    users = await endmsg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    print(users)
    winusers = []
    for i in range(int(winners)):
        win = random.choice(users)
        users.pop(users.index(win))
        winusers.append(win)
    winusers_mention = []
    for user in winusers:
        winusers_mention.append(user.mention)

    winusers_str = ', '.join(winusers_mention)
    em = discord.Embed(title=":tada: Giveaway has ended!", description=f'**{prize}**',
                       color=message.author.color, timestamp=endtime)
    em.add_field(name="Host", value=message.author.mention)
    em.add_field(name="Winners",
                 value=winusers_str)
    em.set_footer(text=f"Ended at ")
    await msg.edit(embed=em)

    for user in winusers:
        print(user)
        dm = await user.create_dm()
        em = discord.Embed(title=":tada: You have won the giveaway!", description=f'**{prize}**',
                           color=message.author.color, timestamp=endtime)
        em.add_field(name="Giveaway",
                     value=msg.jump_url)
        em.set_footer(text=f"Ended at ")
        await dm.send(embed=em)

@bot.command(aliases=['lb'])
async def leaderboard(message, category):
    if category == "bank":
        members = message.guild.members
        banks = []
        allmoney = 0
        for member in members:
            if not member.bot:
                member_data = load_member_data(member.id)
                banks.append([member, member_data.bank])
                allmoney += member_data.bank
        banks = sorted(banks, key=operator.itemgetter(1), reverse=True)
        em = discord.Embed(title=f"{message.guild.name}'s bank leaderboard", colour=message.author.color)
        if banks[0][1] > 0:
            em.add_field(name=":bank: **Server total**", value=allmoney, inline=False)
            em.add_field(name=f":first_place: {banks[0][0].display_name}", value=banks[0][1], inline=False)
        else:
            em.set_footer(text="Nobody here has never earned a penny.")

        if banks[1][1] > 0:
            em.add_field(name=f":second_place: {banks[1][0].display_name}", value=banks[1][1], inline=False)
        else:
            em.set_footer(text="This is all people here who have earned more than nothing")

        if banks[2][1] > 0:
            em.add_field(name=f":third_place: {banks[2][0].display_name}", value=banks[2][1], inline=False)
        else:
            em.set_footer(text="This is all people here who have earned more than nothing")


        for i in range(3, 5):
            if banks[i][1] > 0:
                em.add_field(name=f"{banks[i][0].display_name}", value=banks[i][1], inline=False)
            else:
                em.set_footer(text="This is all people here who have earned more than nothing")
                break

        await message.channel.send(embed=em)
    elif category == "wallet":
        members = message.guild.members
        banks = []
        allmoney = 0
        for member in members:
            if not member.bot:
                member_data = load_member_data(member.id)
                banks.append([member, member_data.wallet])
                allmoney += member_data.wallet
        banks = sorted(banks, key=operator.itemgetter(1), reverse=True)
        em = discord.Embed(title=f"{message.guild.name}'s wallet leaderboard", colour=message.author.color)
        if banks[0][1] > 0:
            em.add_field(name=":bank: **Server total**", value=allmoney, inline=False)
            em.add_field(name=f":first_place: {banks[0][0].display_name}", value=banks[0][1], inline=False)
        else:
            em.set_footer(text="Nobody here has never withdrawn a penny.")

        if banks[1][1] > 0:
            em.add_field(name=f":second_place: {banks[1][0].display_name}", value=banks[1][1], inline=False)
        else:
            em.set_footer(text="This is all people here who have withdrawn more than nothing")

        if banks[2][1] > 0:
            em.add_field(name=f":third_place: {banks[2][0].display_name}", value=banks[2][1], inline=False)
        else:
            em.set_footer(text="This is all people here who have withdrawn more than nothing")

        for i in range(3, 5):
            if banks[i][1] > 0:
                em.add_field(name=f"{banks[i][0].display_name}", value=banks[i][1], inline=False)
            else:
                em.set_footer(text="This is all people here who have withdrawn more than nothing")
                break

        await message.channel.send(embed=em)
    else:
        await message.channel.send(":x: **I don't know this category, type `#help leaderboard` for categories.**")



@bot.command(aliases=['am', 'addm'])
@commands.has_permissions(administrator=True)
async def addmoney(message, amt, member: discord.Member = None):
    if int(amt) > 0 and float(amt) % 1 == 0:
        if member == None:
            member_data = load_member_data(message.author.id)
            bal = member_data.bank
            add_money(message.author, amt)
            bal1 = bal + int(amt)
            em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Recipient", value=message.author.mention)
            em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
            await message.channel.send(embed=em)
        else:
            member_data = load_member_data(member.id)
            bal = member_data.bank
            add_money(member, amt)
            bal1 = bal + int(amt)
            em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Recipient", value=member.mention)
            em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
            await message.channel.send(embed=em)
    else:
        await message.channel.send(":x: **Please enter valid number.**".format(message.author.mention))

@bot.command(aliases=['rm',])
@commands.has_permissions(administrator=True)
async def removemoney(message, amt, member: discord.Member = None):
    if int(amt) > 0 and float(amt) % 1 == 0:
        if member == None:
            member_data = load_member_data(message.author.id)
            bal = member_data.bank
            remove_money(message.author, amt)
            bal1 = bal - int(amt)
            embed = discord.Embed(title=':white_check_mark: Operation complete!', colour=discord.Color.from_rgb(60,179,113))
            embed.add_field(name="Recipient", value=message.author.mention)
            embed.add_field(name="Bank", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
            await message.channel.send(embed=embed)
        else:
            member_data = load_member_data(member.id)
            bal = member_data.bank
            remove_money(member, amt)
            bal1 = bal - int(amt)
            em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Recipient", value=member.mention)
            em.add_field(name="Bank", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
            await message.channel.send(embed=em)
    else:
        await message.channel.send(":x: **Please enter valid number.**".format(message.author.mention))

@bot.command(aliases=['sm','setm'])
@commands.has_permissions(administrator=True)
async def setmoney(message, amt, member: discord.Member = None):
    if int(amt) >= 0 and float(amt) % 1 == 0:
        if member == None:
            member_data = load_member_data(message.author.id)
            bal = member_data.bank
            set_money(message.author, amt)
            bal1 = int(amt)
            em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Recipient", value=message.author.mention)
            em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
            await message.channel.send(embed=em)
        else:
            member_data = load_member_data(member.id)
            bal = member_data.bank
            set_money(member, amt)
            bal1 = int(amt)
            em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Recipient", value=member.mention)
            em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
            await message.channel.send(embed=em)
    else:
        await message.channel.send(":x: **Please enter valid number.**".format(message.author.mention))

@bot.command(aliases=['wd'])
async def withdraw(message, amt):
    member_data = load_member_data(message.author.id)
    if amt != "all":
        if member_data.bank >= int(amt) > 0:
            member_data = load_member_data(message.author.id)
            bbal = member_data.bank
            wbal = member_data.wallet
            withdraw_money(message.author, amt)
            bbal1 = bbal - int(amt)
            wbal1 = wbal + int(amt)

            embed = discord.Embed(title=':white_check_mark: Operation complete!', colour=discord.Color.from_rgb(60,179,113))
            embed.add_field(name="Requester", value=message.author.mention, inline=False)
            embed.add_field(name="Bank", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(bbal, bbal1))
            embed.add_field(name="Wallet", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(wbal, wbal1))

            await message.channel.send(embed=embed)
        else:
            if int(amt) <= 0:
                await message.channel.send(":x: **Please enter valid number.**")
            else:
                await message.channel.send(":x: **You do not have this amount of coins on your bank account**")
    elif amt == "all":
        if member_data.bank > 0:
            member_data = load_member_data(message.author.id)
            bbal = member_data.bank
            wbal = member_data.wallet
            withdraw_money(message.author, bbal)
            bbal1 = 0
            wbal1 = bbal

            embed = discord.Embed(title=':white_check_mark: Operation complete!',
                                  colour=discord.Color.from_rgb(60,179,113))
            embed.add_field(name="Requester", value=message.author.mention, inline=False)
            embed.add_field(name="Bank", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(bbal, bbal1))
            embed.add_field(name="Wallet", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(wbal, wbal1))

            await message.channel.send(embed=embed)
        else:
            await message.channel.send(":x: **You do not have any money on your bank account** ")

@bot.command(aliases=['dep'])
async def deposit(message, amt):
    member_data = load_member_data(message.author.id)
    if amt != "all":
        if member_data.wallet >= int(amt) > 0:
            member_data = load_member_data(message.author.id)
            bbal = member_data.bank
            wbal = member_data.wallet
            deposit_money(message.author, int(amt))
            fee = int(0.1 * int(amt))
            bbal1 = bbal + int(0.9 * int(amt))
            wbal1 = wbal - int(amt)

            embed = discord.Embed(title=':white_check_mark: Operation complete!', colour=discord.Color.from_rgb(60,179,113))
            embed.add_field(name="Requester", value=message.author.mention, inline=False)
            embed.add_field(name="Wallet", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(wbal, wbal1))
            embed.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bbal, bbal1), inline=False)
            embed.add_field(name="Fee", value=f"{fee}:coin:")

            await message.channel.send(embed=embed)
        else:
            if int(amt) <= 0:
                await message.channel.send(":x: **Please enter valid number.**")
            else:
                await message.channel.send(":x: **You do not have this amount of coins in your wallet!**")
    elif amt == "all":
        if member_data.wallet > 0:
            bbal = member_data.bank
            wbal = member_data.wallet
            deposit_money(message.author, wbal)
            fee = int(0.1 * wbal)
            bbal1 = bbal + int(0.9 * wbal)
            wbal1 = 0
            embed = discord.Embed(title=':white_check_mark: Operation complete!', colour=discord.Color.from_rgb(60,179,113))
            embed.add_field(name="Requester", value=message.author.mention, inline=False)
            embed.add_field(name="Wallet", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(wbal, wbal1))
            embed.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bbal, bbal1), inline=False)
            embed.add_field(name="Fee", value=f"**{fee}**:coin:")

            await message.channel.send(embed=embed)
        else:
            await message.channel.send("You don't have any money in wallet")

@bot.command(aliases=['bal'])
async def balance(message, member: discord.Member = None):
    if member == None:
        member_data = load_member_data(message.author.id)

        embed = discord.Embed(title=f"{message.author.display_name}'s Balance", colour=message.author.color)
        embed.add_field(name="Wallet balance", value="{}:coin:".format(str(member_data.wallet)), inline=False)
        embed.add_field(name="Bank balance", value="{}:coin:".format(str(member_data.bank)))

        await message.channel.send(embed=embed)
    else:
        member_data = load_member_data(member.id)

        embed = discord.Embed(title=f"{member.display_name}'s balance", colour=member.color)
        embed.add_field(name="Wallet balance", value="{}:coin:".format(str(member_data.wallet)), inline=False)
        embed.add_field(name="Bank balance", value="{}:coin:".format(str(member_data.bank)))

        await message.channel.send(embed=embed)

@bot.command()
@cooldown(1, 60 * 60 * 24, commands.BucketType.user)
async def daily(ctx):
    member_data = load_member_data(ctx.message.author.id)
    member_data.DailyRewardsCollected += 1
    bal = member_data.bank
    member_data.lastMessage = ctx.message.content
    bank_money = member_data.bank
    if int(bal * DAILY_MULTIPLIER) > DAILY_LIMIT:
        bank_money = add_money(ctx.message.author, int(member_data.bank * DAILY_MULTIPLIER))
        member_data.MoneyGotfromDailyRewards += int(member_data.bank * DAILY_MULTIPLIER)
        bal1 = bal + int(member_data.bank * DAILY_MULTIPLIER)

        em = discord.Embed(title=f":white_check_mark: {ctx.message.author.display_name}'s daily reward",
                       colour=discord.Color.from_rgb(60,179,113))
        em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
        await ctx.message.channel.send(embed=em)
    else:
        bank_money = add_money(ctx.message.author, DAILY_LIMIT)
        member_data.MoneyGotfromDailyRewards += DAILY_LIMIT
        bal1 = bal + DAILY_LIMIT

        em = discord.Embed(title=f":white_check_mark: {ctx.message.author.display_name}'s daily reward",
                           colour=discord.Color.from_rgb(60,179,113))
        em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
        await ctx.message.channel.send(embed=em)
    member_data.bank = bank_money
    save_member_data(ctx.message.author.id, member_data)

@bot.command()
@cooldown(1, 60 * 60, commands.BucketType.user)
async def work(ctx):
    member_data = load_member_data(ctx.message.author.id)
    member_data.WorksCollected += 1
    member_data.lastMessage = ctx.message.content
    bank_money = member_data.bank
    bal = member_data.bank
    work_multiplier = random.uniform(0.05, 0.1)
    if int(bal * work_multiplier) > WORK_LIMIT:
        bank_money = add_money(ctx.message.author, int(member_data.bank * work_multiplier))
        member_data.MoneyGotfromWorkPayments += int(member_data.bank * work_multiplier)
        bal1 = bal + int(member_data.bank * work_multiplier)
        em = discord.Embed(title=f":white_check_mark: {ctx.message.author.display_name}'s work payment, come back in 1 hour to collect next one",
                       colour=discord.Color.from_rgb(60,179,113))
        em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
        await ctx.message.channel.send(embed=em)
    else:
        bank_money = add_money(ctx.message.author, WORK_LIMIT)
        member_data.MoneyGotfromWorkPayments += WORK_LIMIT
        bal1 = bal + WORK_LIMIT

        em = discord.Embed(title=f":white_check_mark: {ctx.message.author.display_name}'s work payment, come back in 1 hour to collect next one",
                           colour=discord.Color.from_rgb(60,179,113))
        em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
        await ctx.message.channel.send(embed=em)
    member_data.bank = bank_money
    save_member_data(ctx.message.author.id, member_data)


@bot.command()
async def dice(message, amt=0):
    member_data = load_member_data(message.author.id)
    wallet_money = member_data.wallet
    amt = int(amt)
    if wallet_money >= amt > 0:
        member_data.DicesPlayed += 1
        member_data.TotalGamesPlayed += 1
        author_values = [ri(1, 6), ri(1, 6)]
        opponent_values = [ri(1, 6), ri(1, 6)]
        author_sum = sum(author_values)
        opponent_sum = sum(opponent_values)
        em = None
        if author_sum > opponent_sum and author_values[0] != author_values[1]:
            em = discord.Embed(title="**Dice** :game_die:", description=":inbox_tray: Wallet: {}:coin: --> {}:coin:".format(wallet_money, wallet_money + amt), colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Your score",
                         value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
            em.add_field(name="Opponent score",
                         value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
            member_data.MoneyWon += amt
            member_data.MoneyWoninDice += amt
            wallet_money = add_wmoney(message.author, amt)
        elif author_sum > opponent_sum and author_values[0] == author_values[1]:
            em = discord.Embed(title="**Dice** :game_die:", description=":inbox_tray: Wallet: {}:coin: --> {}:coin: **(Double!)** ".format(wallet_money, wallet_money + 2 * amt), colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Your score",
                         value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
            em.add_field(name="Opponent score",
                         value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
            member_data.MoneyWon += 2*amt
            member_data.MoneyWoninDice += 2*amt
            wallet_money = add_wmoney(message.author, 2 * amt)
        elif author_sum == opponent_sum:
            em = discord.Embed(title="**Dice** :game_die:", description="It's a draw get your money back", colour=discord.Color.from_rgb(255, 140, 0))
            em.add_field(name="Your score",
                         value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
            em.add_field(name="Opponent score",
                         value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
        elif author_sum < opponent_sum:
            em = discord.Embed(title="**Dice** :game_die:", description=":outbox_tray: Wallet: {}:coin: --> {}:coin:".format(wallet_money, wallet_money - amt), colour=discord.Color.from_rgb(220,20,60))
            em.add_field(name="Your score",
                         value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
            em.add_field(name="Opponent score",
                         value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
            member_data.MoneyLost += amt
            member_data.MoneyLostinDice += amt
            wallet_money = remove_wmoney(message.author, amt)
        else:
            print("smth strange happened")
            print("{} and {} vs {} and {}".format(author_values[0], author_values[1], opponent_values[0], opponent_values[1]))

        member_data.wallet = wallet_money
        save_member_data(message.author.id, member_data)

        await message.channel.send(embed=em)

    else:
        if amt <= 0:
            await message.channel.send("Enter a **valid** number")
        else:
            await message.channel.send(":x: **You don't have enough money in your wallet**")

@bot.command(aliases=['rt'])
async def roulette(message, amt=0):
    member_data = load_member_data(message.author.id)
    wallet_money = member_data.wallet
    if int(amt) > 0:
        amt = int(amt)
        if not member_data.isPlayingRoulette and wallet_money >= amt:
            member_data.isPlayingRoulette = True
            won = random.choice([True, False])
            if won:
                em = discord.Embed(title=":gun: Roulette", description=":hot_face: **You survived!**", colour=discord.Color.from_rgb(60,179,113))
                em.add_field(name=":moneybag: Prize", value=f"{amt}:coin:")
                em.add_field(name="Next prize", value=f"{amt + int(amt * ROULETTE_MULTIPLIER)}:coin:", inline=False)
                em.add_field(name="Actions", value="`#cont-rt` to continue\n`#stop-rt` to stop")

                member_data.isPlayingRoulette = True
                member_data.lastRouletteBet = amt
                member_data.lastRoulettePrize = amt

                save_member_data(message.author.id, member_data)
                await message.channel.send(embed=em)
            else:
                member_data.TotalGamesPlayed += 1
                member_data.RoulettesPlayed += 1
                member_data.MoneyLost += int(amt)
                member_data.MoneyLostinRoulette += int(amt)

                em = discord.Embed(title=":gun: Roulette", description=":skull_crossbones: **You lost!**", colour=discord.Color.from_rgb(220,20,60))
                em.add_field(name="Wallet", value=":outbox_tray: Wallet: {}:coin: --> {}:coin:".format(wallet_money, wallet_money-int(amt)))

                member_data.isPlayingRoulette = False
                member_data.wallet -= int(amt)

                save_member_data(message.author.id, member_data)
                await message.channel.send(embed=em)
        elif wallet_money < amt:
            await message.channel.send(":x: **You don't have enough money in your wallet!**")
        else:
            await message.channel.send(":x: **You're already playing!**")
    else:
        await message.channel.send(":x:**Enter a valid number!**")


@bot.command(aliases=['cont-rt'])
async def cont_rt(message):
    member_data = load_member_data(message.author.id)
    if member_data.isPlayingRoulette:
        won = random.choice([True, False])
        wallet_money = member_data.wallet
        if won:
            prize = member_data.lastRoulettePrize + int(member_data.lastRoulettePrize * ROULETTE_MULTIPLIER)

            em = discord.Embed(title=":gun: Roulette", description=":hot_face: **You survived!**",
                               colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name=":moneybag: Prize", value=f"{prize}:coin:")
            em.add_field(name="Next prize", value=f"{prize + int(prize * ROULETTE_MULTIPLIER)}:coin:", inline=False)
            em.add_field(name="Actions", value="`#cont-rt` to continue\n`#stop-rt` to stop")

            member_data.lastRoulettePrize = prize
            await message.channel.send(embed=em)
            save_member_data(message.author.id, member_data)
        else:
            member_data.TotalGamesPlayed += 1
            member_data.RoulettesPlayed += 1
            member_data.MoneyLost += member_data.lastRouletteBet
            member_data.MoneyLostinRoulette += member_data.lastRouletteBet

            em = discord.Embed(title=":gun: Roulette", description=":skull_crossbones: **You lost!**",
                               colour=discord.Color.from_rgb(220,20,60))
            em.add_field(name="Wallet", value=":outbox_tray: Wallet: {}:coin: --> {}:coin:".format(wallet_money, wallet_money - member_data.lastRouletteBet))

            member_data.isPlayingRoulette = False
            member_data.wallet -= member_data.lastRouletteBet
            await message.channel.send(embed=em)
            save_member_data(message.author.id, member_data)
    else:
        await message.channel.send(":x: **You're not playing roulette!** ")
    save_member_data(message.author.id, member_data)

@bot.command(aliases=['stop-rt'])
async def stop_rt(message):
    member_data = load_member_data(message.author.id)
    if member_data.isPlayingRoulette:
        member_data.TotalGamesPlayed += 1
        member_data.RoulettesPlayed += 1
        member_data.MoneyWon += member_data.lastRoulettePrize
        member_data.MoneyWoninRoulette += member_data.lastRoulettePrize

        wallet_money = member_data.wallet

        em = discord.Embed(title=":gun: Roulette", description=":no_good: You exited!", colour=discord.Color.from_rgb(60,179,113))
        em.add_field(name="Wallet", value=":inbox_tray: {}:coin: --> {}:coin:".format(wallet_money, wallet_money + member_data.lastRoulettePrize))

        member_data.wallet += member_data.lastRoulettePrize
        member_data.isPlayingRoulette = False
        await message.channel.send(embed=em)
        save_member_data(message.author.id, member_data)
    else:
        await message.channel.send(":x: **You're not playing roulette!**")

@bot.command(aliases=["sl"])
async def slots(message, amt=None):
    member_data = load_member_data(message.author.id)
    wallet_money = member_data.wallet
    if amt is None or int(amt) <= 0:
        await message.channel.send(":x: **Enter a valid number!**")
        return
    if wallet_money >= int(amt) > 0:
        member_data.TotalGamesPlayed += 1
        member_data.SlotsPlayed += 1
        em = None
        result = [random.choice(SLOTS_OPTIONS) for i in range(3)]
        #result = [":gem:", ":gem:", ":gem:"]
        #result = [":cherries:", ":cherries:", ":cherries:"]
        if all([i == result[0] for i in result[1::]]) and result[0] == ":gem:":
            wallet_money = add_wmoney(message.author, 100*int(amt))
            member_data.MoneyWon += 100*int(amt)
            member_data.MoneyWoninSlots += 100*int(amt)
            em = discord.Embed(title=":slot_machine: **MEGA WIN**", description=f"{result[0]} {result[1]} {result[2]} **100x**", colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Wallet", value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money + 100*int(amt)}:coin:")
        elif all([i == result[0] for i in result[1::]]) and result[0] == ":cherries:":
            wallet_money = add_wmoney(message.author,50*int(amt))
            member_data.MoneyWon += 50*int(amt)
            member_data.MoneyWoninSlots += 50*int(amt)
            em = discord.Embed(title=":slot_machine: **HUGE WIN**", description=f"{result[0]} {result[1]} {result[2]} **50x**", colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Wallet", value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money + 50*int(amt)}:coin:")
        elif all([i == result[0] for i in result[1::]]):
            wallet_money = add_wmoney(message.author, 20*int(amt))
            member_data.MoneyWon += 20*int(amt)
            member_data.MoneyWoninSlots += 20*int(amt)
            em = discord.Embed(title=":slot_machine: **BINGO**", description=f"{result[0]} {result[1]} {result[2]} **20x**", colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Wallet", value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money + 20*int(amt)}:coin:")
        elif result[0] == result[1] or result[0] == result[2] or result[1] == result[2]:
            wallet_money = add_wmoney(message.author, 5*int(amt))
            member_data.MoneyWon += 5*int(amt)
            member_data.MoneyWoninSlots += 5*int(amt)
            em = discord.Embed(title=":slot_machine: **WIN**", description=f"{result[0]} {result[1]} {result[2]} **5x**", colour=discord.Color.from_rgb(60,179,113))
            em.add_field(name="Wallet", value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money + 5*int(amt)}:coin:")
        else:
            wallet_money = remove_wmoney(message.author, int(amt))
            member_data.MoneyLost += int(amt)
            member_data.MoneyLostinSlots += int(amt)
            em = discord.Embed(title=":slot_machine: **LOSS**", description=f"{result[0]} {result[1]} {result[2]}", colour=discord.Color.from_rgb(220,20,60))
            em.add_field(name="Wallet", value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money - int(amt)}:coin:")

        member_data.wallet = wallet_money
        save_member_data(message.author.id, member_data)
        await message.channel.send(embed=em)
    elif wallet_money < int(amt):
        await message.channel.send(":x: **You don't have enough money in your wallet!**")


@bot.command(aliases=['hl'])
async def highlow(message, bet):
    member_data = load_member_data(message.author.id)
    print(member_data.isPlayingHL)
    if not member_data.isPlayingHL:
        member_data.isPlayingHL = True
        save_member_data(message.author.id, member_data)
        bet = int(bet)
        wallet_bal = member_data.wallet
        if wallet_bal >= bet > 0:
            member_data.TotalGamesPlayed += 1
            member_data.HighLowsPlayed += 1
            secret = ri(0, 100)
            hint = ri(40, 60)
            answers = ["high", "low", "jackpot"]
            if hint > secret:
                answer = 'low'
            elif hint < secret:
                answer = 'high'
            else:
                answer = 'jackpot'

            em = discord.Embed(title=":chart_with_upwards_trend::chart_with_downwards_trend: High-low game",
                               description="A number between 1 and 100 was chosen.")
            em.add_field(name='Hint', value=f'**{hint}**', inline=True)
            em.add_field(name='Bet', value=f'**{bet}**:coin:', inline=False)
            em.add_field(name='Actions', value="`high`, `low` or `jackpot`")
            em.set_footer(text='Choose whether chosen number is higher, lower or equals the hint.')

            await message.channel.send(embed=em)

            def check(m):
                return message.author == m.author

            msg = await bot.wait_for('message', check=check)
            while msg.content not in answers or not check(msg):
                await message.channel.send(
                    ":x: **I expected something from `high`, `low` or `jackpot`**")
                msg = await bot.wait_for('message', check=check)
                print(msg.content)
            if answer == "jackpot":
                member_data.MoneyWon += bet*10
                member_data.MoneyWoninHighLow += bet*10
                em = discord.Embed(title="You won!",
                                   description=f"The hint was **{hint}**, and the number was **{secret}**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray:**{wallet_bal}:coin: --> {wallet_bal + int(10 * bet)}:coin: (Jackpot!!!)**")
                member_data.wallet += int(10 * bet)
                member_data.isPlayingHL = False
                save_member_data(message.author.id, member_data)
                await message.channel.send(embed=em)
            elif msg.content.lower() == answer:
                member_data.MoneyWon += bet
                member_data.MoneyWoninHighLow += bet
                em = discord.Embed(title="You won!",
                                   description=f"The hint was **{hint}**, and the number was **{secret}**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray:**{wallet_bal}:coin: --> {wallet_bal + bet}:coin:**")
                member_data.wallet += bet
                member_data.isPlayingHL = False
                save_member_data(message.author.id, member_data)
                await message.channel.send(embed=em)
            else:
                member_data.MoneyLost += bet
                member_data.MoneyLostinHighLow += bet
                em = discord.Embed(title="You lost!",
                                   description=f"The hint was **{hint}**, and the number was **{secret}**",
                                   colour=discord.Color.from_rgb(220, 20, 60))
                em.add_field(name="Wallet",
                             value=f":inbox_tray:**{wallet_bal}:coin: --> {wallet_bal - bet}:coin:**")
                member_data.wallet -= bet
                member_data.isPlayingHL = False
                save_member_data(message.author.id, member_data)
                await message.channel.send(embed=em)
        else:
            if bet < 0:
                await message.channel.send(":x: **Enter a valid number!**")
            else:
                await message.channel.send(":x: **You don't have enough money in your wallet!**")
    else:
        member_data.isPlayingHL = False
        save_member_data(message.author.id, member_data)
        pass


@bot.command()
async def send(message, amt, member: discord.Member = None):
    author_data = load_member_data(message.author.id)
    member_data = load_member_data(member.id)
    if author_data.bank >= int(amt) > 0 and message.author != member:
        abbal = author_data.bank
        mbbal = member_data.bank
        send_money(message.author, member, amt)
        abbal1 = abbal - int(amt)
        mbbal1 = mbbal + int(amt)

        embed = discord.Embed(title=':white_check_mark: Operation complete!', colour=discord.Color.from_rgb(60,179,113))
        embed.add_field(name="Sender", value=message.author.mention, inline=True)
        embed.add_field(name="Receiver", value=member.mention)
        embed.add_field(name="\u200b", value='\u200b')
        embed.add_field(name=f"Sender's bank", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(abbal, abbal1))
        embed.add_field(name=f"Receiver's bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(mbbal, mbbal1), inline=True)

        await message.channel.send(embed=embed)
    else:
        if int(amt) <= 0:
            await message.channel.send(":x: **Please enter valid number.**")
        elif int(amt) > author_data.bank:
            await message.channel.send(":x: **You do not have this amount of coins on your bank account!**")
        else:
            await message.channel.send(":x: **You can not send money to yourself!**")

@bot.command()
async def rob(message,  member: discord.Member = None):
    if member != None and member != message.author:
        author_data = load_member_data(message.author.id)
        member_data = load_member_data(member.id)
        author_money = [author_data.wallet, author_data.bank]
        member_money = [member_data.wallet, member_data.bank]
        mwbal = member_data.wallet
        if mwbal > 0:
            author_data.RobAttempts += 1
            member_data.TimesRobbed += 1

            robamount = ri(int(0.1 * mwbal), int(0.3 * mwbal))
            robchance = ri(25, 50)
            result = random.randint(0, 100)
            if result < robchance:
                member_money[0], author_money[0] = rob_money(message.author, member, robamount)
                author_data.SuccessfulRobberies += 1
                member_data.TimesSuccessfullyRobbed += 1
                author_data.TotalRobberyProfit += robamount

                em = discord.Embed(title=":white_check_mark: Robbed {} successfully!".format(member.display_name), colour=discord.Color.from_rgb(60,179,113))

                em.add_field(name=":moneybag: Robber", value=message.author.mention)
                em.add_field(name="Victim", value=member.mention)
                em.add_field(name="Money stolen", value=f"{robamount}:coin:")

                dm = discord.Embed(title=":exclamation: **You were robbed!!!**", colour=discord.Color.from_rgb(220,20,60))
                dm.add_field(name=":moneybag: Robber", value=message.author.mention)
                dm.add_field(name="Money stolen", value=f"{robamount}:coin:")

                p = await member.create_dm()

                await p.send(embed=dm)
                await message.channel.send(embed=em)
            else:
                author_data.TotalRobberyProfit -= 3 * robamount

                author_money[0], author_money[1], member_money[0], member_money[1] = send_money(message.author, member, 3 * robamount)

                em = discord.Embed(title=":man_police_officer: {} was caught!".format(message.author.display_name),
                               colour=discord.Color.from_rgb(220,20,60))

                em.add_field(name=":moneybag: Robber", value=message.author.mention)
                em.add_field(name="Victim", value=member.mention)
                em.add_field(name="Fee", value=f"{robamount*3}:coin:")

                dm = discord.Embed(title=":exclamation: **Rob attempt!!!**", description=f"{message.author.mention} attempted to rob you, but got caught", colour=discord.Color.from_rgb(220,20,60))
                dm.add_field(name=":moneybag: Robber", value=message.author.mention)
                dm.add_field(name="Fee", value=f"{robamount*3}:coin:")

                p = await member.create_dm()

                await p.send(embed=dm)
                await message.channel.send(embed=em)

            member_data.wallet, member_data.bank, author_data.wallet, author_data.bank = member_money[0], member_money[1], author_money[0], author_money[1]
            save_member_data(member.id, member_data)
            save_member_data(message.author.id, author_data)

        else:
            await message.channel.send(f":x: **{member.mention} does not have anything in his wallet.**")
    else:
        if member == None:
            await message.channel.send(":x: **Please write someone to rob))**")
        else:
            await message.channel.send(":x: **You can not rob yourself! :rofl:**")

@bot.command()
@commands.has_permissions(administrator=True)
async def shop_add(message, name, dsc, price):
    pass

#error messages
@bot.event
async def on_command_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        print('CommandOnCooldown error')
        if ctx.message.content == "#work":
            await ctx.send(":x:**You're already working. Come back in {}m {}s to collect the payment again.**".format(int((exc.retry_after % 3600) // 60), int(exc.retry_after % 60)))
        elif ctx.message.content == "#daily":
            await ctx.send(
                ":x:**You have already collected your reward. Come back in {}h {}m {}s to collect it.**".format(int(exc.retry_after // 3600), int((exc.retry_after % 3600) // 60), int(exc.retry_after % 60)))
        else:
            print("Unknown cooldown command")
    elif isinstance(exc, MissingRequiredArgument):
        print('MissingRequiredArgument error')
        await ctx.send(
            ":x: **I cannot understand this. Please check #help for valid syntax.**")
    elif isinstance(exc, MissingRole):
        print('MissingRole error')
        await ctx.send(
            ":x: **You do not have permission to run this command!**")
    elif isinstance(exc, MissingPermissions):
        print('MissingPermissions error')
        await ctx.send(
            ":x: **You do not have permission to run this command!**")
    else:
        print(exc)


#utility functions
def load_data():
    if os.path.isfile(data_filename) and os.path.getsize(data_filename) > 0:
        with open(data_filename, "rb") as file:
            return pickle.load(file)
    else:
        return dict()

def load_member_data(member_ID):
    data = load_data()

    if member_ID not in data: #adding data for new members if they dont have it
        return Data(0, 0, False, 0, 0, None, False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    return data[member_ID]

def save_member_data(member_ID, member_data):
    data = load_data()

    data[member_ID] = member_data

    with open(data_filename, "wb") as file:
        pickle.dump(data, file)

def add_money(user, amount):
    member_data = load_member_data(user.id)
    member_data.bank += int(amount)
    save_member_data(user.id, member_data)
    return member_data.bank

def add_wmoney(user, amount):
    member_data = load_member_data(user.id)
    member_data.wallet += int(amount)
    save_member_data(user.id, member_data)
    return member_data.wallet

def remove_money(user, amount):
    member_data = load_member_data(user.id)
    member_data.bank -= int(amount)
    save_member_data(user.id, member_data)

def remove_wmoney(user, amount):
    member_data = load_member_data(user.id)
    member_data.wallet -= int(amount)
    save_member_data(user.id, member_data)
    return member_data.wallet

def set_money(user, amount):
    member_data = load_member_data(user.id)
    member_data.bank = int(amount)
    save_member_data(user.id, member_data)

def withdraw_money(user, amount):
    member_data = load_member_data(user.id)
    member_data.bank -= int(amount)
    member_data.wallet += int(amount)
    save_member_data(user.id, member_data)

def deposit_money(user, amount):
    member_data = load_member_data(user.id)
    member_data.bank += int(0.9 * int(amount))
    member_data.wallet -= int(amount)
    save_member_data(user.id, member_data)

def send_money(sender, receiver, amount):
    sender_data = load_member_data(sender.id)
    receiver_data = load_member_data(receiver.id)
    if sender_data.bank >= int(amount):
        sender_data.bank -= int(amount)
        receiver_data.bank += int(amount)
    else:
        sender_data.wallet -= sender_data.bank + int(amount)
        sender_data.bank = 0
        receiver_data.bank += int(amount)
    save_member_data(sender.id, sender_data)
    save_member_data(receiver.id, receiver_data)
    return sender_data.wallet, sender_data.bank, receiver_data.wallet, receiver_data.bank

def rob_money(robber, victim, amount):
    victim_data = load_member_data(victim.id)
    robber_data = load_member_data(robber.id)
    victim_data.wallet -= int(amount)
    robber_data.wallet += int(amount)
    save_member_data(victim.id, victim_data)
    save_member_data(robber.id, robber_data)
    return victim_data.wallet, robber_data.wallet

def to_sec(time):
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return 'Error'

#importing cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.loop.create_task(change_status()) #enabling changing status
bot.run(TOKEN) #running the bot