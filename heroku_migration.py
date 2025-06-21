import os
import random
from sqlalchemy import create_engine, text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')
# Heroku Postgres URLs start with postgres://, but SQLAlchemy needs postgresql://
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def run_migration():
    """
    Add missing columns to the products table using individual connections for each operation
    to avoid transaction problems
    """
    logger.info("Starting Heroku database migration...")
    
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable not found!")
        return False

    # Create a new engine for each operation to avoid transaction issues
    engine = create_engine(DATABASE_URL)
    
    columns_to_add = [
        {"name": "design_type", "type": "VARCHAR(50)", "default": "NULL"},
        {"name": "vehicle_type", "type": "VARCHAR(50)", "default": "NULL"},
        {"name": "series", "type": "VARCHAR(50)", "default": "NULL"},
        {"name": "is_new_stock", "type": "INTEGER", "default": "0"}
    ]
    
    success = True
    
    for column in columns_to_add:
        try:
            # Create a fresh connection for each column
            with engine.connect() as conn:
                # Check if column exists
                try:
                    logger.info(f"Checking if {column['name']} exists...")
                    conn.execute(text(f"SELECT {column['name']} FROM products LIMIT 1"))
                    logger.info(f"Column {column['name']} already exists")
                except Exception as e:
                    # Close this connection and create a new one since the transaction is aborted
                    logger.info(f"Adding {column['name']} column...")
                    
                    # Create a fresh connection
                    with engine.connect() as new_conn:
                        new_conn.execute(text(f"ALTER TABLE products ADD COLUMN {column['name']} {column['type']} DEFAULT {column['default']}"))
                        new_conn.commit()
                        logger.info(f"Added {column['name']} column successfully")
        except Exception as e:
            logger.error(f"Error adding column {column['name']}: {str(e)}")
            success = False
    
    if success:
        logger.info("Schema migration completed successfully!")
        return True
    else:
        logger.error("Schema migration encountered errors")
        return False

if __name__ == "__main__":
    run_migration()
