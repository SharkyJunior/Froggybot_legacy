from main import *

# initializing cog
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation is ready')

    #kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, message, member: discord.Member = None, *, reason='No reason given'):
        if member != None:
            channel = self.bot.get_channel(836955773513760769) #getting admin channel

            em = discord.Embed(title=":leg: **Kicked {}#{}!**".format(member.name, member.discriminator),
                               colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
            em.add_field(name="Reason", value=reason)
            await message.channel.send(embed=em)

            am = discord.Embed(colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
            am.add_field(name="User", value=member.mention)
            am.add_field(name="Moderator", value=message.author.mention)
            am.add_field(name="Reason", value=reason)
            am.add_field(name="Channel", value=message.channel.mention)
            am.set_author(name=f"[KICK] {member.name}#{member.discriminator}", icon_url=member.avatar_url)
            am.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=am)

            dm = discord.Embed(title="You were kicked from {}".format(message.author.guild.name),
                               colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
            dm.add_field(name="Reason", value=reason)
            p = await member.create_dm()

            await p.send(embed=dm)

            await member.kick(reason=reason)
        else:
            await message.channel.send("**:x: You can not kick yourself! :rofl:**")

    # ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, message, member: discord.User, *, reason='No reason given'):
        if member != None:
            channel = self.bot.get_channel(836955773513760769)

            em = discord.Embed(
                title=":man_police_officer::lock: **Banned {}#{}!**".format(member.name, member.discriminator),
                colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
            em.add_field(name="Reason", value=reason)
            await message.channel.send(embed=em)

            am = discord.Embed(colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
            am.add_field(name="User", value=member.mention)
            am.add_field(name="Moderator", value=message.author.mention)
            am.add_field(name="Reason", value=reason)
            am.add_field(name="Channel", value=message.channel.mention)
            am.set_author(name=f"[BAN] {member.name}#{member.discriminator}", icon_url=member.avatar_url)
            am.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=am)

            dm = discord.Embed(
                title=":man_police_officer::lock: You were banned from {}".format(message.author.guild.name),
                colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
            dm.add_field(name="Reason", value=reason)
            p = await member.create_dm()

            await p.send(embed=dm)

            await member.ban(reason=reason)
        else:
            await message.channel.send("**:x: You can not ban yourself! :rofl:**")

    # unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member=""):
        if member != "":
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)

                    channel = self.bot.get_channel(836955773513760769)

                    em = discord.Embed(
                        description=":man_police_officer::unlock: **Unbanned {}#{}!**".format(user.name,
                                                                                              user.discriminator),
                        colour=discord.Color.from_rgb(60, 179, 113), timestamp=datetime.datetime.utcnow())
                    am = discord.Embed(colour=discord.Color.from_rgb(60, 179, 113),
                                       timestamp=datetime.datetime.utcnow())
                    am.add_field(name="User", value=user.mention)
                    am.add_field(name="Moderator", value=ctx.author.mention)
                    am.add_field(name="Channel", value=ctx.channel.mention)
                    am.set_author(name=f"[UNBAN] {user.name}#{user.discriminator}", icon_url=user.avatar_url)
                    am.set_thumbnail(url=user.avatar_url)

                    await ctx.channel.send(embed=em)
                    await channel.send(embed=am)
        else:
            await ctx.channel.send("**:x: You can not unban yourself! :rofl:**")

    # mute command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, message, member: discord.Member, reason='No reason given'):
        if member != None:
            channel = self.bot.get_channel(836955773513760769)

            em = discord.Embed(
                title=f":mute: **Muted {member.name}#{member.discriminator}!**",
                colour=discord.Color.from_rgb(255, 140, 0), timestamp=datetime.datetime.utcnow())
            em.add_field(name="Reason", value=reason)
            await message.channel.send(embed=em)

            am = discord.Embed(colour=discord.Color.from_rgb(255, 140, 0), timestamp=datetime.datetime.utcnow())
            am.add_field(name="User", value=member.mention)
            am.add_field(name="Moderator", value=message.author.mention)
            am.add_field(name="Reason", value=reason)
            am.add_field(name="Channel", value=message.channel.mention)
            am.set_author(name=f"[MUTE] {member.name}#{member.discriminator}", icon_url=member.avatar_url)
            am.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=am)

            dm = discord.Embed(title=":mute: You were muted in {}.".format(message.author.guild.name),
                               colour=discord.Color.from_rgb(255, 140, 0), timestamp=datetime.datetime.utcnow())
            dm.add_field(name="Reason", value=reason)
            p = await member.create_dm()

            await p.send(embed=dm)

            role = get(member.guild.roles, id=836959443970293771)
            await member.add_roles(role, reason=reason)
        else:
            await message.channel.send("**:x: You can not mute yourself! :rofl:**")

    # unmute command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, message, member: discord.Member):
        if member != None:
            channel = self.bot.get_channel(836955773513760769)

            em = discord.Embed(
                title=":speaker: **Unmuted {}#{}!**".format(member.name, member.discriminator),
                colour=discord.Color.from_rgb(60, 179, 113), timestamp=datetime.datetime.utcnow())
            await message.channel.send(embed=em)

            am = discord.Embed(colour=discord.Color.from_rgb(60, 179, 113), timestamp=datetime.datetime.utcnow())
            am.add_field(name="User", value=member.mention)
            am.add_field(name="Moderator", value=message.author.mention)
            am.add_field(name="Channel", value=message.channel.mention)
            am.set_author(name=f"[UNMUTE] {member.name}#{member.discriminator}", icon_url=member.avatar_url)
            am.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=am)

            dm = discord.Embed(title=":speaker: You were unmuted in {}.".format(message.author.guild.name),
                               colour=discord.Color.from_rgb(60, 179, 113), timestamp=datetime.datetime.utcnow())
            p = await member.create_dm()

            await p.send(embed=dm)

            role = get(member.guild.roles, id=836959443970293771)
            await member.remove_roles(role)
        else:
            await message.channel.send("**:x: You can not unmute yourself! :rofl:**")

    # tempmute command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tempmute(self, message, member: discord.Member, time, *, reason='No reason given'):
        if member != None:
            channel = self.bot.get_channel(836955773513760769)

            timesec = to_sec(time)

            if timesec != 'Error':
                em = discord.Embed(
                    title=f":mute: **Muted {member.name}#{member.discriminator}!**",
                    colour=discord.Color.from_rgb(255, 140, 0), timestamp=datetime.datetime.utcnow())
                em.add_field(name="Reason", value=reason)
                em.add_field(name="Duration", value=time)
                await message.channel.send(embed=em)

                am = discord.Embed(colour=discord.Color.from_rgb(255, 140, 0), timestamp=datetime.datetime.utcnow())
                am.add_field(name="User", value=member.mention)
                am.add_field(name="Moderator", value=message.author.mention)
                am.add_field(name="Reason", value=reason)
                am.add_field(name="Channel", value=message.channel.mention)
                am.add_field(name="Duration", value=time)
                am.set_author(name=f"[MUTE] {member.name}#{member.discriminator}", icon_url=member.avatar_url)
                am.set_thumbnail(url=member.avatar_url)
                await channel.send(embed=am)

                dm = discord.Embed(title=":mute: You were muted in {}.".format(message.author.guild.name),
                                   colour=discord.Color.from_rgb(255, 140, 0), timestamp=datetime.datetime.utcnow())
                dm.add_field(name="Reason", value=reason)
                dm.add_field(name="Duration", value=time)
                p = await member.create_dm()

                await p.send(embed=dm)

                role = get(member.guild.roles, id=836959443970293771)
                await member.add_roles(role, reason=reason)
                await asyncio.sleep(timesec)
                await member.remove_roles(role)

                am = discord.Embed(colour=discord.Color.from_rgb(255, 140, 0), timestamp=datetime.datetime.utcnow())
                am.add_field(name="User", value=member.mention)
                am.set_author(name=f"[UNMUTE] {member.name}#{member.discriminator}", icon_url=member.avatar_url)
                am.set_thumbnail(url=member.avatar_url)
                await channel.send(embed=am)

                dm = discord.Embed(title=":speaker: You were unmuted in {}.".format(message.author.guild.name),
                                   colour=discord.Color.from_rgb(60, 179, 113), timestamp=datetime.datetime.utcnow())

                p = await member.create_dm()

                await p.send(embed=dm)
            else:
                await message.channel.send(
                    "**:x: I can not understand this amount of time, check `#help tempmute` for syntax.**")
        else:
            await message.channel.send("**:x: You can not tempmute yourself! :rofl:**")

    # tempban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, message, member: discord.Member, time, *, reason='No reason given'):
        if member != None:
            channel = self.bot.get_channel(836955773513760769)

            timesec = to_sec(time)

            if timesec != 'Error':
                em = discord.Embed(
                    title=":man_police_officer::lock: **Tempbanned {}#{}!**".format(member.name, member.discriminator),
                    colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
                em.add_field(name="Reason", value=reason)
                em.add_field(name="Duration", value=time)
                await message.channel.send(embed=em)

                am = discord.Embed(colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
                am.add_field(name="User", value=member.mention)
                am.add_field(name="Moderator", value=message.author.mention)
                am.add_field(name="Reason", value=reason)
                am.add_field(name="Channel", value=message.channel.mention)
                em.add_field(name="Duration", value=time)
                am.set_author(name=f"[BAN] {member.name}#{member.discriminator}", icon_url=member.avatar_url)
                am.set_thumbnail(url=member.avatar_url)
                await channel.send(embed=am)

                dm = discord.Embed(
                    title=":man_police_officer::lock: You were banned from {}".format(message.author.guild.name),
                    colour=discord.Color.from_rgb(220, 20, 60), timestamp=datetime.datetime.utcnow())
                dm.add_field(name="Reason", value=reason)
                em.add_field(name="Duration", value=time)
                p = await member.create_dm()

                await p.send(embed=dm)

                await member.ban(reason=reason)
                await asyncio.sleep(timesec)

                #starting unbanning process
                banned_users = await message.guild.bans()
                member_name, member_discriminator = member.name, member.discriminator

                for ban_entry in banned_users:
                    user = ban_entry.user

                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        await message.guild.unban(user)

                        channel = self.bot.get_channel(836955773513760769)

                        am = discord.Embed(colour=discord.Color.from_rgb(60, 179, 113),
                                           timestamp=datetime.datetime.utcnow())
                        am.add_field(name="User", value=user.mention)
                        am.set_author(name=f"[UNBAN] {user.name}#{user.discriminator}", icon_url=user.avatar_url)
                        am.set_thumbnail(url=user.avatar_url)

                        await channel.send(embed=am)
            else:
                await message.channel.send(
                    "**:x: I can not understand this amount of time, check `#help tempmute` for syntax.**")
        else:
            await message.channel.send("**:x: You can not tempban yourself! :rofl:**")

    # clear command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, message, num='100'):
        if num == "all":
            await message.channel.purge() # clears channel
            await message.channel.send(f":white_check_mark: **Deleted all messages!**")
        else:
            await message.channel.purge(limit=int(num) + 1) # clears channel
            await message.channel.send(f":white_check_mark: **Deleted {int(num)} messages!**")


# activating cog
def setup(bot):
    bot.add_cog(Moderation(bot))