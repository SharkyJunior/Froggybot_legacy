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
    async def buy(self, ctx, quantity, item):
        if quantity.isnumeric():
            quantity = int(quantity)
            if quantity > 0:
                shop_data = load_shop_data(ctx.guild)
                member_data = load_member_data(ctx.author, ctx.guild)
                if item in shop_data:
                    if shop_data[item][1] >= quantity:
                        if shop_data[item][0]*quantity <= member_data["bank"]:
                            buy_item(ctx.author, ctx.guild, item, quantity)
                            await ctx.channel.send(f"You successfully bought {quantity} {item}!")

                        else:
                            await ctx.channel.send("You don't have this amount of money")
                    else:
                        await ctx.channel.send("Item isn't present in such quantity!")
                else:
                    await ctx.channel.send("No such an item in shop!")
            else:
                await ctx.channel.send("Enter a **valid** number!")
        else:
            await ctx.channel.send("Enter a **valid** value!")

    @commands.command()
    async def sell(self, ctx, quantity, item):
        if quantity.isnumeric():
            quantity = int(quantity)
            if quantity > 0:
                member_inventory = load_inventory_data(ctx.author, ctx.guild)
                if item in member_inventory:
                    if member_inventory[item] >= quantity:
                        sell_item(ctx.author, ctx.guild, item, quantity)
                        await ctx.channel.send(f"You successfully sold {quantity} {item}!")

                    else:
                        await ctx.channel.send("Item isn't present in such quantity!")
                else:
                    await ctx.channel.send("No such an item in your inventory!")
            else:
                await ctx.channel.send("Enter a **valid** number!")
        else:
            await ctx.channel.send("Enter a **valid** value!")

    @commands.command()
    async def shop(self, ctx):
        shop_data = load_shop_data(ctx.guild)
        lots = []
        for i in list(shop_data.keys()):
            if shop_data[i][1] != 0:
                lots.append(i)
        lots_quantity = len(lots)
        pages = math.ceil(lots_quantity/4)

        arrows = "\u25b6", "\u25c0"

        content = []

        for i in range(pages):
            if lots_quantity - i*4 > 4 or lots_quantity - i*4 == 0:
                page_content = ""
                for j in lots[i*4:(i+1)*4]:
                    page_content += f"{j} - quantity: {shop_data[j][1]}, price: {shop_data[j][0]}:coin:\n"
                content.append(page_content)
            elif lots_quantity - i*4 in [1, 2, 3]:
                page_content = ""
                for j in lots[i*4:]:
                    page_content += f"{j} - quantity: {shop_data[j][1]}, price: {shop_data[j][0]}:coin:\n"
                content.append(page_content)
            else:
                print("Error acquired, HELP!")

        cur_page = 1
        message = await ctx.send(f"Page {cur_page}/{pages}:\n{content[cur_page-1]}")
        # getting the message object for editing and reacting

        await message.add_reaction(arrows[1])
        await message.add_reaction(arrows[0])

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in arrows
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == arrows[0] and cur_page != pages:
                    cur_page += 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{content[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == arrows[1] and cur_page > 1:
                    cur_page -= 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{content[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds

# activating cog
def setup(bot):
    bot.add_cog(Shop(bot))
