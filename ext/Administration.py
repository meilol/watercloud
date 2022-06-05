import datetime
import discord
from Watercloud import bot
from discord.ext import commands

class Administration(commands.Cog):

    def __init__(self, bot): self.bot = bot
    
    @commands.command(name="lockdown", description="Lockdown the server | -lockdown [reason]")
    #@commands.has_permissions(manage_guild=True)
    async def lockdown(self, ctx, *, reason="No reason provided"):
        if ctx.message.author.guild_permissions.manage_guild == False:
            embed = discord.Embed(title=f"❌ Could not lockdown server", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have the permission to manage channels", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)
            return
        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            except Exception as e:
                if e == "403 Forbidden (error code: 50013): Cannot modify send_messages": 
                    continue
                embed = discord.Embed(title=f"❌ Could not lockdown {channel}", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed.add_field(name="Error", value=e, inline=True)
                embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                await ctx.reply(embed=embed)
        
        #Send the lockdown embed
        embed = discord.Embed(title=f"🔒 Server locked down", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.set_footer(text=f"Locked down by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.reply(embed=embed)
        await ctx.guild.edit(reason=reason, system_channel_id=None)
        
    @commands.command(name="unlock", description="Unlock the server | -unlock")
    @commands.has_permissions(manage_guild=True)
    async def unlock(self, ctx, *, reason="No reason provided"):
        if ctx.message.author.guild_permissions.manage_guild == False:
            embed = discord.Embed(title=f"❌ Could not unlock server", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have the permission to manage channels", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)
            return
        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            except Exception as e:
                embed = discord.Embed(title=f"❌ Could not unlock {channel}", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed.add_field(name="Error", value=e, inline=True)
                embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                await ctx.reply(embed=embed)
        
        #Send the unlock embed
        embed = discord.Embed(title=f"🔓 Server unlocked", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.set_footer(text=f"Unlocked by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.reply(embed=embed)
        await ctx.guild.edit(system_channel_id=None)

def setup(bot): bot.add_cog(Administration(bot))
print("Administration cog loaded")
