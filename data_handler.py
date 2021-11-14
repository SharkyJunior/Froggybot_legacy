import json
import os

# missing data segment managers:
# shop

DATA_FILES = ["config.json", "default-data.json",
              "guild-settings.json", "member-data.json"]


'''
data structure:
-config.json
    # a file that stores a specific imformation for bot eg: TOKEN

-default-data.json
 -DEFAULT_SERVER_INFO
     # specific set of information given to any server Froggy joins
 -DEFAULT_MEMBER_INFO
     # specifis set of information given to any user that joins the server
 -DEFAULT_SHOP_INFO
     # set of inforamtion given to the server about shop

-guild-settings.json
    # a set of settings provided to the server

-member-data.json
 -guild id
  -member id
    # a set of information provided to any member of a specific server

'''


class DataHandler:
    def __init__(self, dataPath):
        if not os.path.exists(dataPath):  # make directory for data if not found
            os.mkdir(dataPath)

        self.dataPath = dataPath

        for f in DATA_FILES:  # if file is missing it'll be automatically created
            if not os.path.exists(self.__getPath(f)):
                with open(self.__getPath(f), "w") as file:
                    json.dump(dict(), f, indent=4)

# region guild-data

    # loads guild data, if not found it'll create default one  
    def load_guild_data(self, guild):
        id = str(guild.id)
        data = self.__load_full_guild_data()

        if id not in data:
            data = self.__create_default_guild_data(guild)

        return data[id]

    # dumps guild data 
    def save_guild_data(self, data, guild):
        full_data = self.__load_full_guild_data()
        full_data[str(guild.id)] = data
        self.__save_full_guild_data(full_data)

    # completely clears guild data and fills it up with default one
    def __create_default_guild_data(self, guild):
        id = str(guild.id)
        data = self.__load_full_guild_data()

        default_data = self.__load_default_data()
        data[id] = default_data["DEFAULT_SERVER_INFO"]

        self.__save_full_guild_data(data)
        return data

    # completely deletes guild data entry in full data
    def __remove_guild_data(self, guild):
        data = self.__load_full_guild_data()
        del data[str(guild.id)]
        self.__save_full_guild_data(data) 

# endregion

# region guild-data file

    # loads the whole file with guild data and returns it as a dictionary
    def __load_full_guild_data(self):
        return self.__load_data_file(DATA_FILES[2])

    # dumps data into the file with guild data
    def __save_full_guild_data(self, data):
        self.__save_data_file(DATA_FILES[2], data)

    # completely clears all data from guild data file and puts there an empty dictionary
    def __create_default_full_guild_data(self):
        self.__save_full_guild_data(dict())

# endregion


# region member-data

    # loads data about a specific member if it's missing it'll be created
    def load_member_data(self, guild, member):
        guild_data = self.__load_guild_member_data(guild)
        id = str(member.id)

        if id not in guild_data:
            guild_data = self.create_default_member_data(guild, member)

        return guild_data[id]
    
    # dumps information about a specific member
    def save_member_data(self, data, guild, member):
        guild_data = self.__load_guild_member_data(guild)
        guild_data[str(member.id)] = data
        self.__save_guild_member_data(guild_data, guild)

    # creates default information for a specific member
    def create_default_member_data(self, guild, member):
        guild_data = self.__load_guild_member_data(guild)
        guild_data[str(member.id)] = self.__load_default_data()["DEFAULT_MEMBER_INFO"]
        self.__save_guild_member_data(guild_data, guild)
        return guild_data

    # completely removees a specific member data
    def remove_member_data(self, guild, member):
        guild_data = self.__load_guild_member_data(guild)
        del guild_data[str(member.id)]
        self.__save_guild_member_data(guild_data, guild)

# endregion


# region guild-data

    # loads guild data, if not found it'll create default one  
    def __load_guild_member_data(self, guild):
        id = str(guild.id)
        data = self.__load_full_member_data()

        if id not in data:
            data = self.__create_default_guild_member_data(guild)

        return data[id]

    # dumps guild data 
    def __save_guild_member_data(self, data, guild):
        full_data = self.__load_full_member_data()
        full_data[str(guild.id)] = data
        self.__save_full_member_data(full_data)

    # completely clears guild data and fills it up with default one
    def __create_default_guild_member_data(self, guild):
        id = str(guild.id)
        data = self.__load_full_member_data()

        data[id] = dict()
        default_data = self.__load_default_data()

        for m in guild.members:
            if not m.bot:
                data[id][str(m.id)] = default_data["DEFAULT_MEMBER_INFO"]

        self.__save_full_member_data(data)
        return data

    # completely deletes guild data entry in full data
    def __remove_guild_member_data(self, guild):
        data = self.__load_full_member_data()
        del data[str(guild.id)]
        self.__save_full_member_data(data) 



#endregion


# region member-data file

    # loads the whole file with member data and returns it as a dictionary
    def __load_full_member_data(self):
        return self.__load_data_file(DATA_FILES[3])

    # dumps data into the file with member data
    def __save_full_member_data(self, data):
        self.__save_data_file(DATA_FILES[3], data)

    # completely clears all data from member data file and puts there an empty dictionary
    def __create_default_full_member_data(self):
        self.__save_full_member_data(dict())

# endregion


# region global

    # loads config file
    def load_config(self):
        return self.__load_data_file(DATA_FILES[0])

    # loads a special data file that contains default values for other data files
    def __load_default_data(self):
        return self.__load_data_file(DATA_FILES[1])

    # dumps data into the file !!USE WITH CAUTION!!
    def __save_data_file(self, filename, data):
        with open(self.__getPath(filename), "w") as f:
            json.dump(data, f, indent=4)

    # loads the whole file and returns it as a dictionary, if file's unreadable it'll be reseted to empty dictionary
    def __load_data_file(self, filename):
        f = open(self.__getPath(filename), "r")
        try:
            data = json.load(f)
            f.close()
            return data
        except json.decoder.JSONDecodeError:
            f.close()

            f = open(self.__getPath(filename), "w")
            json.dump(dict(), f, indent=4)
            f.close()
            return dict()
        finally:
            f.close()

    def __getPath(self, filename):
        return self.dataPath + "/" + filename

# endregion
