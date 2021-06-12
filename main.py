from discord.ext import commands
import discord
import os

intents = discord.Intents.default()
# we need members intent too
intents.members = True

bot = commands.Bot(command_prefix = "-", intents = intents)

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"DM Me to Open Modmail | Karuta Shop | Made with ❤️ by KAUSHIK"))
	print("The bot is online!")
	bot.load_extension("cogs.onMessage")

bot.run("your-token-here")
