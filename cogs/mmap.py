import discord
from discord.ext import commands
import checks

import asyncio
import requests

class Mindustry(object):
    def __init__(self, bot):
        self.bot = bot

    '''
    @commands.command(pass_context=True)
    @commands.check(checks.is_not_owner)
    async def test(ctx):
        await client.say('worked')
    '''
    @commands.group(pass_context=True, aliases=["m"], name='mindustry')
    async def mindustry(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("use !m post_map *<description>* to post a map")
        return ctx
    
    @mindustry.command(pass_context=True, aliases=['postmap', 'map'])
    async def post_map(self, ctx, *, bericht=None):
        if not ctx.message.attachments:
            msg = self.bot.say('you must add a .mmap (and a description)')
            await asyncio.sleep(10)
            await self.bot.delete_message(msg)
            return
        
        url = ctx.message.attachments[0]['url']
        name = ctx.message.attachments[0]['filename']
        if (name.count('.') == 1)*(ctx.split('.')[-1] == 'mmap'):
            r = requests.get(url)
            with open(name, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
            print('done', name, url)
        else:
            await self.bot.say("INVALID FILE EXTENSION")
        
    @mindustry.command(pass_context=True, hidden=True)
    @commands.check(checks.is_owner)
    async def collect(self, ctx, limit=100, normal=False, ext='mmap'):
        print(normal)        
        print('called collect command\n\n\n\n')
        def check(message):
            return bool(message.attachments)
        files = [[],[]]
        async for i in self.bot.logs_from(ctx.message.channel, limit=limit):
            if check(i):
                fn = i.attachments[0]['filename']
                if not (fn in files[0]) and fn.split('.')[-1] == ext:
                    files[0].append(fn)
                    files[1].append(i.attachments[0])
                    print(len(files[0]))
        if not normal:
            
            print('started download')
            for i in files[1]:
                r = requests.get(i['url'])
                path = f"{i['filename']}"
                print(path)
                with open(path, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
                print('done\n\n\n')
        else:
            with open('urls.txt', 'w') as file:
                for i in files[1]:
                    file.write(i['url'])
                    file.write('\n')
                

#load cog
def setup(bot):
    bot.add_cog(Mindustry(bot))
       
