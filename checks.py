import discord

global OWNER

with open('D:\\Python\\Discord\\token.txt', 'r') as infile:
    data = [i.strip('\n') for i in infile.readlines()]
    _ = data[0] #first line in token.txt
    OWNER = data[1] #second line in token.txt

def is_not_owner(ctx):
    print('_'*30)
    print(dir(ctx))
    try:
        print('-'*30)
        print(ctx.command)
        print('-'*30)
    except Exception as e:
        print(e)
    return True

def is_owner(ctx):
    return ctx.message.author.id == OWNER
