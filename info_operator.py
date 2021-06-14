import json

FILENAME = "data.json"

DEFAULT_DATA = {"DEFAULT_SERVER_INFO":
    {"server-info":
        {"shop": dict(),
         "members": 0,
         "enter-role-id": 836891624398389298
        }
    }, "DEFAULT_MEMBER_INFO":
    {'wallet': 0, 'bank': 0, 'isPlayingRoulette': False, 'lastMessage': None, 'isPlayingHL': False,
     'TotalGamesPlayed': 0,
     'DicesPlayed': 0, 'RoulettesPlayed': 0, 'SlotsPlayed': 0, 'HighLowsPlayed': 0,
     'DailyRewardsCollected': 0, 'WorksCollected': 0,
     'RobAttempts': 0, 'SuccessfulRobberies': 0, 'TimesRobbed': 0, 'TimesSuccessfullyRobbed': 0,
     'TotalRobberyProfit': 0,
     'MoneyWon': 0, 'MoneyLost': 0, 'MoneyWoninDice': 0, 'MoneyLostinDice': 0, 'MoneyWoninSlots': 0,
     'MoneyLostinSlots': 0, 'MoneyWoninHighLow': 0, 'MoneyLostinHighLow': 0, 'MoneyWoninRoulette': 0,
     'MoneyLostinRoulette': 0,
     'MoneyGotfromDailyRewards': 0, 'MoneyGotfromWorkPayments': 0,
     'TimeJoined': 0
     }, "DEFAULT_SHOP_INFO": {
        "banana": [100, 10],
        "pineapple": [200, 5]
        }
}


# data loaders
def load_member_data(member, guild):
    data = load_guild_data(guild)
    if str(member.id) not in data:
        create_default_member_data(member, guild)

        data = load_guild_data(guild)

    return data[str(member.id)]


def load_guild_data(guild):
    data = load_full_data()
    if str(guild.id) not in data:
        create_default_guild_data(guild)

        data = load_full_data()

    return data[str(guild.id)]


def load_full_data():
    with open(FILENAME, 'r') as file:
        data = json.load(file)

    return data


def load_server_data(guild):
    guild_data = load_guild_data(guild)

    if "server-info" not in guild_data:
        create_default_server_data(guild)

        guild_data = load_guild_data(guild)

    return guild_data["server-info"]


def load_shop_data(guild):
    server_info = load_server_data(guild)

    if "shop" not in server_info:
        create_default_shop_data(guild)

        server_info = load_server_data(guild)

    return server_info["shop"]


# data savers
def save_member_data(data, member, guild):
    guild_data = load_guild_data(guild)
    guild_data[str(member.id)] = data
    save_guild_data(guild_data, guild)


def save_guild_data(data, guild):
    full_data = load_full_data()
    full_data[str(guild.id)].update(data)
    save_full_data(full_data)


def save_full_data(full_data):
    with open(FILENAME, 'w') as f:
        json.dump(full_data, f, indent=4)


def save_server_data(server_data, guild):
    guild_data = load_guild_data(guild)
    guild_data["server-info"] = server_data
    save_guild_data(guild_data, guild)


def save_shop_data(shop_data, guild):
    server_data = load_server_data(guild)
    server_data["shop"] = shop_data
    save_server_data(server_data, guild)


# data management
def create_default_member_data(member, guild):
    guild_data = load_guild_data(guild)
    member_data = DEFAULT_DATA["DEFAULT_MEMBER_INFO"]
    guild_data[member.id] = member_data

    save_guild_data(guild_data, guild)


def create_default_guild_data(guild):
    full = load_full_data()
    members = guild.members
    members_amt = 0
    guild_data = DEFAULT_DATA["DEFAULT_SERVER_INFO"]
    guild_data["server-info"]["shop"] = DEFAULT_DATA["DEFAULT_SHOP_INFO"]

    for i in members:
        if not i.bot:
            guild_data[str(i.id)] = DEFAULT_DATA["DEFAULT_MEMBER_INFO"]
            members_amt += 1

    guild_data["server-info"]["members"] = members_amt

    full[str(guild.id)] = guild_data

    save_full_data(full)


def create_default_data():
    save_full_data(dict())


def create_default_server_data(guild):
    guild_data = load_guild_data(guild)

    guild_data["server-info"] = DEFAULT_DATA["DEFAULT_SERVER_INFO"]

    save_guild_data(guild_data, guild)


def remove_guild_data(guild):
    full_data = load_full_data()
    full_data[str(guild.id)] = dict()
    save_full_data(full_data)


def create_default_shop_data(guild):
    server_data = load_server_data(guild)

    server_data["shop"] = DEFAULT_DATA["DEFAULT_SHOP_INFO"]

    save_server_data(server_data, guild)
