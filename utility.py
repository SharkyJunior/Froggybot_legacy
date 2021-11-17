from data_handler import *
'''
inventory managment remains umimplemented

def buy_item(member, guild, item, quantity):
    shop_data = load_shop_data(guild)

    remove_money(member, guild, shop_data[item][0]*quantity)
    member_data = add_item(member, guild, item, quantity)

    shop_data[item][1] -= quantity

    save_shop_data(shop_data, guild)

    return member_data


def sell_item(member, guild, item, quantity):
    shop_data = load_shop_data(guild)

    remove_item(member, guild, item, quantity)
    add_money(member, guild, shop_data[item][0]*quantity)

    shop_data[item][1] += quantity
    save_shop_data(shop_data, guild)


def add_item(member, guild, item, quantity):
    member_inventory = load_inventory_data(member, guild)
    if item in member_inventory:
        member_inventory[item] += quantity
    else:
        member_inventory[item] = quantity

    save_inventory_data(member_inventory, member, guild)
    return member_inventory


def remove_item(member, guild, item, quantity):
    member_inventory = load_inventory_data(member, guild)
    if item in member_inventory:
        member_inventory[item] -= quantity
        if member_inventory[item] == 0:
            del member_inventory[item]
    else:
        member_inventory[item] = -quantity

    save_inventory_data(member_inventory, member, guild)
    return member_inventory


def set_item(member, guild, item, quantity):
    member_inventory = load_inventory_data(member, guild)

    member_inventory[item] = quantity

    save_inventory_data(member_inventory, member, guild)
    return member_inventory


def send_item(sender, receiver, guild, item, quantity):
    remove_item(sender, guild, item, quantity)
    add_item(receiver, guild, item, quantity)


def to_sec(time):
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return 'Error'

'''

class Utility:
    def __init__(self, DataPath):
        self.dh = DataHandler(DataPath)

    # adds a specific amount of money (amount can be negative) destination can be either b for bank, or w for wallet
    def change(self, member, guild, amount, destination="b"):
        member_data = self.dh.load_member_data(guild, member)
        if destination == "b":
            if member_data["bank"] < amount:
                amount = member_data["bank"]

            member_data["bank"] += amount
            self.dh.save_member_data(member_data, guild, member)

            return member_data["bank"]
        elif destination == "w":
            if member_data["wallet"] < amount:
                amount = member_data["wallet"]

            member_data["wallet"] += amount
            self.dh.save_member_data(member_data, guild, member)

            return member_data["wallet"]


    # sets money to a specifc amount destination can be either b for bank, or w for wallet 
    def set(self, member, guild, amount, destination="b"):
        member_data = self.dh.load_member_data(guild, member)
        if destination == "b":
            member_data["bank"] = amount
            self.dh.save_member_data(member_data, guild, member)

            return member_data["bank"]
        elif destination == "w":
            member_data["wallet"] = amount
            self.dh.save_member_data(member_data, guild, member)

            return member_data["wallet"]

    
    # withdraws or deposits money from your bank account  selected operation is determined with destination parameter (b for deposit, w for withdrawal)
    def transfer(self, member, guild, amount, destination="b"):
        tax = self.dh.load_config()["DEPOSITION-TAX"]
        member_data = self.dh.load_member_data(guild, member)
        if destination == "b":
            if member_data["wallet"] < amount:
                amount = member_data["wallet"]
            
            member_data["bank"] += amount * (1 - tax)
            member_data["wallet"] -= amount

        elif destination == "w":
            if member_data["bank"] < amount:
                amount = member_data["bank"]
            
            member_data["wallet"] += amount
            member_data["bank"] -= amount


        self.dh.save_member_data(member_data, guild, member)
    

    # removes a specific amount of money from sender's source of money, and adds it to receiver's destination
    def send(self, sender, receiver, guild, amount, destination="b", source="b"):
        sender_data = self.dh.load_member_data(guild, sender)

        temp = 0

        if source == "b":
            if sender_data["bank"] < amount:
                temp = amount - sender_data["bank"]
                amount = sender_data["bank"]

        if source == "w":
            if sender_data["wallet"] < amount:
                temp = amount - sender_data["wallet"]
                amount = sender_data["wallet"]

        self.change(receiver, guild, amount + temp, destination)
        self.change(sender, guild, -amount, source)
        self.change(sender, guild, -temp, "b" if source == "w" else "w")

