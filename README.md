﻿# Fetching Videos Using YouTube API

This project is a Django-based application that fetches videos from YouTube using the YouTube Data API. It uses Celery for background task processing and react for frontend.

## Features

- Fetch videos from YouTube using the YouTube Data API
- Background task processing using Celery
- Redis as a message broker for Celery
- Docker support for running Redis
- RESTful API endpoints for video search and details
- Comprehensive logging and error handling
- Interactive and simplified dashboard using react(vite)

## Technologies Used

### 1. **Django**
- **Purpose**: Main web framework for building the application
- **Why Used**: Provides robust structure with built-in ORM, admin panel, and REST framework integration

### 2. **YouTube Data API**
- **Purpose**: Fetches video data from YouTube including video details, search results, and metadata
- **Why Used**: Reliable programmatic access to YouTube's vast video library

### 3. **Celery**
- **Purpose**: Asynchronous task processing for handling long-running operations
- **Why Used**: Ensures application responsiveness while processing time-consuming API requests

### 4. **Redis**
- **Purpose**: Message broker for Celery task queuing
- **Why Used**: Lightweight, fast, and reliable task queue management

### 5. **Docker**
- **Purpose**: Containerizes Redis for easy setup and deployment
- **Why Used**: Ensures consistency across environments and simplifies deployment

### 6. **Python Requests Library**
- **Purpose**: Makes HTTP requests to the YouTube Data API
- **Why Used**: Simple and user-friendly API interaction

### 7. **React**
- **Purpose**: Makes fronted easy and interactive
- **Why Used**: Ensures easy integration of backend with frontend


## Prerequisites

- Python 3.8 or higher
- Docker
- Redis
- YouTube Data API key(s)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd fetching_videos_using_YT_API
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Add your YouTube Data API keys to the `settings.py` file:
```python
YOUTUBE_API_KEY = [
    'your-api-key',
]
```

### 4. Start Redis Server
```bash
docker run -d -p 6379:6379 redis
```

### 5. Start Celery Worker
```bash
celery -A YT_api_project worker --pool=solo --loglevel=info
```

### 6. Start Celery Beat (in a separate terminal)
```bash
celery -A YT_api_project beat -l info
```

### 7. Run Django Development Server
```bash
python manage.py runserver
```

## API Endpoints

### 1. Search Videos
- **Endpoint**: `/api/videos/search/`
- **Method**: `GET`
- **Parameters**:
  - `q`: Search query (required)
  - `max_results`: Number of results to fetch (optional, default: 10)
- **Description**: Fetches videos from YouTube based on the search query

**Example Request**:
```bash
GET /api/videos/search/?q=python tutorial&max_results=5
```

### 2. Video Details
- **Endpoint**: `/api/videos/details/`
- **Method**: `GET`
- **Parameters**:
  - `id`: Video ID (required)
- **Description**: Fetches detailed information about a specific video

**Example Request**:
```bash
GET /api/videos/details/?id=dQw4w9WgXcQ
```

## Project Structure

```
fetching_videos_using_YT_API/
├── YT_api_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── videos/
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   └── ...
├── requirements.txt
├── manage.py
└── README.md
```

## Configuration

### Celery Configuration
Celery is configured to use Redis as the message broker. The configuration is in `settings.py`:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

## Important Notes

- **API Keys**: This project includes API keys in the code for easy testing. In production, always use environment variables or a `.env` file to store sensitive data
- **Background Tasks**: Long-running operations are processed asynchronously using Celery to maintain application responsiveness
- **Docker**: Redis runs in a Docker container for easy setup and isolation

## Production Deployment

For production deployment:

1. **Environment Variables**: Move API keys to environment variables
2. **Database**: Configure a production database (PostgreSQL recommended)
3. **Security**: Update Django security settings
4. **Monitoring**: Set up proper logging and monitoring
5. **Scaling**: Consider using multiple Celery workers for high load

## Troubleshooting

### Common Issues

1. **Redis Connection Error**: Ensure Redis is running on port 6379
2. **API Quota Exceeded**: Add new API key to the configuration
3. **Celery Tasks Not Processing**: Check if Celery worker is running
4. **Import Errors**: Verify all dependencies are installed

### Logs

Check application logs for detailed error information:
- Django logs: Console output when running `python manage.py runserver`
- Celery logs: Console output when running Celery worker
- Redis logs: Docker container logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions, please create an issue in the repository .
