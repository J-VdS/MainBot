import discord
from discord.ext import commands
#import checks

def is_owner(ctx):
    return ctx.message.author.id == OWNER

class Connect4(object):
    def __init__(self, bot):
        self.bot = bot
        self.join = {}
        self.mode = 0 #0:host, 1:join

    @commands.group(pass_context=True)
    async def connect4(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('You will need to add a subcommand ex: connect4 host')

    @connect4.command(pass_context=True)
    @commands.check(is_owner)
    async def change_mode(self, ctx):
        self.mode = (self.mode+1)%2
        print('join' if self.mode else 'host')

    @connect4.command()
    async def join(self):
        print('join')
        print(ctx.message.author.name)
        if not self.mode:
            await self.bot.say('*DISABLED* use host instead')
            return
        pass

    @connect4.command()
    async def host(self):
        if self.mode:
            await self.bot.say('*DISABLED* use join instead')
            return
        
    

#load cog
def setup(bot):
    bot.add_cog(Connect4(bot))
