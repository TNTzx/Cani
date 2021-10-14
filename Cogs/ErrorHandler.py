import discord
import discord.ext.commands as cmds

import main
from Functions import ExtraFunctions as ef
from Cogs import ChannelClaiming as cc

class ErrorHandler(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cmds.Cog.listener()
    async def on_command_error(self, ctx, exc):

        def checkexc(type):
            return isinstance(exc, type)
    
        if checkexc(cmds.CommandOnCooldown):
            time = ef.formatTime(int(str(round(exc.retry_after, 0))[:-2]))
            await ef.sendError(ctx, f"*The command is on cooldown for `{time}` more! >:(*")
            return

        elif checkexc(cmds.MissingRole):
            await ef.sendError(ctx, f"*You don't have the `{exc.missing_role}` role! >:(*")
            return
    
        elif checkexc(cmds.MissingRequiredArgument):
            await ef.sendError(ctx, f"*Make sure you have the correct parameters! Use `{main.commandPrefix}help` to get help!*")
            return

        elif checkexc(cmds.ExpectedClosingQuoteError) or checkexc(cmds.InvalidEndOfQuotedStringError) or checkexc(cmds.UnexpectedQuoteError):
            await ef.sendError(ctx, "*Your quotation marks (`\"`) are wrong! Double-check the command if you have missing quotation marks! >:(*")
            return
        
        elif checkexc(cmds.NoPrivateMessage):
            await ef.sendError(ctx, "*This command is disabled in DMs! >:(*", sendToAuthor=True, resetCooldown=True)
            return


        elif checkexc(cmds.CommandInvokeError):
            if (str(exc.__cause__) == "Exited Function."):
                return

        elif checkexc(cmds.CommandNotFound):
            return

        await ef.sendError(ctx, "*Something went wrong! D:*\n*This error has been reported to the owner of the bot.*", exc=exc, resetCooldown=True, sendToOwner=True, printToConsole=True)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))