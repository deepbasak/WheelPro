-- Fix database schema by adding missing columns
BEGIN;

DO $$ 
BEGIN 
    BEGIN
        ALTER TABLE products ADD COLUMN design_type VARCHAR(50);
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'Column design_type already exists';
    END;

    BEGIN
        ALTER TABLE products ADD COLUMN vehicle_type VARCHAR(50);
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'Column vehicle_type already exists';
    END;
    
    BEGIN
        ALTER TABLE products ADD COLUMN series VARCHAR(50);
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'Column series already exists';
    END;
    
    BEGIN
        ALTER TABLE products ADD COLUMN is_new_stock INTEGER DEFAULT 0;
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'Column is_new_stock already exists';
    END;
END $$;

COMMIT;
