import logging
import sys
from datetime import datetime
from typing import Optional
from ..config.settings import settings
import asyncpg


class DatabaseLogger:
    """
    Logger that stores logs in PostgreSQL database for quality review and monitoring
    """

    def __init__(self):
        self.logger = logging.getLogger("chatbot_logger")
        self.logger.setLevel(logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    async def init_db(self):
        """
        Initialize the database connection and create logs table if it doesn't exist
        """
        try:
            # Create connection to PostgreSQL
            self.connection = await asyncpg.connect(
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                database=settings.POSTGRES_DB
            )

            # Create logs table if it doesn't exist
            await self.connection.execute('''
                CREATE TABLE IF NOT EXISTS chat_logs (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255),
                    user_query TEXT,
                    response TEXT,
                    sources TEXT[],
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    confidence_score FLOAT,
                    user_ip INET,
                    metadata JSONB DEFAULT '{}'
                )
            ''')

            # Create queries table for tracking user queries
            await self.connection.execute('''
                CREATE TABLE IF NOT EXISTS query_logs (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255),
                    query TEXT,
                    response_status VARCHAR(50),
                    response_time_ms INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_ip INET,
                    metadata JSONB DEFAULT '{}'
                )
            ''')

            # Create request logs table for comprehensive monitoring
            await self.connection.execute('''
                CREATE TABLE IF NOT EXISTS request_logs (
                    id SERIAL PRIMARY KEY,
                    endpoint VARCHAR(255),
                    method VARCHAR(10),
                    user_ip INET,
                    user_agent TEXT,
                    request_body JSONB,
                    response_body JSONB,
                    response_status INTEGER,
                    response_time_ms INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_id VARCHAR(255)
                )
            ''')

            # Create monitoring metrics table
            await self.connection.execute('''
                CREATE TABLE IF NOT EXISTS monitoring_metrics (
                    id SERIAL PRIMARY KEY,
                    metric_name VARCHAR(255),
                    metric_value FLOAT,
                    unit VARCHAR(50),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

        except Exception as e:
            self.logger.error(f"Failed to initialize database logger: {e}")

    async def log_request_response(self, endpoint: str, method: str, user_ip: str,
                                 user_agent: str, request_body: dict, response_body: dict,
                                 response_status: int, response_time_ms: int,
                                 session_id: str = None):
        """
        Log comprehensive request and response data for monitoring
        """
        try:
            if hasattr(self, 'connection'):
                await self.connection.execute('''
                    INSERT INTO request_logs
                    (endpoint, method, user_ip, user_agent, request_body, response_body,
                     response_status, response_time_ms, session_id)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ''', endpoint, method, user_ip, user_agent, request_body, response_body,
                       response_status, response_time_ms, session_id)
        except Exception as e:
            self.logger.error(f"Failed to log request/response: {e}")

    async def log_query(self, session_id: str, query: str, response: str,
                       sources: list, confidence_score: float = None,
                       user_ip: str = None, metadata: dict = None):
        """
        Log a query and response to the database
        """
        try:
            if hasattr(self, 'connection'):
                await self.connection.execute('''
                    INSERT INTO chat_logs
                    (session_id, user_query, response, sources, confidence_score, user_ip, metadata)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                ''', session_id, query, response, sources, confidence_score, user_ip, metadata or {})
        except Exception as e:
            self.logger.error(f"Failed to log query: {e}")

    async def log_query_performance(self, session_id: str, query: str,
                                   response_status: str, response_time_ms: int,
                                   user_ip: str = None, metadata: dict = None):
        """
        Log query performance metrics
        """
        try:
            if hasattr(self, 'connection'):
                await self.connection.execute('''
                    INSERT INTO query_logs
                    (session_id, query, response_status, response_time_ms, user_ip, metadata)
                    VALUES ($1, $2, $3, $4, $5, $6)
                ''', session_id, query, response_status, response_time_ms, user_ip, metadata or {})
        except Exception as e:
            self.logger.error(f"Failed to log query performance: {e}")

    async def log_monitoring_metric(self, metric_name: str, metric_value: float, unit: str = ""):
        """
        Log a monitoring metric
        """
        try:
            if hasattr(self, 'connection'):
                await self.connection.execute('''
                    INSERT INTO monitoring_metrics
                    (metric_name, metric_value, unit)
                    VALUES ($1, $2, $3)
                ''', metric_name, metric_value, unit)
        except Exception as e:
            self.logger.error(f"Failed to log monitoring metric: {e}")

    def log_info(self, message: str):
        """
        Log an info message
        """
        self.logger.info(message)

    def log_error(self, message: str):
        """
        Log an error message
        """
        self.logger.error(message)

    def log_warning(self, message: str):
        """
        Log a warning message
        """
        self.logger.warning(message)


# Global logger instance
db_logger = DatabaseLogger()


async def get_logger():
    """
    Get the database logger instance
    """
    if not hasattr(db_logger, 'connection'):
        await db_logger.init_db()
    return db_logger