"""Contains error handling."""


import asyncio
import traceback
import nextcord as nx
import nextcord.ext.commands as nx_cmds

import global_vars
import backend.discord_utils as disc_utils
import backend.exc_utils as exc_utils
import backend.logging as lgr
import backend.other as ot

from ... import utils as cog


class CogErrorHandler(cog.RegisteredCog):
    """Contains error handling."""

    @nx_cmds.Cog.listener()
    async def on_command_error(self,
            ctx: nx_cmds.Context,
            exc: Exception | nx_cmds.CommandInvokeError
            ):
        """Called when there is an error in one of the commands."""
        try:
            if isinstance(exc, nx_cmds.CommandOnCooldown):
                time = ot.format_time(int(str(round(exc.retry_after, 0))[:-2]))
                await exc_utils.SendFailedCmd(
                    error_place = exc_utils.ErrorPlace.from_context(ctx),
                    suffix = f"The command is on cooldown for `{time}` more!"
                ).send()


            if isinstance(exc, nx_cmds.MissingRole):
                exc_utils.reset_cooldown(ctx)
                await exc_utils.SendFailedCmd(
                    error_place = exc_utils.ErrorPlace.from_context(ctx),
                    suffix = f"You don't have the `{exc.missing_role}` role!"
                    ).send()


            if isinstance(exc, (nx_cmds.MissingRequiredArgument, nx_cmds.BadArgument)):
                exc_utils.reset_cooldown(ctx)
                await exc_utils.SendFailedCmd(
                    error_place = exc_utils.ErrorPlace.from_context(ctx),
                    suffix = f"Make sure you have the correct parameters! Use `{global_vars.CMD_PREFIX}help {ctx.command.name}` to get help!"
                    ).send()


            if isinstance(exc, (
                        nx_cmds.ExpectedClosingQuoteError,
                        nx_cmds.InvalidEndOfQuotedStringError,
                        nx_cmds.UnexpectedQuoteError
                        )
                    ):
                exc_utils.reset_cooldown(ctx)
                await exc_utils.SendFailedCmd(
                    error_place = exc_utils.ErrorPlace.from_context(ctx),
                    suffix = "Your quotation marks (`\"`) are wrong! Double-check the command if you have missing quotation marks!"
                    ).send()


            if isinstance(exc, nx_cmds.NoPrivateMessage):
                exc_utils.reset_cooldown(ctx)
                await exc_utils.SendFailedCmd(
                    error_place = exc_utils.ErrorPlace.from_context(ctx),
                    suffix = "This command is disabled in DMs!"
                ).send()


            if isinstance(exc, nx_cmds.CommandInvokeError):
                if isinstance(exc.original, exc_utils.ExitFunction):
                    return

                if isinstance(exc.original, exc_utils.FailedCmd):
                    exc_utils.reset_cooldown(ctx)
                    return


                if hasattr(exc.original, "status"):
                    if exc.original.status == 403:
                        error_message = f"Forbidden from sending. Code {exc.original.code}: {exc.original.text}"
                        lgr.log_discord_forbidden.warning(error_message)


                if isinstance(exc.original, asyncio.TimeoutError):
                    exc_utils.reset_cooldown(ctx)
                    await exc_utils.SendTimeout(
                        error_place = exc_utils.ErrorPlace.from_context(ctx),
                    ).send()


                if isinstance(exc.original, nx.NotFound):
                    error_message = f"Not found. Code {exc.original.code}: {exc.original.text}"
                    lgr.log_discord_forbidden.warning(error_message)
                    return


                if isinstance(exc.original, disc_utils.UsageReqNotMet):
                    return


            if isinstance(exc, (
                        nx_cmds.CommandNotFound,
                    )
                ):
                return

        except exc_utils.FailedCmd:
            return


        # If command is not in the list of handles, send a fatal error.
        exc_utils.reset_cooldown(ctx)


        await global_vars.tntz.send((
            "Fatal error!\n"
            f"Command used: `{ctx.message.content}`\n"
            f"```{exc}```"
        ))


        if isinstance(exc, nx_cmds.CommandInvokeError):
            error = exc.original
        else:
            error = exc

        formatted_exc = "".join(traceback.format_exception(error))

        print((
            f"A fatal error occurred in command {ctx.command.name}:"
            f"{formatted_exc}"
        ))


        await ctx.send(
            "**FATAL! :(**\n"
            "Something bad went wrong. This error has been reported to the owner of the bot."
        )
        lgr.log_global_exc.error(formatted_exc)
