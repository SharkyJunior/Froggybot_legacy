import discord
from discord.ext import commands

# initializing cog
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help is ready')

    # initiate help command
    @commands.group(invoke_without_command=True)
    async def help(self, message):
        em = discord.Embed(title="Help menu", description="Use **#help <command>** for detail information",
                           colour=message.author.color)

        em.add_field(name=":moneybag: Economy",
                     value="`addmoney | balance | daily | deposit | removemoney | rob | send | setmoney | withdraw | work`")
        em.add_field(name=":tools: Utility & Moderation",
                     value="`ban | clear | giveaway_setup | giveaway_start | kick | leaderboard | mute | tempban | tempmute | unban | unmute | user_info`")
        em.add_field(name=":slot_machine: Gamble", value="`dice | highlow | roulette | slots`")

        await message.send(embed=em)

    #then it goes for each command
    @help.command()
    async def addmoney(self, message):
        em = discord.Embed(title="addmoney", description="Adds a written amount of coins to person's bank account",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#addmoney [amount] <member>(optional)`")
        em.add_field(name="**Aliases**", value="`#am, #addm`")
        em.add_field(name="Permissions", value="**administrator**")
        await message.send(embed=em)

    @help.command()
    async def balance(self, message):
        em = discord.Embed(title="balance", description="Shows person's bank and wallet balance",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#balance <member>(optional)`")
        em.add_field(name="**Aliases**", value="`#bal`")
        await message.send(embed=em)

    @help.command()
    async def daily(self, message):
        em = discord.Embed(title="daily", description="Claims your daily reward (40% of your bank account)",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#daily`")
        await message.send(embed=em)

    @help.command()
    async def leaderboard(self, message):
        em = discord.Embed(title="leaderboard", description="Shows server's leaderboard in chosen category.",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#leaderboard <category>`")
        em.add_field(name="**Aliases**", value="`#lb`")
        em.add_field(name="**Categories**", value="`bank`\n`wallet`")
        await message.send(embed=em)

    @help.command()
    async def work(self, message):
        em = discord.Embed(title="work", description="Go to work for a payment(5%-10% of your bank account)",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#work`")
        await message.send(embed=em)

    @help.command()
    async def deposit(self, message):
        em = discord.Embed(title="deposit",
                           description="Transfers a certain amount of money from wallet to bank account (10% fee)",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#deposit [amount]`")
        em.add_field(name="**Aliases**", value="`#dep`")
        await message.send(embed=em)

    @help.command()
    async def dice(self, message):
        em = discord.Embed(title="dice", description="Throw 2 dice and win against computer!",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#dice [bet]`")
        await message.send(embed=em)

    @help.command()
    async def roulette(self, message):
        em = discord.Embed(title="roulette", description="Try to survive in russian roulette and win coins!\n"
                                                         "More rounds you load - more you win",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#roulette [bet] [loaded rounds (up to 5)]`")
        em.add_field(name="**Aliases**", value="`#rt`")
        await message.send(embed=em)

    @help.command()
    async def highlow(self, message):
        em = discord.Embed(title="highlow",
                           description="Guess whether chosen number is higher, lower or equals the hint and win coins!",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#highlow [bet]`")
        em.add_field(name="**Aliases**", value="`#hl`")
        await message.send(embed=em)

    @help.command()
    async def slots(self, message):
        em = discord.Embed(title="slots", description="Test your luck and win up to 100x your bet",
                           colour=message.author.color)
        em.add_field(name="**Possible results**",
                     value="2 in a row - **5x**\n3 in a row - **20x**\n:cherries::cherries::cherries: - **50x**\n:gem::gem::gem: - **100x**")
        em.add_field(name="**Syntax**", value="`#slots [bet]`")
        em.add_field(name="**Aliases**", value="`#sl`")
        await message.send(embed=em)

    @help.command()
    async def removemoney(self, message):
        em = discord.Embed(title="removemoney",
                           description="Substracts a written amount of coins from person's bank account",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#removemoney [amount] <member>(optional)`")
        em.add_field(name="**Aliases**", value="`#rm`")
        em.add_field(name="Permissions", value="`**administrator**")
        await message.send(embed=em)

    @help.command()
    async def rob(self, message):
        em = discord.Embed(title="rob", description="Try to rob a person (you can be caught!)",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#rob <member>`")
        await message.send(embed=em)

    @help.command()
    async def sendmoney(self, message):
        em = discord.Embed(title="send",
                           description="Transfers a certain amount of money from your bank account to a person's bank account",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#send [amount] <member>`")
        await message.send(embed=em)

    @help.command()
    async def setmoney(self, message):
        em = discord.Embed(title="setmoney",
                           description="Sets the written amount of money in the person's bank account",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#setmoney [amount] <member>(optional)`")
        em.add_field(name="**Aliases**", value="`#sm, #setm`")
        em.add_field(name="Permissions", value="**administrator**")
        await message.send(embed=em)

    @help.command()
    async def withdraw(self, message):
        em = discord.Embed(title="withdraw",
                           description="Transfers a certain amount of money from bank account to wallet",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#withdraw [amount]`")
        em.add_field(name="**Aliases**", value="`#wd`")
        await message.send(embed=em)

    @help.command()
    async def kick(self, message):
        em = discord.Embed(title="kick", description="Kicks a member from the server",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#kick <member> <reason>(optional)`")
        em.add_field(name="Permissions", value="**kick members**")
        await message.send(embed=em)

    @help.command()
    async def mute(self, message):
        em = discord.Embed(title="mute", description="Mutes a member",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#mute <member> <reason>(optional)`")
        em.add_field(name="Permissions", value="**administrator**")
        await message.send(embed=em)

    @help.command()
    async def tempmute(self, message):
        em = discord.Embed(title="tempmute", description="Temporarily mutes a member",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#tempmute <member> [duration(for example: 10s)] <reason>(optional)`")
        em.add_field(name="Permissions", value="**administrator**")
        await message.send(embed=em)

    @help.command()
    async def unmute(self, message):
        em = discord.Embed(title="unmute", description="Unmute a member",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#unmute <member>`")
        em.add_field(name="Permissions", value="**administrator**")
        await message.send(embed=em)

    @help.command()
    async def ban(self, message):
        em = discord.Embed(title="ban", description="Bans a member from the server",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#ban <member> <reason>(optional)`")
        em.add_field(name="Permissions", value="**ban members**")
        await message.send(embed=em)

    @help.command()
    async def tempban(self, message):
        em = discord.Embed(title="tempban", description="Temporarily bans a member from the server",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#tempban <member> [duration(for example: 10s)] <reason>(optional)`")
        em.add_field(name="Permissions", value="**ban members**")
        await message.send(embed=em)

    @help.command()
    async def unban(self, message):
        em = discord.Embed(title="unban", description="Unbans a player",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#unban <name#discriminator>`")
        em.add_field(name="Permissions", value="**ban members**")
        await message.send(embed=em)

    @help.command()
    async def clear(self, message):
        em = discord.Embed(title="clear",
                           description="Clears given amount of messages (if amount wasn't typed, clears 100 messages)",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#clear [amount](optional)`")
        em.add_field(name="Permissions", value="**administrator**")
        await message.send(embed=em)

    @help.command()
    async def clearmoney(self, message):
        em = discord.Embed(title="clear", description="Clears wallet and bank account data",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#clear <member>(optional)`")
        em.add_field(name="Permissions", value="**administrator**")
        await message.send(embed=em)

    @help.command()
    async def giveaway_setup(self, message):
        em = discord.Embed(title="giveaway_setup", description="Setups and creates a giveaway",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#giveaway_setup`")
        em.add_field(name="Permissions", value="**manage messages**")
        em.add_field(name="**Aliases**", value="`#gsetup, #giveaway-setup`")
        await message.send(embed=em)

    @help.command()
    async def giveaway_start(self, message):
        em = discord.Embed(title="giveaway_start", description="Instantly creates a giveaway",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#giveaway_start [time] [winners amount] <channel> <prize>`")
        em.add_field(name="Permissions", value="**manage messages**")
        em.add_field(name="**Aliases**", value="`#gstart, #giveaway-start, #gs`")
        await message.send(embed=em)

    @help.command()
    async def user_info(self, message):
        em = discord.Embed(title="user_info", description="Gives you lots of information about a user",
                           colour=message.author.color)
        em.add_field(name="**Syntax**", value="`#user_info [the info shown (mode)] [server member]`")
        em.add_field(name="Possible modes",
                     value="`full` - displays all info about the user\n `money` - displays all money stats\n `games` "
                           "- displays all games stats\n `rewards` - displays all info about Daily rewards and Work "
                           "payments\n `robbery` - displays all robbery stats")
        em.add_field(name="**Aliases**", value="`#user-info, #user_info`")
        await message.send(embed=em)

# activating cog
def setup(bot):
    bot.add_cog(Help(bot))