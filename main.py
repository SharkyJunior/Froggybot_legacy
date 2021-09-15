import os.path
import random
import math
import datetime
import asyncio
import time
import operator
from discord_slash import SlashCommand, SlashContext

from discord.utils import *
from discord import *
from discord.ext import commands
from discord.ext.commands import cooldown, CommandOnCooldown, MissingRequiredArgument, MissingRole, MissingPermissions

from info_operator import *

TOKEN = 'ODM3MzIwODIxMDAwODk2NTYy.YIq1yA.w4nZlr7tfs0jyUGrvauASD8VqrI'
PREFIX = '#'
ROULETTE_MULTIPLIER = 1.2
GUILD_ID = 836887040364511283
DAILY_LIMIT = 2400
DAILY_MULTIPLIER = 0.4
WORK_LIMIT = 100
ENTER_ROLE_ID = 836891624398389298
MESSAGES_PER_LEVEL_MODIFIER = 1.4

intents = Intents.all()
intents.members = True
activity = Game(name='#help')
bot = commands.Bot(command_prefix=PREFIX, activity=activity, intents=intents)
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command('help')
guilds_ids = [839566467375956041]


@bot.listen('on_message')
async def message_tracker(message):
    if not message.author.bot:
        member_data = load_member_data(message.author, message.guild)
        member_data["Messages_Quantity"] += 1
        if member_data["Messages_Quantity"] >= ((member_data["Level"]+1)*MESSAGES_PER_LEVEL_MODIFIER)**2:
            member_data["Level"] += 1
            level = member_data["Level"]
            await message.channel.send(f"{message.author.mention} Congrats! You achieved level {level}")
        save_member_data(member_data, message.author, message.guild)


@bot.command()
async def ping(msg):
    await msg.channel.send(f'My latency is **{int(bot.latency * 1000)}** ms')

@bot.command()
@commands.has_permissions(administrator=True)
async def load(message, extension):
    bot.load_extension(f'cogs.{extension}')
    await message.channel.send(f"Successfully loaded `{extension}` up!")


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(message, extension):
    bot.unload_extension(f'cogs.{extension}')
    await message.channel.send(f"Successfully unloaded `{extension}`!")


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(message, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await message.channel.send(f"Successfully reloaded `{extension}`!")


async def change_status():
    await bot.wait_until_ready()
    statuses = ['#help', f'on {len(bot.guilds)} servers', 'slots', 'with coins', 'dice', 'on v0.2', 'with the ban hammer',
                "with cogs", "roulette", "music", "highlow"]

    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity=Game(name=status))

        await asyncio.sleep(15)


@bot.event
async def on_ready():
    print('Froggy is logged in as {0.user}'.format(bot))


@bot.event
async def on_guild_join(guild):
    setup_channel = guild.text_channels[0]
    await setup_channel.send("Hello, I'm Froggy!")
    create_default_guild_data(guild)


@bot.event
async def on_guild_remove(guild):
    remove_guild_data(guild)


@bot.event
async def on_member_join(member):
    server_info = load_server_data(member.guild)

    if server_info["on-member-join-message"] != "no" and server_info["on-member-join-channel"] != "no":
        channel = bot.get_channel(int(server_info["on-member-join-channel"]))
        message = server_info["on-member-join-message"].replace("|", member.guild.name)
        message = message.replace("~", member.mention)

        await channel.send(message)

    if server_info["on-member-join-dm"] != "no":
        p = await member.create_dm()
        if "|" in server_info["on-member-join-dm"]:
            await p.send(server_info["on-member-join-dm"].replace("|", member.guild.name))
        else:
            await p.send(server_info["on-member-join-dm"])

    if server_info["enter-role-id"] != "no":
        role = get(member.guild.roles, id=server_info["enter-role-id"])
        await member.add_roles(role)


@bot.event
async def on_member_left(member):
    server_info = load_server_data(member.guild)

    if server_info["on-member-left-message"] != "no" and server_info["on-member-left-channel"] != "no":
        channel = bot.get_channel(int(server_info["on-member-left-channel"]))
        if "|" in server_info["on-member-left-message"]:
            await channel.send(server_info["on-member-left-message"].replace("|", member.guild.name))
        else:
            await channel.send(server_info["on-member-left-message"])

    if server_info["on-member-left-dm"] != "no":
        p = await member.create_dm()
        if "|" in server_info["on-member-left-dm"]:
            await p.send(server_info["on-member-left-dm"].replace("|", member.guild.name))
        else:
            await p.send(server_info["on-member-left-dm"])


@slash.slash(name="ping",description="Pings the bot", guild_ids=guilds_ids)
async def ping(ctx: SlashContext):
    embed = Embed(title=f'My latency is **{int(bot.latency * 1000)}** ms')
    await ctx.send(embed=embed)


@bot.command()
async def cdmd(ctx, member: User = None):
    if member is None:
        member = ctx.author
    create_default_member_data(member, ctx.guild)
    await ctx.channel.send(f"Default member data created successfully for {member.mention}!")


@bot.command()
async def cdgd(ctx):
    create_default_guild_data(ctx.guild)
    await ctx.channel.send("Default guild data created successfully!")


@bot.command()
async def cdd(ctx):
    create_default_data()
    await ctx.channel.send("Default data created successfully!")


@bot.command()
async def cdsd(ctx):
    create_default_server_data(ctx.guild)
    await ctx.channel.send("Default server info created successfully!")


@bot.command()
async def cdshd(ctx):
    create_default_shop_data(ctx.guild)
    await ctx.channel.send("Default shop info created successfully!")


@bot.command()
async def cdid(ctx, member: User = None):
    if member is None:
        member = ctx.author
    create_default_inventory_data(member, ctx.guild)
    await ctx.channel.send(f"Default inventory created for {member.mention} successfully!")


@bot.command()
async def server_info(ctx):
    await ctx.channel.send(":x: Nothing made here yet! :no_good:")
    server_info = ctx.guild

@slash.slash(name='user_info', description='Shows person\'s statistics', guild_ids=guilds_ids)
async def user_info(ctx: SlashContext, member: Member = None, mode='full'):
    print(member)
    print(ctx.author)
    if member is None:
        md = load_member_data(ctx.author, ctx.guild)
        info_owner = ctx.author.display_name
        #user_age = time.time() - ctx.message.author.created_at.timestamp()
        creationDate = ctx.author.created_at
    else:
        md = load_member_data(member, ctx.guild)
        info_owner = member.display_name
        #user_age = time.time() - member.created_at.timestamp()
        creationDate = member.created_at

    em = Embed(title=f':ledger: {info_owner}', colour=Color.from_rgb(255, 211, 0))
    if mode == "full":
        em.add_field(name='Money stats',       value=f"Money total won = {md['MoneyWon']}:coin:\n\
                                                       Money total lost = {md['MoneyLost']}:coin:\n\
                                                       Money in wallet = {md['wallet']}:coin:\n\
                                                       Money on bank account = {md['bank']}:coin:\n\
                                                       Money won in Dice = {md['MoneyWoninDice']}:coin:\n\
                                                       Money lost in Dice = {md['MoneyLostinDice']}:coin:\n\
                                                       Money won in Roulette = {md['MoneyWoninRoulette']}:coin:\n\
                                                       Money lost in Roulette = {md['MoneyLostinRoulette']}:coin:\n\
                                                       Money won in Slots = {md['MoneyWoninSlots']}:coin:\n\
                                                       Money lost in Slots = {md['MoneyLostinSlots']}:coin:\n\
                                                       Money won in HighLow = {md['MoneyWoninHighLow']}:coin:\n\
                                                       Money lost in HighLow = {md['MoneyLostinHighLow']}:coin:")
        em.add_field(name='Games played',      value=f"Total games played = {md['TotalGamesPlayed']}\n\
                                                       Dice = {md['DicesPlayed']}\n\
                                                       Roulette = {md['RoulettesPlayed']}\n\
                                                       Slots = {md['SlotsPlayed']}\n\
                                                       HighLow = {md['HighLowsPlayed']}")
        em.add_field(name='Rewards collected', value=f"Daily rewards = {md['DailyRewardsCollected']}\n\
                                                       Total money collected from daily rewards = {md['MoneyGotfromDailyRewards']}:coin:\n\
                                                       Work payments = {md['WorksCollected']}\n\
                                                       Total money collected from work = {md['MoneyGotfromWorkPayments']}:coin:")
        em.add_field(name='Robbery',           value=f"Total robbery profit = {md['TotalRobberyProfit']}:coin:\n\
                                                       Rob attempts = {md['RobAttempts']}\n\
                                                       Successful robberies = {md['SuccessfulRobberies']}\n\
                                                       The amount of times you were tried to get robbed = {md['TimesRobbed']}\n\
                                                       The amount of times you were succesfully robbed = {md['TimesSuccessfullyRobbed']}")
        #em.add_field(name='General info',      value=f"The account age = {int(user_age // 31536000)}y {int(user_age // 86400) - int(user_age // 31536000 * 365)}d {int(user_age // 3600) - int(user_age // 86400) * 24}h {int(user_age // 60) - int(user_age // 3600) * 60}m\n\
        #                                               The account creation date = {creationDate.year}-{creationDate.month}-{creationDate.day}")


    elif mode == "money" or mode == "m":
        em.add_field(name='Money stats',       value=f"Money total won = {md['MoneyWon']}:coin:\n\
                                                       Money total lost = {md['MoneyLost']}:coin:\n\
                                                       Money in wallet = {md['wallet']}:coin:\n\
                                                       Money on bank account = {md['bank']}:coin:\n\
                                                       Money won in Dice = {md['MoneyWoninDice']}:coin:\n\
                                                       Money lost in Dice = {md['MoneyLostinDice']}:coin:\n\
                                                       Money won in Roulette = {md['MoneyWoninRoulette']}:coin:\n\
                                                       Money lost in Roulette = {md['MoneyLostinRoulette']}:coin:\n\
                                                       Money won in Slots = {md['MoneyWoninSlots']}:coin:\n\
                                                       Money lost in Slots = {md['MoneyLostinSlots']}:coin:\n\
                                                       Money won in HighLow = {md['MoneyWoninHighLow']}:coin:\n\
                                                       Money lost in HighLow = {md['MoneyLostinHighLow']}:coin:")
    elif mode == "games" or mode == "g":
        em.add_field(name='Games played', value=f"Total games played = {md['TotalGamesPlayed']}\n\
                                                       Dice = {md['DicesPlayed']}\n\
                                                       Roulette = {md['RoulettesPlayed']}\n\
                                                       Slots = {md['SlotsPlayed']}\n\
                                                       HighLow = {md['HighLowsPlayed']}")
    elif mode == "rewards" or mode == "rd":
        em.add_field(name='Rewards collected', value=f"Daily rewards = {md['DailyRewardsCollected']}\n\
                                                       Total money collected from daily rewards = {md['MoneyGotfromDailyRewards']}:coin:\n\
                                                       Work payments = {md['WorksCollected']}\n\
                                                       Total money collected from work = {md['MoneyGotfromWorkPayments']}:coin:")
    elif mode == "robbery" or mode == "r":
        em.add_field(name='Robbery', value=f"Total robbery profit = {md['TotalRobberyProfit']}:coin:\n\
                                                       Rob attempts = {md['RobAttempts']}\n\
                                                       Successful robberies = {md['SuccessfulRobberies']}\n\
                                                       The amount of times you were tried to get robbed = {md['TimesRobbed']}\n\
                                                       The amount of times you were succesfully robbed = {md['TimesSuccessfullyRobbed']}")
    else:
        await ctx.channel.send(":x: No such a mode check `#help user_info` for the syntax")
        return

    

    await ctx.send(embed=em)


@bot.command()
@cooldown(1, 60 * 60 * 24, commands.BucketType.user)
async def daily(ctx):
    member_data = load_member_data(ctx.author, ctx.guild)
    member_data['DailyRewardsCollected'] += 1
    bal = member_data['bank']
    member_data['lastMessage'] = ctx.message.content
    bank_money = member_data['bank']
    if int(bal * DAILY_MULTIPLIER) > DAILY_LIMIT:
        amt = int(bank_money * DAILY_MULTIPLIER)
        bank_money = add_money(ctx.message.author, ctx.guild, amt)
        member_data['MoneyGotfromDailyRewards'] += amt
        bal1 = bal + int(member_data['bank'] * DAILY_MULTIPLIER)

        em = Embed(title=f":white_check_mark: {ctx.message.author.display_name}'s daily reward",
                           colour=Color.from_rgb(60, 179, 113))
        em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
        await ctx.message.channel.send(embed=em)
    else:
        bank_money = add_money(ctx.message.author, ctx.guild, DAILY_LIMIT)
        member_data['MoneyGotfromDailyRewards'] += DAILY_LIMIT
        bal1 = bal + DAILY_LIMIT

        em = Embed(title=f":white_check_mark: {ctx.message.author.display_name}'s daily reward",
                           colour=Color.from_rgb(60, 179, 113))
        em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
        await ctx.message.channel.send(embed=em)
    member_data['bank'] = bank_money
    save_member_data(member_data, ctx.author, ctx.guild)


@bot.command()
@cooldown(1, 60 * 60, commands.BucketType.user)
async def work(ctx):
    member_data = load_member_data(ctx.author, ctx.guild)
    member_data["WorksCollected"] += 1
    member_data['lastMessage'] = ctx.message.content
    bank_money = member_data['bank']
    bal = member_data['bank']
    work_multiplier = random.uniform(0.05, 0.1)
    if int(bal * work_multiplier) > WORK_LIMIT:
        bank_money = add_money(ctx.message.author, ctx.guild, int(member_data['bank'] * work_multiplier))
        member_data['MoneyGotfromWorkPayments'] += int(member_data['bank'] * work_multiplier)
        bal1 = bal + int(member_data['bank'] * work_multiplier)
        em = Embed(
            title=f":white_check_mark: {ctx.message.author.display_name}'s work payment, come back in 1 hour to collect next one",
            colour=Color.from_rgb(60, 179, 113))
        em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
        await ctx.message.channel.send(embed=em)
    else:
        bank_money = add_money(ctx.message.author, ctx.guild, WORK_LIMIT)
        member_data['MoneyGotfromWorkPayments'] += WORK_LIMIT
        bal1 = bal + WORK_LIMIT

        em = Embed(
            title=f":white_check_mark: {ctx.message.author.display_name}'s work payment, come back in 1 hour to collect next one",
            colour=Color.from_rgb(60, 179, 113))
        em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
        await ctx.message.channel.send(embed=em)
    member_data['bank'] = bank_money
    save_member_data(member_data, ctx.author, ctx.guild)


# error messages
# @bot.event
async def on_command_error(ctx, exc):
    if isinstance(exc, CommandOnCooldown):
        print('CommandOnCooldown error')
        if ctx.message.content == "#work":
            await ctx.send(":x:**You're already working. Come back in {}m {}s to collect the payment again.**".format(
                int((exc.retry_after % 3600) // 60), int(exc.retry_after % 60)))
        elif ctx.message.content == "#daily":
            await ctx.send(
                ":x:**You have already collected your reward. Come back in {}h {}m {}s to collect it.**".format(
                    int(exc.retry_after // 3600), int((exc.retry_after % 3600) // 60), int(exc.retry_after % 60)))
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


def buy_item(member, guild, item, quantity):
    shop_data = load_shop_data(guild)

    remove_money(member, guild, shop_data[item][0]*quantity)
    member_data = add_item(member, guild, item, quantity)

    shop_data[item][1] -= quantity

    save_shop_data(shop_data, guild)

    return member_data


def sell_item(member, guild, item, quantity):
    shop_data = load_shop_data(guild)

    remove_item(member, guild, item, quantity)
    add_money(member, guild, shop_data[item][0]*quantity)

    shop_data[item][1] += quantity
    save_shop_data(shop_data, guild)


def add_item(member, guild, item, quantity):
    member_inventory = load_inventory_data(member, guild)
    if item in member_inventory:
        member_inventory[item] += quantity
    else:
        member_inventory[item] = quantity

    save_inventory_data(member_inventory, member, guild)
    return member_inventory


def remove_item(member, guild, item, quantity):
    member_inventory = load_inventory_data(member, guild)
    if item in member_inventory:
        member_inventory[item] -= quantity
        if member_inventory[item] == 0:
            del member_inventory[item]
    else:
        member_inventory[item] = -quantity

    save_inventory_data(member_inventory, member, guild)
    return member_inventory


def set_item(member, guild, item, quantity):
    member_inventory = load_inventory_data(member, guild)

    member_inventory[item] = quantity

    save_inventory_data(member_inventory, member, guild)
    return member_inventory


def send_item(sender, receiver, guild, item, quantity):
    remove_item(sender, guild, item, quantity)
    add_item(receiver, guild, item, quantity)


# adds money to user's bank account and returns the final amount
def add_money(user, guild, amount):
    member_data = load_member_data(user, guild)
    member_data['bank'] += int(amount)
    save_member_data(member_data, user, guild)
    return member_data['bank']


# adds money to user's wallet and returns the final amount
def add_wmoney(user, guild, amount):
    member_data = load_member_data(user, guild)
    member_data['wallet'] += int(amount)
    save_member_data(member_data, user, guild)
    return member_data['wallet']


# removes money from user's bank account and returns the final amount
def remove_money(user, guild, amount):
    member_data = load_member_data(user, guild)
    member_data['bank'] -= int(amount)
    save_member_data(member_data, user, guild)
    return member_data['bank']


# removes money from user's wallet and returns the final amount
def remove_wmoney(user, guild, amount):
    member_data = load_member_data(user, guild)
    member_data['wallet'] -= int(amount)
    save_member_data(member_data, user, guild)
    return member_data['wallet']


# sets the amount of money on user's bank account and returns the final amount
def set_money(user, guild, amount):
    member_data = load_member_data(user, guild)
    member_data['bank'] = int(amount)
    save_member_data(member_data, user, guild)
    return member_data['bank']


# sets the amount of money in user's wallet and returns the final amount
def set_wmoney(user, guild, amount):
    member_data = load_member_data(user, guild)
    member_data['wallet'] = int(amount)
    save_member_data(member_data, user, guild)
    return member_data['wallet']


# transfers money from bank account to wallet and returns both final values
def withdraw_money(user, guild, amount):
    member_data = load_member_data(user, guild)
    member_data['bank'] -= int(amount)
    member_data['wallet'] += int(amount)
    save_member_data(member_data, user, guild)
    return member_data['bank'], member_data['wallet']


# transfers money from wallet to bank account and takes the fee out returning final values
def deposit_money(user, guild, amount):
    member_data = load_member_data(user, guild)
    member_data['bank'] += int(0.9 * int(amount))
    member_data['wallet'] -= int(amount)
    save_member_data(member_data, user, guild)
    return member_data['bank'], member_data['wallet']


# transfers money from sender's bank account to receiver's one if lack of money on sender's account,
# the money will be taken from sender's wallet
def send_money(sender, receiver, guild, amount):
    sender_data = load_member_data(sender, guild)
    receiver_data = load_member_data(receiver, guild)
    if sender_data['bank'] >= int(amount):
        sender_data['bank'] -= int(amount)
        receiver_data['bank'] += int(amount)
    else:
        sender_data['wallet'] -= sender_data['bank'] + int(amount)
        sender_data['bank'] = 0
        receiver_data['bank'] += int(amount)
    save_member_data(sender_data, sender, guild)
    save_member_data(receiver_data, receiver, guild)
    return sender_data['wallet'], sender_data['bank'], receiver_data['wallet'], receiver_data['bank']


def rob_money(robber, victim, guild, amount):
    victim_data = load_member_data(victim, guild)
    robber_data = load_member_data(robber, guild)
    victim_data['wallet'] -= int(amount)
    robber_data['wallet'] += int(amount)
    save_member_data(victim_data, victim, guild)
    save_member_data(robber_data, robber, guild)
    return victim_data['wallet'], robber_data['wallet']


def to_sec(time):
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return 'Error'


# importing cogs
#for filename in os.listdir('./cogs'):
#    if filename.endswith('.py'):
#        bot.load_extension(f'cogs.{filename[:-3]}')


bot.loop.create_task(change_status())  # enabling changing status
bot.run(TOKEN)  # running the bot
