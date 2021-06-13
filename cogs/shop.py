from main import *

# initializing cog
class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ready report
    @commands.Cog.listener()
    async def on_ready(self):
        print('Shop is ready')

    @commands.command()
    async def shop(self, message, page):
        pass


# activating cog
def setup(bot):
    bot.add_cog(Shop(bot))