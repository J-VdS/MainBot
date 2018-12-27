import discord
from discord.ext import commands
#import checks to do: move all checks to 1 python file

with open('D:\\Python\\Discord\\token.txt', 'r') as infile:
    data = [i.strip('\n') for i in infile.readlines()]
    TOKEN = data[0] #first line in token.txt
    OWNER = data[1] #second line in token.txt

client = commands.Bot(command_prefix = '..') 
emos = {}

def is_owner(ctx):
    return ctx.message.author.id == OWNER

@client.event
async def on_ready():
    print('Bot is ready')
    #gets all custom emojis
    for x in client.get_all_emojis():
        emos[x.name] = x
    print(emos)
    
#loading cogs
@client.command(pass_context=True)
@commands.check(is_owner)
async def load(ctx, cog=None):
    if not cog:
        await client.say('add cog')
        return
    try:
        client.load_extension(f'cogs.{cog}')
        print(f'loaded {cog}')
    except Exception as e:
        print(f'failed to load {cog} reason: [{e}]')

@client.command(pass_context=True)
@commands.check(is_owner)
async def unload(ctx, cog=None):
    if not cog:
        await client.say('add cog')
        return
    try:
        client.unload_extension(f'cogs.{cog}')
        print(f'unloaded {cog}')
    except Exception as e:
        print(f'failed to unload {cog} reason: [{e}]')

#error handling
@client.event
async def on_error(error):
    print(error)

'''
@client.event
async def on_command_error(ctx,error):
    print(type(error))
'''

#testing
@client.command(pass_context=True)
@commands.check(is_owner)
async def eval(ctx, *args):
    print(eval(''.join((i+' ' for i in args))))
    
try:
    client.load_extension('cogs.mmap')
except Exception as e:
    print(e)
client.run(TOKEN)
