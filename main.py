"""Where the bot starts its life."""



import os
import nextcord as nx
import nextcord.ext.commands as cmds

import global_vars
import backend.logging as lgr

import cogs


def log_something(log_str: str):
    """Logs something."""
    print(log_str)
    lgr.log_bot_status.info(log_str)


def main():
    """...main!"""
    bot = nx.Client()

    intents = nx.Intents.default()
    intents.reactions = True
    intents.members = True
    intents.guilds = True

    bot = cmds.Bot(command_prefix=global_vars.CMD_PREFIX, intents=intents)
    bot.remove_command("help")

    global_vars.global_bot = bot


    # Load all cogs
    log_something("Loading cogs...")
    cogs.RegisteredCog.load_all_cogs_to_bot(bot)
    log_something("Loaded all cogs!")


    # def test_for_commands(command):
    #     """Prints the commands registered."""
    #     log_something(bot.all_commands.keys(), command in bot.all_commands.keys())

    # testForCommands("test")

    # Log in
    log_something("Logging into bot...")
    bot_token = os.environ['CaniToken']
    bot.run(bot_token)

if __name__ == "__main__":
    main()
