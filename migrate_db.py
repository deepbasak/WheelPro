import os
import random
from app import app, db
from models import Product
from sqlalchemy import text
from data_store import DESIGN_TYPES, VEHICLE_TYPES, WHEEL_SERIES

def run_migration():
    """
    Add missing columns to the products table and update existing products with sample data
    """
    print("Starting database migration...")
    
    with app.app_context():
        try:
            connection = db.engine.connect()
            
            # Step 1: Add missing columns if they don't exist
            print("Step 1: Adding missing columns...")
            
            # Check if the design_type column exists
            try:
                connection.execute(text("SELECT design_type FROM products LIMIT 1"))
                print("Column design_type already exists")
            except Exception as e:
                print("Adding design_type column...")
                connection.execute(text("ALTER TABLE products ADD COLUMN design_type VARCHAR(50)"))
                db.session.commit()
                print("Added design_type column successfully")
            
            # Check if the vehicle_type column exists
            try:
                connection.execute(text("SELECT vehicle_type FROM products LIMIT 1"))
                print("Column vehicle_type already exists")
            except Exception as e:
                print("Adding vehicle_type column...")
                connection.execute(text("ALTER TABLE products ADD COLUMN vehicle_type VARCHAR(50)"))
                db.session.commit()
                print("Added vehicle_type column successfully")
            
            # Check if the series column exists
            try:
                connection.execute(text("SELECT series FROM products LIMIT 1"))
                print("Column series already exists")
            except Exception as e:
                print("Adding series column...")
                connection.execute(text("ALTER TABLE products ADD COLUMN series VARCHAR(50)"))
                db.session.commit()
                print("Added series column successfully")
            
            # Check if the is_new_stock column exists
            try:
                connection.execute(text("SELECT is_new_stock FROM products LIMIT 1"))
                print("Column is_new_stock already exists")
            except Exception as e:
                print("Adding is_new_stock column...")
                connection.execute(text("ALTER TABLE products ADD COLUMN is_new_stock INTEGER DEFAULT 0"))
                db.session.commit()
                print("Added is_new_stock column successfully")
            
            # Step 2: Update existing products with sample data
            print("Step 2: Updating existing products with default values...")
            products = Product.query.all()
            
            # Create a mapping of product types based on names
            type_mapping = {
                'racing': {'design_type': 'Multi Spoke', 'vehicle_type': 'Muscle Car', 'series': 'Racing Series'},
                'sport': {'design_type': '5 Spoke', 'vehicle_type': 'Sports', 'series': 'Sport Series'},
                'carbon': {'design_type': 'Mesh', 'vehicle_type': 'Exotic', 'series': 'Performance Series'},
                'fiber': {'design_type': 'Mesh', 'vehicle_type': 'Exotic', 'series': 'Performance Series'},
                'luxury': {'design_type': 'Full Face', 'vehicle_type': 'Luxury', 'series': 'Luxury Series'},
                'chrome': {'design_type': '8 Spoke', 'vehicle_type': 'Luxury', 'series': 'Classic Series'},
                'off': {'design_type': 'Split 5', 'vehicle_type': 'Truck', 'series': 'Off-Road Series'},
                'truck': {'design_type': 'Split 5', 'vehicle_type': 'Truck', 'series': 'Off-Road Series'},
            }
            
            updated_count = 0
            for product in products:
                # Skip products that already have values set
                if product.design_type and product.vehicle_type and product.series:
                    continue
                
                # Try to match product name to a type
                matched = False
                for keyword, attributes in type_mapping.items():
                    if keyword.lower() in product.name.lower() or keyword.lower() in product.description.lower():
                        product.design_type = attributes['design_type']
                        product.vehicle_type = attributes['vehicle_type']
                        product.series = attributes['series']
                        matched = True
                        break
                
                # If no match, assign random values
                if not matched:
                    product.design_type = random.choice(DESIGN_TYPES)
                    product.vehicle_type = random.choice(VEHICLE_TYPES)
                    product.series = random.choice(WHEEL_SERIES)
                
                # Set one-third of products as new stock
                product.is_new_stock = random.choice([0, 0, 1])
                
                updated_count += 1
            
            db.session.commit()
            print(f"Updated {updated_count} products with default attributes.")
            
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    run_migration()
