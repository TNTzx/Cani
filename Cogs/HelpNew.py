import discord
import discord.ext.commands as cmds

import main
from Functions import CommandWrappingFunction as cw
from Functions import ExtraFunctions as ef


class Help(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cw.command(
        category = cw.Categories.basicCommands,
        description="WHY DID YOU GET HELP FOR A HELP COMMAND?????",
        parameters={"[command]": "I DON'T UNDERSTAND YOU, WHY, WHY DID YOU DO THIS????"},
        aliases=["h"],
        guildOnly=False,
        cooldown=1, cooldownType=cmds.BucketType.user
    )
    async def help(self, ctx, command=None):
        async def showAll():
            embed = discord.Embed(
                title="Help!",
                description=f"what the dog doin\n**__Command Prefix: {main.commandPrefix}__**",
                color=0x4e5d94
            )
            for category, name in cw.ListOfCommands.commandsAll.items():
                nameFormat = f"`{'`, `'.join(name)}`"
                embed.add_field(name=category, value=nameFormat, inline=False)
            await ctx.send(embed=embed)

            
        async def specific():
            if not command in cw.ListOfCommands.commands:
                await ef.sendError(ctx, "This command doesn't exist! Make sure you typed it correctly!")
                return

            cmd: cw.CustomCommandClass = cw.ListOfCommands.commands[command]
            help = cmd.help

            embed = discord.Embed(
                title=f"Help: {help.category} // {main.commandPrefix}{cmd.name}",
                color=0x4e5d94
            )

            async def createSeparator():
                separator = f"{'-' * 20}"
                embed.add_field(name=separator, value="_ _", inline=False)
            

            embed.add_field(name="Description", value=help.description, inline=False)

            if len(help.aliases) > 0:
                aliases = "`, `".join(help.aliases)
                embed.add_field(name=f"Aliases:", value=f"`{aliases}`", inline=False)
            
            await createSeparator()

            syntaxList = "> <".join([x for x in help.parameters.keys()])
            syntaxList = f" `<{syntaxList}>`" if not syntaxList == "" else "_ _"
            embed.add_field(name=f"Syntax:", value=f"`{main.commandPrefix}{cmd.name}`{syntaxList}", inline=False)

            if len(help.parameters) > 0:
                paramsList = "\n".join([f"`<{param}>`: {paramDesc}" for param, paramDesc in help.parameters.items()])
                embed.add_field(name=f"Parameters:", value=f"{paramsList}", inline=False)
            
            await createSeparator()

            guildOnly = "only in servers" if help.guildOnly else "in Direct Messages and servers"
            embed.add_field(name=f"Can be used {guildOnly}", value="_ _", inline=False)

            require = cmd.help.require
            if require.guildOwner or require.guildAdmin or require.dev:
                requirements = []
                if require.guildOwner: requirements.append("Server Owner")
                if require.guildAdmin: requirements.append("Server Owner / Admins")
                if require.dev: requirements.append("Bot Developer")

                requirementsForm = "`, `".join(requirements)

                embed.add_field(name=f"Only allowed for:", value=f"`{requirementsForm}`")

            cooldown = cmd.help.cooldown
            if cooldown.length > 0:
                if cooldown.typeOfCooldown == cmds.BucketType.guild:
                    cooldownType = "Entire server"
                elif cooldown.typeOfCooldown == cmds.BucketType.member:
                    cooldownType = "Per member"
                elif cooldown.typeOfCooldown == cmds.BucketType.channel:
                    cooldownType = "Per channel"
                elif cooldown.typeOfCooldown == cmds.BucketType.category:
                    cooldownType = "Per channel category"
                elif cooldown.typeOfCooldown == cmds.BucketType.role:
                    cooldownType = "Per role"
                else:
                    cooldownType = "TNTz messed up, they didn't add another edge case, please ping him"
                cooldownForm = f"Duration: `{help.cooldown.length}`\nApplies to: {cooldownType}"
                embed.add_field(name=f"Cooldown Info:", value=f"{cooldownForm}")

            if not len(help.exampleUsage) == 0:
                exampleUsageForm = "`\n`".join(help.exampleUsage)
                embed.add_field(name=f"Examples on How To Use:", value=f"`{exampleUsageForm}`", inline=False)

            await ctx.send(embed=embed)


        if command == None:
            await showAll()
        else:
            await specific()

def setup(bot):
    bot.add_cog(Help(bot))