from app import app, db
from sqlalchemy import text, inspect
from migrate_db import run_migration

def check_db_schema():
    """
    Check if all required columns exist in the database.
    If not, prompt the user to run the migration script.
    """
    print("Checking database schema...")
    
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            product_columns = [column['name'] for column in inspector.get_columns('products')]
            
            # Check if all required columns exist
            required_columns = ['design_type', 'vehicle_type', 'series', 'is_new_stock']
            missing_columns = [col for col in required_columns if col not in product_columns]
            
            if missing_columns:
                print(f"WARNING: Missing columns in products table: {', '.join(missing_columns)}")
                print("You need to run the database migration script.")
                
                # Ask if user wants to run the migration now
                user_input = input("Would you like to run the migration now? (y/n): ")
                if user_input.lower() == 'y':
                    print("Running migration...")
                    run_migration()
                    print("Migration complete. Please restart the application.")
                else:
                    print("Please run the migrate_db.py script manually before starting the application.")
                    print("You can do this by running: python migrate_db.py")
            else:
                print("Database schema is up to date.")
                
        except Exception as e:
            print(f"Error checking database schema: {str(e)}")
            print("This could indicate database connection issues or that the tables don't exist yet.")
            print("If this is your first run, the tables will be created automatically.")
            print("Otherwise, please check your database connection settings.")

if __name__ == "__main__":
    check_db_schema()
