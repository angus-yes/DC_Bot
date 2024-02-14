import discord
import math
import random
import rename as rn
import wfa
import funcdoc as fd
import dice
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DC_TOKEN")

client = discord.Client(intents=discord.Intents.all())

@client.event

async def on_ready():
    print('Logged in as ', client.user)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='command in bot-channel; Type "?" for help'))

@client.event
async def on_guild_join(guild):
    
    botchan = discord.utils.find(lambda x: x.name == 'bot-channel',  guild.text_channels)
    if not(botchan):
        botcat = discord.utils.find(lambda x: x.name == 'bot',  guild.categories)
        if not(botcat):
            await guild.create_category('bot')
            botcat = discord.utils.find(lambda x: x.name == 'bot',  guild.categories)
        await botcat.create_text_channel('bot-channel')

@client.event

async def on_message(message):

    if (message.author == client.user) or not((message.content.startswith('!')) or (message.content.startswith('?'))) or not(message.channel.name == 'bot-channel'):
        return

    else:
        msg = message.content.split()
        print(msg)
        cmd = msg[0]
        if cmd == '!rename':
            await rn.rename(msg, message)

        elif cmd == '!wolf' or cmd == '!wolf+':
            await wfa.wfa(message)
        
        elif cmd == '!random':
            await dice.roll(msg, message)

        elif message.content.startswith('?'):
            
            
            if len(msg) == 1 and len(cmd) == 1:
                await message.channel.send('Available Functions:\n'+'\n'.join(f"{fd.funcdict[keys]}\n" for keys in fd.funcdict))
            elif len(msg) == 2:
                try:
                    func = fd.funcdict[msg[1]]
                    await message.channel.send(f"{func}\n")
                except:
                    await message.channel.send('Error: Function not found; Type "?" for help')
            elif len(cmd) > 1:
                try:
                    func = fd.funcdict[cmd[1:]]
                    await message.channel.send(f"{func}\n")
                except:
                    await message.channel.send('Error: Function not found; Type "?" for help')
            else:
                await message.channel.send(f'Error: Too many arguments; Expected 1, Found {len(msglist)-1}; Type "?" for help')

        else: 
            await message.channel.send('Error: Invalid command; Type "?" for help')

client.run(token) 