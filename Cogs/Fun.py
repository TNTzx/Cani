import discord
import discord.ext.commands as cmds

import main
from Functions import FirebaseInteraction as fi
from Functions import ExtraFunctions as ef

class Fun(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def barkPath(self, ctx):
        return ["guilds", ctx.guild.id, "fun", "barking"]
        

    async def specialEvents(self, ctx):
        path = await self.barkPath(ctx)

        async def eventTrigger(milestone, message):
            if fi.getData(path + ["totalBarks"]) >= milestone and (not fi.getData(path + ["barkMilestone"]) == milestone):
                await ctx.send("*>>> Oh? Something's happening...*")
                fi.editData(path, {"barkMilestone": milestone})
                await ctx.send(message)

        await eventTrigger(10000, ">>> YAYYAYAYAYYAAYAYA- AM HAPPY!! :D!!\n*Cani likes this server! The command `++pat` has been unlocked!*\n*Use `++help pat` for more information.*")


    async def updateBark(self, ctx, added):
        path = await self.barkPath(ctx)
        
        barkCount = fi.getData(path + ["totalBarks"])
        barkCount += added
        fi.editData(path, {"totalBarks": barkCount})
        
        if fi.isDataExists(path + ["users", ctx.author.id]):
            barkUser = fi.getData(path + ["users", ctx.author.id, "barkCount"])
            barkUser += added
            fi.editData(path + ["users", ctx.author.id], {"barkCount": barkUser})
        else:
            defaultData = {
                ctx.author.id: {
                    "barkCount": added
                }
            }
            fi.editData(path + ["users"], defaultData)

        await self.specialEvents(ctx)


    @cmds.command(aliases=["b"])
    @cmds.cooldown(1, 2, cmds.BucketType.user)
    async def bark(self, ctx):
        await ctx.send(f"*Bark! :D*")
        await self.updateBark(ctx, 1)
    
    @cmds.command(aliases=["pt"])
    @cmds.cooldown(1, 1 * 60 * 60 * 12, cmds.BucketType.guild)
    async def pat(self, ctx: cmds.Context):
        path = await self.barkPath(ctx)

        if not fi.getData(path + ["barkMilestone"]) >= 10000:
            ctx.command.reset_cooldown(ctx)
            return

        addBark = 200

        await ctx.send("https://cdn.discordapp.com/emojis/889713240714649650.gif")
        await ctx.send(f"""*:D!! Bark! Bark!*\n*I barked happily thanks to your pat! (+{addBark} barks {ctx.author.mention}!)*""")
        await self.updateBark(ctx, addBark)
        
    
    @cmds.command(aliases=["br"])
    @cmds.cooldown(1, 60 * 2, cmds.BucketType.guild)
    async def barkrank(self, ctx):
        await ctx.send("*Getting leaderboard...*")
        path = await self.barkPath(ctx)

        users = fi.getData(path + ["users"])
        if users == "null":
            await ef.sendError(ctx, "*There wasn't anyone that made me bark yet. Be the first one!*")
            return

        userSort = sorted(users, key=lambda x: users[x]["barkCount"])
        userSort.reverse()

        totalBarks = fi.getData(path + ["totalBarks"])

        embed = discord.Embed(name="Leaderboard", title=f"Barking Leaderboard!", color=0x00FFFF)
        embed.add_field(name=f"Total Barks: {totalBarks}", value=f"`----------`", inline=False)

        formatList = []
        for userId in userSort:
            userObj = await main.bot.fetch_user(userId)
            userBarks = users[userId]["barkCount"]
            formatList.append(f"{userSort.index(userId) + 1}. {userObj.name}: {userBarks}")

        formatStr = "\n".join(formatList)   
        embed.add_field(name=f"Leaderboard:", value=f"```{formatStr}```", inline=False)
        embed.add_field(name=f"`----------`", value=f"_ _", inline=False)

        if str(ctx.author.id) in users:
            userYou = users[str(ctx.author.id)]["barkCount"]
            userYouIndex = userSort.index(str(ctx.author.id))
            userYouPos = userYouIndex + 1
        else:
            userYou = 0
            userYouIndex = "?"
            userYouPos = "?"
        
        async def barkRelative(pos, place):
            async def getUser(pos, offset):
                pos -= 1
                user = await main.bot.fetch_user(userSort[pos + offset])
                userBarks = users[str(user.id)]["barkCount"]
                return user, userBarks
            
            if place == "up":
                user, userBarks = await getUser(pos, -1)
                return f"Next place up: `{pos - 1}. {user.name}: {userBarks}`"
            elif place == "down":
                user, userBarks = await getUser(pos, 1)
                return f"Previous place down: `{pos + 1}. {user.name}: {userBarks}`"
        

        if userYouIndex == "?":
            descFirst = await barkRelative(len(userSort), "up")
            descLast = "You didn't make me bark yet!"
        elif userYouIndex == 0:
            descFirst = await barkRelative(userYouPos, "down")
            descLast = "You're #1!"
        elif userYouIndex == (len(userSort) - 1):
            descFirst = await barkRelative(userYouPos, "up")
            descLast = "You're last place!"
        else:
            descFirst = await barkRelative(userYouPos, "up")
            descLast = await barkRelative(userYouPos, "down")
        
        embed.add_field(name=f"Your total barks: {userYou} (#{userYouPos})", value=f"{descFirst}\n{descLast}", inline=False)

        await ctx.send(embed=embed)


    @cmds.command()
    @cmds.cooldown(1, 60 * 2, type=cmds.BucketType.guild)
    async def meow(self, ctx):
        await ef.delayMessage(ctx, f"...")
        await ef.delayMessage(ctx, f"...what did you just make me do.")
        await ef.delayMessage(ctx, f"*grrrrrrrrrrRRRRRR**RRRRRRRRRR***", duration=1)
        await ctx.send("*(Art by glasses!)*")
        await ef.delayMessage(ctx, f"https://cdn.discordapp.com/attachments/588692481001127936/867477895924154378/image0.png", duration=0.5)
        await ef.delayMessage(ctx, f"**FEEL THE WRATH OF MY MACHINE GUN ATTACHMENTS, HUMAN**", duration=1)
        await ef.delayMessage(ctx, f"*BULLET RAIN*", duration=2)
        

    @cmds.command()
    @cmds.cooldown(1, 60 * 2, type=cmds.BucketType.guild)
    async def pork(self, ctx):
        await ef.delayMessage(ctx, f"https://media1.giphy.com/media/Lt3qObVV60Qda/200.gif", duration=7, delete=True)
        await ef.delayMessage(ctx, f"https://i.redd.it/bgmfikr8j9751.png", duration=2, delete=True)
        await ef.delayMessage(ctx, f"https://thumbs.gfycat.com/GreedyCourageousKrill-max-1mb.gif", duration=2)
        await ctx.send("*Yum!*")
    

def setup(bot):
    bot.add_cog(Fun(bot))