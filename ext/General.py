from Watercloud import bot
from discord.ext import commands
from evalcc import *

class General(commands.Cog):
    def __init__(self, bot): self.bot = bot
        
    @commands.command(name="ping", description="Ping the bot and get the latency | -ping")
    async def ping(self, ctx): await ctx.send(f"Pong! `{round(bot.latency * 1000)}ms`")
    
def setup(bot): bot.add_cog(General(bot))
print(f"General cog loaded")