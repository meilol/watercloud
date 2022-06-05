import datetime
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="The help command | -help [command]")
    async def help(self, ctx, _command=None):
        """The help command"""
        embed = discord.Embed(title="Click here for help", url="https://watercloud.wtf/commands", color=0x8E72BE)
        
        if _command is not None:
            command = self.bot.get_command(_command)
            if _command == command.name:
                if command.aliases == []: command.aliases = "No aliases"
                aliases = str(command.aliases).replace("[", "").replace("]", "").replace("'", "")
                embed.add_field(name=f"{command.name} | {aliases} ", value=f"{command.description}", inline=False)
                embed.set_footer(text=f"Requested by: {ctx.author}")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
        
        await ctx.send(embed=embed)
        return
            
        
    
def setup(bot):
    bot.add_cog(Help(bot))
print(f"Help cog loaded") 