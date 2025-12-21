import logging
import logging.config
import sys
from logging.handlers import RotatingFileHandler
import json
import time
from datetime import datetime
from fastapi import Request

def setup_logging():
    # Create logs directory
    import os
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default",
                "level": "INFO"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "formatter": "default",
                "level": "INFO"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/error.log",
                "maxBytes": 10485760,
                "backupCount": 5,
                "formatter": "json",
                "level": "ERROR"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file", "error_file"]
        }
    }
    
    logging.config.dictConfig(logging_config)

class RequestLogger:
    @staticmethod
    async def log_request(request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger = logging.getLogger("request")
        log_data = {
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        process_time = time.time() - start_time
        log_data.update({
            "status_code": response.status_code,
            "duration": round(process_time, 4)
        })
        
        logger.info(json.dumps(log_data))
        
        # Add X-Process-Time header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

# Create middleware instance
async def request_logging_middleware(request: Request, call_next):
    return await RequestLogger.log_request(request, call_next)