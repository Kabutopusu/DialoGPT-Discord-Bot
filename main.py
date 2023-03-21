import os
import json
import requests
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv('./key.env')

API_URL = 'https://api-inference.huggingface.co/models/Kabutopusu/'

#---setup client, load cogs and sync slash commands---

class Client(commands.Bot):
  def __init__(self):
      super().__init__(
        command_prefix = 'mae!',
        intents = discord.Intents.all(),
        application_id = 971720676337655890
        )

      self.api_endpoint = API_URL + 'DialoGPT-medium-NITWMae'
      huggingface_token = os.environ['HUGGINGFACE_TOKEN']
      self.request_headers = {
          'Authorization': 'Bearer {}'.format(huggingface_token)
      }

  async def load_extentions(self):
    for v in os.listdir('./cogs'):
      if v.endswith('.py'):
        await client.load_extension(f'cogs.{v[:-3]}')

  async def setup_hook(self):
    self.remove_command('help')
    await self.load_extentions()
    await client.tree.sync()

  async def on_ready(self):
      print(f'\nlogged in as:', self.user.name, '\naccount id:', self.user.id, '\n')
      await self.change_presence(
                status=discord.Status.online,
                activity=discord.Game(name='Demontower'))

  async def on_command_error(ctx, err):
      print(err)



#---querying api and responding to author below---

  def query(self, payload):
      """
      request to HF API
      """
      data = json.dumps(payload)
      response = requests.request('POST',
                                self.api_endpoint,
                                headers=self.request_headers,
                                data=data)
      ret = json.loads(response.content.decode('utf-8'))
      print(payload)
      print(ret)
      return ret

  async def on_message(self, message):

    async with client:
        with open('guildDB.json', 'r') as v:
          guildDict = json.load(v)
        if message.guild.id in guildDict:
            customChannel = client.get_channel(guildDict[message.guild.id])
            print(customChannel)

        if message.author.id == self.user.id:
            return

        payload = {'inputs': {'text': message.content}}

        async with customChannel.typing() or message.channel.typing():
          response = self.query(payload)
        bot_response = response.get('generated_text', None)
        
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = '''`damn. I wasn't able to think of a response. try and talk to me again?`'''

        await customChannel.send(bot_response) or await message.channel.send(bot_response)



#---run client---

client = Client()
client.run(os.environ['DISCORD_TOKEN'])