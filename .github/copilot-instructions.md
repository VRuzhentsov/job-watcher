# Copilot Instructions - Jobs Watcher Application

## Development Guidelines

This file contains coding guidelines and patterns for developing the Jobs Watcher application. For project overview, setup instructions, and user documentation, see the main README.md.

**Context Requirement**: Always include the README.md in prompts to provide complete project context, including features, setup instructions, and project structure.

**CRITICAL - Prompt Reading**: Read user prompts with extreme care and follow their EXACT intent:
- **"Basic"** = Simple, minimal implementation with only essential components
- **"Minimal"** = Bare minimum structure, no extra features
- **"Empty"** = Basic skeleton/template only
- **Specific requests** = Follow exactly as stated, don't add unrequested features
- **One service** = Create only that service, not additional ones
- **File names** = Use EXACTLY the filename user specifies, never add prefixes/suffixes like "test_", "new_", "_backup"
- **Example**: If user asks for "basic docker compose", create ONLY the requested service, not a full multi-service stack

## Core Architecture
- **Flask Application**: Webhook endpoints for Telegram updates and background job orchestration
- **Scrapers**: Integrate third-party libraries (e.g., JobSpy, JobFunnel) for job data collection
- **AI Categorization**: Use OpenAI to classify jobs by sector
- **Telegram Bot**: User interaction and notifications (aiogram)
- **Database**: Flask-SQLAlchemy with migrations for users, jobs, keywords
- **Scheduler**: APScheduler for cron-style jobs (scraping, cleanup)
- **Background Processing**: Celery for heavy tasks (bulk messaging, data processing)

## Technology Stack
- **Flask** with Flask-SQLAlchemy and Flask-Migrate for web framework and ORM
- **Python 3.9+** with aiogram for Telegram bot
- **APScheduler** (Flask-APScheduler) for cron-style scheduled jobs
- **Celery + Redis/RabbitMQ** for background job processing
- **UV** for package management and script running
- **OpenAI API** (GPT-4o-mini) for job categorization
- **Third-party scrapers** (e.g., JobSpy, JobFunnel) for job data collection
- **PostgreSQL** with Alembic migrations for data storage
- **Docker Compose** for production deployment

## Coding Guidelines

### Scrapers
- Wrap each scraper in try/catch to isolate failures
- Use existing libraries (JobSpy, JobFunnel) rather than custom scraping
- Process in parallel but handle errors independently
- Return standardized format: `{title: [link, source]}`

### AI Categorization
- Batch process titles in chunks of 150 items (token limits)
- Use GPT-4o-mini for cost-effective categorization
- Implement retry logic for malformed JSON responses
- Map to predefined job sectors/categories

### Database Operations
- Use `INSERT IGNORE` for duplicate handling
- Bulk insert with pandas for efficiency
- Index on frequently queried fields (date, category)
- Clean up old records periodically

### Telegram Bot
- **Basic Commands**: `/start`, `/search`, `/browse`, `/help`
- **Features**: Job search, sector browsing, user notifications
- **Error Handling**: Catch all exceptions, alert admin chat
- Simple keyboard navigation, 40 results per page

### Error Handling & Monitoring
- Real-time alerts to admin Telegram chat for failures
- Log errors but avoid log bloat
- Graceful degradation when scrapers fail
- Use early returns in conditionals

## Essential Patterns

### Resilient Scraping
- Wrap each scraper in try/catch blocks to isolate failures
- Use dict union operations to merge results from multiple sources
- Send admin notifications when scrapers fail
- Return empty dict if scraper fails to prevent pipeline breakage

### AI Categorization
- Process job titles in batches of 150 items to respect token limits
- Implement retry logic with exponential backoff for API failures
- Parse JSON responses with fallback handling for malformed data
- Cache categorization results to reduce API costs

### Database Bulk Insert
- Use pandas DataFrames for efficient bulk operations
- Implement INSERT IGNORE pattern for duplicate handling
- Process data in chunks to manage memory usage
- Add proper indexing on frequently queried fields

## Documentation Guidelines

### Using Context7 MCP for Library Documentation
When working with external libraries or frameworks, use the `f1e_get-library-docs` tool to get up-to-date documentation:

- **Before implementation**: Fetch current docs for libraries like aiogram, pandas, psycopg2, BeautifulSoup
- **When debugging**: Get specific documentation sections for troubleshooting
- **For best practices**: Retrieve examples and patterns from official documentation
- **API changes**: Stay current with library updates and deprecated methods

This ensures code follows current best practices and uses the latest API patterns.

## Development Rules
- Keep components independent and simple
- Use UV for dependency management
- Use type hints and follow PEP 8
- Write minimal, focused functions
- Test core functionality with unit tests
- Keep all comments, even temporary ones
- Use early returns to avoid nested conditions
- **Documentation**: Use f1e_get-library-docs tool to fetch up-to-date documentation for libraries and frameworks when needed
- **File Management**: NEVER create backup/versioned files (app-new.py, app.backup, app_old.py). NEVER delete or move existing files unless explicitly requested. NEVER modify user-specified filenames by adding prefixes/suffixes (test_, new_, _backup, _old). Edit files in place using replace_string_in_file or insert_edit_into_file tools.

## Production Deployment
- **Container Orchestration**: Docker Compose with restart policies
- **Hourly Scraping**: Configurable scheduler container (TODO: make interval customizable)
- **Process Management**: Docker handles restarts and health checks
- **Monitoring**: Container health checks and log aggregation
- **Scaling**: Easy horizontal scaling with Docker Compose

---

**Note**: Prioritize simplicity and reliability over complex features. Independent modules make debugging easier.

**CRITICAL FILE HANDLING**: Never create backup files (app-new.py, app.backup) or delete existing files. Never modify filenames by adding prefixes/suffixes (test_, new_, _old). Always use EXACT filenames specified by user. Always edit in place.

Keep all code comments. Use early returns in conditionals. Make minimal edits to satisfy requirements.
Keep all code comments and do not remove them anytime, keep even dumb test & temp comments.
Make as minimum edits as it needed to satisfy the requirements. (like: do not remove comments, or other excessive modifications)
Always use early return in 'if' conditions when they fail, to keep the code concise and avoid unnecessary nested blocks.