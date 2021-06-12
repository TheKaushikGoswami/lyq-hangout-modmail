
from discord.ext import commands
from discord import errors, message, utils
import discord
import asyncio
import datetime

from discord.ext.commands.converter import MemberConverter, UserConverter
from discord.ext.commands.core import command

class onMessage(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		member = message.author
		if message.author.bot:
			return

		if isinstance(message.channel, discord.DMChannel):
			guild = self.bot.get_guild(823167447582507040)
			categ = utils.get(guild.categories, name = "Modmail tickets")
			if not categ:
				overwrites = {
					guild.default_role : discord.PermissionOverwrite(read_messages = False),
					guild.me : discord.PermissionOverwrite(read_messages = True)
				}
				categ = await guild.create_category(name = "Modmail tickets", overwrites = overwrites)

			channel = utils.get(categ.channels, topic = str(message.author.id))
			if not channel:
				channel = await categ.create_text_channel(name = f"{message.author.name}#{message.author.discriminator}", topic = str(message.author.id))
				await channel.send(f"New modmail created by {message.author.mention}")
				await channel.send(f"<@&839840167630995486>", delete_after=10)

			embed = discord.Embed(description = message.content, colour = 0x1ABC9C)
			embed.set_author(name = message.author, icon_url = message.author.avatar_url)
			await channel.send(embed = embed)

			log = self.bot.get_channel(843161932278267944)

			em = discord.Embed(title=f'New Modmail', color = 0x2ECC71)
			em.set_footer(text=f"{member.name} | {member.id}", icon_url=message.author.avatar_url)
			em.timestamp = datetime.datetime.utcnow()
			await log.send(embed=em)

		elif isinstance(message.channel, discord.TextChannel):
			if message.content.startswith(self.bot.command_prefix):
				pass
			else:
				topic = message.channel.topic
				if topic:
					member = message.guild.get_member(int(topic))
					if member:
						embed = discord.Embed(description = message.content, colour = 0x1ABC9C)
						embed.set_author(name = message.author, icon_url = message.author.avatar_url)
#					embed.set_footer(text=f"Modmail Bot Developed by `_TheKaushikG_#5300` | From **Karuta Shop**")
						embed.timestamp = datetime.datetime.utcnow()
						await member.send(embed = embed)

	@commands.command()
	async def close(self, ctx, *, reason = f"No Reason Provided"):

		guild = self.bot.get_guild(823167447582507040)
		author = ctx.author
		user = guild.get_member(int(ctx.channel.topic))

		if ctx.channel.category.name == "Modmail tickets":
			await ctx.send("Deleting the channel in 10 seconds!")
			await asyncio.sleep(10)
			await ctx.channel.delete()

			log = self.bot.get_channel(843161932278267944)

			em = discord.Embed(title=f'Modmail Closed', description=f'Reason : {reason}' ,color = 0xE74C3C)
			em.set_author(name=f"Closed By : {author.name}", icon_url=f'{author.avatar_url}')
			em.set_footer(text=f"Modmail user : {user} | {user.id} ")
			em.timestamp = datetime.datetime.utcnow()
			await log.send(embed=em)





def setup(bot):
	bot.add_cog(onMessage(bot))
