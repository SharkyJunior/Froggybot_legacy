from main import *


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Setup is ready')

    @commands.command()
    async def setup(self, ctx):
        server_data = load_server_data(ctx.guild)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.channel.send(f"Ok let's setup Froggy on {ctx.guild.name}!")
        await asyncio.sleep(0.5)
        await ctx.channel.send(
            "First, what **role** should be given to user on his join?\n if no role should be given write `no` \n"
            "\n`Please mention a role in this channel`")

        msg = await self.bot.wait_for('message', check=check)

        while True:
            try:
                if msg.content == "no":
                    server_data["enter-role-id"] = "no"
                    await ctx.channel.send("**No** roles will be given to members, when they join")
                    break
                server_data["enter-role-id"] = int(msg.content[3:-1])
                await ctx.channel.send(f"{msg} will be given to members on join")
                break
            except:
                await ctx.channel.send(
                    f":x: Sorry, I could not understand this role, please type it like this: {ctx.author.mention} "
                    f"or `no`")
                msg = await self.bot.wait_for('message', check=check)

        await ctx.channel.send(
            "on-member-join-message, mark server mention with `|`, and member mention with `~`")

        msg = await self.bot.wait_for('message', check=check)

        if msg.content == "no":
            server_data["on-member-join-message"] = "no"
            await ctx.channel.send("**No** on-member-join-message")
        else:
            server_data["on-member-join-message"] = msg.content
            await ctx.channel.send(f"{msg} will be shown to members on join")

        await ctx.channel.send(
            "on-member-join-channel, mark server mention with `|`")

        if server_data["on-member-join-message"] != "no":

            msg = await self.bot.wait_for('message', check=check)

            while True:
                try:
                    server_data["on-member-join-channel"] = int(msg.content[2:-1])
                    await ctx.channel.send(f"{msg} will be given to members on join")
                    break
                except:
                    await ctx.channel.send(
                        f":x: Sorry, I could not understand this channel, please type it like this: {ctx.channel.mention}")
                    msg = await self.bot.wait_for('message', check=check)

        await ctx.channel.send(
            "on-member-join-dm, mark server mention with `|`")

        msg = await self.bot.wait_for('message', check=check)

        if msg.content == "no":
            server_data["on-member-join-dm"] = "no"
            await ctx.channel.send("**No** on-member-join-dm")
        else:
            server_data["on-member-join-dm"] = msg.content
            await ctx.channel.send(f"{msg} will be shown to members on join")

        await ctx.channel.send("No more settings are available")

        save_server_data(server_data, ctx.guild)




# activating cog
def setup(bot):
    bot.add_cog(Setup(bot))
