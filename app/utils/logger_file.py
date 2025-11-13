from loguru import logger
import sys
import os

# Create logs folder
os.makedirs("logs", exist_ok=True)

# Remove default handler
logger.remove()

# Console output
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    level="DEBUG"
)

# File output
logger.add(
    "logs/dental_ai.log",
    rotation="5 MB",
    retention="10 days",
    compression="zip",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Export logger for import elsewhere
log = logger
