import random
# import string
from replit import db
from random import randint
import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import os
from ply.lex import lex
from ply.yacc import yacc
# import json
token = os.getenv('token')

import keepalive
# import time

from characterManager import CharacterCog

keepalive.awake("https://Astral-Defender.plasmium.repl.co")

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
	
	if (sides > 1000):
		sides = 1000

	if (rolls > 1000):
		rolls = 1000
	
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
t_NUMBER    = r'[0-9]+(\.([0-9])*)?'
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
            my_roll = actual_roll(int(l_branch[0]), int(r_branch[0]))
            return [my_roll[0], l_branch[1] + "d" + r_branch[1]+ " [" + my_roll[1] + "]"]
        elif (first == "("):
            l_branch = branch([exp[1], ""])
            return [l_branch[0], "(" + l_branch[1] + ")"]
    else:
        return [float(exp), str(exp)]


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
            my_roll = actual_roll(int(l_branch[0]), int(r_branch[0]))
            return [my_roll[0], l_branch[1] + "d" + r_branch[1] + " [" + my_roll[1] + "]"]
        elif (first == "("):
            l_branch = branch([exp[0][1], exp[1]])
            return [l_branch[0], "(" + l_branch[1] + ")"]
    else:
        return [float(exp[0]), str(exp[0])]


global thisPage
	
delete_logger = { }

print ("Loading..")
intents = discord.Intents.default()
client = discord.Client(intents=discord.Intents.default())
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix=['>', '{}'])
bot.add_cog(CharacterCog(bot))

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
	msgcontent = message.content.lower()
	msgcontent = msgcontent.replace("x", "i")
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
	elif "nigga" in msgcontent or "niggas" in msgcontent or "nigger" in msgcontent:
		try:
			await message.delete()
		except:
			pass
	elif "https://images-ext-2.discordapp.net/external/WlCcgtV_C1ygC7rErRTbj4kUc5A6mqE_bG6TW2KoM1A/https/media.tenor.com/pyUTSY5MeusAAAPo/makima.mp4" in message.content or "https://tenor.com/view/makima-gif-26321924" in message.content:
		try:
			await message.delete()
		except:
			pass
		

modlist = (454820620824215553, 423798867868516373, 681931899584905390, 945430077863243797, 429988152866897933, 195354841592233985, 348791436075991061)

@bot.event
async def on_member_ban(guild, member):
	logs = await guild.audit_logs(limit=3, action=discord.AuditLogAction.ban).flatten()
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
	logs = await ctx.guild.audit_logs(limit=3, action=discord.AuditLogAction.channel_delete).flatten()
	logs = logs[0]
	user=logs.user
	global delete_logger
	try:
		delete_logger[str(logs.user)] += 1
	except KeyError:
		delete_logger[str(logs.user)] = 1
	
	if user.id not in modlist:
		for user, deleted in delete_logger.items():
			print(user," deleted a channel ("+str(deleted)+"/3)")
			if deleted >= 3:
				await ctx.guild.ban(logs.user)


@bot.event
async def on_guild_role_delete(ctx):
	logs = await ctx.guild.audit_logs(limit=3, action=discord.AuditLogAction.role_delete).flatten()
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
			print(user," deleted a role ("+str(deleted)+"/3)")
			if deleted >= 3:
				await ctx.guild.ban(logs.user)


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.MissingPermissions):
		await ctx.send(
			"You do not have the required roles to run this command.")
		
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
			embed.add_field(name="Remove-Currency", 	value="Removes a currency from a character.\n**Syntax: **`>remove-currency (name) (currency abbreviation)`Aka rm-cu")
			embed.add_field(name="Page 2", 				value="Flip to Page 2 with `>help Characters 2`", inline=False)
		elif page == 2:
			embed.add_field(name="Add-Energy", 			value="Adds an energy type to a character.\n**Syntax: **`>add-energy (name) (energy abbreviation) [Starting maximum, default 100. Automatically based on Wis x 5 if is MP or EP.]`\nAka a-e")
			embed.add_field(name="Remove-Energy", 		value="Removes an energy type from a character.\n**Syntax: **`>remove-energy (name) (energy abbreviation)`\nAka rm-e")
			embed.add_field(name="Add-Title", 			value="Adds a title to a character.\n**Syntax: **`>add-title (name) (title name)`\nAka a-t",inline=False)
			embed.add_field(name="Remove-Title", 		value="Removes a title from a character.\n**Syntax: **`>remove-title (name) (title name)`\nAka rm-t")
			
			
	elif entry == "rolls":
		embed.add_field(name="Roll", value="This command is basically a calculator that has the 4 basic arithmetic operations, and an extra operation for rolling dice.\nSyntax:\n"+
					   	"`Addition: 			[expression] + [expression].`\n" +
					   	"`Subtraction: 		 [expression] - [expression].`\n" +
					   	"`Multiplication: 	  [expression] * [expression].`\n" +
					   	"`Division: 			[expression] / [expression].`\n" +
					   	"`Rolling: 			 [expressiond[expression]` (limited to 1000 sides and rolls).\n" +
						"To use brackets, write `([expression])`.\n" +
					   	"To use the command, type `>roll [expression]`.\n" +
		 				"When showing the output, the roll oprand will automatically cut off after the 12th roll, to show all the rolls, put `-nl` **at the start** of the expression (case sensative.).\n"+
					   	"Here is an example of the -nl header used in an expression:\n`>roll -nl 20d6 + 5 - 15d4`.")
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
@commands.has_permissions(moderate_members=True)
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
@commands.has_permissions(moderate_members=True)
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

#Rolling
@bot.command(name="roll",
			 pass_context=True,
			 aliases=["Roll", "calculate", "Calculate", "calc", "Calc"])
async def roll(ctx, *args):
	try:
		global do_roll_limit
		do_roll_limit = True

		if (args[0] == "-nl"):
			args = args[1::]
			do_roll_limit = False
			pass

		message_inp = ""

		for i in args:
			message_inp += i + " "

		parsed = parser.parse(message_inp)
		compiled = compile(parsed)

		if (ctx.message.author.id == 423798867868516373):
			embed = discord.Embed(title="Rolling:",
								  description=compiled[1] + " - ∞" +
								  "\nSum: -∞",
								  color=0x33FBFF)
			embed.set_thumbnail(
				url=
				"https://media.discordapp.net/attachments/843632677533777940/980579446371258418/PngItem_1087634.png?width=2138&height=1404"
			)
		else:
			embed = discord.Embed(title="Rolling:",
								  description=compiled[1] + "\nSum: " +
								  str(compiled[0]),
								  color=0x33FBFF)
			embed.set_thumbnail(
				url=
				"https://media.discordapp.net/attachments/843632677533777940/980579446371258418/PngItem_1087634.png?width=2138&height=1404"
			)
			#embed.add_field(name="Blah", value="yes")
		await ctx.send(embed=embed)
	except:
		await ctx.send(
			"An error occurred while trying to execute the command, please use >help Rolls and check the syntax and grammar, if you cannot find the mistake, please contact the bot developers."
		)

	
#Add qi command

#Set qi level command

#Set qi tempering command

#Remove qi command

"""def getStatTotals(receivedDict):
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
	await ctx.send(totalString)"""
		

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
