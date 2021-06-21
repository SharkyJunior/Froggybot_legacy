from main import *

SLOTS_OPTIONS = [":watch:", ":bulb:", ":yo_yo:", ":paperclip:", ":cd:", ":dvd:", ":mag_right:", ":amphora:",
                 ":ringed_planet:", ":gem:", ":rugby_football:", ":nut_and_bolt:", ":lemon:", ":package:",
                 ":crystal_ball:", ":cherries:", ":video_game:", ":tickets:"]


# initializing cog
class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Games are ready')

    # commands
    @commands.command()
    async def dice(self, message, amt=0):
        member_data = load_member_data(message.author, message.guild)
        wallet_money = member_data['wallet']
        amt = int(amt)
        if wallet_money >= amt > 0:
            member_data['DicesPlayed'] += 1
            member_data['TotalGamesPlayed'] += 1
            author_values = [random.randint(1, 6), random.randint(1, 6)]
            opponent_values = [random.randint(1, 6), random.randint(1, 6)]
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
                member_data['MoneyWon'] += amt
                member_data['MoneyWoninDice'] += amt
                wallet_money = add_wmoney(message.author, message.guild, amt)
            elif author_sum > opponent_sum and author_values[0] == author_values[1]:
                em = discord.Embed(title="**Dice** :game_die:",
                                   description=":inbox_tray: Wallet: {}:coin: --> {}:coin: **(Double!)** ".format(
                                       wallet_money, wallet_money + 2 * amt),
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Your score",
                             value="{}:game_die: and {}:game_die:".format(author_values[0], author_values[1]))
                em.add_field(name="Opponent score",
                             value="{}:game_die: and {}:game_die:".format(opponent_values[0], opponent_values[1]))
                member_data['MoneyWon'] += 2 * amt
                member_data['MoneyWoninDice'] += 2 * amt
                wallet_money = add_wmoney(message.author, message.guild, 2 * amt)
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
                member_data['MoneyLost'] += amt
                member_data['MoneyLostinDice'] += amt
                wallet_money = remove_wmoney(message.author, message.guild, amt)
            else:
                print("smth strange happened")
                print("{} and {} vs {} and {}".format(author_values[0], author_values[1], opponent_values[0],
                                                      opponent_values[1]))

            member_data['wallet'] = wallet_money
            save_member_data(member_data, message.author, message.guild)

            await message.channel.send(embed=em)

        else:
            if amt <= 0:
                await message.channel.send("Enter a **valid** number")
            else:
                await message.channel.send(":x: **You don't have enough money in your wallet**")

    @commands.command(aliases=["sl"])
    async def slots(self, message, amt=None):
        member_data = load_member_data(message.author, message.guild)
        if amt is None or int(amt) <= 0:
            await message.channel.send(":x: **Enter a valid number!**")
            return
        if member_data['wallet'] >= int(amt) > 0:
            member_data["TotalGamesPlayed"] += 1
            member_data["SlotsPlayed"] += 1
            result = [random.choice(SLOTS_OPTIONS) for i in range(3)]
            # result = [":gem:", ":gem:", ":gem:"]
            # result = [":cherries:", ":cherries:", ":cherries:"]
            if all([i == result[0] for i in result[1::]]) and result[0] == ":gem:":
                add_wmoney(message.author, message.guild, 100 * int(amt))
                member_data['wallet'] = load_member_data(message.author, message.guild)['wallet']
                member_data['MoneyWon'] += 100 * int(amt)
                member_data['MoneyWoninSlots'] += 100 * int(amt)
                em = discord.Embed(title=":slot_machine: **MEGA WIN**",
                                   description=f"{result[0]} {result[1]} {result[2]} **100x**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {member_data['wallet'] - 100 * int(amt)}:coin: --> {member_data['wallet']}:coin:")
            elif all([i == result[0] for i in result[1::]]) and result[0] == ":cherries:":
                add_wmoney(message.author, message.guild, 50 * int(amt))
                member_data['wallet'] = load_member_data(message.author, message.guild)['wallet']
                member_data['MoneyWon'] += 50 * int(amt)
                member_data['MoneyWoninSlots'] += 50 * int(amt)
                em = discord.Embed(title=":slot_machine: **HUGE WIN**",
                                   description=f"{result[0]} {result[1]} {result[2]} **50x**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {member_data['wallet'] - 50 * int(amt)}:coin: --> {member_data['wallet']}:coin:")
            elif all([i == result[0] for i in result[1::]]):
                add_wmoney(message.author, message.guild, 20 * int(amt))
                member_data['wallet'] = load_member_data(message.author, message.guild)['wallet']
                member_data['MoneyWon'] += 20 * int(amt)
                member_data['MoneyWoninSlots'] += 20 * int(amt)
                em = discord.Embed(title=":slot_machine: **BINGO**",
                                   description=f"{result[0]} {result[1]} {result[2]} **20x**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {member_data['wallet'] - 20 * int(amt)}:coin: --> {member_data['wallet']}:coin:")
            elif result[0] == result[1] or result[0] == result[2] or result[1] == result[2]:
                add_wmoney(message.author, message.guild, 5 * int(amt))
                member_data['wallet'] = load_member_data(message.author, message.guild)['wallet']
                member_data['MoneyWon'] += 5 * int(amt)
                member_data['MoneyWoninSlots'] += 5 * int(amt)
                em = discord.Embed(title=":slot_machine: **WIN**",
                                   description=f"{result[0]} {result[1]} {result[2]} **5x**",
                                   colour=discord.Color.from_rgb(60, 179, 113))
                em.add_field(name="Wallet",
                             value=f":inbox_tray: {member_data['wallet'] - 5 * int(amt)}:coin: --> {member_data['wallet']}:coin:")
            else:
                remove_wmoney(message.author, message.guild, int(amt))
                member_data['wallet'] = load_member_data(message.author, message.guild)['wallet']
                member_data['MoneyLost'] += int(amt)
                member_data['MoneyLostinSlots'] += int(amt)
                em = discord.Embed(title=":slot_machine: **LOSS**", description=f"{result[0]} {result[1]} {result[2]}",
                                   colour=discord.Color.from_rgb(220, 20, 60))
                em.add_field(name="Wallet",
                             value=f":outbox_tray: {member_data['wallet'] + int(amt)}:coin: --> {member_data['wallet']}:coin:")

            member_data['wallet'] = load_member_data(message.author, message.guild)['wallet']
            save_member_data(member_data, message.author, message.guild)
            await message.channel.send(embed=em)
        elif member_data['wallet'] < int(amt):
            await message.channel.send(":x: **You don't have enough money in your wallet!**")

    @commands.command(aliases=['hl'])
    async def highlow(self, message, bet):
        member_data = load_member_data(message.author, message.guild)
        if not member_data['isPlayingHL']:
            member_data['isPlayingHL'] = True
            save_member_data(member_data, message.author, message.guild)
            bet = int(bet)
            wallet_bal = member_data['wallet']
            if wallet_bal >= bet > 0:
                member_data['TotalGamesPlayed'] += 1
                member_data['HighLowsPlayed'] += 1
                secret = random.randint(0, 100)
                hint = random.randint(40, 60)
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
                while msg.content not in answers or not check(msg):  # waiting for appropriate answer
                    await message.channel.send(
                        ":x: **I expected something from `high`, `low` or `jackpot`**")
                    msg = await self.bot.wait_for('message', check=check)
                if answer == "jackpot" and msg.content.lower() == answer:
                    member_data['MoneyWon'] += bet * 10
                    member_data['MoneyWoninHighLow'] += bet * 10
                    em = discord.Embed(title="You won!",
                                       description=f"The hint was **{hint}**, and the number was **{secret}**",
                                       colour=discord.Color.from_rgb(60, 179, 113))
                    em.add_field(name="Wallet",
                                 value=f":inbox_tray:**{wallet_bal}:coin: --> {wallet_bal + int(10 * bet)}:coin: (Jackpot!!!)**")
                    member_data['wallet'] += int(10 * bet)
                    member_data['isPlayingHL'] = False
                    save_member_data(member_data, message.author, message.guild)
                    await message.channel.send(embed=em)
                elif msg.content.lower() == answer:
                    member_data['MoneyWon'] += bet
                    member_data['MoneyWoninHighLow'] += bet
                    em = discord.Embed(title="You won!",
                                       description=f"The hint was **{hint}**, and the number was **{secret}**",
                                       colour=discord.Color.from_rgb(60, 179, 113))
                    em.add_field(name="Wallet",
                                 value=f":inbox_tray:**{wallet_bal}:coin: --> {wallet_bal + bet}:coin:**")
                    member_data['wallet'] += bet
                    member_data['isPlayingHL'] = False
                    save_member_data(member_data, message.author, message.guild)
                    await message.channel.send(embed=em)
                else:
                    member_data['MoneyLost'] += bet
                    member_data['MoneyLostinHighLow'] += bet
                    em = discord.Embed(title="You lost!",
                                       description=f"The hint was **{hint}**, and the number was **{secret}**",
                                       colour=discord.Color.from_rgb(220, 20, 60))
                    em.add_field(name="Wallet",
                                 value=f":inbox_tray:**{wallet_bal}:coin: --> {wallet_bal - bet}:coin:**")
                    member_data['wallet'] -= bet
                    member_data['isPlayingHL'] = False
                    save_member_data(member_data, message.author, message.guild)
                    await message.channel.send(embed=em)
            else:
                if bet < 0:
                    await message.channel.send(":x: **Enter a valid number!**")
                else:
                    await message.channel.send(":x: **You don't have enough money in your wallet!**")
        else:
            member_data['isPlayingHL'] = False
            save_member_data(member_data, message.author, message.guild)
            pass

    @commands.command(aliases=['rt'])
    async def roulette(self, ctx, amt, loaded_rounds):
        if amt.isnumeric() and loaded_rounds.isnumeric():
            amt = int(amt)
            loaded_rounds = int(loaded_rounds)
            if amt > 0 and loaded_rounds > 0:
                member_data = load_member_data(ctx.author, ctx.guild)
                member_wallet = member_data["wallet"]
                if amt <= member_wallet and loaded_rounds < 6:
                    if not member_data["isPlayingRoulette"]:
                        member_data["isPlayingRoulette"] = True
                        total_won = 0
                        chamber = [True for i in range(loaded_rounds)] + [False for i in range(6-loaded_rounds)]

                        def stop_roulette(context, amount, mw, md):
                            mw += amount
                            md["isPlayingRoulette"] = False

                            md["TotalGamesPlayed"] += 1
                            md["RoulettesPlayed"] += 1

                            md["wallet"] = mw
                            save_member_data(md, context.author, context.guild)

                        if not random.choice(chamber):
                            total_won += int(amt * ROULETTE_MULTIPLIER * (loaded_rounds/2))

                            em = discord.Embed(title=":gun: Roulette",
                                               description=":hot_face: **You survived!**",
                                               colour=discord.Color.from_rgb(60, 179, 113))
                            em.add_field(name=":moneybag: Prize", value=f"{total_won}:coin:")
                            em.add_field(name="Next prize",
                                         value=f"{total_won + int(total_won * ROULETTE_MULTIPLIER * (loaded_rounds / 2))}:coin:",
                                         inline=False)
                            em.add_field(name="Actions", value="`continue` or `stop`")

                            await ctx.channel.send(embed=em)

                            def check(m):
                                return ctx.author == m.author

                            while True:
                                msg = await self.bot.wait_for('message', check=check)
                                while msg.content not in ['continue', 'stop'] or not check(msg):
                                    await ctx.channel.send(":x: **I expected something from `continue` or `stop`**")
                                    msg = await self.bot.wait_for('message', check=check)

                                if msg.content == "continue":
                                    if not random.choice(chamber):
                                        total_won += int(total_won * ROULETTE_MULTIPLIER * (loaded_rounds/2))

                                        em = discord.Embed(title=":gun: Roulette",
                                                           description=":hot_face: **You survived!**",
                                                           colour=discord.Color.from_rgb(60, 179, 113))
                                        em.add_field(name=":moneybag: Prize", value=f"{total_won}:coin:")
                                        em.add_field(name="Next prize",
                                                     value=f"{total_won + int(total_won * ROULETTE_MULTIPLIER * (loaded_rounds/2))}:coin:", inline=False)
                                        em.add_field(name="Actions", value="`continue` or `stop`")

                                        await ctx.channel.send(embed=em)
                                    else:
                                        em = discord.Embed(title=":gun: Roulette",
                                                           description=":skull_crossbones: **You lost!**",
                                                           colour=discord.Color.from_rgb(220, 20, 60))
                                        em.add_field(name="Wallet",
                                                     value=":outbox_tray: Wallet: {}:coin: --> {}:coin:".format(
                                                         member_wallet,
                                                         member_wallet - int(amt)))

                                        await ctx.channel.send(embed=em)

                                        member_data['MoneyLost'] += amt
                                        member_data['MoneyLostinRoulette'] += amt
                                        stop_roulette(ctx, -amt, member_wallet, member_data)
                                        break
                                elif msg.content == "stop":
                                    em = discord.Embed(title=":gun: Roulette", description=":no_good: You exited!",
                                                       colour=discord.Color.from_rgb(60, 179, 113))
                                    em.add_field(name="Wallet",
                                                 value=":inbox_tray: {}:coin: --> {}:coin:".format(member_wallet,
                                                                                                   member_wallet +
                                                                                                   total_won))

                                    await ctx.channel.send(embed=em)

                                    member_data['MoneyWon'] += total_won
                                    member_data['MoneyWoninRoulette'] += total_won
                                    stop_roulette(ctx, total_won, member_wallet, member_data)
                                    break
                        else:
                            em = discord.Embed(title=":gun: Roulette", description=":skull_crossbones: **You lost!**",
                                               colour=discord.Color.from_rgb(220, 20, 60))
                            em.add_field(name="Wallet",
                                         value=":outbox_tray: Wallet: {}:coin: --> {}:coin:".format(member_wallet,
                                                                                                    member_wallet - int(
                                                                                                        amt)))
                            member_data['MoneyLost'] += amt
                            member_data['MoneyLostinRoulette'] += amt
                            stop_roulette(ctx, -amt, member_wallet, member_data)
                            await ctx.channel.send(embed=em)
                    else:
                        await ctx.channel.send("You are already playing roulette!")
                else:
                    await ctx.channel.send("You don't have such an amount of money in your wallet!")
            else:
                await ctx.channel.send("Enter **valid** numbers!")
        else:
            await ctx.channel.send("Enter **valid** values!")

    @commands.command()
    async def rob(self, message, member: discord.Member = None):
        if member is not None and member != message.author:
            author_data = load_member_data(message.author, message.guild)
            member_data = load_member_data(member, message.guild)
            print("loading info")
            author_money = [author_data['wallet'], author_data['bank']]
            member_money = [member_data['wallet'], member_data['bank']]
            mwbal = member_data['wallet']
            if mwbal > 0:
                author_data['RobAttempts'] += 1
                member_data['TimesRobbed'] += 1

                robamount = random.randint(int(0.1 * mwbal), int(0.3 * mwbal))
                robchance = random.randint(25, 50)
                result = random.randint(0, 100)
                if result < robchance:
                    member_money[0], author_money[0] = rob_money(message.author, member, message.guild, robamount)
                    author_data['SuccessfulRobberies'] += 1
                    member_data['TimesSuccessfullyRobbed'] += 1
                    author_data['TotalRobberyProfit'] += robamount

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
                    author_data['TotalRobberyProfit'] -= 3 * robamount

                    author_money[0], author_money[1], member_money[0], member_money[1] = send_money(message.author,
                                                                                                    member,
                                                                                                    message.guild,
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

                member_data['wallet'], member_data['bank'], author_data['wallet'], author_data['bank'] = member_money[0], \
                                                                                             member_money[1], \
                                                                                             author_money[0], \
                                                                                             author_money[1]
                save_member_data(member_data, member, message.guild)
                save_member_data(author_data, message.author, message.guild)

            else:
                await message.channel.send(f":x: **{member.mention} does not have anything in his wallet.**")
        else:
            if member is None:
                await message.channel.send(":x: **Please write someone to rob))**")
            else:
                await message.channel.send(":x: **You can not rob yourself! :rofl:**")

# activating cog
def setup(bot):
    bot.add_cog(Games(bot))