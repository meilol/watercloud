import random
import re
from discord.ext import commands
import discord

class Fun(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command(aliases=['8ball'], description="Ask a question and I'll answer it | -8ball <question>")
    async def _8ball(self, ctx, *, question):
        responses = [
        discord.Embed(title='🎱 It is certain.', footer=question),
        discord.Embed(title='🎱 It is decidedly so.', footer=question),
        discord.Embed(title='🎱 Without a doubt.', footer=question),
        discord.Embed(title='🎱 Yes - definitely.', footer=question),
        discord.Embed(title='🎱 You may rely on it.', footer=question),
        discord.Embed(title='🎱 Most likely.', footer=question),
        discord.Embed(title='🎱 Outlook good.', footer=question),
        discord.Embed(title='🎱 Yes.', footer=question),
        discord.Embed(title='🎱 Signs point to yes.', footer=question),
        discord.Embed(title='🎱 Reply hazy, try again.', footer=question),
        discord.Embed(title='🎱 Ask again later.', footer=question),
        discord.Embed(title='🎱 Better not tell you now.', footer=question),
        discord.Embed(title='🎱 Cannot predict now.', footer=question),
        discord.Embed(title='🎱 Concentrate and ask again.', footer=question),
        discord.Embed(title="🎱 Don't count on it."),
        discord.Embed(title='🎱 My reply is no.', footer=question),
        discord.Embed(title='🎱 My sources say no.', footer=question),
        discord.Embed(title='🎱 Outlook not very good.', footer=question),
        discord.Embed(title='🎱 Very doubtful.', footer=question)]
        responses = random.choice(responses)
        await ctx.send(embed=responses)

    @commands.command(pass_context=True, aliases=['pick'])
    async def choose(self, ctx, *, choices = "Water Fire Earth Air"):
        await ctx.send(embed=discord.Embed(f'I choose: {random.choice(choices.split(" "))}'))

    @commands.command(pass_context=True)
    async def dice(self, ctx, *, msg="1"):
        dice_rolls = []
        dice_roll_ints = []
        try:
            dice, sides = re.split("[d\s]", msg)
        except ValueError:
            dice = msg
            sides = "6"
        try:
            for roll in range(int(dice)):
                result = random.randint(1, int(sides))
                dice_rolls.append(str(result))
                dice_roll_ints.append(result)
        except ValueError:
            return await ctx.send(embed=discord.Embed(title="Error", description="Invalid syntax", color=0xFF0000))
        embed = discord.Embed(title="Dice rolls:", description=' '.join(dice_rolls))
        embed.add_field(name="Total:", value=sum(dice_roll_ints))
        await ctx.send("", embed=embed)

def setup(bot): bot.add_cog(Fun(bot))
print("Fun cog loaded")