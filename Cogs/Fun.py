import discord
import discord.ext.commands as commands
import asyncio

import main
from Functions import sqlInteraction as sI
from Functions import firebaseInteraction as fi
from Functions import extraFunctions as ef

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["b"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def bark(self, ctx, *args):
        barkPath = ["guilds", ctx.guild.id, "fun", "barking"]

        if len(args) == 0:
            #Normal Barking
            await ctx.send(f"*Bark! :D*")

            # Update Data
            barkCount = fi.getData(barkPath + ["totalBarks"])
            barkCount += 1
            fi.editData(barkPath, {"totalBarks": barkCount})

            if fi.isDataExists(barkPath + ["users", ctx.author.id]):
                barkUser = fi.getData(barkPath + ["users", ctx.author.id, "barkCount"])
                barkUser += 1
                fi.editData(barkPath + ["users", ctx.author.id], {"barkCount": barkUser})
            else:
                defaultData = {
                    ctx.author.id: {
                        "barkCount": 1
                    }
                }
                fi.editData(barkPath + ["users"], defaultData)

        else:
            # Bark Rank
            if args[0] == "rank":
                users = fi.getData(barkPath + ["users"])
                if users == "null":
                    await ef.sendError(ctx, "*There wasn't anyone that made me bark yet. Be the first one!*")
                    return

                userSort = sorted(users, key=lambda x: users[x]["barkCount"])
                userSort.reverse()

                totalBarks = fi.getData(barkPath + ["totalBarks"])

                embed = discord.Embed(name="Leaderboard", title=f"Barking Leaderboard!", color=0x00FFFF)

                embed.add_field(name=f"Total Barks: {totalBarks}", value=f"`----------`", inline=False)

                formatList = []
                for i in range(5):
                    try:
                        userId = userSort[i]
                    except IndexError:
                        continue
                    userObj = await main.bot.fetch_user(userId)
                    userBarks = users[userId]["barkCount"]
                    formatList.append(f"{i + 1}. {userObj.name}: {userBarks}")

                formatStr = "\n".join(formatList)   
                embed.add_field(name=f"Leaderboard:", value=f"```{formatStr}```", inline=False)

                embed.add_field(name=f"`----------`", value=f"_ _", inline=False)

                if str(ctx.author.id) in users:
                    userYou = users[str(ctx.author.id)]["barkCount"]
                else:
                    userYou = 0
                
                embed.add_field(name=f"Your total barks: {userYou}", value=f"_ _", inline=False)

                await ctx.send(embed=embed)

            else:
                await ef.sendError(ctx, f"*Make sure you have the correct parameters! Use `{main.commandPrefix}help` to get help!*")
    


    @commands.command()
    @commands.cooldown(1, 120, type=commands.BucketType.guild)
    async def meow(self, ctx):
        await ef.delayMessage(ctx, f"...")
        await ef.delayMessage(ctx, f"...what did you just make me do.")
        await ef.delayMessage(ctx, f"*grrrrrrrrrrRRRRRR**RRRRRRRRRR***", duration=1)
        await ef.delayMessage(ctx, f"https://cdn.discordapp.com/attachments/588692481001127936/867477895924154378/image0.png", duration=0.5)
        await ef.delayMessage(ctx, f"**FEEL THE WRATH OF MY MACHINE GUN ATTACHMENTS, HUMAN**", duration=1)
        await ef.delayMessage(ctx, f"*BULLET RAIN*", duration=2)
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