import discord
from discord.ext import commands

import main
from Functions import extraFunctions as ef
from Cogs import ChannelClaiming as cC

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):

        def checkexc(type):
            return isinstance(exc, type)
        
        isRp = await cC.ChannelClaim(main.bot).isRpChannel(ctx)
    
        if checkexc(commands.CommandOnCooldown):
            time = await ef.formatTime(int(str(round(exc.retry_after, 0))[:-2]))
            await ef.sendError(ctx, f"*The command is on cooldown for `{time}` more! >:(*", sendToAuthor=isRp, resetCooldown=isRp)
            return

        elif checkexc(commands.MissingRole):
            await ef.sendError(ctx, f"*You don't have the `{exc.missing_role}` role! >:(*", sendToAuthor=isRp, resetCooldown=isRp)
            return
    
        elif checkexc(commands.MissingRequiredArgument):
            await ef.sendError(ctx, f"*Make sure you have the correct parameters! Use `{main.commandPrefix}help` to get help!*", sendToAuthor=isRp, resetCooldown=isRp)
            return

        elif checkexc(commands.ExpectedClosingQuoteError) or checkexc(commands.InvalidEndOfQuotedStringError) or checkexc(commands.UnexpectedQuoteError):
            await ef.sendError(ctx, "*Your quotation marks (`\"`) are wrong! Double-check the command if you have missing quotation marks! >:(*", sendToAuthor=isRp, resetCooldown=isRp)
            return
        
        elif checkexc(commands.NoPrivateMessage):
            await ef.sendError(ctx, "*This command is disabled in DMs! >:(*", sendToAuthor=True, resetCooldown=True)
            return


        elif checkexc(commands.CommandInvokeError):
            if (str(exc.__cause__) == "Exited Function."):
                return

        elif checkexc(commands.CommandNotFound):
            return

        await ef.sendError(ctx, "*Something went wrong! D:*\n*This error has been reported to the owner of the bot.*", exc=exc, resetCooldown=isRp, sendToOwner=True, printToConsole=True)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))