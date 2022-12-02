import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext import *
import os
import random
import asyncio
import time
import Bot
from Bot import *

Client = discord.Client(intents=discord.Intents.default())
client = commands.Bot(command_prefix="}", intents=discord.Intents.default())

accounts = ['rgb', ':p', 'w', 'pl', 'id', 'ez', 'fu', 'uk', 'gg', 'qq', 'ey', 'ye', 'um', 'cm', 'iq', 'kg', 'tv', 'xp', 'ah', '69', '10', 'k2', 'f', 'z', 
            'pb', '0,', 'yx', '34', '00', ',,_', 'ej', 'wp', 'ui', 'hz', 'ii', 'pz', 'su', '7z', 'if', 'ie', 'za', 'is', 'ig', 'lp', 'mb', 'f1', 'pf',
            'kurwa', 'polish', 'luck', 'michal2', 'good', 'puke', 'sacolors', 'what', 'cba', 'facepalm', '12940', 'professor',
            'google', 'mafia', 'kiddo', 'x.x', 'z.z', 's.s', 'o.o', ',,i,,', 'qwenton', 'l_o_l', 'gorgeous',
            'smart', 'notorious', 'boy', 'myth', 'freedom', 'mysterious', 'rude', 'silent', 'anomaly', 'fierce', 'vibrant', 'jack',
            'disrespectful', 'undefined', 'sigma']

g = ['smart', 'notorious', 'boy', 'myth', 'freedom', 'mysterious', 'rude', 'silent', 'anomaly', 'fierce', 'vibrant', 'jack',
     'disrespectful', 'undefined', 'sigma']

r5 = ['good', 'pl', ':p', 'polish']

@client.event
async def on_ready():
  activity = discord.Game(name="Mind Yo Business.")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Mind Yo Business.'))
  print("Name: {}".format(client.user.name))
  print("ID: {}".format(client.user.id))
  print('Servers connected to:')
  for server in client.guilds:
    print(server.name + " = " + str(server.id))
  await collect()
    
async def collect():
  mainPW = os.environ['pw1']
  while True:
    creds_channel = client.get_channel(988771125456691230)
    for x in accounts:
      if x in g:
        mainPW = os.environ['gpw']
      elif x in r5:
        mainPW = os.environ['r5pw']
      else:
        mainPW = os.environ['pw1']
      a = Bot.SABot(x, mainPW, 'ballistick5.xgenstudios.com', 1138, True)
      time.sleep(0.5)
      if a.banned == True:
        await creds_channel.send(x + " is currently banned. Can't collect any creds.")
      elif a.incorrect == True:
        await creds_channel.send("Incorrect password for " + x)
      
      if a.receivedCreds != '':
        await creds_channel.send("""```fix
Just collected {} creds on '{}' and it makes {} creds in total.```""".format(a.receivedCreds, x, a.creds))
      
      a.SocketConn.shutdown(socket.SHUT_RD)
      a.SocketConn.close()
    await asyncio.sleep(7*60*60)
    
client.run(os.environ['BOT_TOKEN'])
