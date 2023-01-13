#!/usr/bin/env python
import os

from telegram import __version__ as tg_ver
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, Defaults, MessageHandler, filters

from bot.data.database import Database
from bot.handlers.commands import Commands
from bot.handlers.queries import Queries
from bot.i18n.locales import Locale
from logs import Logger

try:
    from telegram import __version_info__

except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This code is not compatible with your current PTB version {tg_ver}. It requires a version later than v20.0."
    )


def main() -> None:
    Logger.init_logger()

    Locale.init_locales()

    Database.init_db()

    Queries.register_fixed_queries()

    defaults = Defaults(parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    application = Application.builder().token(os.getenv("TOKEN")).defaults(defaults).build()

    application.add_handler(MessageHandler(filters=filters.COMMAND, callback=Commands.commands_handler))
    application.add_handler(CallbackQueryHandler(callback=Queries.callback_queries_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
