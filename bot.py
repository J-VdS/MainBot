import discord
from discord.ext import commands

with open('token.txt', 'r') as infile:
    data = [i.strip('\n') for i in infile.readlines()]
    TOKEN = data[0] #first line in token.txt
    #OWNER = data[1] #second line in token.txt

client = commands.Bot(command_prefix = '!') #not used
emos = {}

@client.event
async def on_ready():
    print('Bot is ready')

    #gets all custom emojis
    for x in client.get_all_emojis():
        emos[x.name] = x
    print(emos)
        
@client.event
async def on_message(message):
    content = message.content.lower()
    if 'router' in content or 'splitter' in content:
        await client.add_reaction(message, emos['router'])
    await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    await on_message(after)
   
@client.command(pass_context=True,
                brief='Deletes messages')
@commands.has_role('test')
async def clear(ctx, limit=99):
    channel = ctx.message.channel
    print(channel.name)
    if 1:#str(ctx.message.author).split('#')[-1] == OWNER.split('#')[-1]:
        message = [msg async for msg in client.logs_from(channel, limit=int(limit)+1)]
        print(len(message))
        await client.delete_messages(message)

@client.command(pass_context=True,
                brief='connect4')
async def image(ctx, file):
    await client.send_file(ctx.message.channel, file)
    try:
        embed = discord.Embed(title='dit is een test')
        await client.send_message(ctx.message.channel, embed=embed)
    except Exception as e:
        print(e)
@client.command(pass_context=True)
async def get(ctx):
    for i in client.servers:
        await client.say(i.id)
    

client.run(TOKEN)
