"""Where the bot starts its life."""


import os
import sys

import nextcord as nx
import nextcord.ext.commands as nx_cmds

import cogs

import global_vars
import backend.logging as lgr


def log_something(log_str: str):
    """Logs something."""
    print(log_str)
    lgr.log_bot_status.info(log_str)


def main():
    """...main!"""
    dev_environment_str = sys.argv[1]
    if dev_environment_str == "production":
        global_vars.dev_environment = False
        log_something("===PRODUCTION ENVIRONMENT===")
    elif dev_environment_str == "dev":
        global_vars.dev_environment = True
        log_something("===DEV ENVIRONMENT===")
    else:
        raise ValueError("Missing environment argument. Use \"production\" or \"dev\".")


    bot = nx.Client()

    intents = nx.Intents.default()
    intents.reactions = True
    intents.members = True
    intents.guilds = True

    bot = nx_cmds.Bot(command_prefix=global_vars.CMD_PREFIX, intents=intents)
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
