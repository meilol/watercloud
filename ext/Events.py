import datetime
import discord
import requests
import re
from Watercloud import bot
from discord.ext import commands
from Watercloud import cnx, mycursor, VERSION


class Events(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.version = VERSION
    
    @commands.Cog.listener()
    async def on_ready(self):
        await bot.change_presence(activity=discord.Game(name="-help"))
        print("Logged in as: " + bot.user.name + "#" + bot.user.discriminator + " (" + str(bot.user.id) + ")")
        print("Version: " + self.version)
        channel = bot.get_channel(931148500710875156)
        
        embed = discord.Embed(title=f"✅ Watercloud started successfully", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
        embed.add_field(name="Console", value=f"```py\nLogged in as: {bot.user.name}#{bot.user.discriminator}\nReady```", inline=True)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            embed = discord.Embed(title=f"Message deleted", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Author", value=f"{message.author} [{message.author.id}]", inline=True)
            embed.add_field(name="Content", value=message.content, inline=True)
            if 'http' in message.content:
                if 'https' in message.content: url = re.findall(r'(https?://[^\s]+)', message.content)
                else: url = re.findall(r'(http?://[^\s]+)', message.content)
                embed.add_field(name="Link(s)", value=f"{url}", inline=True)
            
            ServerID = message.guild.id
            
            cnx.reconnect(attempts=3)
            mycursor.execute(f"SELECT * FROM WCTable WHERE ServerID = {ServerID}")

            result = mycursor.fetchall()

            ChannelID = str(result[0]).split(", ")[1].replace(")", "") #¯\_(ツ)_/¯
            ServerID = str(result[0]).split(", ")[0].replace("(", "") #¯\_(ツ)_/¯
            
            
            ChannelToSend = bot.get_channel(int(ChannelID))
            await ChannelToSend.send(embed=embed)
        except:
            embed = discord.Embed(title=f"Message deleted", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Author", value=f"{message.author} [{message.author.id}]", inline=True)
            embed.add_field(name="Content", value="Most likely an embed or attachment", inline=True)

            if message.attachments:
                if len(message.attachments) == 1:
                    embed.add_field(name="Attachment", value=message.attachments[0].url)
                    if message.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')): 
                        
                        extension = message.attachments[0].url.split(".")[-1] #it works

                        img_data = requests.get(message.attachments[0].url).content
                        with open(f'attachments/{message.id}.{extension}', 'wb') as handler:
                            handler.write(img_data)
                        file = discord.File("attachments/" + str(message.id) + "." + str(extension), filename=f"image.{extension}")
                        embed.set_image(url=f"attachment://image.{extension}") #it works: also
            
            try:
                ServerID = message.guild.id
                
                mycursor.execute(f"SELECT * FROM WCTable WHERE ServerID = {ServerID}")

                result = mycursor.fetchall()

                ChannelID = str(result[0]).split(", ")[1].replace(")", "")
                ServerID = str(result[0]).split(", ")[0].replace("(", "")
                
                
                ChannelToSend = bot.get_channel(int(ChannelID))
                await ChannelToSend.send(file=file, embed=embed)
            except:
                return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "<@!931264476852928643>": await message.channel.send("-help for more info")
        #if str(message.content).startswith("-"): await bot.process_commands(message) 
        
        if message.author.bot: return
        if message.guild is None: return

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        try:
            if message_before.content == message_after.content: return
            embed=discord.Embed(title=f"Message edited (click to view)", url=f"https://discord.com/channels/{message_before.guild.id}/{message_before.channel.id}/{message_before.id}", timestamp=datetime.datetime.utcnow(), color=0xFFFF00)
            embed.add_field(name="Author", value=f"{message_before.author} [{message_before.author.id}]", inline=True)
            embed.add_field(name="Before", value=message_before.content, inline=True)
            embed.add_field(name="After", value=message_after.content, inline=True)
            ServerID = message_before.guild.id
                
            if message_before.attachments:
                if len(message_before.attachments) == 1:
                    embed.add_field(name="Attachment", value=message_before.attachments[0].url)
                    if message_before.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')): 
                        
                        extension = message_before.attachments[0].url.split(".")[-1]

                        img_data = requests.get(message_before.attachments[0].url).content
                        with open(f'attachments/{message_before.id}.{extension}', 'wb') as handler:
                            handler.write(img_data)
                        file = discord.File("attachments/" + str(message_before.id) + "." + str(extension), filename=f"image.{extension}")
                        embed.set_image(url=f"attachment://image.{extension}")
                
            cnx.reconnect(attempts=3)
            mycursor.execute(f"SELECT * FROM WCTable WHERE ServerID = {ServerID}")

            result = mycursor.fetchall()

            ChannelID = str(result[0]).split(", ")[1].replace(")", "")
            ServerID = str(result[0]).split(", ")[0].replace("(", "")
                
                
            ChannelToSend = bot.get_channel(int(ChannelID))
            try:
                await ChannelToSend.send(file=file, embed=embed)
            except: 
                await ChannelToSend.send(embed=embed)
        except:
            embed=discord.Embed(title=f"Message edited (click to view)", url=f"https://discord.com/channels/{message_before.guild.id}/{message_before.channel.id}/{message_before.id}", timestamp=datetime.datetime.utcnow(), color=0xFFFF00)
            embed.add_field(name="Author", value=f"{message_before.author} [{message_before.author.id}]", inline=True)
            embed.add_field(name="Before", value="Most likely an embed or attachment", inline=True)
            embed.add_field(name="After", value=message_after.content, inline=True)
            if message_before.attachments:
                if len(message_before.attachments) == 1:
                    embed.add_field(name="Attachment", value=message_before.attachments[0].url)
                    if message_before.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')): #Find the extension, if not supported, crashes. Oops
                        
                        extension = message_before.attachments[0].url.split(".")[-1]

                        img_data = requests.get(message_before.attachments[0].url).content
                        with open(f'attachments/{message_before.id}.{extension}', 'wb') as handler:
                            handler.write(img_data)
                        file = discord.File("attachments/" + str(message_before.id) + "." + str(extension), filename=f"image.{extension}")
                        embed.set_image(url=f"attachment://image.{extension}")
                        
            ServerID = message_before.guild.id
                
            #cnx.reconnect(attempts=3, delay=1)
            mycursor.execute(f"SELECT * FROM WCTable WHERE ServerID = {ServerID}")

            result = mycursor.fetchall()

            ChannelID = str(result[0]).split(", ")[1].replace(")", "")
            ServerID = str(result[0]).split(", ")[0].replace("(", "")
                
                
            ChannelToSend = bot.get_channel(int(ChannelID))
            try:
                await ChannelToSend.send(file=file, embed=embed)
            except:
                try:
                    await ChannelToSend.send(embed=embed)
                except:
                    embed=discord.Embed(title=f"CRITICAL ERROR", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                    embed.add_field(name="What caused this?", value="Either a bug in Discord, or a bug in Watercloud's code.", inline=True)
                    embed.add_field(name="How to fix?", value="Simple. [Watercloud's critical error page](https://watercloud.tk/critical)", inline=True)
                    embed.add_field(name="Author", value=f"{message_before.author} [{message_before.author.id}]", inline=True)
                    await ChannelToSend.send(embed=embed)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #if isinstance(error, commands.CommandNotFound):  return
        if isinstance(error, commands.errors.DisabledCommand): return
        if hasattr(ctx.command, "on_error"): return
            
        error = getattr(error, "original", error)
        em = discord.Embed(title="Error", description=str(error).capitalize(), color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=em, delete_after=5.0)

        
def setup(bot): bot.add_cog(Events(bot))
print("Events cog loaded")