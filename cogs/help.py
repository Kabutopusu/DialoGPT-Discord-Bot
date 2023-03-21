import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
client = commands.Bot(command_prefix='mae!', intents=intents)

embedGifList = [
  'https://cdn.discordapp.com/attachments/803983551736578118/1041459423543046155/gif1.gif',
  'https://cdn.discordapp.com/attachments/803983551736578118/1041459681748602880/gif2.gif',
  'https://cdn.discordapp.com/attachments/803983551736578118/1041459693404573716/gif3.gif',
  'https://cdn.discordapp.com/attachments/803983551736578118/1041459706906030182/gif4.gif'
]

class helpCog(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("help slash cog loaded")

  @client.tree.command(name='help', description='Info about Mae!')
  async def maeHelp(self, interaction: discord.Interaction):
    embed = discord.Embed(
            title=f'Mae',
            description='⦊ whoa. now THIS is cool.',
            colour=discord.Colour.gold()
        )
    embed.set_thumbnail(url=random.choice(embedGifList))
    embed.set_footer(text="I'm a total trash mammal!")
    
    embed.add_field(name='Info', value="An AI chatbot made with the DialoGPT-medium conversational model. Trained with around 5200~ lines of dialogue from Mae. Perplexity is 1.43, which is 90%~ accuracy. There'll be some imperfections (aka yarnspinner code) as the lines were ripped straight from the game and I didn't bother making a good regex lol (textwall uh oh)", inline=False)
          
    await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
  await bot.add_cog(helpCog(bot))