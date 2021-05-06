import os
import os.path
import pickle
import random
import datetime
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
ENTER_ROLE_ID = 836891624398389298
SLOTS_OPTIONS = [":watch:", ":bulb:", ":yo_yo:", ":paperclip:", ":cd:", ":dvd:", ":mag_right:", ":amphora:", ":ringed_planet:", ":gem:", ":rugby_football:", ":nut_and_bolt:", ":lemon:", ":package:", ":crystal_ball:", ":cherries:", ":video_game:", ":tickets:"]

intents = discord.Intents.all()
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
    statuses = ['#help', f'on {len(bot.guilds)} servers', 'slots', 'with coins', 'dice', 'on v0.2', 'the ban hammer', "with cogs"]

    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity=discord.Game(name=status))

        await asyncio.sleep(15)



class Data:
    def __init__(self, wallet, bank, isPlayingRoulette, lastRouletteBet, lastRoulettePrize, lastMessage, isPlayingHL, DicesPlayed, RoulettesPlayed, SlotsPlayed, HighLowsPlayed, MoneyWon, MoneyLost, RobAttempts, TimesRobbed, DailyRewardsCollected, WorksCollected, SuccessfulRobberies, TimesSuccessfullyRobbed, MoneyWoninDice, MoneyLostinDice, MoneyWoninSlots, MoneyLostinSlots, MoneyWoninHighLow, MoneyLostinHighLow, MoneyWoninRoulette, MoneyLostinRoulette, TotalRobberyProfit, TotalGamesPlayed, MoneyGotfromDailyRewards, MoneyGotfromWorkPayments, TimeJoined):
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

        self.TimeJoined = TimeJoined

@bot.event
async def on_ready():
    print('Froggy is logged in as {0.user}'.format(bot))

@bot.event
async def on_guild_join(guild):
    setup_channel = random.choice(guild.text_channels)
    await setup_channel.send("Hello, I'm Froggy!")

@bot.event
async def on_member_join(member):
    member_data = load_member_data(member.id)
    member_data.TimeJoined = datetime.datetime.today()

    role = get(member.guild.roles, id=836891624398389298)
    await member.add_roles(role)

    p = await member.create_dm()
    await p.send(f"Nice to meet you on {member.guild.name} server!")

    save_member_data(member.id, member_data)

@bot.event
async def on_member_left(member):
    p = await member.create_dm()
    await p.send(f"Bye, bye!")

@bot.command()
async def test(ctx):
    pass

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
        creationDate = ctx.message.author.created_at
    else:
        md = load_member_data(member.id)
        info_owner = member.display_name
        user_age = time.time() - member.created_at.timestamp()
        creationDate = member.created_at


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
        em.add_field(name='General info',      value=f"The account age = {int(user_age//31536000)}y {int(user_age//86400) - int(user_age//31536000*365)}d {int(user_age//3600) - int(user_age//86400)*24}h {int(user_age//60) - int(user_age//3600)*60}m\n\
                                                       The account creation date = {creationDate.year}-{creationDate.month}-{creationDate.day}\n\
                                                       Last time joined this server = {md.TimeJoined.year}-{md.TimeJoined.month}-{md.TimeJoined.day}")
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
        return Data(0, 0, False, 0, 0, None, False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, datetime.datetime.today())

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