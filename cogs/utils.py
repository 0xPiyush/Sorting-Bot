import discord
from discord.ext import commands

class utils(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot
    
    async def ErrorHandler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(error)

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['c', 'cls'])
    async def clear(self, ctx, amount=None):
        if amount != None:
           await ctx.channel.purge(limit=(int(amount)+1))
        else:
            await ctx.channel.purge()

    @clear.error
    async def clear_error(self, ctx, error):
        await self.ErrorHandler(ctx, error)

def setup(Bot):
    Bot.add_cog(utils(Bot))
    