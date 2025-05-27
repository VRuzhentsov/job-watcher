"""
Simple Telegram Bot Service for Jobs Watcher
"""

import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
# TELEGRAM_BOT_TOKEN
logger.info("Initializing Telegram bot with token: %s", bot_token)
if not bot_token:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    exit(1)

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    """Handle /start command"""
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer("🚀 Welcome to Jobs Watcher Bot!\n\nI'm here to help you find job opportunities.")

async def start_bot():
    """Main entry point for the bot"""
    logger.info("Starting Telegram bot...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.session.close()

def run_bot():
    """Run bot in main thread"""
    logger.info("Starting Telegram bot polling...")
    asyncio.run(start_bot())
