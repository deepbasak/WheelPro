import os
import logging
from sqlalchemy import create_engine, text

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')
# Heroku Postgres URLs start with postgres://, but SQLAlchemy needs postgresql://
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def execute_sql(sql):
    """Execute SQL command and log the result"""
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable not found!")
        return False
    
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
            return True
    except Exception as e:
        logger.error(f"Error executing SQL: {str(e)}")
        return False

def fix_schema():
    """Fix the database schema by adding missing columns one by one with error handling"""
    logger.info("Starting database schema fix...")
    
    # List of columns to add with their SQL definitions
    columns = [
        {"name": "design_type", "definition": "VARCHAR(50)"},
        {"name": "vehicle_type", "definition": "VARCHAR(50)"},
        {"name": "series", "definition": "VARCHAR(50)"},
        {"name": "is_new_stock", "definition": "INTEGER DEFAULT 0"}
    ]
    
    success = True
    for column in columns:
        # We use DO blocks with exception handling for each column
        sql = f"""
        DO $$ 
        BEGIN 
            BEGIN
                ALTER TABLE products ADD COLUMN {column['name']} {column['definition']};
                RAISE NOTICE 'Added column {column['name']} successfully';
            EXCEPTION
                WHEN duplicate_column THEN 
                    RAISE NOTICE 'Column {column['name']} already exists';
            END;
        END $$;
        """
        
        logger.info(f"Adding column {column['name']}...")
        if execute_sql(sql):
            logger.info(f"Column {column['name']} processed successfully")
        else:
            logger.error(f"Failed to process column {column['name']}")
            success = False
    
    if success:
        logger.info("All columns processed successfully!")
    else:
        logger.warning("Some columns failed to process")
    
    return success

if __name__ == "__main__":
    fix_schema()
