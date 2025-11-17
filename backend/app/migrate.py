"""
Migration script to add missing columns to analyses table
Run this before starting the app: python -m app.migrate
"""

from sqlalchemy import inspect, text
from app.core.database import engine
from app.core.config.settings import get_settings

def migrate():
    """Add missing columns if they don't exist"""
    settings = get_settings()
    
    inspector = inspect(engine)
    existing_columns = {col['name'] for col in inspector.get_columns('analyses')}
    
    # Define all migrations needed
    migrations = [
        ('processing_ms', 'ALTER TABLE analyses ADD COLUMN processing_ms INTEGER'),
        ('status', "ALTER TABLE analyses ADD COLUMN status VARCHAR(50) DEFAULT 'success'"),
    ]
    
    with engine.connect() as connection:
        for col_name, sql in migrations:
            if col_name not in existing_columns:
                print(f"Adding {col_name} column to analyses table...")
                try:
                    connection.execute(text(sql))
                    connection.commit()
                    print(f"✓ {col_name} column added successfully")
                except Exception as e:
                    print(f"✗ Error adding {col_name}: {e}")
                    connection.rollback()
            else:
                print(f"✓ {col_name} column already exists")

if __name__ == "__main__":
    migrate()
