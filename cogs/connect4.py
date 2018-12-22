import discord
from discord.ext import commands
#import checks

def is_owner(ctx):
    return ctx.message.author.id != 5

class Connect4(object):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.mode = 0 #0:host, 1:join

    @commands.group(pass_context=True)
    async def connect4(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('You will need to add a subcommand ex: connect4 host')
        return ctx
    
    @connect4.command(pass_context=True)
    async def change_mode(self, ctx):
        self.mode = (self.mode+1)%2
        print('join' if self.mode else 'host')
        return

    @connect4.command(pass_context=True)
    async def join(self, ctx):
        print(ctx.message.author)
        

    @connect4.command(pass_context=True)
    async def host(self, ctx):
        print(ctx.message.author)
        if self.mode:
            await self.bot.say('*DISABLED* use join instead')
            return
        

#load cog
def setup(bot):
    bot.add_cog(Connect4(bot))
