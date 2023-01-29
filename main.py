import random
import string
from replit import db
from random import randint
import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import os
from ply.lex import lex
from ply.yacc import yacc
import json
token = os.getenv('token')

import keepalive
import time

keepalive.awake("https://Astral-Defender.plasmium.repl.co", )

# Randog
class randomPicture:
	def __init__(self, picture, rarity, name):
		self.picture = picture;
		self.rarity = rarity;
		self.name = name;

timPics = [
	randomPicture("images/staretim.jpeg", 			10, 	"Stare"),
	randomPicture("images/sittim.jpeg", 			10, 	"Sit"),
	randomPicture("images/windowtim.jpeg", 		10, 	"Window"),
	randomPicture("images/leafytim.jpeg", 			5, 		"Leaves"),
	randomPicture("images/timshirt.jpeg", 			5, 		"Shirt"),
	randomPicture("images/timblanket.jpeg", 		5, 		"Blanket"),
	randomPicture("images/timdogbed.jpeg", 		15, 	"Dog Bed"),
	randomPicture("images/shirttim.jpeg", 			1, 		"MACCABI HAIFA"),
	randomPicture("images/timcutesuper.jpeg", 		1, 		"Cute Super-Dog"),
	randomPicture("images/curled.jpeg", 			3, 		"Curled"),
	randomPicture("images/timrun.MP4", 			15, 	"Run"),
	randomPicture("images/grasstim.jpeg", 			10, 	"Grassy Tim"),
	randomPicture("images/ohnotim.jpeg", 			3, 		"Murderer Duo"),
	randomPicture("images/trusttim.jpeg", 			10, 	"Trust the Tim"),
	randomPicture("images/timnsmall.jpeg", 		5, 		"Meeting"),
	randomPicture("images/cartim.jpeg", 			10, 	"Tim doesn't like car rides"),
	randomPicture("images/timbirdride.jpeg", 		15, 	"Tim bird ride"),
	randomPicture("images/gaytim.jpeg", 			15, 	"Sorry, but our Tim is in another castle"),
	randomPicture("images/firstmeeting.jpeg", 		5, 		"Hello there"),
	randomPicture("images/timdoll.jpeg", 			10,	 	"Tim chew doll"),
	randomPicture("images/selphieTim.jpeg", 		15, 	"Zoomed in sleeping Tim"),
	randomPicture("images/timwakeup.jpeg", 		15, 	"Tim wakeup"),
	randomPicture("images/smilebitch.jpeg", 		1, 		"Smile, bitch"),
	randomPicture("images/selfietim.jpeg", 		5, 		"Tim selfie"),
	randomPicture("images/arabtim.jpeg", 			3, 		"Arab Tim"),
	randomPicture("images/yogatim.jpeg", 			15, 	"Tim stretch"),
	randomPicture("images/underTableTim.jpeg", 	10, 	"Tim under a table")
]

# Rolling variables

do_roll_limit = True

def actual_roll(rolls, sides):
	ret_message = ""
	add_to_message = True
	
	sum = 0
	counter = 0
	
	if (sides > 100000):
		sides = 100000
	
	for i in range(rolls):
		this_roll = random.randint(1, sides);
		
		if (counter > 12 and add_to_message and do_roll_limit):
			add_to_message = False
			ret_message += "..."
		elif (counter == 0 and add_to_message):
			ret_message += str(this_roll)
		elif (add_to_message):
			ret_message += ", " + str(this_roll)
		
		counter += 1
		sum += this_roll

	ret_message += " **Sum: " + str(sum) + "**"
	
	return [sum, ret_message]

tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NUMBER', 'CUBE', 'LPAREN', 'RPAREN')

precedence = (
    ('left', 'PLUS', 'MINUS'),
    #('right', 'UMINUS'),
    ('left', 'DIVIDE', 'TIMES'),
    ('left', 'NUMBER'),
    ('nonassoc', 'CUBE'),
    ('left', 'RPAREN'),
    ('right', 'LPAREN')
)

t_ignore = ' \t\n'

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_NUMBER    = r'[0-9]+'
t_CUBE      = r'd'

lexer = lex()

def p_expression(p):
    '''
    expression  : LPAREN expression RPAREN
                | expression CUBE expression
                | CUBE expression
                | expression TIMES expression
                | expression DIVIDE expression
                | expression PLUS expression
                | expression MINUS expression
                | NUMBER
    '''
    try:
        p[0] = [p[2], p[1], p[3]]
        if (p[1] == "("):
            p[0] = ["(", p[2], ")"]
    except:
        p[0] = p[1]
        if (p[1] == t_CUBE):
            p[0] = [p[1], '1', p[2]]


parser = yacc()


def compile(exp):
    if (isinstance(exp, list)):
        first = exp[0]
        if (first == "+"):
            l_branch = branch([exp[1], ""])
            r_branch = branch([exp[2], ""])
            return [l_branch[0] + r_branch[0], l_branch[1] + " + " + r_branch[1]]
        elif (first == "-"):
            l_branch = branch([exp[1], ""])
            r_branch = branch([exp[2], ""])
            return [l_branch[0] - r_branch[0], l_branch[1] + " - " + r_branch[1]]
        elif (first == "*"):
            l_branch = branch([exp[1], ""])
            r_branch = branch([exp[2], ""])
            return [l_branch[0] * r_branch[0], l_branch[1] + " * " + r_branch[1]]
        elif (first == "/"):
            l_branch = branch([exp[1], ""])
            r_branch = branch([exp[2], ""])
            return [l_branch[0] / r_branch[0], l_branch[1] + "/" + r_branch[1]]
        elif (first == "d"):
            l_branch = branch([exp[1], ""])
            r_branch = branch([exp[2], ""])
            my_roll = actual_roll(l_branch[0], r_branch[0])
            return [my_roll[0], l_branch[1] + "d" + r_branch[1]+ " [" + my_roll[1] + "]"]
        elif (first == "("):
            l_branch = branch([exp[1], ""])
            return [l_branch[0], "(" + l_branch[1] + ")"]
    else:
        return [int(exp), str(exp)]


def branch(exp):
    if (isinstance(exp[0], list)):
        first = exp[0][0]
        if (first == "+"):
            l_branch = branch([exp[0][1], exp[1]])
            r_branch = branch([exp[0][2], exp[1]])
            return [l_branch[0] + r_branch[0], l_branch[1] + " + " + r_branch[1]]
        elif (first == "-"):
            l_branch = branch([exp[0][1], exp[1]])
            r_branch = branch([exp[0][2], exp[1]])
            return [l_branch[0] - r_branch[0], l_branch[1] + " - " + r_branch[1]]
        elif (first == "*"):
            l_branch = branch([exp[0][1], exp[1]])
            r_branch = branch([exp[0][2], exp[1]])
            return [l_branch[0] * r_branch[0], l_branch[1] + " * " + r_branch[1]]
        elif (first == "/"):
            l_branch = branch([exp[0][1], exp[1]])
            r_branch = branch([exp[0][2], exp[1]])
            return [l_branch[0] / r_branch[0], l_branch[1] + "/" + r_branch[1]]
        elif (first == "d"):
            l_branch = branch([exp[0][1], exp[1]])
            r_branch = branch([exp[0][2], exp[1]])
            my_roll = actual_roll(l_branch[0], r_branch[0])
            return [my_roll[0], l_branch[1] + "d" + r_branch[1] + " [" + my_roll[1] + "]"]
        elif (first == "("):
            l_branch = branch([exp[0][1], exp[1]])
            return [l_branch[0], "(" + l_branch[1] + ")"]
    else:
        return [int(exp[0]), str(exp[0])]


global thisPage
	
delete_logger = { }

print ("Loading..")
intents = discord.Intents.default()
client = discord.Client(intents=discord.Intents.default())
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix=['>', '{}'])

bot.remove_command('help')


@bot.event
async def on_ready():
	print ("Your realm shall now be protected by the Decree of the Stellar Covenant.")
	await bot.change_presence(activity=discord.Game(name=">help"))

#Contingency Orders:

@bot.event
async def on_member_join(member:discord.Member):
	await asyncio.sleep(2)
	role = discord.utils.get(member.guild.roles, name="Unverified")
	rolebanRole = discord.utils.get(member.guild.roles, name="Roleban")
	if rolebanRole not in member.roles:
		await member.add_roles(role)

@bot.listen('on_message')
async def messagemonitor(message): #Anti-Scam
	#if message.channel.type is discord.ChannelType.private:

	if "https://" in message.content and "gift" in message.content:

		try:
			
			await message.delete()

		except:
			pass
	elif "discord.gg" in message.content and message.channel.name != "partners" and message.channel.category.name != "RP Hubs" and message.author.id != 454820620824215553:
		try:
			await message.delete()
		
		except:
			pass
	elif "igger" in message.content.lower() and not (("bigger" in message.content.lower()) or ("trigger" in message.content.lower()) or ("triggered" in message.content.lower()) or ("digger" in message.content.lower())):
		try:
			await message.delete()
		except:
			pass
	elif "fag" in message.content.lower() or "f@g" in message.content.lower():
		try:
			await message.delete()
		except:
			pass
	elif "nigga" in message.content.lower() or "niggas" in message.content.lower() or "niggers" in message.content.lower():
		try:
			await message.delete()
		except:
			pass
	elif "https://images-ext-2.discordapp.net/external/WlCcgtV_C1ygC7rErRTbj4kUc5A6mqE_bG6TW2KoM1A/https/media.tenor.com/pyUTSY5MeusAAAPo/makima.mp4" in message.content or "https://tenor.com/view/makima-gif-26321924" in message.content:
		try:
			await message.delete()
		except:
			pass
		

modlist = (454820620824215553, 423798867868516373, 681931899584905390, 945430077863243797)

@bot.event
async def on_member_ban(guild, member):
	logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
	logs = logs[0]
	user=logs.user
	global delete_logger
	try:
		delete_logger[str(logs.user)] += 1

	except KeyError:
		delete_logger[str(logs.user)] = 1

	if user.id not in modlist:
		for user, deleted in delete_logger.items():
			print(user," removed someone ("+str(deleted)+"/3)")
			if deleted >= 3:
				await guild.ban(logs.user)



@bot.event
async def on_guild_channel_delete(ctx):
	logs = await ctx.guild.audit_logs(limit=1,
	action=discord.AuditLogAction.channel_delete).flatten()
	logs = logs[0]
	user=logs.user
	global delete_logger
	try:
		delete_logger[str(logs.user)] += 1
	except KeyError:
		delete_logger[str(logs.user)] = 1
	
	if user.id not in modlist:
		for user, deleted in delete_logger.items():
			print(user," deleted a channel ("+str(deleted)+"/1)")
			if deleted >= 3:
				await ctx.guild.ban(logs.user)


@bot.event
async def on_guild_role_delete(ctx):
	logs = await ctx.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete).flatten()
	logs = logs[0]
	user=logs.user
	id=user.id
	global delete_logger
	try:
		delete_logger[str(logs.user)] += 1
	except KeyError:
		delete_logger[str(logs.user)] = 1
 
	if id not in modlist:
		for user, deleted in delete_logger.items():
			print(user," deleted a role ("+str(deleted)+"/5)")
			if deleted >= 1:
				await ctx.guild.ban(logs.user)

@bot.event
async def on_guild_join(guild):
	db[str(guild.id)] = {}
	


@tasks.loop(seconds=60)
async def clear_delete_logger():
	global delete_logger
	delete_logger.clear()


@clear_delete_logger.before_loop
async def before():
	await client.wait_until_ready()
	clear_delete_logger.start()

@bot.command(name="help", pass_context=True)
async def help(ctx, entry="", page=1):
	entry = entry.title()
	embed = discord.Embed(title="Help Page", description="This is the help page. Refer to this command for help on the commands you can use with this bot.", color=0x33FBFF)
	embed.set_thumbnail(url="https://media.discordapp.net/attachments/843632677533777940/934961324478300160/editedcircle.png")
	entry = str(entry).lower()
	
	if (entry == "moderation" or entry == "mod"):
		embed.add_field(name="Roleban", 	value="Locks the mentioned user to the roleban channel.", inline=True)
		embed.add_field(name="Unroleban", 	value="Removes the mentioned user from the roleban channel, if they are rolebanned.", inline=True)
		embed.add_field(name="Ban", 		value="Bans the mentioned user from the Discord server.", inline=True)
		embed.add_field(name="Unban", 		value="Unbans the mentioned user from the Discord server.", inline=True)
		embed.add_field(name="Purge", 		value="Purges a specified amount of messages (not including the message sent to use the command).).", inline=True)

	elif entry == "characters":
		if page == 1:
			embed.add_field(name="Create-Character", 	value="Create a character with the name, race, and sin/virtue. A sheet will be automatically generated.\n**Syntax: **`>create-character (name) (race) [Sin/Virtue]`\nAka create-c")
			embed.add_field(name="Check-Character", 	value="Displays a character sheet for the character with the referenced name.\n**Syntax: **`>check-character (name)`\nAka c-c")
			embed.add_field(name="Add-Stat", 			value="Adds to a stat on a character sheet\n**Syntax: **`>add-stat (name) (stat) (amount)`\nAka a-s")
			embed.add_field(name="Set-Stat", 			value="Sets a given character's statistic to a value\n**Syntax:**`>set-stat (name) (stat) (amount) [stat2] [amount2] ...`\nAka s-s")
			embed.add_field(name="Generate-Skills", 	value="Generates the initial skill values for a no-bonus character.\n**Syntax: **`>generate-skills (name) (skill1 skill2 ...)`\nAka g-s")
			embed.add_field(name="Add-Skills", 			value="Adds a number to a skill level.\n**Syntax: **`>add-skills (name) (skill1) (value1) [skill2] [value2]...`\nAka a-s")
			embed.add_field(name="Remove-Skills", 		value="Remove a skill from a character.\n**Syntax: **`>remove-skills (name) (skill)`\nAka rm-s")
			embed.add_field(name="Delete-Character", 	value="Deletes a character.\n**Syntax: **`>delete-character (name)`\nAka d-c")
			embed.add_field(name="Set-Race", 			value="Sets the character race to another specified value.\n**Syntax: **`>set-race (name) (new race)`\nAka s-r")
			embed.add_field(name="Rename-Character", 	value="Renames a character to a new name.\n**Syntax: **`>rename-character (name) (new name)`\nAka r-c")
			embed.add_field(name="Add-Ability", 		value="Adds an ability to the character.\n**Syntax: **`>add-ability (name) (ability) [ability 2] ...`\nAka a-a")
			embed.add_field(name="Level-Ability", 		value="Adds levels to an ability.\n**Syntax: **`>level-ability (name) (ability) (amount)`\nAka l-a")
			embed.add_field(name="Remove-Ability",	 	value="Removes an ability from a character's abilities.\n**Syntax: **`>remove-ability (name) (ability)`\nAka rm-a")
			embed.add_field(name="Add-Currency", 		value="Adds a currency amount (positive or negative), to a player character's currencies\n**Syntax:**`>add-currency (name) (currency abbreviation) (amount)`\nAka a-cu")
			embed.add_field(name="Remove-Currency", 	value="Removes a currency from a character.\n**Syntax: **`>remove-currency (name) (currency abbreviation)`Aka rm-c")
			embed.add_field(name="Page 2", 				value="Flip to Page 2 with `>help Characters 2`", inline=False)
		elif page == 2:
			embed.add_field(name="Add-Energy", 			value="Adds an energy type to a character.\n**Syntax: **`>add-energy (name) (energy abbreviation) [Starting maximum, default 100. Automatically based on Wis x 5 if is MP or EP.]`\nAka a-e")
			embed.add_field(name="Remove-Energy", 		value="Removes an energy type from a character.\n**Syntax: **`>remove-energy (name) (energy abbreviation)`\nAka rm-e")
			embed.add_field(name="Add-Title", 			value="Adds a title to a character.\n**Syntax: **`>add-title (name) (title name)`\nAka a-t",inline=False)
			embed.add_field(name="Remove-Title", 		value="Removes a title from a character.\n**Syntax: **`>remove-title (name) (title name)`\nAka rm-t")
			
			
	elif entry == "rolls":
		embed.add_field(name="Roll", value="This command is basically a calculator that has the 4 basic arithmetic operations, and an extra operation for rolling dice.\nSyntax:\n"+
					   	"`Addition: 			[value] + [value]`\n" +
					   	"`Subtraction: 		 [value] - [value]`\n" +
					   	"`Multiplication: 	  [value] * [value]`\n" +
					   	"`Division: 			[value] / [value]`\n" +
					   	"`Rolling: 			 [value]d[value]`\n" +
						"To use brackets, write `([expression])`.\n" +
					   	"To use the command, type `>roll [expression]`, the roll command is going to automatically cut off after the 12th roll, to show all the rolls, put `NL` (stands for no limit) **at the start** of the expression (CAPITALIZATION MATTERS).\n"+
					   	"Here is an example of the NL header used in an expression:\n`>roll NL 20d6 + 5 - 15d4`.")
	elif entry == "antiraid":
		embed.add_field(name="Anti-Scam", 				value="Automatic bot action that deletes server invites in places you don't want them, and deletes scam messages sent by other bots. Anti-scam does not activate in categories named \"RP Hubs\" or in channels named \"partners.\"", inline=False)
		embed.add_field(name="Anti-Moderation Abuse", 	value="Bot detects moderation abuse, where a user may be deleting too many things at once. By forcing lower-ranked moderators to restrict their channel deletions and bans to 3 within a minute, the bot restricts the speed of raiders. In the case this is violated, the moderator is immediately banned.")
	else:
		embed.add_field(name="Help", 		value="This command!")
		embed.add_field(name="Randog", 		value="Generates a random dog image, ranked with different rarities.")
		embed.add_field(name="Dogsleep", 	value="Sends the sleeping Tim", inline=True)
		embed.add_field(name="Antiraid", 	value="Use >help Antiraid for more info.", inline=False)
		embed.add_field(name="Characters", 	value="Use >help Characters for more info.", inline=False)
		embed.add_field(name="Rolls", 		value="use >help Rolls for more info.", inline=False)
		embed.add_field(name="Moderation", 	value="use >help Mod for more info.", inline=False)
		# Add a translate command becuase why not
	await ctx.send(embed=embed)
	
#Sends image of Retro's dog asleep
@bot.command(name="dogsleep", pass_context=True)
async def dogsleep(ctx):
	await ctx.send("Sleeping Tim!")
	await ctx.send(file=discord.File('images/dogsleep.jpeg'))

# Translate command
"""@bot.command(name="translate", pass_context=True)	
@commands.cooldown(1, 5, commands.BucketType.user)
async def translate(ctx, language, *args):"""
	


#Moderation Commands
@bot.command(name="purge", pass_context=True)
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def purge(ctx, amount = None):
	if (amount == None):
		await ctx.send("Sorry, cannot delete an unspecified amount of messages")
		return "";
	elif (int(amount) > 20):
		await ctx.send("Sorry, you cannot delete more than 20 messages")
		return "";
	await ctx.channel.purge(limit= (int(amount) + 1))

@bot.command(name="unban", pass_context=True)
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 15, commands.BucketType.user)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"Unbanned: {user.mention}")



@bot.command(name="ban", pass_context=True)
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 15, commands.BucketType.user)
async def ban(ctx, member:discord.Member, *reason):
	actual_reason = " ".join(reason)
	
	if actual_reason == "":
		await ctx.send("Do not ban a member for no reason.")
		return
	await ctx.guild.ban(member, reason = actual_reason)
	await ctx.send("Banned " + member.name)


@bot.command(name="roleban", pass_context=True)
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.has_permissions(manage_roles=True)
async def roleban(ctx, member:discord.Member, reason=None):
	role = discord.utils.find(lambda r: r.name == "Lesser Agent", ctx.message.guild.roles)
	role2 = discord.utils.find(lambda r: r.name == "Greater Agent", ctx.message.guild.roles)
	role3 = discord.utils.find(lambda r: r.name == "Grand Agent", ctx.message.guild.roles)
	role4 = discord.utils.find(lambda r: r.name == "Prime Agent", ctx.message.guild.roles)
	if (role not in member.roles) and (role2 not in member.roles) and (role3 not in member.roles) and (role4 not in member.roles):
		roleban = discord.utils.get(member.guild.roles, name="Roleban")
		await member.edit(roles=[roleban])
		string = member.name + " has been rolebanned"
		if reason != None:
			string += " for " + reason + "."
		else:
			string += "."
		await ctx.send(string)
	else:
		await ctx.send("The user is a staff member. That is not allowed.")

@bot.command(name="unroleban", pass_context=True)
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.has_permissions(manage_roles=True)
async def unroleban(ctx, member:discord.Member, reason=None):
	role = discord.utils.find(lambda r: r.name == "Roleban", ctx.message.guild.roles)
	role2 = discord.utils.find(lambda r: r.name == "Unverified", ctx.message.guild.roles)
	try:
		if role in member.roles:
			await member.edit(roles=[role2])
			await ctx.send(member.name + " has been removed from roleban.")
		else:
			await ctx.send(member.name + " is not rolebanned.")
	except:
		await ctx.send(member.name + " is not rolebanned.")

#Fortress-Specific commands and functions
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
			te = " [ Item Bonus: " + str((val + valueDict["Con"]) * 10) + "/" + str((val + valueDict["Con"]) * 10) + " ]"
	elif stat == "MP" or stat == "EP":
		wisBonus = dict(bonuses["Wis"])
		if len(wisBonus) != 0:
			val = 0
			for value in wisBonus.values():
				val += value
			te = " [ Item Bonus: " + str((val + valueDict["Wis"]) * 5) + "/" + str((val + valueDict["Wis"]) * 5) + " ]"
	return te

def returnCharacterRank(valueDict):
	
	value = valueDict["Str"] + valueDict["Con"] + valueDict["Dex"] + valueDict["Agi"] + valueDict["Per"] + valueDict["Int"] + valueDict["Wis"]
	thresholds = {10:"F-", 25:"F", 35:"F+", 55:"D-", 125:"D", 200:"D+", 860:"C-", 1060:"C", 2200:"C+", 3440:"B-", 6000:"B", 9000:"B+", 125000:"A-", 160000:"A", 206000:"A+", 250800:"S-", 311400:"S", 382000:"S+", 447600:"S++", 584070:"S+++", 700000:"SS-", 858000:"SS", 970000:"SS+", 1021000:"SS++", 1236000:"SS+++", 1480000:"SSS-", 1884500:"SSS", 2440500:"SSS+", 3040200:"SSS++", 3956000:"SSS+++", 4100000:"X-", 5380900:"X", 6815000:"X+"}
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
			skillThresholds = {0:"Unskilled ", 15:"Novice ", 30:"Apprentice ", 50:"Journeyman ", 65:"Adept ", 80:"Minor ", 95:"Major ", 110:"Expert ", 125:"Master ", 140:"Grandmaster ", 180:"Legendary ", 200:"Ascendant ", 250:"Transcendant ", 400:"Eminent ", 401:"Peerless "}
			sinVirtThresholds = {25:"", 50:"Knight of ", 75:"Lord of ", 100:"Baron of ", 125:"Viscount of ", 150:"Count of ", 175:"Earl of ", 200:"Marquis of ", 225:"Duke of ", 250:"King of ", 275:"Emperor of ", 300:"Dominion of ", 325:"Symbol of ", 350:"Incarnation of ", 375:"Soulborne of ", 400:"Embodiment of ", 401:"Epitome of "}
			sinVirts = ["Lust", "Gluttony", "Greed", "Pride", "Wrath", "Sloth", "Envy", "Justice", "Bravery", "Charity", "Kindness", "Patience", "Hope", "Faith"]
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
	val = [
			1000, 900, 500, 400,
			100, 90, 50, 40,
			10, 9, 5, 4,
			1]
	syb = [
			"M", "CM", "D", "CD",
			"C", "XC", "L", "XL",
			"X", "IX", "V", "IV",
			"I"]
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
            inp[n] = i.title()
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
			string += "\n**" + key + "**: " + str(value[0]) + "/" + str(value[1])
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

@bot.command(name="create-character", pass_context=True, aliases=["create-c", "Create-Character", "Create-character"])
@commands.has_permissions(manage_roles=True)
async def createCharacter(ctx, name="", race="", sinVirtue=""):
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
	playerDict = {"Name":name, "Race":race, "Sin/Virtue":sinVirtue, "Str":randint(11, 30), "Con":con, "Dex":randint(11, 30), "Agi":randint(11, 30), "Per":randint(11, 30), "Int":randint(11, 30), "Wis":wis, "Current HP":con*10, "Max HP":con*10, "Energies":{"MP":[wis*5, wis*5]}, "Titles":[startingTitle], "Skills":{}, "Abilities":{}, "Item Bonuses":{"Str":{}, "Con":{}, "Dex":{}, "Agi":{}, "Per":{}, "Int":{}, "Wis":{}}, "Currencies":{}}
	db[str(ctx.guild.id)][name.title()] = playerDict
	temp = db[str(ctx.guild.id)][name]
	bonuses = temp["Item Bonuses"]
	playerDict.update({"Stat String":("**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"]) + returnEnergies(temp) + "\n\n**Str**: " + str(temp["Str"]) + " " + returnItemBonusDict(bonuses, "Str") + "\n**Con**: " + str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") + "\n**Dex**: " + str(temp["Dex"]) + " " + returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " + str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") + "\n**Per**: " + str(temp["Per"]) + " " + returnItemBonusDict(bonuses, "Per") + "\n**Int**: " + str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") + "\n**Wis**: " + str(temp["Wis"]) + " " + returnItemBonusDict(bonuses, "Wis"))})
	db[str(ctx.guild.id)][name.title()] = playerDict
	await ctx.send("Created character " + name)

@bot.command(name="check-character", pass_context=True, aliases=["c-c", "Check-Character", "Check-character"])
async def checkCharacter(ctx, name="", inSetStats=False):
	name = name.title()
	if name not in db[str(ctx.guild.id)].keys():
		await ctx.send(name + " is not a generated character.")
		return
	temp = db[str(ctx.guild.id)][name]
	embed = discord.Embed(title=(name + "'s Character Sheet"), description=("The following is their Astral Fantasy character sheet:\n" + temp["Name"] + ":"))
	titlesString = ""
	for i in temp["Titles"]:
		titlesString += i
		if i != temp["Titles"][-1]:
			titlesString += ", "
	embed.add_field(name="Titles", value=titlesString, inline=False)
	embed.add_field(name="Rank", value=returnCharacterRank(temp), inline=False)
	embed.add_field(name="Money", value=returnMoney(temp), inline=False)
	embed.add_field(name="Core Stats", value=temp["Stat String"], inline=False)
	embed.add_field(name="Skills:", value=returnSkills(temp), inline=False)
	embed.add_field(name="Abilities:", value=returnAbilities(temp), inline=False)
	if inSetStats:
		return embed
	else:
		await ctx.send(embed=embed)

@bot.command(name="copy-character", pass_context=True, aliases=["cc-c"])
@commands.has_permissions(administrator=True)
async def copyCharacter(ctx, fromID=0, toID=0, name=""):
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
	
	


@bot.command(name="add-stat", pass_context=True, aliases=["a-s", "Add-Stat", "Add-stat"])
@commands.has_permissions(administrator=True)
async def addStat(ctx, name="", *furtherStats):
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
			stat = {"Strength":"Str", "Constitution":"Con", "Dexterity":"Dex", "Agility":"Agi", "Perception":"Per", "Intelligence":"Int", "Wisdom":"Wis"}[stat]
		except:
			pass
		try:
			amount = int(furtherStats[i+1])
			i += 2
		except:
			await ctx.send("Amount for stat entered is not a valid integer or does not exist.")
			i += 2
		temp[stat] += amount
		if "Current MP" in temp.keys():
			temp.update({"Energies":{"MP":[temp["Wis"]*5, temp["Wis"]*5]}})
			del temp["Current MP"]
			del temp["Max MP"]
		if stat == "Con":
			temp["Current HP"] = temp[stat] * 10
			temp["Max HP"] = temp[stat] * 10
		elif stat == "Wis":
			if "MP" in temp["Energies"].keys() and "EP" in temp["Energies"].keys():
				temp["Energies"]["MP"] = [temp[stat] * 5, temp[stat] * 5]
				temp["Energies"]["EP"] = [temp[stat] * 5, temp[stat] * 5]
			elif "MP" in temp["Energies"].keys():
				temp["Energies"]["MP"] = [temp[stat] * 5, temp[stat] * 5]
			elif "EP" in temp["Energies"].keys():
				temp["Energies"]["EP"] = [temp[stat] * 5, temp[stat] * 5]
	temp["Stat String"] = ("**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"])  + returnItemBonusBar(temp, "HP") + returnEnergies(temp) + "\n\n**Str**: " + str(temp["Str"]) + " " + 
returnItemBonusDict(bonuses, "Str") + "\n**Con**: " + str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") + "\n**Dex**: " + str(temp["Dex"]) + " " + returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " + str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") + "\n**Per**: " + str(temp["Per"]) + " " + returnItemBonusDict(bonuses, "Per") + "\n**Int**: " + str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") + "\n**Wis**: " + str(temp["Wis"]) + " " + returnItemBonusDict(bonuses, "Wis"))
	
	embed = discord.Embed(title=(name + "'s Character Sheet"), description=("The following is their Astral Fantasy character sheet:\n" + temp["Name"] + ":"))
	titlesString = ""
	for i in temp["Titles"]:
		titlesString += i
		if i != temp["Titles"][-1]:
			titlesString += ", "
	embed.add_field(name="Titles", value=titlesString, inline=False)
	embed.add_field(name="Rank", value=returnCharacterRank(temp), inline=False)
    
	embed.add_field(name="Money", value=returnMoney(temp), inline=False)
	embed.add_field(name="Core Stats", value=temp["Stat String"], inline=False)
	embed.add_field(name="Skills:", value=returnSkills(temp), inline=False)
	embed.add_field(name="Abilities:", value=returnAbilities(temp), inline=False)
	await ctx.send(embed=embed)

@bot.command(name="set-stat", pass_context=True, aliases=["s-s", "Set-Stat", "Set-stat"])
@commands.has_permissions(administrator=True)
async def setStat(ctx, name="", *furtherStats):
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
			stat = {"Strength":"Str", "Constitution":"Con", "Dexterity":"Dex", "Agility":"Agi", "Perception":"Per", "Intelligence":"Int", "Wisdom":"Wis"}[stat]
		except:
			pass
		if stat not in temp.keys():
			await ctx.send(stat + " is not a valid statistic.")
			i += 2
		try:
			amount = int(furtherStats[i+1])
			i += 2
		except:
			await ctx.send("Amount for stat entered is not a valid integer or does not exist.")
			i += 2
		temp[stat] = amount
		if "Current MP" in temp.keys():
			temp.update({"Energies":{"MP":[temp["Wis"]*5, temp["Wis"]*5]}})
			del temp["Current MP"]
			del temp["Max MP"]
		if stat == "Con":
			temp["Current HP"] = temp[stat] * 10
			temp["Max HP"] = temp[stat] * 10
		elif stat == "Wis":
			if "MP" in temp["Energies"].keys() and "EP" in temp["Energies"].keys():
				temp["Energies"]["MP"] = [temp[stat] * 5, temp[stat] * 5]
				temp["Energies"]["EP"] = [temp[stat] * 5, temp[stat] * 5]
			elif "MP" in temp["Energies"].keys():
				temp["Energies"]["MP"] = [temp[stat] * 5, temp[stat] * 5]
			elif "EP" in temp["Energies"].keys():
				temp["Energies"]["EP"] = [temp[stat] * 5, temp[stat] * 5]
	temp["Stat String"] = ("**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"])  + returnItemBonusBar(temp, "HP") + returnEnergies(temp) + "\n\n**Str**: " + str(temp["Str"]) + " " + 
returnItemBonusDict(bonuses, "Str") + "\n**Con**: " + str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") + "\n**Dex**: " + str(temp["Dex"]) + " " + returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " + str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") + "\n**Per**: " + str(temp["Per"]) + " " + returnItemBonusDict(bonuses, "Per") + "\n**Int**: " + str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") + "\n**Wis**: " + str(temp["Wis"]) + " " + returnItemBonusDict(bonuses, "Wis"))
	
	embed = discord.Embed(title=(name + "'s Character Sheet"), description=("The following is their Astral Fantasy character sheet:\n" + temp["Name"] + ":"))
	titlesString = ""
	for i in temp["Titles"]:
		titlesString += i
		if i != temp["Titles"][-1]:
			titlesString += ", "
	embed.add_field(name="Titles", value=titlesString, inline=False)
	embed.add_field(name="Rank", value=returnCharacterRank(temp), inline=False)
	embed.add_field(name="Money", value=returnMoney(temp), inline=False)
	embed.add_field(name="Core Stats", value=temp["Stat String"], inline=False)
	embed.add_field(name="Skills:", value=returnSkills(temp), inline=False)
	embed.add_field(name="Abilities:", value=returnAbilities(temp), inline=False)
	await ctx.send(embed=embed)

def find_nth(haystack, needle, n):
	start = haystack.find(needle)
	while start >= 0 and n > 1:
		start = haystack.find(needle, start+len(needle))
		n -= 1
	return start
	
# Implement commands

@bot.command(name="rename-character", pass_context=True, aliases=["r-c", "Rename-Character", "Rename-character"])
@commands.has_permissions(administrator=True)
async def renameCharacter(ctx, name="", newName=""):
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

@bot.command(name="list-characters", pass_context=True, aliases=["l-c", "List-Characters", "List-characters"])
@commands.cooldown(1, 30, commands.BucketType.guild)
async def listCharacters(ctx, page=0):
	totalList = list(db[str(ctx.guild.id)].keys())
	string = ""
	thisList = totalList[10*page:10*(page+1)]
	for i in thisList:
		string += i + "\n"
	await ctx.send(string)

@listCharacters.error
async def listCharactersError(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f'Command "list-character" is on cooldown, you can use it in {round(error.retry_after, 2)} seconds.')

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.MissingPermissions):
		await ctx.send("You do not have the required roles to run this command.")

@bot.command(name="set-race", pass_context=True, aliases=["s-r", "Set-Race", "Set-race"])
@commands.has_permissions(administrator=True)
async def setRace(ctx, name="", race=""):
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


"""
Hi fallen, I will be AFK for a bit, while I am AFK, DO NOT TOUCH THE ROLL COMMAND AT ALL.
I will need to adjust some things before copying it to here.
"""

@bot.command(name = "roll", pass_context=True, aliases=["Roll", "calculate", "Calculate", "calc", "Calc"])
async def roll(ctx, *args):
	try:
		global do_roll_limit
		do_roll_limit = True
		
		if (args[0] == "NL"):
			args = args[1::]
			do_roll_limit = False
			pass
		
		message_inp = "";
	
		for i in args:
			message_inp += i + " "
	
		parsed = parser.parse(message_inp)
		compiled = compile(parsed)

		if (ctx.message.author.id == 423798867868516373):
			embed = discord.Embed(title = "Rolling:" , description = compiled[1] + " - ∞" + "\nSum: -∞", color = 0x33FBFF)
			embed.set_thumbnail(url="https://media.discordapp.net/attachments/843632677533777940/980579446371258418/PngItem_1087634.png?width=2138&height=1404")
		else:
			embed = discord.Embed(title = "Rolling:" , description = compiled[1] + "\nSum: " + str(compiled[0]), color = 0x33FBFF)
			embed.set_thumbnail(url="https://media.discordapp.net/attachments/843632677533777940/980579446371258418/PngItem_1087634.png?width=2138&height=1404")
			#embed.add_field(name="Blah", value="yes")
		await ctx.send(embed=embed)
	except:
		await ctx.send("An error occurred while trying to execute the command, please use >help Rolls and check the syntax and grammar, if you cannot find the mistake, please contact the bot developers.")
	
@bot.command(name="generate-skills", pass_context=True, aliases=["g-s", "Generate-Skills", "Generate-skills"])
@commands.has_permissions(administrator=True)
async def generateInitialSkills(ctx, name="", *skillsList):
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
				listString[i.index("'") + 1] = listString[i.index("'") + 1].lower()
				value = ""
				for n in listString:
					value += n
				i = value
		except:
			pass
		temp["Skills"].update({i:randint(1,16)+15})
	
	await ctx.send(name + "'s Skills have been updated.")

@bot.command(name="remove-skills", pass_context=True, aliases=["rm-s", "Remove-Skills", "Remove-skills"])
@commands.has_permissions(administrator=True)
async def removeSkills(ctx, name="", skill=""):
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

@bot.command(name="add-skills", pass_context=True, aliases=["a-skills", "a-sk", "Add-Skills", "Add-skills"])
@commands.has_permissions(administrator=True)
async def addToSkills(ctx, name, *skills):
	name = name.title()
	if name not in db[str(ctx.guild.id)].keys():
		await ctx.send(name + " is not a generated character.")
		return
	temp = db[str(ctx.guild.id)][name]
	for i in range(0, len(skills)-1):
		try:
			if type(int(skills[i])) == int:
				continue
		except:
			val = skills[i].title()
			if val in temp["Skills"]:
				temp["Skills"][val] += int(skills[i+1])
			else:
				temp["Skills"].update({val:int(skills[i+1])})
	await ctx.send(name + "'s Skills have been updated.")


@bot.command(name="delete-character", pass_context=True, aliases=["d-c", "rm-c", "Delete-Character", "Delete-character"])
@commands.has_permissions(administrator=True)
async def deleteCharacter(ctx, name=""):
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

@bot.command(name="add-title", pass_context=True, aliases=["a-t", "Add-Title", "Add-title"])
@commands.has_permissions(administrator=True)
async def addTitle(ctx, name="", title=""):
	name = name.title()
	if name == "":
		await ctx.send("Please input a name.")
		return
	if title == "":
		await ctx.send("Please input a title to add.")
		return
	temp = db[str(ctx.guild.id)][name]
	temp["Titles"].append(title)
	await ctx.send(title + " has been added to " + name + "'s titles.")

@bot.command(name="remove-title", pass_context=True, aliases=["rm-t", "Remove-Title", "Remove-title"])
@commands.has_permissions(administrator=True)
async def removeTitle(ctx, name="", title=""):
	name = name.title()
	if name == "":
		await ctx.send("Please input a name.")
		return
	temp = db[str(ctx.guild.id)][name]
	if title not in temp["Titles"]:
		await ctx.send(title + " is not one of " + name + "'s titles.")
		return
	temp["Titles"].remove(title)
	await ctx.send(title + " has been removed from " + name + "'s titles.")


@bot.command(name="add-ability", pass_context=True, aliases=["a-a", "Add-Ability", "Add-ability"])
@commands.has_permissions(administrator=True)
async def addAbility(ctx, name="", *abilities):
    name = name.title()
    if name not in db[str(ctx.guild.id)].keys():
        await ctx.send(name + " is not a valid character.")
        return
    temp = db[str(ctx.guild.id)][name]
    a = dict(temp["Abilities"])
    for i in abilities:
        i = properTitle(i)
        a.update({i:1})
    temp["Abilities"] = a
    await ctx.send("Added to " + name + "'s abilities")

@bot.command(name="level-ability", pass_context=True, aliases=["l-a", "Level-Ability", "Level-ability"])
@commands.has_permissions(administrator=True)
async def levelAbility(ctx, name="", ability="", level=0):
	name = name.title()
	if name not in db[str(ctx.guild.id)].keys():
		await ctx.send(name + " is not a valid character.")
		return
	temp = db[str(ctx.guild.id)][name]
	ability = ability.title()
	if ability not in temp["Abilities"]:
		await ctx.send(ability + " is not one of " + name + "'s abilities.")
		return
	if level == 0:
		await ctx.send("Please enter a level to add.")
		return
	temp["Abilities"][ability] += level
	await ctx.send("Edited " + name + "'s abilities.")

@bot.command(name="remove-ability", pass_context=True, aliases=["rm-a", "Remove-Ability", "Remove-ability"])
@commands.has_permissions(administrator=True)
async def removeAbility(ctx, name="", ability=""):
	name = name.title()
	ability = ability.title()
	if name not in db[str(ctx.guild.id)].keys():
		await ctx.send(name + " is not a valid character.")
		return
	temp = db[str(ctx.guild.id)][name]
	if ability not in temp["Abilities"]:
		await ctx.send(ability + " is not one of " + name + "'s abilities.")
		return
	temp["Abilities"].pop(ability)
	await ctx.send("Removed " + ability + " from " + name + "'s abilities.")

@bot.command(name="add-energy", pass_context=True, aliases=["a-e", "Add-Energy", "Add-energy"])
@commands.has_permissions(administrator=True)
async def addEnergy(ctx, name="", energy="", startingMaximum=100):
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
		await ctx.send("The energy type requested is already in " + name + "'s possession.")
		return
	if energy in ["MP", "EP"]:
		startingMaximum = temp["Wis"] * 5
	temp["Energies"].update({energy:[startingMaximum, startingMaximum]})
	bonuses = temp["Item Bonuses"]
	if "MP" in temp["Energies"].keys() and "EP" in temp["Energies"].keys():
		temp["Energies"]["MP"] = [temp["Wis"] * 5, temp["Wis"] * 5]
		temp["Energies"]["EP"] = [temp["Wis"] * 5, temp["Wis"] * 5]
	elif "MP" in temp["Energies"].keys():
		temp["Energies"]["MP"] = [temp["Wis"] * 5, temp["Wis"] * 5]
	elif "EP" in temp["Energies"].keys():
		temp["Energies"]["EP"] = [temp["Wis"] * 5, temp["Wis"] * 5]
	temp["Stat String"] = ("**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"])  + returnItemBonusBar(temp, "HP") + returnEnergies(temp) + "\n\n**Str**: " + str(temp["Str"]) + " " + 
returnItemBonusDict(bonuses, "Str") + "\n**Con**: " + str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") + "\n**Dex**: " + str(temp["Dex"]) + " " + returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " + str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") + "\n**Per**: " + str(temp["Per"]) + " " + returnItemBonusDict(bonuses, "Per") + "\n**Int**: " + str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") + "\n**Wis**: " + str(temp["Wis"]) + " " + returnItemBonusDict(bonuses, "Wis"))
	await ctx.send("Added " + energy + " to " + name + ".")

@bot.command(name="remove-energy", pass_context=True, aliases=["rm-e", "Remove-Energy", "Remove-energy"])
@commands.has_permissions(administrator=True)
async def removeEnergy(ctx, name="", energy=""):
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
	temp["Stat String"] = ("**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"])  + returnItemBonusBar(temp, "HP") + returnEnergies(temp) + "\n\n**Str**: " + str(temp["Str"]) + " " + 
returnItemBonusDict(bonuses, "Str") + "\n**Con**: " + str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") + "\n**Dex**: " + str(temp["Dex"]) + " " + returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " + str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") + "\n**Per**: " + str(temp["Per"]) + " " + returnItemBonusDict(bonuses, "Per") + "\n**Int**: " + str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") + "\n**Wis**: " + str(temp["Wis"]) + " " + returnItemBonusDict(bonuses, "Wis"))
	await ctx.send("Removed " + energy + " from " + name + ".")
	
@bot.command(name="add-currency", pass_context=True, aliases=["a-cu", "Add-Currency", "Add-currency"])
@commands.has_permissions(administrator=True)
async def addCurrency(ctx, name="", currency="", amount=0):
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
		temp.update({"Currencies":{}})
	if currency in temp["Currencies"].keys():
		temp["Currencies"][currency] += amount
		await ctx.send("Added " + str(amount) + " to " + name + "'s " + currency + ".")
		return
	else:
		temp["Currencies"].update({currency:amount})
		await ctx.send("Added " + str(amount) + " to " + name + "'s " + currency + ".")
		return

@bot.command(name="remove-currency", pass_context=True, aliases=["rm-cu", "Remove-Currency", "Remove-currency"])
@commands.has_permissions(administrator=True)
async def removeCurrency(ctx, name="", currency=""):
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

@bot.command(name="add-item-bonus", pass_context=True, aliases=["a-ib", "a-i-b", "Add-Item-Bonus", "Add-item-bonus"])
@commands.has_permissions(administrator=True)
async def addItemBonus(ctx, name="", itemBonusName="", bonusStat="", bonusAmount=0):
	name = name.title()
	if name not in db[str(ctx.guild.id)].keys():
		await ctx.send(name + " is not a valid character.")
		return
	temp = db[str(ctx.guild.id)][name]
	if itemBonusName == "":
		await ctx.send("Please enter a proper name for the item bonus.")
		return
	if bonusStat == "":
		await ctx.send("Please enter a statistic for this bonus to be added to.")
		return
	bonusStat = bonusStat.title()
	try:
		bonusStat = {"Strength":"Str", "Constitution":"Con", "Dexterity":"Dex", "Agility":"Agi", "Perception":"Per", "Intelligence":"Int", "Wisdom":"Wis"}[bonusStat]
	except:
		pass
	if bonusStat not in temp.keys():
		await ctx.send(bonusStat + " is not a valid statistic.")
		return
	try:
		if int(bonusAmount) == 0:
			await ctx.send("Please enter a number greater than or less than 0 for the bonus amount.")
			return
		bonusAmount = int(bonusAmount)
	except:
		await ctx.send("Enter an integer as the bonus amount.")
		return

	temporaryDict = temp["Item Bonuses"][bonusStat]
	temporaryDict.update({itemBonusName:bonusAmount})
	temp["Item Bonuses"][bonusStat] = temporaryDict
	bonuses = temp["Item Bonuses"]
	temp["Stat String"] = ("**HP**: " + str(temp["Current HP"]) + "/" + str(temp["Max HP"])  + returnItemBonusBar(temp, "HP") + returnEnergies(temp) + "\n\n**Str**: " + str(temp["Str"]) + " " + 
returnItemBonusDict(bonuses, "Str") + "\n**Con**: " + str(temp["Con"]) + " " + returnItemBonusDict(bonuses, "Con") + "\n**Dex**: " + str(temp["Dex"]) + " " + returnItemBonusDict(bonuses, "Dex") + "\n**Agi**: " + str(temp["Agi"]) + " " + returnItemBonusDict(bonuses, "Agi") + "\n**Per**: " + str(temp["Per"]) + " " + returnItemBonusDict(bonuses, "Per") + "\n**Int**: " + str(temp["Int"]) + " " + returnItemBonusDict(bonuses, "Int") + "\n**Wis**: " + str(temp["Wis"]) + " " + returnItemBonusDict(bonuses, "Wis"))
	await ctx.send(name + "'s item bonus for " + bonusStat + " has been updated to " + itemBonusName + " with an amount of " + str(bonusAmount) + ".")

#Remove item bonus command

@bot.command(name="remove-item-bonus", pass_context=True, aliases=["rm-ib", "rm-i-b", "Remove-Item-Bonus", "Remove-item-bonus"])
@commands.has_permissions(administrator=True)
async def removeItemBonus(ctx, name="", stat="", bonusName=""):
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
		await ctx.send(bonusName + " is not an item bonus existant on " + stat + " for " + name + ".")
		return
	valueDict.pop(bonusName)
	temp["Item Bonuses"][stat] = valueDict
	await ctx.send("Removed " + bonusName + " from " + stat + " of " + name + ".")
	
#Add qi command

#Set qi level command

#Set qi tempering command

#Remove qi command

def getStatTotals(receivedDict):
	mySum = 0
	receivedDict = dict(receivedDict)
	for i in ("Str", "Con", "Dex", "Agi", "Per", "Int", "Wis"):
		mySum += receivedDict[i]
	return mySum

@bot.command(name="leaderboard", pass_context=True, aliases=["Leaderboard", "lb", "LB"])
async def playerLeaderboard(ctx, lbType="Stats"):
	lbType = lbType.title()
	temp = db[str(ctx.guild.id)]
	topTen = []
	if lbType == "Stats":
		x = dict(sorted(temp, key=lambda n: getStatTotals(temp[n])))
		iteration = 0
		while len(topTen) <= 10:
			try:
				topTen.append((list(x.keys())[iteration], returnCharacterRank(list(x.values()[iteration])), getStatTotals(dict(list(x.items())[iteration]))))
				iteration += 1
			except KeyError:
				break
	else:
		await ctx.send("Not a valid leaderboard type.")
	totalString = ""
	for i in topTen:
		strin = ""
		for j in i:
			if j != i[-1]:
				strin += j + ", "
			else:
				strin += j
		totalString += strin + "\n"
	await ctx.send(totalString)
		

"""def testLeaderboard(lbType="Stats"):
	lbType = lbType.title()
	temp = dict(db["Astral Fantasy (The Fortress)"])
	print(temp)
	topTen = []
	if lbType == "Stats":
		x = dict(sorted(temp.items(), key=lambda n: getStatTotals(dict(temp[n]))))
		iteration = 0
		while len(topTen) <= 10:
			try:
				topTen.append((list(x.keys())[iteration], returnCharacterRank(list(x.values()[iteration])), getStatTotals(dict(list(x.items())[iteration]))))
				iteration += 1
			except KeyError:
				break
	else:
		print("Not a valid leaderboard type.")
	totalString = ""
	for i in topTen:
		strin = ""
		for j in i:
			if j != i[-1]:
				strin += j + ", "
			else:
				strin += j
		totalString += strin + "\n"
	print(totalString)

testLeaderboard()"""

@bot.command(name="randog", pass_context=True)
async def randog(ctx, index = None):
	role = discord.utils.find(lambda r: r.name == 'Bot Dev', ctx.message.guild.roles)
	#print(role in ctx.message.author.roles)
	
	if ((role in ctx.message.author.roles) or (ctx.message.author.id in [420604478949949452, 454820620824215553])) and (index != None):
		
		if (timPics[int(index)].rarity == 1):
			rarity = "Legendary"
		elif (timPics[int(index)].rarity <= 3):
			rarity = "Rare"
		elif (timPics[int(index)].rarity <= 5):
			rarity = "Special"
		elif (timPics[int(index)].rarity <= 10):
			rarity = "Uncommon"
		else:
			rarity = "Common"
		
		await ctx.send(rarity + " Dog: " + timPics[int(index)].name)
		await ctx.send(file = discord.File(timPics[int(index)].picture))
	else:	
		sum = 0
		for i in timPics:
			sum += i.rarity
	
		pic_ind = randint(0, sum);
	
		pic_sum = 0
		curr_pic = -1
	
		while (pic_sum < pic_ind):
			curr_pic += 1
			pic_sum += timPics[curr_pic].rarity
	
		rarity = ""
		if (timPics[curr_pic].rarity == 1):
			rarity = "Legendary"
		elif (timPics[curr_pic].rarity <= 3):
			rarity = "Rare"
		elif (timPics[curr_pic].rarity <= 5):
			rarity = "Special"
		elif (timPics[curr_pic].rarity <= 10):
			rarity = "Uncommon"
		else:
			rarity = "Common"
	
		await ctx.send(rarity + " Dog: " + timPics[curr_pic].name)
		await ctx.send(file = discord.File(timPics[curr_pic].picture))

"""@bot.command(name="allperms", pass_contest=True)
async def allPerms(ctx, roleName="Roleban"):
    guild = ctx.guild
    # if permission == "":
    #     await ctx.send("Please enter a permission name.")
    role = discord.utils.get(guild.roles, name=roleName)
    for channel in guild.text_channels:
        await channel.set_permissions(role, view_channel=False)"""
        



print(db.keys())

# Data Migration Code

# db["846225388551405590"] = {}
# placeholder = dict(db["Astral Fantasy (The Fortress)"])
# for key1, val1 in placeholder.items():
# 	val1 = dict(val1)
# 	val1["Energies"] = dict(val1["Energies"])
# 	for key2, val2 in val1["Energies"].items():
# 		val1["Energies"][key2] = list(val2)
# 	val1["Titles"] = list(val1["Titles"])
# 	val1["Skills"] = dict(val1["Skills"])
# 	val1["Currencies"] = dict(val1["Currencies"])
# 	val1["Abilities"] = dict(val1["Abilities"])
# 	val1["Item Bonuses"] = dict(val1["Item Bonuses"])
# 	for key2, val2 in val1["Item Bonuses"].items():
# 		val1["Item Bonuses"][key2] = dict(val2)
# 	db["846225388551405590"][key1] = val1

# print(db["846225388551405590"] == db["Astral Fantasy (The Fortress)"])

bot.run(token)
