import os
import discord

from discord.ext import commands
client = commands.Bot(command_prefix='?')

async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.event
async def on_ready():
  print('The bot is online')
  for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
          if(filename == "VoiceCommands.py"):
            continue
          client.load_extension(f'cogs.{filename[:-3]}')
os.environ["TOKEN"] = "NzMwMzEwNjE1OTY4Nzc2MjIz.XwVoww.DFiCvYeLeCEa_7aGXC6DpJTcG60"
client.run(os.getenv("TOKEN"))
