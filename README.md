# Jobs Watcher

A Flask-based Python jobs scraper with Telegram bot integration that scrapes, categorizes jobs with AI, and notifies users via webhooks and scheduled background jobs.

## Technology Stack

- **Flask** web framework
- **Python 3.9+**
- **UV** for package management and script running

## Project Structure

```
jobs-watcher/
├── src/
│   ├── app.py           # Flask application factory
│   ├── models/          # SQLAlchemy models (User, Job, Keyword)
│   ├── bot/             # Telegram bot handlers
│   ├── scrapers/        # Third-party scraper integrations
│   ├── tasks/           # Celery background tasks
│   ├── scheduler/       # APScheduler job definitions
│   ├── migrations/      # Database migrations
│   └── config/          # Configuration
└── pyproject.toml       # UV project config & dependencies
```

## Quick Start

### Prerequisites

- Python 3.9+
- UV package manager
- PostgreSQL database
- Telegram Bot Token
- OpenAI API Key

## Setup

### TODO

## Bot Commands

- `/start` - Initialize the bot and show welcome message
- `/search <query>` - Search for jobs by keyword
- `/browse` - Browse jobs by category/sector
- `/help` - Show available commands

### Configuration

- **Scraping**: Runs hourly (configurable)
- **Notifications**: Real-time via Telegram
- **Database Cleanup**: Periodic removal of old records

## Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `OPENAI_API_KEY` - OpenAI API key for job categorization
- `DATABASE_URL` - PostgreSQL connection string
- `ADMIN_CHAT_ID` - Telegram chat ID for admin notifications

### Job Scraping Libraries

The application integrates with existing third-party job scraping libraries. Examples include:

- **[JobSpy](https://github.com/speedyapply/JobSpy)**: Fast job scraping from LinkedIn, Indeed, Glassdoor, and more
- **[JobFunnel](https://github.com/PaulMcInnis/JobFunnel)**: Comprehensive job aggregation with filtering capabilities

Each scraper can be configured independently:

- Enable/disable specific sources
- Set scraping intervals
- Configure retry logic and timeouts

## Contributing

1. Follow the coding guidelines in `.github/copilot-instructions.md`
2. Keep components independent and simple
3. Use type hints and follow PEP 8
4. Write tests for core functionality
5. Use early returns to avoid nested conditions

## License

MIT License - see LICENSE file for details.
