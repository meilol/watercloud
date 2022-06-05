import contextlib
import datetime
import io
import textwrap
from traceback import format_exception
import discord
from Watercloud import bot
from discord.ext import commands
from evalcc import *

class Owner(commands.Cog):
    def __init__(self, bot): self.bot = bot
        
    @commands.command(name="eval", aliases=["exec", "evaluate"], description="Evaluate code | -eval <code>/<codeblock>")
    @commands.is_owner() #Change this and you're fucked
    async def _eval(self, ctx, *, code):
        """Evaluate commands."""
        code = cleancode(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pager = Pag(
            timeout=100,
            entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```python\n",
            suffix="```"
        )

        await ctx.message.add_reaction('✅')
        await pager.start(ctx)

    @commands.command(name="shutdown", description="Shutdown the bot | -shutdown", aliases=["shtdwn"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot."""
        await ctx.send("Shutting down...")
        await self.bot.logout()
        
    @commands.command(name="toggle", description="Enable/Disable a command | -toggle <command>")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        """Toggle a command."""
        command = bot.get_command(command)
        
        if command is None: await ctx.send(discord.Embed(title=f"That command doesn't exist", timestamp=datetime.datetime.utcnow(), color=discord.Color.red()))
        elif ctx.command == command: await ctx.send(discord.Embed(title=f"You cannot disable the toggle command", timestamp=datetime.datetime.utcnow(), color=discord.Color.red()))
        else:
            command.enabled = not command.enabled
            ternary = 'Enabled' if command.enabled else 'Disabled'
            color = discord.Color.green() if command.enabled else discord.Color.red()
            await ctx.send(embed=discord.Embed(title=f"{ternary} {command.qualified_name}", timestamp=datetime.datetime.utcnow(), color=color))

def setup(bot): bot.add_cog(Owner(bot))
print("Owner cog loaded")