import discord
from discord.ext import commands
#import checks

import asyncio
import requests

class Mindustry(object):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True, aliases=["m"], name='mindustry')
    async def mindustry(self, ctx):
        if ctx.invoked_subcommand is None:
            print(dir(Mindustry))
        return ctx
    
    @mindustry.command(pass_context=True, aliases=['postmap', 'map'])
    async def post_map(self, ctx, *, bericht=None):
        if not ctx.message.attachments:
            msg = self.bot.say('you must add a .mmap (and a picture)')
            await asyncio.sleep(10)
            await self.bot.delete_message(msg)
            return
        '''
        data = {i['filename'][-3:]:[i['url'],i['filename']] for i in ctx.message.attachments}
        print(data)
        '''
        #url = ctx.message.attachments[0]['url']
        #name = ctx.message.attachments[0]['filename']
        r = requests.get(url)
        with open(name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        print('done', name, url)
        
    @mindustry.command(pass_context=True, hidden=True)
    async def collect(self, ctx, ext='.mmap'):
        
        print('called collect command\n\n\n\n')
        def check(message):
            return bool(message.attachments)
        async for i in self.bot.purge_from(ctx.channel, check=check):
            print(i)
        
#load cog
def setup(bot):
    bot.add_cog(Mindustry(bot))
       
