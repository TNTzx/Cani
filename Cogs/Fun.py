import discord
import discord.ext.commands as commands
import asyncio

from Functions import sqlInteraction as sI
from Functions import extraFunctions as ef

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["b"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def bark(self, ctx):
        barkCount = sI.getData(ctx.guild.id, "bark_count", type=int)
        barkCount += 1
        sI.editData(ctx.guild.id, bark_count=barkCount)
        await ctx.send(f"*Bark! :D*")
    
    @commands.command(aliases=["bc"])
    async def barkcount(self, ctx):
        barkCount = sI.getData(ctx.guild.id, "bark_count", type=int)
        await ctx.send(f"*I've barked for a total of {barkCount} times!*")


    @commands.command()
    @commands.cooldown(1, 120, type=commands.BucketType.guild)
    async def meow(self, ctx):
        await ef.delayMessage(ctx, f"...")
        await ef.delayMessage(ctx, f"...what did you just make me do.")
        await ef.delayMessage(ctx, f"*grrrrrrrrrrRRRRRR**RRRRRRRRRR***", duration=1)
        await ef.delayMessage(ctx, f"https://cdn.discordapp.com/attachments/588692481001127936/867477895924154378/image0.png", duration=0.5)
        await ef.delayMessage(ctx, f"**FEEL THE WRATH OF MY MACHINE GUN ATTACHMENTS, HUMAN**", duration=1)
        await ef.delayMessage(ctx, f"*BULLET RAIN*", duration=1)
        await ctx.send("*Art by glasses.*")

    @commands.command()
    @commands.cooldown(1, 120, type=commands.BucketType.guild)
    async def pork(self, ctx):
        await ef.delayMessage(ctx, f"https://media1.giphy.com/media/Lt3qObVV60Qda/200.gif", duration=7, delete=True)
        await ef.delayMessage(ctx, f"https://i.redd.it/bgmfikr8j9751.png", duration=2, delete=True)
        await ef.delayMessage(ctx, f"https://thumbs.gfycat.com/GreedyCourageousKrill-max-1mb.gif", duration=2)
        await ctx.send("*Yum!*")
    

def setup(bot):
    bot.add_cog(Hello(bot))