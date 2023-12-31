import discord
from random import randint
from replit import db
from discord.ext import commands


def returnItemBonusDict(valueDict, stat):
    te = ""
    valueDict = dict(valueDict)
    valueDict = dict(valueDict[stat])

    for key, value in valueDict.items():
        if value > 0:
            te += "[" + key + ": +" + str(value) + "] "
        elif value < 0:
            te += "[" + key + ": " + str(value) + "] "
        if list(valueDict.keys())[-1] != key:
            te += " "
    return te


def returnItemBonusBar(valueDict, stat):
    te = ""
    valueDict = dict(valueDict)
    bonuses = dict(valueDict["Item Bonuses"])
    if stat == "HP":
        conBonus = dict(bonuses["Con"])
        if len(conBonus) != 0:
            val = 0
            for value in conBonus.values():
                val += value
            te = " [ Item Bonus: " + str(
                (val + valueDict["Con"]) * 10) + "/" + str(
                    (val + valueDict["Con"]) * 10) + " ]"
    elif stat == "MP" or stat == "EP":
        wisBonus = dict(bonuses["Wis"])
        if len(wisBonus) != 0:
            val = 0
            for value in wisBonus.values():
                val += value
            te = " [ Item Bonus: " + str(
                (val + valueDict["Wis"]) * 5) + "/" + str(
                    (val + valueDict["Wis"]) * 5) + " ]"
    return te


def returnCharacterRank(valueDict):

    value = valueDict["Str"] + valueDict["Con"] + valueDict["Dex"] + valueDict[
        "Agi"] + valueDict["Per"] + valueDict["Int"] + valueDict["Wis"]
    thresholds = {
        10: "F-",
        25: "F",
        35: "F+",
        55: "D-",
        125: "D",
        200: "D+",
        860: "C-",
        1060: "C",
        2200: "C+",
        3440: "B-",
        6000: "B",
        9000: "B+",
        125000: "A-",
        160000: "A",
        206000: "A+",
        250800: "S-",
        311400: "S",
        382000: "S+",
        447600: "S++",
        584070: "S+++",
        700000: "SS-",
        858000: "SS",
        970000: "SS+",
        1021000: "SS++",
        1236000: "SS+++",
        1480000: "SSS-",
        1884500: "SSS",
        2440500: "SSS+",
        3040200: "SSS++",
        3956000: "SSS+++",
        4100000: "X-",
        5380900: "X",
        6815000: "X+"
    }
    for key2, value2 in thresholds.items():
        if value <= key2:
            rank = value2
            break
        else:
            pass
    return rank


def returnSkills(valueDict):
    string = ""
    if len(valueDict["Skills"].keys()) > 0:
        for key, value in valueDict["Skills"].items():
            skillThresholds = {
                0: "Unskilled ",
                15: "Novice ",
                30: "Apprentice ",
                50: "Journeyman ",
                65: "Adept ",
                80: "Minor ",
                95: "Major ",
                110: "Expert ",
                125: "Master ",
                140: "Grandmaster ",
                180: "Legendary ",
                200: "Ascendant ",
                250: "Transcendent ",
                400: "Eminent ",
                401: "Peerless "
            }
            sinVirtThresholds = {
                25: "",
                50: "Knight of ",
                75: "Lord of ",
                100: "Baron of ",
                125: "Viscount of ",
                150: "Count of ",
                175: "Earl of ",
                200: "Marquis of ",
                225: "Duke of ",
                250: "King of ",
                275: "Emperor of ",
                300: "Dominion of ",
                325: "Symbol of ",
                350: "Incarnation of ",
                375: "Soulborne of ",
                400: "Embodiment of ",
                401: "Epitome of "
            }
            sinVirts = [
                "Lust", "Gluttony", "Greed", "Pride", "Wrath", "Sloth", "Envy",
                "Justice", "Bravery", "Charity", "Kindness", "Patience",
                "Hope", "Faith"
            ]
            namePrefix = ""
            if key in sinVirts:
                for key2, value2 in sinVirtThresholds.items():
                    if value <= key2:
                        namePrefix = value2
                        break
                    else:
                        pass

            else:
                if value == 400:
                    namePrefix = "Peerless "
                else:
                    value3 = value % 400
                    for key2, value2 in skillThresholds.items():
                        if value3 < key2:
                            namePrefix = value2
                            break
                        elif value3 >= key2:
                            pass
            string += namePrefix
            string += key + " " + str(value)
            if list(valueDict["Skills"].keys())[-1] != key:
                string += ", "
    else:
        string = "None yet."
    return string


def int_to_Roman(num):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = [
        "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num


def properTitle(inp):
    inp = inp.split(" ")
    inp[0] = inp[0].capitalize()
    inp[-1] = inp[-1].capitalize()
    n = 1
    for i in inp[1:-1]:
        if i.lower() not in ("in", "for", "of", "a", "an", "and", "on", "the"):
            inp[n] = i.capitalize()
        n += 1
    ret = ""
    for i in inp:
        ret += i + " "
    ret = ret.strip()
    return ret


def returnAbilities(valueDict):
    string = ""
    if len(valueDict["Abilities"].keys()) > 0:
        for key, value in valueDict["Abilities"].items():
            string += key + " " + int_to_Roman(value)
            if list(valueDict["Abilities"].keys())[-1] != key:
                string += ", "
    else:
        string = "None yet."
    return string


def returnEnergies(valueDict):
    string = ""
    if len(valueDict["Energies"].keys()) > 0:
        energies = dict(valueDict["Energies"])
        for key, value in energies.items():
            string += "\n**" + key + "**: " + str(value[0]) + "/" + str(
                value[1])
            if (key == "MP" or key == "EP"):
                string += returnItemBonusBar(valueDict, key)

    else:
        string = "\nNo magic."
    return string


def returnMoney(valueDict):
    string = ""
    if len(valueDict["Currencies"].keys()) > 0:
        for key, value in valueDict["Currencies"].items():
            string += "\n" + key + ": " + str(value)
    else:
        string = "No money."
    return string


class CharacterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-character",
                 pass_context=True,
                 aliases=["create-c", "Create-Character", "Create-character"])
    @commands.has_permissions(moderate_members=True)
    async def createCharacter(self, ctx, name="", race="", sinVirtue=""):
        con = randint(11, 30)
        wis = randint(11, 30)
        if name == "":
            await ctx.send("Please enter a name.")
            return
        name = name.title()
        if name in db[str(ctx.guild.id)].keys():
            await ctx.send("Character already exists here.")
            return
        if race == "":
            await ctx.send("Please enter a race.")
            return
        if sinVirtue != "":
            startingTitle = race.title() + " of " + sinVirtue.title()
        else:
            startingTitle = race.title()
        race = race.title()
        playerDict = {
            "Name": name,
            "Race": race,
            "Sin/Virtue": sinVirtue,
            "Str": randint(11, 30),
            "Con": con,
            "Dex": randint(11, 30),
            "Agi": randint(11, 30),
            "Per": randint(11, 30),
            "Int": randint(11, 30),
            "Wis": wis,
            "Current HP": con * 10,
            "Max HP": con * 10,
            "Energies": {
                "MP": [wis * 5, wis * 5]
            },
            "Titles": [startingTitle],
            "Skills": {},
            "Abilities": {},
            "Item Bonuses": {
                "Str": {},
                "Con": {},
                "Dex": {},
                "Agi": {},
                "Per": {},
                "Int": {},
                "Wis": {}
            },
            "Currencies": {}
        }
        db[str(ctx.guild.id)][name.title()] = playerDict
        temp = db[str(ctx.guild.id)][name]
        bonuses = temp["Item Bonuses"]
        playerDict.update({
            "Stat String":
            ("**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"]) +
             returnEnergies(temp) + "\n\n**Str**: " + str(temp["Str"]) + " " +
             returnItemBonusDict(bonuses, "Str") + "\n**Con**: " +
             str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") +
             "\n**Dex**: " + str(temp["Dex"]) + " " +
             returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " +
             str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") +
             "\n**Per**: " + str(temp["Per"]) + " " +
             returnItemBonusDict(bonuses, "Per") + "\n**Int**: " +
             str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") +
             "\n**Wis**: " + str(temp["Wis"]) + " " +
             returnItemBonusDict(bonuses, "Wis"))
        })
        db[str(ctx.guild.id)][name.title()] = playerDict
        await ctx.send("Created character " + name)

    @commands.command(name="check-character",
                 pass_context=True,
                 aliases=["c-c", "Check-Character", "Check-character"])
    async def checkCharacter(self, ctx, name="", inSetStats=False):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a generated character.")
            return
        temp = db[str(ctx.guild.id)][name]
        embed = discord.Embed(
            title=(name + "'s Character Sheet"),
            description=(
                "The following is their Astral Fantasy character sheet:\n" +
                temp["Name"] + ":"))
        titlesString = ""
        for i in temp["Titles"]:
            titlesString += i
            if i != temp["Titles"][-1]:
                titlesString += ", "
        embed.add_field(name="Titles", value=titlesString, inline=False)
        embed.add_field(name="Rank",
                        value=returnCharacterRank(temp),
                        inline=False)
        embed.add_field(name="Money", value=returnMoney(temp), inline=False)
        embed.add_field(name="Core Stats",
                        value=temp["Stat String"],
                        inline=False)
        embed.add_field(name="Skills:", value=returnSkills(temp), inline=False)
        embed.add_field(name="Abilities:",
                        value=returnAbilities(temp),
                        inline=False)
        if inSetStats:
            return embed
        else:
            await ctx.send(embed=embed)

    @commands.command(name="copy-character", pass_context=True, aliases=["cc-c"])
    @commands.has_permissions(manage_messages=True)
    async def copyCharacter(self, ctx, fromID=0, toID=0, name=""):
        if fromID == 0:
            print("Please enter a server ID to copy from.")
        if toID == 0:
            print("Please enter a server ID to copy to.")
        if name == "":
            print("Please enter a character name.")
        val1 = db[str(fromID)][name]
        val1 = dict(val1)
        val1["Energies"] = dict(val1["Energies"])
        for key2, val2 in val1["Energies"].items():
            val1["Energies"][key2] = list(val2)
        val1["Titles"] = list(val1["Titles"])
        val1["Skills"] = dict(val1["Skills"])
        val1["Currencies"] = dict(val1["Currencies"])
        val1["Abilities"] = dict(val1["Abilities"])
        val1["Item Bonuses"] = dict(val1["Item Bonuses"])
        for key2, val2 in val1["Item Bonuses"].items():
            val1["Item Bonuses"][key2] = dict(val2)
        db[str(toID)][name] = val1
        print("Data successfully migrated.")

    @commands.command(name="add-stat",
                 pass_context=True,
                 aliases=["a-s", "Add-Stat", "Add-stat"])
    @commands.has_permissions(manage_messages=True)
    async def addStat(self, ctx, name="", *furtherStats):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a generated character.")
            return
        temp = db[str(ctx.guild.id)][name]
        i = 0
        bonuses = temp["Item Bonuses"]
        while i < len(furtherStats):
            stat = furtherStats[i].title()
            if stat not in temp.keys():
                await ctx.send(stat + " is not a valid statistic.")
                i += 2
            try:
                stat = {
                    "Strength": "Str",
                    "Constitution": "Con",
                    "Dexterity": "Dex",
                    "Agility": "Agi",
                    "Perception": "Per",
                    "Intelligence": "Int",
                    "Wisdom": "Wis"
                }[stat]
            except:
                pass
            try:
                amount = int(furtherStats[i + 1])
                i += 2
            except:
                await ctx.send(
                    "Amount for stat entered is not a valid integer or does not exist."
                )
                i += 2
            temp[stat] += amount
            if "Current MP" in temp.keys():
                temp.update(
                    {"Energies": {
                        "MP": [temp["Wis"] * 5, temp["Wis"] * 5]
                    }})
                del temp["Current MP"]
                del temp["Max MP"]
            if stat == "Con":
                temp["Current HP"] = temp[stat] * 10
                temp["Max HP"] = temp[stat] * 10
            elif stat == "Wis":
                if "MP" in temp["Energies"].keys(
                ) and "EP" in temp["Energies"].keys():
                    temp["Energies"]["MP"] = [temp[stat] * 5, temp[stat] * 5]
                    temp["Energies"]["EP"] = [temp[stat] * 5, temp[stat] * 5]
                elif "MP" in temp["Energies"].keys():
                    temp["Energies"]["MP"] = [temp[stat] * 5, temp[stat] * 5]
                elif "EP" in temp["Energies"].keys():
                    temp["Energies"]["EP"] = [temp[stat] * 5, temp[stat] * 5]
        temp["Stat String"] = (
            "**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"]) +
            returnItemBonusBar(temp, "HP") + returnEnergies(temp) +
            "\n\n**Str**: " + str(temp["Str"]) + " " +
            returnItemBonusDict(bonuses, "Str") + "\n**Con**: " +
            str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") +
            "\n**Dex**: " + str(temp["Dex"]) + " " +
            returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " +
            str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") +
            "\n**Per**: " + str(temp["Per"]) + " " +
            returnItemBonusDict(bonuses, "Per") + "\n**Int**: " +
            str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") +
            "\n**Wis**: " + str(temp["Wis"]) + " " +
            returnItemBonusDict(bonuses, "Wis"))

        embed = discord.Embed(
            title=(name + "'s Character Sheet"),
            description=(
                "The following is their Astral Fantasy character sheet:\n" +
                temp["Name"] + ":"))
        titlesString = ""
        for i in temp["Titles"]:
            titlesString += i
            if i != temp["Titles"][-1]:
                titlesString += ", "
        embed.add_field(name="Titles", value=titlesString, inline=False)
        embed.add_field(name="Rank",
                        value=returnCharacterRank(temp),
                        inline=False)

        embed.add_field(name="Money", value=returnMoney(temp), inline=False)
        embed.add_field(name="Core Stats",
                        value=temp["Stat String"],
                        inline=False)
        embed.add_field(name="Skills:", value=returnSkills(temp), inline=False)
        embed.add_field(name="Abilities:",
                        value=returnAbilities(temp),
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="set-stat",
                 pass_context=True,
                 aliases=["s-s", "Set-Stat", "Set-stat"])
    @commands.has_permissions(manage_messages=True)
    async def setStat(self, ctx, name="", *furtherStats):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a generated character.")
            return
        temp = db[str(ctx.guild.id)][name]
        i = 0
        bonuses = temp["Item Bonuses"]
        while i < len(furtherStats):
            stat = furtherStats[i].title()
            print(stat)
            try:
                stat = {
                    "Strength": "Str",
                    "Constitution": "Con",
                    "Dexterity": "Dex",
                    "Agility": "Agi",
                    "Perception": "Per",
                    "Intelligence": "Int",
                    "Wisdom": "Wis"
                }[stat]
            except:
                pass
            if stat not in temp.keys():
                await ctx.send(stat + " is not a valid statistic.")
                i += 2
            try:
                amount = int(furtherStats[i + 1])
                i += 2
            except:
                await ctx.send(
                    "Amount for stat entered is not a valid integer or does not exist."
                )
                i += 2
            temp[stat] = amount
            if "Current MP" in temp.keys():
                temp.update(
                    {"Energies": {
                        "MP": [temp["Wis"] * 5, temp["Wis"] * 5]
                    }})
                del temp["Current MP"]
                del temp["Max MP"]
            if stat == "Con":
                temp["Current HP"] = temp[stat] * 10
                temp["Max HP"] = temp[stat] * 10
            elif stat == "Wis":
                if "MP" in temp["Energies"].keys(
                ) and "EP" in temp["Energies"].keys():
                    temp["Energies"]["MP"] = [temp[stat] * 5, temp[stat] * 5]
                    temp["Energies"]["EP"] = [temp[stat] * 5, temp[stat] * 5]
                elif "MP" in temp["Energies"].keys():
                    temp["Energies"]["MP"] = [temp[stat] * 5, temp[stat] * 5]
                elif "EP" in temp["Energies"].keys():
                    temp["Energies"]["EP"] = [temp[stat] * 5, temp[stat] * 5]
        temp["Stat String"] = (
            "**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"]) +
            returnItemBonusBar(temp, "HP") + returnEnergies(temp) +
            "\n\n**Str**: " + str(temp["Str"]) + " " +
            returnItemBonusDict(bonuses, "Str") + "\n**Con**: " +
            str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") +
            "\n**Dex**: " + str(temp["Dex"]) + " " +
            returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " +
            str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") +
            "\n**Per**: " + str(temp["Per"]) + " " +
            returnItemBonusDict(bonuses, "Per") + "\n**Int**: " +
            str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") +
            "\n**Wis**: " + str(temp["Wis"]) + " " +
            returnItemBonusDict(bonuses, "Wis"))

        embed = discord.Embed(
            title=(name + "'s Character Sheet"),
            description=(
                "The following is their Astral Fantasy character sheet:\n" +
                temp["Name"] + ":"))
        titlesString = ""
        for i in temp["Titles"]:
            titlesString += i
            if i != temp["Titles"][-1]:
                titlesString += ", "
        embed.add_field(name="Titles", value=titlesString, inline=False)
        embed.add_field(name="Rank",
                        value=returnCharacterRank(temp),
                        inline=False)
        embed.add_field(name="Money", value=returnMoney(temp), inline=False)
        embed.add_field(name="Core Stats",
                        value=temp["Stat String"],
                        inline=False)
        embed.add_field(name="Skills:", value=returnSkills(temp), inline=False)
        embed.add_field(name="Abilities:",
                        value=returnAbilities(temp),
                        inline=False)
        await ctx.send(embed=embed)

    def find_nth(haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start + len(needle))
            n -= 1
        return start

    # Implement commands

    @commands.command(name="rename-character",
                 pass_context=True,
                 aliases=["r-c", "Rename-Character", "Rename-character"])
    @commands.has_permissions(manage_messages=True)
    async def renameCharacter(self, ctx, name="", newName=""):
        name = name.title()
        newName = newName.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send("Please enter a valid character name to rename.")
            return
        if newName == "":
            await ctx.send("Please enter a new name to rename.")
            return
        temp = db[str(ctx.guild.id)][name]
        temp["Name"] = newName
        db[str(ctx.guild.id)][newName] = temp
        del db[str(ctx.guild.id)][name]
        await ctx.send("Renamed " + name + " to " + newName + ".")

    @commands.command(name="list-characters",
                 pass_context=True,
                 aliases=["l-c", "List-Characters", "List-characters"])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def listCharacters(self, ctx, page=0):
        totalList = list(db[str(ctx.guild.id)].keys())
        string = ""
        thisList = totalList[10 * page:10 * (page + 1)]
        for i in thisList:
            string += i + "\n"
        await ctx.send(string)

    @listCharacters.error
    async def listCharactersError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'Command "list-character" is on cooldown, you can use it in {round(error.retry_after, 2)} seconds.'
            )

    

    @commands.command(name="set-race",
                 pass_context=True,
                 aliases=["s-r", "Set-Race", "Set-race"])
    @commands.has_permissions(manage_messages=True)
    async def setRace(self, ctx, name="", race=""):
        name = name.title()
        race = race.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send("Please input a valid name.")
            return
        if race == "":
            await ctx.send("Please input a race.")
            return
        temp = db[str(ctx.guild.id)][name]
        temp["Race"] = race

        if temp["Sin/Virtue"] != "":
            startingTitle = race.title() + " of " + temp["Sin/Virtue"].title()
        else:
            startingTitle = race.title()
        temp["Titles"][0] = startingTitle
        await ctx.send("Updated " + name + "'s race to " + race + ".")

    @commands.command(name="generate-skills",
                 pass_context=True,
                 aliases=["g-s", "Generate-Skills", "Generate-skills"])
    @commands.has_permissions(manage_messages=True)
    async def generateInitialSkills(self, ctx, name="", *skillsList):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a generated character.")
            return
        temp = db[str(ctx.guild.id)][name]
        for i in skillsList:
            i = i.title()
            try:
                if i.index("'") != -1:
                    listString = [j for j in i]
                    listString[i.index("'") + 1] = listString[i.index("'") +
                                                              1].lower()
                    value = ""
                    for n in listString:
                        value += n
                    i = value
            except:
                pass
            temp["Skills"].update({i: randint(1, 16) + 15})

        await ctx.send(name + "'s Skills have been updated.")

    @commands.command(name="remove-skills",
                 pass_context=True,
                 aliases=["rm-sk", "Remove-Skills", "Remove-skills"])
    @commands.has_permissions(manage_messages=True)
    async def removeSkills(self, ctx, name="", skill=""):
        name = name.title()
        skill = skill.title()

        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a generated character.")
            return
        temp = db[str(ctx.guild.id)][name]

        if skill not in temp["Skills"]:
            await ctx.send(name + " doesn't have this skill to remove.")
            return
        temp["Skills"].pop(skill)
        await ctx.send(skill + " has been removed from " + name + "'s skills.")

    @commands.command(name="rename-skills",
                 pass_context=True,
                 aliases=["rn-sk", "Rename-Skills", "Rename-skills"])
    @commands.has_permissions(manage_messages=True)
    async def renameSkills(self, ctx, name="", skill="", newName=""):
        name = name.title()
        skill = skill.title()

        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a generated character.")
            return
        temp = db[str(ctx.guild.id)][name]

        if skill not in temp["Skills"]:
            await ctx.send(name + " doesn't have this skill to remove.")
            return
        temp["Skills"][newName] = temp["Skills"][skill]
        del temp["Skills"][skill]
        await ctx.send(skill + " has been renamed to " + newName + ".")

    @commands.command(name="add-skills",
                 pass_context=True,
                 aliases=["a-skills", "a-sk", "Add-Skills", "Add-skills"])
    @commands.has_permissions(manage_messages=True)
    async def addToSkills(self, ctx, name, *skills):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a generated character.")
            return
        temp = db[str(ctx.guild.id)][name]
        for i in range(0, len(skills) - 1):
            try:
                if type(int(skills[i])) == int:
                    continue
            except:
                val = skills[i].title()
                if val in temp["Skills"]:
                    temp["Skills"][val] += int(skills[i + 1])
                else:
                    temp["Skills"].update({val: int(skills[i + 1])})
        await ctx.send(name + "'s Skills have been updated.")

    @commands.command(
        name="delete-character",
        pass_context=True,
        aliases=["d-c", "rm-c", "Delete-Character", "Delete-character"])
    @commands.has_permissions(administrator=True)
    async def deleteCharacter(self, ctx, name=""):
        name = name.title()
        if name == "":
            await ctx.send("Delete which character? Reference by name.")

            def check(message):
                def inner_check(author):
                    return message.author == ctx.author and msg.channel == ctx.channel

                return inner_check

            msg = await bot.wait_for("message", check=check)
            name = msg
            name = name.title()
        try:
            del db[str(ctx.guild.id)][name]
            await ctx.send(name + " has been deleted.")
        except KeyError:
            await ctx.send(name + " is not a valid character to be deleted.")

    @commands.command(name="add-title",
                 pass_context=True,
                 aliases=["a-t", "Add-Title", "Add-title"])
    @commands.has_permissions(manage_messages=True)
    async def addTitle(self, ctx, name="", *titles):
        name = name.title()
        if name == "":
            await ctx.send("Please input a name.")
            return

        temp = db[str(ctx.guild.id)][name]
        for i in titles:
            if properTitle(i) not in temp["Titles"]:
                temp["Titles"].append(properTitle(i))
                await ctx.send(
                    properTitle(i) + " has been added to " + name +
                    "'s titles.")

    @commands.command(name="remove-title",
                 pass_context=True,
                 aliases=["rm-t", "Remove-Title", "Remove-title"])
    @commands.has_permissions(manage_messages=True)
    async def removeTitle(self, ctx, name="", userTitle=""):
        name = name.title()
        userTitle = properTitle(userTitle)
        if name == "":
            await ctx.send("Please input a name.")
            return
        temp = db[str(ctx.guild.id)][name]
        if userTitle not in temp["Titles"]:
            await ctx.send(title + " is not one of " + name + "'s titles.")
            return
        temp["Titles"].remove(userTitle)
        await ctx.send(userTitle + " has been removed from " + name + "'s titles.")

    @commands.command(name="add-ability",
                 pass_context=True,
                 aliases=["a-a", "Add-Ability", "Add-ability"])
    @commands.has_permissions(manage_messages=True)
    async def addAbility(self, ctx, name="", *abilities):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        temp = db[str(ctx.guild.id)][name]
        a = dict(temp["Abilities"])
        for i in abilities:
            if i != "":
                i = properTitle(i)
                a.update({i: 1})
        temp["Abilities"] = a
        await ctx.send("Added to " + name + "'s abilities")

    @commands.command(name="level-ability",
                 pass_context=True,
                 aliases=["l-a", "Level-Ability", "Level-ability"])
    @commands.has_permissions(manage_messages=True)
    async def levelAbility(self, ctx, name="", ability="", level=0):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        temp = db[str(ctx.guild.id)][name]
        ability = ability.title()
        if ability not in temp["Abilities"]:
            await ctx.send(ability + " is not one of " + name +
                           "'s abilities.")
            return
        if level == 0:
            await ctx.send("Please enter a level to add.")
            return
        temp["Abilities"][ability] += level
        await ctx.send("Edited " + name + "'s abilities.")

    @commands.command(name="remove-ability",
                 pass_context=True,
                 aliases=["rm-a", "Remove-Ability", "Remove-ability"])
    @commands.has_permissions(manage_messages=True)
    async def removeAbility(self, ctx, name="", ability=""):
        name = name.title()
        ability = properTitle(ability)
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        temp = db[str(ctx.guild.id)][name]
        if ability not in temp["Abilities"]:
            await ctx.send(ability + " is not one of " + name +
                           "'s abilities.")
            return
        temp["Abilities"].pop(ability)
        await ctx.send("Removed " + ability + " from " + name +
                       "'s abilities.")

    @commands.command(name="add-energy",
                 pass_context=True,
                 aliases=["a-e", "Add-Energy", "Add-energy"])
    @commands.has_permissions(manage_messages=True)
    async def addEnergy(self, ctx, name="", energy="", startingMaximum=100):
        name = name.title()
        energy = energy.upper()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        if energy == "":
            await ctx.send("Please enter an energy type as its abbreviation.")
            return
        try:
            startingMaximum = int(startingMaximum)
        except:
            await ctx.send("Starting " + energy + " amount is not a number.")
            return
        temp = db[str(ctx.guild.id)][name]
        if energy in temp["Energies"].keys():
            await ctx.send("The energy type requested is already in " + name +
                           "'s possession.")
            return
        if energy in ["MP", "EP"]:
            startingMaximum = temp["Wis"] * 5
        temp["Energies"].update({energy: [startingMaximum, startingMaximum]})
        bonuses = temp["Item Bonuses"]
        if "MP" in temp["Energies"].keys() and "EP" in temp["Energies"].keys():
            temp["Energies"]["MP"] = [temp["Wis"] * 5, temp["Wis"] * 5]
            temp["Energies"]["EP"] = [temp["Wis"] * 5, temp["Wis"] * 5]
        elif "MP" in temp["Energies"].keys():
            temp["Energies"]["MP"] = [temp["Wis"] * 5, temp["Wis"] * 5]
        elif "EP" in temp["Energies"].keys():
            temp["Energies"]["EP"] = [temp["Wis"] * 5, temp["Wis"] * 5]
        temp["Stat String"] = (
            "**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"]) +
            returnItemBonusBar(temp, "HP") + returnEnergies(temp) +
            "\n\n**Str**: " + str(temp["Str"]) + " " +
            returnItemBonusDict(bonuses, "Str") + "\n**Con**: " +
            str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") +
            "\n**Dex**: " + str(temp["Dex"]) + " " +
            returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " +
            str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") +
            "\n**Per**: " + str(temp["Per"]) + " " +
            returnItemBonusDict(bonuses, "Per") + "\n**Int**: " +
            str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") +
            "\n**Wis**: " + str(temp["Wis"]) + " " +
            returnItemBonusDict(bonuses, "Wis"))
        await ctx.send("Added " + energy + " to " + name + ".")

    @commands.command(name="remove-energy",
                 pass_context=True,
                 aliases=["rm-e", "Remove-Energy", "Remove-energy"])
    @commands.has_permissions(manage_messages=True)
    async def removeEnergy(self, ctx, name="", energy=""):
        name = name.title()
        energy = energy.upper()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        temp = db[str(ctx.guild.id)][name]
        if energy not in temp["Energies"].keys():
            await ctx.send(name + " does not have this energy type to remove.")
            return
        temp["Energies"].pop(energy)
        bonuses = temp["Item Bonuses"]
        temp["Stat String"] = (
            "**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"]) +
            returnItemBonusBar(temp, "HP") + returnEnergies(temp) +
            "\n\n**Str**: " + str(temp["Str"]) + " " +
            returnItemBonusDict(bonuses, "Str") + "\n**Con**: " +
            str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") +
            "\n**Dex**: " + str(temp["Dex"]) + " " +
            returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " +
            str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") +
            "\n**Per**: " + str(temp["Per"]) + " " +
            returnItemBonusDict(bonuses, "Per") + "\n**Int**: " +
            str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") +
            "\n**Wis**: " + str(temp["Wis"]) + " " +
            returnItemBonusDict(bonuses, "Wis"))
        await ctx.send("Removed " + energy + " from " + name + ".")

    @commands.command(name="add-currency",
                 pass_context=True,
                 aliases=["a-cu", "Add-Currency", "Add-currency"])
    @commands.has_permissions(manage_messages=True)
    async def addCurrency(self, ctx, name="", currency="", amount=0):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        if currency == "":
            await ctx.send("Please enter a currency.")
            return
        temp = db[str(ctx.guild.id)][name]
        try:
            amount = int(amount)
        except:
            await ctx.send("Starting " + currency + " amount is not a number.")
            return
        if "Currencies" not in temp.keys():
            temp.update({"Currencies": {}})
        if currency in temp["Currencies"].keys():
            temp["Currencies"][currency] += amount
            await ctx.send("Added " + str(amount) + " to " + name + "'s " +
                           currency + ".")
            return
        else:
            temp["Currencies"].update({currency: amount})
            await ctx.send("Added " + str(amount) + " to " + name + "'s " +
                           currency + ".")
            return

    @commands.command(name="remove-currency",
                 pass_context=True,
                 aliases=["rm-cu", "Remove-Currency", "Remove-currency"])
    @commands.has_permissions(manage_messages=True)
    async def removeCurrency(self, ctx, name="", currency=""):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        temp = db[str(ctx.guild.id)][name]
        if currency not in temp["Currencies"].keys():
            await ctx.send(name + " does not have this currency.")
            return
        temp["Currencies"].pop(currency)
        await ctx.send("Removed " + currency + " from " + name + ".")

    @commands.command(name="add-item-bonus",
                 pass_context=True,
                 aliases=["a-ib", "a-i-b", "Add-Item-Bonus", "Add-item-bonus"])
    @commands.has_permissions(manage_messages=True)
    async def addItemBonus(self, ctx,
                           name="",
                           itemBonusName="",
                           bonusStat="",
                           bonusAmount=0):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        temp = db[str(ctx.guild.id)][name]
        if itemBonusName == "":
            await ctx.send("Please enter a proper name for the item bonus.")
            return
        if bonusStat == "":
            await ctx.send(
                "Please enter a statistic for this bonus to be added to.")
            return
        bonusStat = bonusStat.title()
        try:
            bonusStat = {
                "Strength": "Str",
                "Constitution": "Con",
                "Dexterity": "Dex",
                "Agility": "Agi",
                "Perception": "Per",
                "Intelligence": "Int",
                "Wisdom": "Wis"
            }[bonusStat]
        except:
            pass
        if bonusStat not in temp.keys():
            await ctx.send(bonusStat + " is not a valid statistic.")
            return
        try:
            if int(bonusAmount) == 0:
                await ctx.send(
                    "Please enter a number greater than or less than 0 for the bonus amount."
                )
                return
            bonusAmount = int(bonusAmount)
        except:
            await ctx.send("Enter an integer as the bonus amount.")
            return

        temporaryDict = temp["Item Bonuses"][bonusStat]
        temporaryDict.update({itemBonusName: bonusAmount})
        temp["Item Bonuses"][bonusStat] = temporaryDict
        bonuses = temp["Item Bonuses"]
        temp["Stat String"] = (
            "**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"]) +
            returnItemBonusBar(temp, "HP") + returnEnergies(temp) +
            "\n\n**Str**: " + str(temp["Str"]) + " " +
            returnItemBonusDict(bonuses, "Str") + "\n**Con**: " +
            str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") +
            "\n**Dex**: " + str(temp["Dex"]) + " " +
            returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " +
            str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") +
            "\n**Per**: " + str(temp["Per"]) + " " +
            returnItemBonusDict(bonuses, "Per") + "\n**Int**: " +
            str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") +
            "\n**Wis**: " + str(temp["Wis"]) + " " +
            returnItemBonusDict(bonuses, "Wis"))
        await ctx.send(name + "'s item bonus for " + bonusStat +
                       " has been updated to " + itemBonusName +
                       " with an amount of " + str(bonusAmount) + ".")

    #Remove item bonus command

    @commands.command(
        name="remove-item-bonus",
        pass_context=True,
        aliases=["rm-ib", "rm-i-b", "Remove-Item-Bonus", "Remove-item-bonus"])
    @commands.has_permissions(manage_messages=True)
    async def removeItemBonus(self, ctx, name="", stat="", bonusName=""):
        name = name.title()
        if name not in db[str(ctx.guild.id)].keys():
            await ctx.send(name + " is not a valid character.")
            return
        temp = db[str(ctx.guild.id)][name]
        stat = stat.title()
        if stat not in ("Str", "Con", "Dex", "Agi", "Per", "Int", "Wis"):
            await ctx.send(stat + " is not a valid statistic.")
            return

        valueDict = dict(temp["Item Bonuses"])
        valueDict = dict(valueDict[stat])
        if bonusName not in valueDict:
            await ctx.send(bonusName + " is not an item bonus existant on " +
                           stat + " for " + name + ".")
            return
        valueDict.pop(bonusName)
        temp["Item Bonuses"][stat] = valueDict
        await ctx.send("Removed " + bonusName + " from " + stat + " of " +
                       name + ".")

    # @commands.has_permissions(manage_messages=True)
    # async def addQi(self, ctx, name="", tier="", subLevel=""):
    #     name = name.title()
    #     if name not in db[str(ctx.guild.id)].keys():
    #         await ctx.send(f"{name} is not a valid character.")
    #         return
    #     temp = db[str(ctx.guild.id)][name]
    #     if tier == "":
    #         await ctx.send("Please write the requested tier.")
    #     tier = tier.title()
    #     try:
    #         subLevel = int(subLevel)
    #     except:
    #         print("Qi tier sub-level must be an integer.")
