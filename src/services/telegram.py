"""
Simple Telegram Bot Service for Jobs Watcher
"""

import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FSM States for job search conversation
class JobSearchStates(StatesGroup):
    waiting_for_search_term = State()
    waiting_for_location = State()

# Bot setup
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
# TELEGRAM_BOT_TOKEN
logger.info("Initializing Telegram bot with token: %s", bot_token)
if not bot_token:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    exit(1)

bot = Bot(token=bot_token)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start_handler(message: Message):
    """Handle /start command"""
    if not message.from_user:
        logger.error("Received message without user information")
        return
    logger.info(f"User {message.from_user.id} started the bot")
      # Find or create user in database
    try:
        from models import User, db
        from app import app
        
        with app.app_context():
            user = User.find_or_create(message.from_user)
            logger.info(f"User processed: {user}")
    except Exception as e:
        logger.error(f"Database error: {e}")
        # Continue without database for now
    
    # Get version info
    try:
        from utils import get_version
        version = get_version()
        version_text = f" v{version}" if version != 'unknown' else ""
    except Exception:
        version_text = ""
    
    await message.answer(f"🚀 Welcome to Jobs Watcher Bot{version_text}!\n\nI'm here to help you find job opportunities.")

@dp.message(Command("search"))
async def search_handler(message: Message, state: FSMContext):
    """Handle /search command - start job search conversation"""
    if not message.from_user:
        logger.warning("Received search command without user information")
        return
        
    logger.info(f"User {message.from_user.id} requested search")
    
    # Start conversation by asking for search term
    await message.answer("🔍 Let's find you some jobs!\n\nWhat job position are you looking for? (e.g., 'python developer', 'data scientist', 'frontend engineer')")
    await state.set_state(JobSearchStates.waiting_for_search_term)

@dp.message(JobSearchStates.waiting_for_search_term)
async def process_search_term(message: Message, state: FSMContext):
    """Process search term and ask for location"""
    if not message.text:
        await message.answer("Please enter a valid job position.")
        return
    
    # Store search term
    await state.update_data(search_term=message.text.strip())
    
    # Ask for location
    await message.answer("📍 What location would you like to search in? (e.g., 'remote', 'New York', 'London', 'San Francisco')")
    await state.set_state(JobSearchStates.waiting_for_location)

@dp.message(JobSearchStates.waiting_for_location)
async def process_location_and_search(message: Message, state: FSMContext):
    """Process location and perform job search"""
    if not message.text:
        await message.answer("Please enter a valid location.")
        return
    
    # Get stored data
    data = await state.get_data()
    search_term = data.get('search_term', '')
    location = message.text.strip()
    
    # Clear state
    await state.clear()
    
    logger.info(f"User {message.from_user.id if message.from_user else 'Unknown'} searching for '{search_term}' in '{location}'")
    
    # Import job scraping service and perform search
    try:
        from .job_scraping import JobScrapingService
        
        scraper = JobScrapingService()
        
        await message.answer(f"🔎 Searching for '{search_term}' jobs in '{location}'... Please wait.")
          # Perform search with user input
        result = await scraper.search_jobs(
            search_term=search_term,
            location=location
        )
        
        # Log job details for debugging
        if result and 'jobs' in result:
            job_count = len(result['jobs'])
            logger.info(f"Search completed: {job_count} jobs found")
            for i, job in enumerate(result['jobs'][:5], 1):  # Log first 5 jobs
                job_id = job.get('id', 'N/A')
                title = job.get('title', 'No title')
                logger.info(f"Job {i}: ID={job_id}, Title='{title}'")
        else:
            logger.info("Search result: No jobs found or invalid result format")
            
        # Format and send results
        formatted_message = scraper.format_jobs_summary(result)
        await message.answer(formatted_message, parse_mode="Markdown")
        
    except ImportError:
        logger.warning("Job scraping service not available")
        await message.answer("Job search is temporarily unavailable. Please try again later.")
    except Exception as e:
        logger.error(f"Search error: {e}")
        await message.answer("An error occurred during job search. Please try again later.")

@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    """Cancel current conversation"""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Nothing to cancel.")
        return
    
    await state.clear()
    await message.answer("❌ Search cancelled. You can start a new search anytime with /search")

@dp.message(Command("help"))
async def help_handler(message: Message):
    """Show help message"""
    help_text = """
🤖 *Jobs Watcher Bot Commands*

/start - Start the bot and register your account
/search - Search for job opportunities
/cancel - Cancel current search conversation
/help - Show this help message

*How to search for jobs:*
1. Use /search command
2. Enter the job position you're looking for
3. Enter your preferred location
4. Get results from job sites!

You can use /cancel anytime to stop the current search.
    """
    await message.answer(help_text, parse_mode="Markdown")

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
