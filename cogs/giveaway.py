from main import *

# initializing cog
class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Giveaway is ready')

    # commands
    @commands.command(aliases=['gstart', 'gs', 'giveaway-start'])
    @commands.has_permissions(manage_messages=True)
    async def giveaway_start(self, message, time, winners, channel: discord.TextChannel = None, *, prize=''):
        time = to_sec(time)
        if time != "Error" and channel != None and prize != '':
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
            users.pop(users.index(self.bot.user))
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

    @commands.command(aliases=['gsetup', 'giveaway-setup'])
    @commands.has_permissions(manage_messages=True)
    async def giveaway_setup(self, message):
        def check(m):
            return m.author == message.author and m.channel == message.channel

        await message.channel.send(":tada: Ok, now let's setup your giveaway!")
        await asyncio.sleep(0.5)
        await message.channel.send(
            ":tada: First, what **channel** should the giveaway be hosted in?\n\n`Please mention a channel in this server`")

        msg = await self.bot.wait_for('message', check=check)

        while True:
            try:
                channel_id = int(msg.content[2:-1])
                break
            except:
                await message.channel.send(
                    f":x: Sorry, I could not understand this channel, please type it like this: {message.channel.mention}")
                msg = await self.bot.wait_for('message', check=check)
        print(channel_id)
        channel = self.bot.get_channel(channel_id)
        await message.channel.send(f":tada: Sweet! The giveaway will be hosted in {channel.mention}.")
        await asyncio.sleep(0.5)
        await message.channel.send(
            ":tada: **How long** will the giveaway stay?\n\n`Please type the amount of time (s|m|h|d)`")

        msg = await self.bot.wait_for('message', check=check)

        time = to_sec(msg.content)

        while time == "Error":
            await message.channel.send(
                f":x: Sorry, I could not understand this amount of time, please type it like this: `10m`, `3h`, `2d`")
            msg = await self.bot.wait_for('message', check=check)
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

        msg = await self.bot.wait_for('message', check=check)

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
                msg = await self.bot.wait_for('message', check=check)

        if winners == 1:
            await message.channel.send(f':tada: Neat! There will be only **{winners} winner**')
        else:
            await message.channel.send(f':tada: Neat! There will be **{winners} winners**')

        await asyncio.sleep(0.5)
        await message.channel.send(
            ":tada: And last question, what are you giveawaying?\n\n`Please type the prize`")

        msg = await self.bot.wait_for('message', check=check)

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

        await channel.send('@everyone')
        msg = await channel.send(embed=embed)
        await msg.add_reaction("🎉")
        print(time)
        while time > 0:
            await asyncio.sleep(5)
            time -= 5
            em = discord.Embed(title=":tada: Giveaway!", description=f'**{prize}**\nReact with :tada: to enter!',
                               color=message.author.color, timestamp=endtime)
            em.add_field(name="Host", value=message.author.mention)
            em.add_field(name="Time remaining",
                         value=f'{time // 86400}d {time % 86400 // 3600}h {time % 86400 % 3600 // 60}m {time % 60}s')
            em.set_footer(text=f"Ends at ")
            await msg.edit(embed=em)

        endmsg = await channel.fetch_message(msg.id)

        users = await endmsg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
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


# activating cog
def setup(bot):
    bot.add_cog(Giveaway(bot))