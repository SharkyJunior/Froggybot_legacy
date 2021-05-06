import operator

import discord
from discord.ext import commands
from main import load_member_data, deposit_money, withdraw_money, set_money, remove_money, add_money, send_money


# initializing cog
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Utils are ready')

    # commands
    @commands.command(aliases=['lb'])
    async def leaderboard(self, message, category):
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

    @commands.command(aliases=['am', 'addm'])
    @commands.has_permissions(administrator=True)
    async def addmoney(self, message, amt, member: discord.Member = None):
        if int(amt) > 0 and float(amt) % 1 == 0:
            if member == None:
                member_data = load_member_data(message.author.id)
                bal = member_data.bank
                add_money(message.author, amt)
                bal1 = bal + int(amt)
                em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Recipient", value=message.author.mention)
                em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
                await message.channel.send(embed=em)
            else:
                member_data = load_member_data(member.id)
                bal = member_data.bank
                add_money(member, amt)
                bal1 = bal + int(amt)
                em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Recipient", value=member.mention)
                em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
                await message.channel.send(embed=em)
        else:
            await message.channel.send(":x: **Please enter valid number.**".format(message.author.mention))

    @commands.command(aliases=['rm'])
    @commands.has_permissions(administrator=True)
    async def removemoney(message, amt, member: discord.Member = None):
        if int(amt) > 0 and float(amt) % 1 == 0:
            if member == None:
                member_data = load_member_data(message.author.id)
                bal = member_data.bank
                remove_money(message.author, amt)
                bal1 = bal - int(amt)
                embed = discord.Embed(title=':white_check_mark: Operation complete!',
                                      colour=discord.Color.from_rgb(60, 179, 113))
                embed.add_field(name="Recipient", value=message.author.mention)
                embed.add_field(name="Bank", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
                await message.channel.send(embed=embed)
            else:
                member_data = load_member_data(member.id)
                bal = member_data.bank
                remove_money(member, amt)
                bal1 = bal - int(amt)
                em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Recipient", value=member.mention)
                em.add_field(name="Bank", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
                await message.channel.send(embed=em)
        else:
            await message.channel.send(":x: **Please enter valid number.**".format(message.author.mention))

    @commands.command(aliases=['sm', 'setm'])
    @commands.has_permissions(administrator=True)
    async def setmoney(self, message, amt, member: discord.Member = None):
        if int(amt) >= 0 and float(amt) % 1 == 0:
            if member == None:
                member_data = load_member_data(message.author.id)
                bal = member_data.bank
                set_money(message.author, amt)
                bal1 = int(amt)
                em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Recipient", value=message.author.mention)
                em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
                await message.channel.send(embed=em)
            else:
                member_data = load_member_data(member.id)
                bal = member_data.bank
                set_money(member, amt)
                bal1 = int(amt)
                em = discord.Embed(title=':white_check_mark: Operation complete!',
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Recipient", value=member.mention)
                em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
                await message.channel.send(embed=em)
        else:
            await message.channel.send(":x: **Please enter valid number.**".format(message.author.mention))

    @commands.command(aliases=['wd'])
    async def withdraw(self, message, amt):
        member_data = load_member_data(message.author.id)
        if amt != "all":
            if member_data.bank >= int(amt) > 0:
                member_data = load_member_data(message.author.id)
                bbal = member_data.bank
                wbal = member_data.wallet
                withdraw_money(message.author, amt)
                bbal1 = bbal - int(amt)
                wbal1 = wbal + int(amt)

                embed = discord.Embed(title=':white_check_mark: Operation complete!',
                                      colour=discord.Color.from_rgb(60, 179, 113))
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
                                      colour=discord.Color.from_rgb(60, 179, 113))
                embed.add_field(name="Requester", value=message.author.mention, inline=False)
                embed.add_field(name="Bank", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(bbal, bbal1))
                embed.add_field(name="Wallet", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(wbal, wbal1))

                await message.channel.send(embed=embed)
            else:
                await message.channel.send(":x: **You do not have any money on your bank account** ")

    @commands.command(aliases=['dep'])
    async def deposit(self, message, amt):
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

                embed = discord.Embed(title=':white_check_mark: Operation complete!',
                                      colour=discord.Color.from_rgb(60, 179, 113))
                embed.add_field(name="Requester", value=message.author.mention, inline=False)
                embed.add_field(name="Wallet", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(wbal, wbal1))
                embed.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bbal, bbal1),
                                inline=False)
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
                embed = discord.Embed(title=':white_check_mark: Operation complete!',
                                      colour=discord.Color.from_rgb(60, 179, 113))
                embed.add_field(name="Requester", value=message.author.mention, inline=False)
                embed.add_field(name="Wallet", value=":outbox_tray: **{}:coin: --> {}:coin:**".format(wbal, wbal1))
                embed.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bbal, bbal1),
                                inline=False)
                embed.add_field(name="Fee", value=f"**{fee}**:coin:")

                await message.channel.send(embed=embed)
            else:
                await message.channel.send("You don't have any money in wallet")

    @commands.command(aliases=['bal'])
    async def balance(self, message, member: discord.Member = None):
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

    @commands.command()
    async def send(self, message, amt, member: discord.Member = None):
        author_data = load_member_data(message.author.id)
        member_data = load_member_data(member.id)
        if author_data.bank >= int(amt) > 0 and message.author != member:
            abbal = author_data.bank
            mbbal = member_data.bank
            send_money(message.author, member, amt)
            abbal1 = abbal - int(amt)
            mbbal1 = mbbal + int(amt)

            embed = discord.Embed(title=':white_check_mark: Operation complete!',
                                  colour=discord.Color.from_rgb(60, 179, 113))
            embed.add_field(name="Sender", value=message.author.mention, inline=True)
            embed.add_field(name="Receiver", value=member.mention)
            embed.add_field(name="\u200b", value='\u200b')
            embed.add_field(name=f"Sender's bank",
                            value=":outbox_tray: **{}:coin: --> {}:coin:**".format(abbal, abbal1))
            embed.add_field(name=f"Receiver's bank",
                            value=":inbox_tray: **{}:coin: --> {}:coin:**".format(mbbal, mbbal1), inline=True)

            await message.channel.send(embed=embed)
        else:
            if int(amt) <= 0:
                await message.channel.send(":x: **Please enter valid number.**")
            elif int(amt) > author_data.bank:
                await message.channel.send(":x: **You do not have this amount of coins on your bank account!**")
            else:
                await message.channel.send(":x: **You can not send money to yourself!**")
# activating cog
def setup(bot):
    bot.add_cog(Utils(bot))
