import discord
from discord.ext import commands
import os
import copy
import random
intents = discord.Intents.default()
intents.members = True

def secret_santa(ids):
  li = ids
  choose = copy.copy(li)
  result = []
  for i in li:
    ids = copy.copy(li)
    ids.pop(ids.index(i))
    chosen = random.choice(list(set(choose)&set(ids)))
    result.append((i, chosen))
    choose.pop(choose.index(chosen))
  return result

bot = commands.Bot(command_prefix = '^', intents = intents, help_command=None)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.  Do ^help")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the appropriate permissions to run this command.")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!")
    else:
        print("error not caught")
        print(error) 

@bot.command()
async def help(ctx):
  await ctx.channel.send("Create a secret santa role, then send a command like this: ```^play @role [optional: party name]``` Shortly after, everyone will get their secret santa person via DM - happy gifting!")

@bot.command()
async def play(ctx, role: discord.Role, *, message = None):
  message = message or "SECRET SANTA"
  members = []
  for member in ctx.guild.members:
    if role in member.roles:
      members.append(member)
  if len(members) == 1:
    await ctx.channel.send("You're the only one in that role, maybe find some friends first?")
    return
  elif len(members) == 0:
    await ctx.channel.send("There's no one in that role")
    return
  santas = secret_santa(members)
  for i, j in santas:
    msg = "Hi its your friendly neighbourhood santa assigner here, your person is **{}** for _{}_! Don't forget to get them something nice :)".format(j.name, message)
    await i.send(msg)
  await ctx.channel.send("Okay, I've sent the username of a randomly picked person to everyone in that role")

@bot.command()
async def hello(ctx):
  await ctx.channel.send("HO HO HO HO HO")

bot.run(os.environ['TOKEN'])
