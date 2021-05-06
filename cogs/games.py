import discord
from discord.ext import commands
from random import randint as ri
import random
from main import load_member_data, add_wmoney, remove_wmoney, save_member_data, SLOTS_OPTIONS, rob_money, send_money


# initializing cog
class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Games are ready')

    @commands.command()
    async def dice(self, message, amt=0):
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
                em = discord.Embed(title="**Dice** :game_die:",
                                   description=":inbox_tray: Wallet: {}:coin: --> {}:coin:".format(wallet_money,
                                                                                                   wallet_money + amt),
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Your score",
                             value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
                em.add_field(name="Opponent score",
                             value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
                member_data.MoneyWon += amt
                member_data.MoneyWoninDice += amt
                wallet_money = add_wmoney(message.author, amt)
            elif author_sum > opponent_sum and author_values[0] == author_values[1]:
                em = discord.Embed(title="**Dice** :game_die:",
                                   description=":inbox_tray: Wallet: {}:coin: --> {}:coin: **(Double!)** ".format(
                                       wallet_money, wallet_money + 2 * amt),
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Your score",
                             value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
                em.add_field(name="Opponent score",
                             value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
                member_data.MoneyWon += 2 * amt
                member_data.MoneyWoninDice += 2 * amt
                wallet_money = add_wmoney(message.author, 2 * amt)
            elif author_sum == opponent_sum:
                em = discord.Embed(title="**Dice** :game_die:", description="It's a draw get your money back",
                                   colour=discord.Color.from_rgb(255, 140, 0))
                em.add_field(name="Your score",
                             value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
                em.add_field(name="Opponent score",
                             value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
            elif author_sum < opponent_sum:
                em = discord.Embed(title="**Dice** :game_die:",
                                   description=":outbox_tray: Wallet: {}:coin: --> {}:coin:".format(wallet_money,
                                                                                                    wallet_money - amt),
                                   colour=discord.Color.from_rgb(220, 20, 60))
                em.add_field(name="Your score",
                             value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
                em.add_field(name="Opponent score",
                             value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
                member_data.MoneyLost += amt
                member_data.MoneyLostinDice += amt
                wallet_money = remove_wmoney(message.author, amt)
            else:
                print("smth strange happened")
                print("{} and {} vs {} and {}".format(author_values[0], author_values[1], opponent_values[0],
                                                      opponent_values[1]))

            member_data.wallet = wallet_money
            save_member_data(message.author.id, member_data)

            await message.channel.send(embed=em)

        else:
            if amt <= 0:
                await message.channel.send("Enter a **valid** number")
            else:
                await message.channel.send(":x: **You don't have enough money in your wallet**")

    @commands.command(aliases=["sl"])
    async def slots(self, message, amt=None):
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
            # result = [":gem:", ":gem:", ":gem:"]
            # result = [":cherries:", ":cherries:", ":cherries:"]
            if all([i == result[0] for i in result[1::]]) and result[0] == ":gem:":
                wallet_money = add_wmoney(message.author, 100 * int(amt))
                member_data.MoneyWon += 100 * int(amt)
                member_data.MoneyWoninSlots += 100 * int(amt)
                em = discord.Embed(title=":slot_machine: **MEGA WIN**",
                                   description=f"{result[0]} {result[1]} {result[2]} **100x**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money + 100 * int(amt)}:coin:")
            elif all([i == result[0] for i in result[1::]]) and result[0] == ":cherries:":
                wallet_money = add_wmoney(message.author, 50 * int(amt))
                member_data.MoneyWon += 50 * int(amt)
                member_data.MoneyWoninSlots += 50 * int(amt)
                em = discord.Embed(title=":slot_machine: **HUGE WIN**",
                                   description=f"{result[0]} {result[1]} {result[2]} **50x**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money + 50 * int(amt)}:coin:")
            elif all([i == result[0] for i in result[1::]]):
                wallet_money = add_wmoney(message.author, 20 * int(amt))
                member_data.MoneyWon += 20 * int(amt)
                member_data.MoneyWoninSlots += 20 * int(amt)
                em = discord.Embed(title=":slot_machine: **BINGO**",
                                   description=f"{result[0]} {result[1]} {result[2]} **20x**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money + 20 * int(amt)}:coin:")
            elif result[0] == result[1] or result[0] == result[2] or result[1] == result[2]:
                wallet_money = add_wmoney(message.author, 5 * int(amt))
                member_data.MoneyWon += 5 * int(amt)
                member_data.MoneyWoninSlots += 5 * int(amt)
                em = discord.Embed(title=":slot_machine: **WIN**",
                                   description=f"{result[0]} {result[1]} {result[2]} **5x**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money + 5 * int(amt)}:coin:")
            else:
                wallet_money = remove_wmoney(message.author, int(amt))
                member_data.MoneyLost += int(amt)
                member_data.MoneyLostinSlots += int(amt)
                em = discord.Embed(title=":slot_machine: **LOSS**", description=f"{result[0]} {result[1]} {result[2]}",
                                   colour=discord.Color.from_rgb(220, 20, 60))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {wallet_money}:coin: --> {wallet_money - int(amt)}:coin:")

            member_data.wallet = wallet_money
            save_member_data(message.author.id, member_data)
            await message.channel.send(embed=em)
        elif wallet_money < int(amt):
            await message.channel.send(":x: **You don't have enough money in your wallet!**")

    @commands.command(aliases=['hl'])
    async def highlow(self, message, bet):
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

                msg = await self.bot.wait_for('message', check=check)
                while msg.content not in answers or not check(msg):
                    await message.channel.send(
                        ":x: **I expected something from `high`, `low` or `jackpot`**")
                    msg = await self.bot.wait_for('message', check=check)
                    print(msg.content)
                if answer == "jackpot":
                    member_data.MoneyWon += bet * 10
                    member_data.MoneyWoninHighLow += bet * 10
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

    @commands.command()
    async def rob(self, message, member: discord.Member = None):
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

                    em = discord.Embed(title=":white_check_mark: Robbed {} successfully!".format(member.display_name),
                                       colour=discord.Color.from_rgb(60, 179, 113))

                    em.add_field(name=":moneybag: Robber", value=message.author.mention)
                    em.add_field(name="Victim", value=member.mention)
                    em.add_field(name="Money stolen", value=f"{robamount}:coin:")

                    dm = discord.Embed(title=":exclamation: **You were robbed!!!**",
                                       colour=discord.Color.from_rgb(220, 20, 60))
                    dm.add_field(name=":moneybag: Robber", value=message.author.mention)
                    dm.add_field(name="Money stolen", value=f"{robamount}:coin:")

                    p = await member.create_dm()

                    await p.send(embed=dm)
                    await message.channel.send(embed=em)
                else:
                    author_data.TotalRobberyProfit -= 3 * robamount

                    author_money[0], author_money[1], member_money[0], member_money[1] = send_money(message.author,
                                                                                                    member,
                                                                                                    3 * robamount)

                    em = discord.Embed(title=":man_police_officer: {} was caught!".format(message.author.display_name),
                                       colour=discord.Color.from_rgb(220, 20, 60))

                    em.add_field(name=":moneybag: Robber", value=message.author.mention)
                    em.add_field(name="Victim", value=member.mention)
                    em.add_field(name="Fee", value=f"{robamount * 3}:coin:")

                    dm = discord.Embed(title=":exclamation: **Rob attempt!!!**",
                                       description=f"{message.author.mention} attempted to rob you, but got caught",
                                       colour=discord.Color.from_rgb(220, 20, 60))
                    dm.add_field(name=":moneybag: Robber", value=message.author.mention)
                    dm.add_field(name="Fee", value=f"{robamount * 3}:coin:")

                    p = await member.create_dm()

                    await p.send(embed=dm)
                    await message.channel.send(embed=em)

                member_data.wallet, member_data.bank, author_data.wallet, author_data.bank = member_money[0], \
                                                                                             member_money[1], \
                                                                                             author_money[0], \
                                                                                             author_money[1]
                save_member_data(member.id, member_data)
                save_member_data(message.author.id, author_data)

            else:
                await message.channel.send(f":x: **{member.mention} does not have anything in his wallet.**")
        else:
            if member == None:
                await message.channel.send(":x: **Please write someone to rob))**")
            else:
                await message.channel.send(":x: **You can not rob yourself! :rofl:**")

# activating cog
def setup(bot):
    bot.add_cog(Games(bot))