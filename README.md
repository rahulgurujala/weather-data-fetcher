# Weather Data Fetcher

A Python application that uses Celery to concurrently fetch and store weather data for multiple locations using the Open-Meteo API.

## Features

- Concurrent weather data fetching using Celery chord
- SQLite database for data storage
- Redis as message broker and result backend
- Automated retry mechanism for failed tasks
- Docker containerization
- Comprehensive error handling and logging
- Unit tests with pytest
- Configurable through environment variables

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```
project/
├── app/
│   ├── core/
│   │   ├── database.py
│   │   └── weather.py
│   ├── models/
│   │   └── weather.py
│   ├── schemas/
│   │   └── weather.py
│   ├── tasks/
│   │   ├── weather_tasks.py
│   │   └── scheduler.py
│   └── utils/
│       ├── logger.py
│       ├── csv_handler.py
│       └── retry.py
├── data/
│   └── locations.csv
├── tests/
│   └── ...
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Quick Start

1. Clone the repository:

```bash
git clone <repository-url>
cd weather-data-fetcher
```

2. Create .env file (or copy from .env.example):

```bash
cp .env.example .env
```

3. Start the application:

```bash
docker compose up --build
```

The application will automatically:

- Initialize the database
- Start Redis
- Launch Celery workers
- Begin fetching weather data for locations in locations.csv

## Configuration

### Environment Variables

Key environment variables that can be configured in `.env`:

```ini
# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Database Configuration
DATABASE_URL=sqlite:///data/weather.db

# API Configuration
OPEN_METEO_API_URL=https://api.open-meteo.com/v1/
API_TIMEOUT=30

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=/var/log/celery-weather-app/app.log
```

### Location Data

Add or modify locations in `data/locations.csv`. Format:

```csv
city,latitude,longitude,country,timezone
London,51.5074,-0.1278,UK,Europe/London
```

## Components

### 1. Weather Data Fetching

- Uses Open-Meteo API for weather data
- Concurrent processing using Celery chord
- Automatic retries for failed requests

### 2. Data Storage

- SQLite database for storing weather data
- Automated database initialization
- Efficient data model design

### 3. Task Processing

- Redis-based message broker
- Celery for task queue management
- Scheduled updates using Celery beat

## Docker Services

The application runs these Docker services:

1. **Redis**: Message broker and result backend
2. **Worker**: Celery worker for processing tasks
3. **Beat**: Celery beat for scheduled tasks
4. **Scheduler**: Main application scheduler

## Monitoring and Maintenance

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f worker
```

### Health Checks

Check service health:

```bash
# Redis
docker compose exec redis redis-cli ping

# Worker status
docker compose exec worker celery -A app.tasks inspect active
```

### Database Management

The SQLite database is stored in `data/weather.db`. You can:

- Access it using any SQLite client
- Back it up by copying the file
- Reset by deleting the file (it will be recreated)

## Testing

Run tests using pytest:

```bash
docker compose exec worker pytest
```

## Error Handling

The application includes:

- Automatic task retries with exponential backoff
- Comprehensive error logging
- Failed task tracking
- Database transaction management

## Troubleshooting

Common issues and solutions:

1. **Redis Connection Error**

   - Check if Redis container is running
   - Verify Redis URL in .env

2. **Database Issues**

   - Check file permissions in data directory
   - Verify database URL in .env

3. **API Errors**
   - Check internet connectivity
   - Verify API endpoint in configuration

## Development

### Adding New Locations

1. Edit `data/locations.csv`
2. Add new rows with required fields
3. Restart the application

### Modifying Task Schedule

Edit the beat schedule in `app/celery_app.py`:

```python
celery_app.conf.beat_schedule = {
    'update-weather-data': {
        'task': 'app.tasks.update_weather_data',
        'schedule': 3600.0,  # Adjust frequency (in seconds)
    },
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
