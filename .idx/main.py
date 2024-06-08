# Importing libraries
import discord
import os
import asyncio
import string
import json
import random 

from discord.ext import commands
from discord.ext import tasks
from discord import Intents
from discord import interactions
from discord import app_commands


intents = discord.Intents.default()

# Balance logic
def formatBalance(balance):
    if balance < 1000:
        return str(balance)
    elif balance < 1000000:
        return f'{balance / 1000:.1f}K'
    elif balance < 1000000000:
        return f'{balance / 1000000:.1f}M'
    elif balance < 1000000000000:
        return f'{balance / 1000000000:.1f}B'
    else:
        return f'{balance / 1000000000000:.1f}T'

def addBalance(id, amount):
    # add balance logic goes here
    pass

def getBalance(id):
    # get balance logic goes here
    pass

cash_emoji = '💵'  # default cash emoji

# Json
if not os.path.exists('users.json'):
    with open('users.json', 'w') as f:
        json.dump({}, f)

if not os.path.exists('config.json'):
    with open('config.json', 'w') as f:
        json.dump({'cash_emoji': cash_emoji}, f)

with open('config.json', 'r') as f:
    config = json.load(f)

# Discord bot Initialization
bot = discord.Client(intents=intents)
key = "MTA2ODM1MzE1Mjc1MzA3NDE4Ng.GjEu5j.6LcokKqbma4NUCFI_44AjwCW2qxabxk76150pY"

# This event happens when the bot gets run
bot = commands.Bot(command_prefix = "*", intents= discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.activity.Game(name="W.I.P"), 
                              status=discord.Status.online)
    print(f"Bot logged in as {bot.user}")

    
# Discord bot Commands
@bot.command(name='status', help='it will show the current bot status')
async def info(ctx):
    await ctx.send("The bot currently in testing")

@bot.command(name='info', help='it will show more information about the bot')
async def info(ctx):
    await ctx.send("Hi there! It's so unfortunate that i'm still in testing, sorry for the inconvenience")


@bot.command(name='command', help='it will show available commands')
async def command(ctx):
    Basics = [
    "`ping`",
    "`status`",
    "`info`",
]

embeds = []
pages = 2
commands_per_page = len(Basics) // pages + 1

for i in range(pages):
    embed = discord.Embed(title="Command List", description='Here is the list of commands!')
    embed.color = discord.Color.orange()
    embed.set_author(name='Command List',
                     icon_url=ctx.author.avatar.url)
    embed.set_footer(text=f"Page {i+1}/{pages} | Information requested by: {ctx.author.display_name}")

    for j in range(commands_per_page):
        command_index = i * commands_per_page + j
        if command_index < len(Basics):
            embed.add_field(name=f"Command {j+1}", value=Basics[command_index], inline=True)
            embeds.append(embed)

        msg = await ctx.send(embed=embeds[0])
        await msg.add_reaction('◀️')
        await msg.add_reaction('▶️')
            
i = 0
emoji = ''

while True:
        if emoji == '▶️':
            if i < len(embeds) - 1:
                i += 1
            else:
                i = 0
        elif emoji == '◀️':
            if i > 0:
                i -= 1
            else:
                i = len(embeds) - 1
        await (await ctx.send(embed=embeds[0])).edit(embed=embeds[i])
        react = await bot.wait_for('reaction_add', timeout=30.0, check=lambda r, u: u == ctx.author and str(r.emoji) in ['◀️', '▶️'])
        emoji = str(react[0].emoji)

@bot.command(name='invite', help='it will show available commands')
async def invite(ctx):
    embed = discord.Embed(title='Click here!',  url="https://discord.com/oauth2/authorize?client_id=1207980846699515914&permissions=8&scope=bot+applications.commands", description=''
                          , color=discord.Color.orange())
    embed.set_author(name='Want to invite me you your server?', icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)
    
@bot.command(name='ping', help='it will show the ping')
async def ping(ctx):
    await ctx.send(f'Pong! In {round(bot.latency * 100)}ms')

@bot.command(name='setprefix', help="it will change the default to any you'd like")
async def setprefix(ctx, new_prefix: str):
    bot.command_prefix = commands.when_mentioned_or(new_prefix)
    await ctx.send("Prefixes set!")

if not os.path.exists('users.json'):
    with open('users.json', 'w') as f:
        json.dump({}, f)

@bot.command()
async def start(ctx):
    """Creates a new account for the user."""
    user_id = str(ctx.author.id)
    with open('users.json', 'r') as f:
        users = json.load(f)
    if user_id in users:
        await ctx.send('You already have an account.')
        return
    users[user_id] = {'bank': 0, 'wallet': 0}
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
    await ctx.send('Your account has been created.')

@bot.command()
async def deposit(ctx, amount: int):
    """Deposits the specified amount into the user's bank."""
    user_id = str(ctx.author.id)
    with open('users.json', 'r') as f:
        users = json.load(f)
    if user_id not in users:
        await ctx.send('You do not have an account yet. Use the `start` command to create one.')
        return
    if users[user_id]['wallet'] < amount:
        await ctx.send('You do not have enough cash in your wallet.')
        return
    users[user_id]['wallet'] -= amount
    users[user_id]['bank'] += amount
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
    await ctx.send(f'You have deposited {config["cash_emoji"]}{amount} into your bank.')

@bot.command()
async def withdraw(ctx, amount: int):
    """Withdraws the specified amount from the user's bank."""
    user_id = str(ctx.author.id)
    with open('users.json', 'r') as f:
        users = json.load(f)
    if user_id not in users:
        await ctx.send('You do not have an account yet. Use the `start` command to create one.')
        return
    if users[user_id]['bank'] < amount:
        await ctx.send('You do not have enough cash in your bank.')
        return
    users[user_id]['bank'] -= amount
    users[user_id]['wallet'] += amount
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
    await ctx.send(f'You have withdrawn {config["cash_emoji"]}{amount} from your bank.')

@bot.command()
async def balance(ctx, user: discord.Member = None):
    """Shows the user's current balance."""
    if user is None:
        user = ctx.author
    user_id = str(user.id)
    with open('users.json', 'r') as f:
        users = json.load(f)
    if user_id not in users:
        await ctx.send(f"This user doesn't have an account yet.")
        return
    bank = users[user_id]['bank']
    wallet = users[user_id]['wallet']
    embed = discord.Embed(title='', description='Here is their balance!'
                          , color=discord.Color.orange())
    embed.set_author(name=f"{user.display_name}'s balance", icon_url=user.display_avatar.url)
    embed.add_field(name="Wallet", value=f"{config['cash_emoji']}{wallet}", inline=False)
    embed.add_field(name="Bank", value=f"{config['cash_emoji']}{bank}", inline=False)
    embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
    
@bot.command()
async def transfer(ctx, user: discord.Member,amount: int):
    """Transfers the specified amount from the user's wallet to the target user's wallet."""
    if amount <= 0:
        await ctx.send("The amount should be a positive integer.")
        return

    user_id = str(ctx.author.id)
    target_id = str(user.id)
    with open('users.json', 'r') as f:
        users = json.load(f)
        
    if user_id not in users or target_id not in users:
        await ctx.send("One of the users doesn't have an account yet.")
        return

    if users[user_id]['wallet'] < amount:
        await ctx.send("You don't have enough balance to complete the transfer.")
        return

    users[user_id]['wallet'] -= amount
    users[target_id]['wallet'] += amount

    embed = discord.Embed(title='', description='Wallet transfer completed!'
                          , color=discord.Color.orange())
    embed.set_author(name=f"{ctx.author.display_name}'s balance", icon_url=ctx.author.display_avatar.url)
    embed.add_field(name="Sender", value=f"{config['cash_emoji']}{wallet[user_id]}", inline=False)
    embed.add_field(name="Receiver", value=f"{config['cash_emoji']}{wallet[target_id]}", inline=False)
    embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)

@bot.command()
async def work(ctx):
    """Allows the user to earn cash by working."""
    user_id = str(ctx.author.id)
    with open('users.json', 'r') as f:
        users = json.load(f)
    if user_id not in users:
        await ctx.send('You do not have an account yet. Use the `start` command to create one.')
        return
    earnings = random.randint(9000, 20000)
    last_three_digits = random.randint(0, 999)
    earnings += last_three_digits
    users[user_id]['wallet'] += earnings
    with open('users.json', 'w') as f:
        json.dump(users, f)
    balance = users[user_id]['wallet']
    formattedBalance = formatBalance(balance)

    embed = discord.Embed(title="", color=discord.Color.orange())
    embed.set_author(name="Great work!", icon_url=ctx.author.avatar)
    embed.add_field(name="You were given:", value=f"- {config['cash_emoji']}{earnings:,}", inline=False)

    await ctx.send(embed=embed)

from difflib import get_close_matches

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        command = ctx.message.content.split()[0]
        existing_commands = [cmd.name for cmd in bot.commands]
        close_matches = get_close_matches(command, existing_commands, n=1, cutoff=0.6)
        if close_matches:
            await ctx.send(f"Did you mean `{close_matches[0]}`? Please check your spelling and try again.")
        else:
            await ctx.send(f"The command `{command}` isn't exist, are you sure you're typing the right command?")
    else:
        raise error
        
# Shop command

# Admin Commands
@bot.command()
@commands.has_permissions(administrator=True)
async def set_currency(ctx, emoji: str):
    """Set a custom emoji for cash."""
    global cash_emoji  # access the global variable
    cash_emoji = emoji
    with open('config.json', 'r+') as f:
        config = json.load(f)
        config['cash_emoji'] = emoji
        f.seek(0)
        json.dump(config, f)
        f.truncate()
    await ctx.send(f'Cash emoji set to {emoji}')
async def set_currency_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permissions to use this command.')
    else:
        raise error

bot.run(key)
