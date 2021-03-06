#!/usr/bin/env python3
# catgirl.py
# main file for catgirl bot
import discord, sys, os

# check versions before continuing
if sys.version_info[0] < 3:
    raise Exception('Python 3 or higher is required for this bot! Recommended version: 3.9.1')

if int(discord.__version__[2]) < 5:
	raise Exception('Discord.py 1.5.0 or higher is required for this bot! Recommended version: 1.5.1')

sys.path.insert(1, 'mod')
sys.path.insert(1, 'data')
import cfg, settings, filemanager
from logger import write_log_message
from debug import spawn_debug_thread
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Here we load our extensions(cogs) listed in cfg.
if __name__ == '__main__':

    print(f'Loading {len(cfg.cogs)} cogs!')

    for extension_name in cfg.cogs:
        cfg.bot.load_extension(f'cogs.{extension_name}')
    print(f'Loaded cogs: {", ".join(cfg.cogs)}')

    if os.getenv('DEBUG') == 'yes':
        print('') # newline
        print('Debug is enabled, spawning debug thread...')
        spawn_debug_thread()
        
    print('') # newline

async def connected():

    # setup the directories we need
    filemanager.make_initial_dirs()

    # read config file once
    if os.path.exists(f'config/bot/settings.ini'):
        cfg.config.read(f'config/bot/settings.ini')

    filemanager.setup_guilds_config(cfg.bot.guilds)

@cfg.bot.event
async def on_ready():
    # bot is completely connected and ready to process commands
    print(f'{cfg.bot.user} has logged in to Discord!')
    await cfg.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="catgirls"))

    await connected()

    # log botevent
    botevent_log = f'logs/botevent/botevent.log'
    message = f'{str(datetime.now())} {cfg.bot.user} is now online in {len(cfg.bot.guilds)} guilds!\n'
    write_log_message(message, botevent_log)

    print(f'{cfg.bot.user} is now online in {len(cfg.bot.guilds)} guilds!')
    print(f'Bot is ready to process commands! Current ping: {round(cfg.bot.latency * 1000, 2)}ms')
    print('') # newline

@cfg.bot.event
async def on_guild_join(guild):
    # setup the guild files
    new_guild_list = [guild]
    filemanager.setup_guilds_config(new_guild_list)

    # log botevent
    botevent_log = f'logs/botevent/botevent.log'
    message = f'{str(datetime.now())} {cfg.bot.user} joined the guild {guild.id} ({guild.name})!\n'
    write_log_message(message, botevent_log)

    print(f'\nJoined the guild {guild.id} ({guild.name})!\n')

    await guild.owner.send(f'Hello! Please make sure I have the permissions needed to send messages in your server, and to perform the commands you wish to use!')
    await guild.owner.send(f'That means if you wish to use my moderation commands, you should give me permissions to kick/ban members and adjust their roles!')
    await guild.owner.send(f'*If I do not have permissions to send messages in a channel, you will not get a warning, the output simply will not be sent.*')

@cfg.bot.event
async def on_guild_remove(guild):
    # log botevent
    botevent_log = f'logs/botevent/botevent.log'
    message = f'{str(datetime.now())} {cfg.bot.user} left the guild {guild.id} ({guild.name})!\n'
    write_log_message(message, botevent_log)

    print(f'\nLeft the guild {guild.id} ({guild.name})!\n')


# run actual bot
cfg.bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)
