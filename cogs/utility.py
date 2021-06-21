from main import *


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
    async def leaderboard(self, message):
        members = message.guild.members
        for i in members:
            if i.bot:
                members.remove(i)

        banks = []
        all_money = 0
        for member in members:
            member_data = load_member_data(member, message.guild)
            member_money = member_data['bank'] + member_data['wallet']
            banks.append([member, member_money])
            all_money += member_money
        banks = sorted(banks, key=operator.itemgetter(1), reverse=True)
        em = discord.Embed(title=f"{message.guild.name}'s money leaderboard", colour=message.author.color)

        places = 0
        if len(members) > 5:
            places = 5
        else:
            places = len(members)

        for i in range(places):
            if i == 0:
                if banks[0][1] > 0:
                    em.add_field(name=":bank: **Server total**", value=str(all_money), inline=False)
                    em.add_field(name=f":first_place: {banks[0][0].display_name}", value=banks[0][1], inline=False)
                else:
                    em.set_footer(text="Nobody here has never earned a penny.")
                    break
            elif i == 1:
                if banks[1][1] > 0:
                    em.add_field(name=f":second_place: {banks[1][0].display_name}", value=banks[1][1], inline=False)
                else:
                    em.set_footer(text="This is all people here who have withdrawn more than nothing")
                    break
            elif i == 2:
                if banks[2][1] > 0:
                    em.add_field(name=f":third_place: {banks[2][0].display_name}", value=banks[2][1], inline=False)
                else:
                    em.set_footer(text="This is all people here who have withdrawn more than nothing")
                    break
            else:
                if banks[i][1] > 0:
                    em.add_field(name=f"{banks[i][0].display_name}", value=banks[i][1], inline=False)
                else:
                    em.set_footer(text="This is all people here who have withdrawn more than nothing")
                    break

        await message.channel.send(embed=em)

    @commands.command(aliases=['am', 'addm'])
    @commands.has_permissions(administrator=True)
    async def addmoney(self, message, amt, member: discord.Member = None):
        if int(amt) > 0 and float(amt) % 1 == 0:
            if member is None:
                member = message.author
            member_data = load_member_data(member, message.guild)
            bal = member_data['bank']
            add_money(member, message.guild, amt)
            bal1 = bal + int(amt)
            em = discord.Embed(title=':white_check_mark: Operation complete!',
                               colour=discord.Color.from_rgb(60, 179, 113))
            em.add_field(name="Recipient", value=member.mention)
            em.add_field(name="Bank", value=":inbox_tray: **{}:coin: --> {}:coin:**".format(bal, bal1))
            await message.channel.send(embed=em)
        else:
            await message.channel.send(":x: **Please enter valid number.**".format(message.author.mention))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removemoney(self, message, amt, member: discord.Member = None):
        if int(amt) > 0 and float(amt) % 1 == 0:
            if member is None:
                member = message.author
            member_data = load_member_data(member, message.guild)
            bal = member_data['bank']
            remove_money(member, message.guild, amt)
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
            if member is None:
                member = message.author
            member_data = load_member_data(member, message.guild)
            bal = member_data['bank']
            set_money(member, message.guild, amt)
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
        member_data = load_member_data(message.author, message.guild)
        if amt != "all":
            if member_data['bank'] >= int(amt) > 0:
                bbal = member_data['bank']
                wbal = member_data['wallet']
                withdraw_money(message.author, message.guild, amt)
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
            if member_data['bank'] > 0:
                bbal = member_data['bank']
                wbal = member_data['wallet']
                withdraw_money(message.author, message.guild, bbal)
                bbal1 = 0
                wbal1 = bbal + wbal

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
        member_data = load_member_data(message.author, message.guild)
        if amt != "all":
            if member_data['wallet'] >= int(amt) > 0:
                bbal = member_data['bank']
                wbal = member_data['wallet']
                deposit_money(message.author, message.guild, int(amt))
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
            if member_data['wallet'] > 0:
                bbal = member_data['bank']
                wbal = member_data['wallet']
                deposit_money(message.author, message.guild, wbal)
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
        if member is None:
            member_data = load_member_data(message.author, message.guild)

            embed = discord.Embed(title=f"{message.author.display_name}'s Balance", colour=message.author.color)
            embed.add_field(name="Wallet balance", value="{}:coin:".format(str(member_data['wallet'])), inline=False)
            embed.add_field(name="Bank balance", value="{}:coin:".format(str(member_data['bank'])))

            await message.channel.send(embed=embed)
        else:
            member_data = load_member_data(member, message.guild)

            embed = discord.Embed(title=f"{member.display_name}'s balance", colour=member.color)
            embed.add_field(name="Wallet balance", value="{}:coin:".format(str(member_data['wallet'])), inline=False)
            embed.add_field(name="Bank balance", value="{}:coin:".format(str(member_data['bank'])))

            await message.channel.send(embed=embed)

    @commands.command()
    async def sendmoney(self, message, amt, member: discord.Member = None):
        author_data = load_member_data(message.author, message.guild)
        member_data = load_member_data(member, message.guild)
        if author_data['bank'] >= int(amt) > 0 and message.author != member:
            abbal = author_data['bank']
            mbbal = member_data['bank']
            send_money(message.author, member, message.guild, amt)
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
            elif int(amt) > author_data['bank']:
                await message.channel.send(":x: **You do not have this amount of coins on your bank account!**")
            else:
                await message.channel.send(":x: **You can not send money to yourself!**")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearmoney(self, message, member: discord.Member = None):
        if member is None:
            member_data = load_member_data(message.author, message.guild)
            member_data['wallet'] = 0
            member_data['bank'] = 0
            save_member_data(member_data, message.author, message.guild)
            await message.channel.send(
                f":white_check_mark: **Cleared {message.author.mention}'s account successfully!**")
        else:
            member_data = load_member_data(member, message.guild)
            member_data['wallet'] = 0
            member_data['bank'] = 0
            save_member_data(member_data, member, message.guild)
            await message.channel.send(f":white_check_mark: **Cleared {member.mention}'s account successfully!**")

    @commands.command()
    async def senditem(self, ctx, quantity, item, member: discord.Member):
        if quantity.isnumeric():
            quantity = int(quantity)
            if quantity > 0:
                member_inventory = load_inventory_data(ctx.author, ctx.guild)
                if not (member_inventory.get(item, None) is None or member_inventory.get(item, None) == 0):
                    if member_inventory[item] >= quantity:
                        send_item(ctx.author, member, ctx.guild, item, quantity)
                        await ctx.channel.send(f"{quantity} {item} sent successfully to {member.mention}!")
                    else:
                        await ctx.channel.send(f"You don't have {item} in this quantity!")
                else:
                    await ctx.channel.send("You don't have this item!")
            else:
                await ctx.channel.send("Enter a **valid** number!")
        else:
            await ctx.channel.send("Enter a **valid** value!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def additem(self, ctx, quantity, item, member: discord.Member = None):
        if quantity.isnumeric():
            quantity = int(quantity)
            if quantity > 0:
                if member is None:
                    member = ctx.author
                add_item(member, ctx.guild, item, quantity)
                await ctx.channel.send(f"{quantity} {item} added successfully to {member.mention} inventory!")
            else:
                await ctx.channel.send("Enter a **valid** number!")
        else:
            await ctx.channel.send("Enter a **valid** value!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeitem(self, ctx, quantity, item, member: discord.Member = None):
        if quantity.isnumeric():
            quantity = int(quantity)
            if quantity > 0:
                if member is None:
                    member = ctx.author
                member_inventory = load_inventory_data(member, ctx.guild)
                if quantity > member_inventory[item]:
                    quantity = member_inventory[item]

                remove_item(member, ctx.guild, item, quantity)
                await ctx.channel.send(f"{quantity} {item} removed successfully from {member.mention} inventory!")
            else:
                await ctx.channel.send("Enter a **valid** number!")
        elif quantity == "all":
            if member is None:
                member = ctx.author
            member_inventory = load_inventory_data(member, ctx.guild)
            quantity = member_inventory[item]

            remove_item(member, ctx.guild, item, quantity)
            await ctx.channel.send(f"All {item} removed successfully from {member.mention} inventory!")
        else:
            await ctx.channel.send("Enter a **valid** value!")

    @commands.command()
    async def inventory(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        member_inventory = load_inventory_data(member, ctx.guild)
        server_data = load_server_data(ctx.guild)
        items = []
        max_items = server_data["max-items-on-page"]
        for i in list(member_inventory.keys()):
            if member_inventory[i] != 0:
                items.append(i)
        items_quantity = len(items)
        pages = math.ceil(items_quantity / max_items)

        arrows = "\u25b6", "\u25c0"

        content = []

        for i in range(pages):
            if items_quantity - i * max_items > max_items or items_quantity - i * max_items == 0:
                em = discord.Embed(title=f'{member.display_name}\'s inventory', description=f'Page {i + 1}/{pages}',
                                   color=ctx.author.color)
                em.set_footer(text=f"Requester: {ctx.author.display_name}")
                for j in items[i * max_items:(i + 1) * max_items]:
                    em.add_field(name=f'{j}', value=f'{member_inventory[j]}',
                                 inline=False)

                content.append(em)
            elif items_quantity - i * max_items in [k for k in range(1, max_items)]:
                em = discord.Embed(title=f'{member.display_name}\'s shop', description=f'Page {i + 1}/{pages}',
                                   color=ctx.author.color)
                em.set_footer(text=f"Requester: {ctx.author.display_name}")
                for j in items[i * max_items:]:
                    em.add_field(name=f'{j}', value=f'{member_inventory[j]}',
                                 inline=False)

                content.append(em)
            else:
                print("Inventory error acquired, HELP!")

        cur_page = 1
        message = await ctx.send(embed=content[0])
        # getting the message object for editing and reacting

        await message.add_reaction(arrows[1])
        await message.add_reaction(arrows[0])

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in arrows
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=30, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == arrows[0] and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == arrows[1] and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=content[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        member_data = load_member_data(member, ctx.guild)
        level = member_data["Level"]

        await ctx.channel.send(f"{member.mention} Your level's {level}")


# activating cog
def setup(bot):
    bot.add_cog(Utils(bot))
