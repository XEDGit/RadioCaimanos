from bot.bot import Bot
from pathlib import Path
import logging
import sys
import asyncio

def setup_logging():
    """Configure logging for the bot."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('discord_bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

async def connect_bot(bot, token):
    await bot.start(token)

def main():
    bot = None
    try:
        setup_logging()
        token_file = Path('discord_bot_token')
        if not token_file.exists():
            logging.error('No "discord_bot_token" file was found')

        bot = Bot()
        asyncio.run(connect_bot(bot, token_file.read_text().strip()))
    except KeyboardInterrupt:
        logging.info('Bot stopped by user')
    finally:
        if bot:
            asyncio.run(bot.close())
        logging.info('Bot has been shut down')
if __name__ == '__main__':
    main()
