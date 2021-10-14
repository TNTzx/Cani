import discord
import discord.ext.commands as cmds


class Help(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot

    


def setup(bot):
    bot.add_cog(Help(bot))