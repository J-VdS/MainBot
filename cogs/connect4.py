import discord
from discord.ext import commands

#custom emoji check
def custom(reaction, user):
        return not reaction.custom_emoji

#connect4 data functions
def check(veld, speler):
    #horizontaal:
        for y in range(6):
            if veld[7*y:7*y+7].count(speler)>3:
                for x in range(4):
                    if veld[7*y+x:7*y+x+4] == speler*4:
                        return True
        #verticaal:
        for x in range(7):
            if veld[x::7].count(speler)>3:
                for y in range(3):
                    if veld[7*y+x:7*(y+4)+x:7] == speler*4:
                        return True
        #diagonaal linksonder naar rechtsboven
        for x in range(3,7):
            for y in range(3):
                if veld[7*y+x:7*y+x+19:6] == speler*4:
                    return True
        #diagonaal linksboven naar rechtsonder
        for x in range(4):
            for y in range(3):
                if veld[7*y+x:7*y+x+25:8] == speler*4:
                    return True

        return False


def move(data, speler, x, blank):
    '''
    data = [speler1, emo1, speler2, emo2, veld]
    speler = 0 or 2
    x = 1 to 7
    '''
    y = data[-1][x::7].count('E')-1
    if y < 0:
        #doe iets
        pass
    data[-1] = data[-1][:y*7+x]+str(speler)+data[-1][y*7+x+1:]
    return (data[-1], make_veld(data, blank), check(data[-1], str(speler)))

def make_veld(data, blank):
    msg = f'{data[0].mention} : {str(data[1])} - {data[2].mention} : {str(data[3])}\n'
    for i in range(6):
        for j in range(7):
            num = data[-1][i*7+j]
            msg += str(data[int(num)+1] if num.isdigit() else blank)
        msg += '\n'
    return msg


class Connect4(object):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.mode = 0 #0:host, 1:join
        #get router as blank emoji
        self.blank = discord.utils.get(self.bot.get_all_emojis(), name='router')
        if not self.blank:
            self.blank = ':black_medium_square:'
        self.waardes = {'1⃣':0, '2⃣':1, '3⃣':2,'4⃣':3, '5⃣':4, '6⃣':5, '7⃣':6}
        
    @commands.group(pass_context=True)
    async def connect4(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('You will need to add a subcommand ex: connect4 host')
        return ctx
    
    @connect4.command(pass_context=True, hidden=True)
    @commands.check()
    async def change_mode(self, ctx):
        self.mode = (self.mode+1)%2
        print('join' if self.mode else 'host')
        return

    @connect4.command(pass_context=True)
    async def join(self, ctx):
        if not self.mode:
            await self.bot.say('*DISABLED* use host instead')
    
    @connect4.command(pass_context=True)
    async def host(self, ctx):
        #one command --> edit it pls
        if self.mode:
            await self.bot.say('*DISABLED* use join instead')
            return
        host = ctx.message.author
        #start procedure
        await self.bot.delete_message(ctx.message)
        msg = await self.bot.say('react to choose (custom emojis disabled)')
        rea = await self.bot.wait_for_reaction(
            user=host,
            message=msg,
            check=custom)
        game = [host, rea.reaction.emoji]
        #get other player
        await self.bot.clear_reactions(msg)
        msg = await self.bot.edit_message(
            msg,
            f'React to play against {game[0].mention} : {str(game[1])}')
        rea = await self.bot.wait_for_reaction(
                message=msg,
                check=custom)
        game += [rea.user, rea.reaction.emoji, 42*'E']
        #todo add don't play against yourself
        await self.bot.delete_message(msg)
        #game starts
        print('\n\nstart game')
        player = 2*(random.random()<0.5)
        msg = await self.bot.say(
            f'{game[0].mention} : {str(game[1])} - {game[2].mention} : {str(game[3])}\n'+\
            make_veld(game, self.blank)+f'{game[player].mention} may start')
        for i in ['1⃣', '2⃣', '3⃣','4⃣', '5⃣', '6⃣', '7⃣']:
            await self.bot.add_reaction(msg, i)

        while game:
                rea = await self.bot.wait_for_reaction(
                        user=game[player],
                        message=msg,
                        emoji=['1⃣', '2⃣', '3⃣','4⃣', '5⃣', '6⃣', '7⃣'])
                await self.bot.remove_reaction(
                        msg,
                        rea.reaction.emoji,
                        game[player])
                        
                x = self.waardes[rea.reaction.emoji]
                game[-1], be, end = move(game, player, x, self.blank)
                if end:
                        be += f'{game[player].mention} won'
                        game = None
                else:
                        player = (2+player)%4 #2 of 4
                        print(player)
                        be += f'{game[player].mention} it is your turn'
                msg = await self.bot.edit_message(msg, be)
        
            
    
#load cog
def setup(bot):
    bot.add_cog(Connect4(bot))
