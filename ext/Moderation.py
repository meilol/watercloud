import datetime
import discord
import mysql.connector
from discord.ext import commands
from discord.ext import tasks


config = {
    "host":  "",
    "user": "",
    "password": "",
    "database": "",
    "raise_on_warnings": True,
}

try: #Everything
    cum = mysql.connector.connect(**config)
    cursor = cum.cursor()
    print(f"Connected to {config['user']}")
except mysql.connector.Error as err: print("You fucked up lmao" + str(err))

class Moderation(commands.Cog):
    def __init__(self, bot): self.bot = bot
        
    #TODO: Add mute/unmute, purge, auto moderation and custom filtered words
    
    @commands.command(name="mute", description="Mute a user | -mute <user mention> <time (int)s/m/h/d/w/m> [reason (str)]")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: str = None, *, reason: str = "No reason given"):
            if len(reason) > 255: reason = reason[:252] + "..."
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            timeConvert = {"s": 1, "m": 60, "h": 3600,"d": 86400}
            tempmute = int(time[0]) * timeConvert[time[-1]]
            if role not in ctx.guild.roles:
                await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False))
                await member.add_roles(role)
                embed = discord.Embed(description= f"✅ **{member.display_name}#{member.discriminator} muted successfully**", color=discord.Color.green())
            else:
                await member.add_roles(role) 
                embed = discord.Embed(description= f"✅ **{member.display_name}#{member.discriminator} muted successfully**", color=discord.Color.green())
            await ctx.send(embed=embed)
            
            member = int(member.id)
            try:
                #Add to the database
                cursor.execute("INSERT INTO `"+ str(ctx.guild.id) +"` (ClientID, MutedBy, MutedTime, MutedReason) VALUES (" + str(member) + ", " + str(ctx.author.name + "#" + ctx.author.discriminator) + ", " + str(datetime.datetime.now() + datetime.timedelta(seconds=tempmute)) + ", '" + reason + "');")
                cum.commit()
            except:
                cursor.execute("CREATE TABLE `" + str(ctx.guild.id) + "` (ClientID BIGINT, MutedBy VARCHAR(255), MutedTime INT, MutedReason VARCHAR(255));")
                cursor.execute("INSERT INTO `"+ str(ctx.guild.id) +"` (ClientID, MutedBy, MutedTime, MutedReason) VALUES (" + str(member) + ", " + str(ctx.author.name + "#" + ctx.author.discriminator) + ", " + str(datetime.datetime.now() + datetime.timedelta(seconds=tempmute)) + ", '" + reason + "');")
                cum.commit()
                
            
    
    #Check if user time has expired, and if so, unmute them
    @tasks.loop(seconds=10)
    async def checkMute(self):
        for guild in self.bot.guilds:
            cursor.execute("SELECT * FROM `"+ str(guild.id) +"`;")
            data = cursor.fetchall()
            for row in data:
                if row[2] < datetime.datetime.now():
                    member = guild.get_member(row[0])
                    role = discord.utils.get(guild.roles, name="Muted")
                    await member.remove_roles(role)
                    cursor.execute("DELETE FROM `"+ str(guild.id) +"` WHERE ClientID = " + str(row[0]) + ";")
                    cum.commit()
        
            
            
    @commands.command(name="kick", description="Kick a user from the server | -kick <user> [reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.kick(reason=reason)
            memberE = discord.Embed(title=f"You have been kicked from {ctx.guild.name} | {reason}", color=discord.Color.red())
            await member.send(embed=memberE)
            embed = discord.Embed(title=f"✅ Kicked {member} ({member.id})", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            embed.add_field(name="Reason", value=reason, inline=True)
            embed.set_footer(text=f"Kicked by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)
        except Exception as e:
            if e == "403 Forbidden (error code: 50007): Cannot send messages to this user": 
                await member.kick(reason=reason)
                embed = discord.Embed(title=f"✅ Kicked {member} ({member.id})", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                embed.add_field(name="Reason", value=reason, inline=True)
                embed.set_footer(text=f"Kicked by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                await ctx.reply(embed=embed)
                return
            embed = discord.Embed(title=f"❌ Could not kick {member} ({member.id})", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value=e, inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)

    @commands.command(name="ban", description="Ban a user from the server | -ban <user> [reason]")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.ban(reason=reason)
            memberE = discord.Embed(title=f"You have been banned from {ctx.guild.name} | {reason}", color=discord.Color.red())
            await member.send(embed=memberE)
            embed = discord.Embed(title=f"✅ Banned {member} ({member.id})", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            embed.add_field(name="Reason", value=reason, inline=True)
            embed.set_footer(text=f"Banned by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)
        except Exception as e:
            if e == "403 Forbidden (error code: 50007): Cannot send messages to this user": 
                await member.ban(reason=reason)
                embed = discord.Embed(title=f"✅ Banned {member} ({member.id})", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                embed.add_field(name="Reason", value=reason, inline=True)
                embed.set_footer(text=f"Banned by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                await ctx.reply(embed=embed)
                return
            embed = discord.Embed(title=f"❌ Could not ban {member} ({member.id})", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value=e, inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)

    @commands.command(name="unban", description="Unban a user from the server | -unban <user>")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans()
        memberName, memberDiscriminator = member.split('#')
        
        try:
            for banEntry in bannedUsers:
                user = banEntry.user
                
                if (user.name, user.discriminator) == (memberName, memberDiscriminator):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(title=f"✅ Unbanned {member}", description=f"Executed successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
                    embed.set_footer(text=f"Unbanned by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    await ctx.reply(embed=embed)
                    return
                
        except Exception as e:     
            embed = discord.Embed(title=f"❌ Could not unban {member}", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value=e, inline=True)
            embed.set_footer(text=f"Unban attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)
            return

    @ban.error
    async def ban_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f"❌ Could not ban that user", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have permission to ban members", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)

    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f"❌ Could not kick that user", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have permission to kick members", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)
            
    @unban.error
    async def unban_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f"❌ Could not unban that user", description=f"Failed to execute", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Error", value="You do not have permission to unban members", inline=True)
            embed.set_footer(text=f"Attempted by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.reply(embed=embed)
        
def setup(bot): bot.add_cog(Moderation(bot))
print("Moderation cog loaded")