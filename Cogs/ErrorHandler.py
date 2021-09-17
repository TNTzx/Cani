import discord
from discord.ext import commands

import main
from Functions import functionsandstuff as fas

errorPrefix = "**Error! D:**\n"

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):

        def checkexc(type):
            return isinstance(exc, type)
    
        if checkexc(commands.CommandOnCooldown):
            time = await fas.formatTime(int(str(round(exc.retry_after, 0))[:-2]))
            await fas.sendError(ctx, f"*The command is on cooldown for `{time}` more! >:(*")
            return

        elif checkexc(commands.MissingRole):
            await fas.sendError(ctx, f"*You don't have the `{exc.missing_role}` role! >:(*")
            return
    
        elif checkexc(commands.MissingRequiredArgument):
            await fas.sendError(ctx, f"Make sure you have the correct parameters! Use `{main.commandPrefix}help` to get help!")
            return
        
        elif checkexc(commands.NoPrivateMessage):
            await fas.sendError(ctx, "*This command is disabled in DMs! >:(*", sendToOwner=True)
        
        elif checkexc(commands.CommandInvokeError):
            if (str(exc.__cause__) == "Exited Function."):
                return

        elif checkexc(commands.CommandNotFound):
            return

        await fas.sendError(ctx, "*Something went wrong! D: This error has been reported to the owner of the bot.*", exc=exc, sendToOwner=True, printToConsole=True)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))