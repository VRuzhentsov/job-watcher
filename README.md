# Jobs Watcher

A Flask-based Python jobs scraper with Telegram bot integration that scrapes, categorizes jobs with AI, and notifies users via webhooks and scheduled background jobs.

## Features

- **Flask Application**: Webhook endpoints for Telegram updates and background job management
- **Multi-source Job Scraping**: Uses existing third-party scrapers (e.g., JobSpy, JobFunnel)
- **AI-Powered Categorization**: Uses OpenAI GPT-4o-mini to classify jobs by sector
- **Telegram Bot Integration**: Interactive bot for job search, browsing, and notifications
- **Database with ORM**: Flask-SQLAlchemy with migrations for users, jobs, keywords
- **Scheduled Jobs**: APScheduler for cron-style job scraping and cleanup
- **Background Processing**: Celery for heavy tasks like bulk message sending
- **Real-time Notifications**: Hourly job alerts via Telegram webhooks

## Technology Stack

- **Flask** with Flask-SQLAlchemy and Flask-Migrate
- **Python 3.9+** with aiogram for Telegram bot
- **APScheduler** for cron-style scheduled jobs
- **Celery + Redis** for background job processing
- **UV** for package management and script running
- **OpenAI API** (GPT-4o-mini) for job categorization
- **Third-party scrapers** (e.g., JobSpy, JobFunnel) for job data collection
- **PostgreSQL** for data storage
- **Docker Compose** for production deployment

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
- Docker & Docker Compose (for containerized deployment)
- PostgreSQL database (for local development)
- Telegram Bot Token
- OpenAI API Key

### Deployment Options

#### Production Deployment (Docker Hub)

For production deployment using the pre-built Docker Hub image:

```bash
# Clone the repository
git clone <repository-url>
cd jobs-watcher

# Set up environment variables
cp .env.example .env
# Edit .env and set your DOCKER_USERNAME

# Start production services (pulls from Docker Hub)
docker-compose up -d

# Check health status
curl http://localhost:5000/health
```

#### Local Development

For local development with live code reloading:

```bash
# Set up local development override
cp docker-compose.override.yml.example docker-compose.override.yml

# Start development services (builds locally with volume mounting)
docker-compose up -d

# View logs
docker-compose logs -f jobs-watcher
```

The override file automatically:

- Builds the image locally instead of pulling from Docker Hub
- Sets development environment variables
- Mounts source code for live reloading

#### Native Local Development

For native local development without Docker:
./docker.sh up

# Windows PowerShell

.\docker.ps1 up

````

### Docker Configuration

#### Files Overview

| File | Purpose | Image Source |
|------|---------|--------------|
| `docker-compose.yml` | Production deployment | Docker Hub |
| `docker-compose.override.yml` | Local development | Local build |

#### Quick Commands

```bash
# Production (Docker Hub image)
docker-compose up -d

# Local development (with override file)
cp docker-compose.override.yml.example docker-compose.override.yml
docker-compose up -d

# Stop services
docker-compose down
````

The override file is automatically loaded when present and overrides production settings for local development.

### Local Development

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd jobs-watcher
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

4. **Initialize database**

   ```bash
   uv run flask db init
   uv run flask db migrate -m "Initial migration"
   uv run flask db upgrade
   ```

5. **Run the Flask application**

   ```bash
   uv run src/app.py
   ```

6. **Start background workers (separate terminal)**
   ```bash
   uv run celery -A src.tasks worker --loglevel=info
   uv run celery -A src.tasks beat --loglevel=info
   ```

## Bot Commands

- `/start` - Initialize the bot and show welcome message
- `/search <query>` - Search for jobs by keyword
- `/browse` - Browse jobs by category/sector
- `/help` - Show available commands

## Production Deployment

### Docker Compose Services

The application runs as multiple services:

1. **Flask App**: Webhook endpoints under Gunicorn

   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 src.app:app
   ```

2. **Celery Worker**: Background job processing

   ```bash
   celery -A src.tasks worker --loglevel=info
   ```

3. **Celery Beat**: Scheduled job dispatcher

   ```bash
   celery -A src.tasks beat --loglevel=info
   ```

4. **Redis**: Message broker for Celery
5. **PostgreSQL**: Database with persistent storage

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

## CI/CD Pipeline

### Automated Docker Hub Deployment

The project uses GitHub Actions to automatically build and deploy Docker images to Docker Hub:

- **Triggers**: Push to `main`/`develop` branches, tags, and pull requests
- **Multi-platform**: Builds for `linux/amd64` and `linux/arm64`
- **Auto-tagging**:
  - `latest` for main branch
  - Branch names for feature branches
  - Semantic versioning for tags (e.g., `v1.0.0`)

### Setup GitHub Secrets

To enable automatic deployment, configure these secrets in your GitHub repository:

1. Go to `Settings > Secrets and variables > Actions`
2. Add the following secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub access token

### Using the Docker Hub Image

Once deployed, the image is available at:

```
docker pull your-username/jobs-watcher:latest
```

The Docker Compose files automatically use this image when you set the `DOCKER_USERNAME` environment variable.

## Contributing

1. Follow the coding guidelines in `.github/copilot-instructions.md`
2. Keep components independent and simple
3. Use type hints and follow PEP 8
4. Write tests for core functionality
5. Use early returns to avoid nested conditions

## License

MIT License - see LICENSE file for details.
