from app import db
from models import Product, Quote, Admin

# Vehicle data
VEHICLE_MAKES = [
    'Acura', 'Audi', 'BMW', 'Cadillac', 'Chevrolet', 'Chrysler', 'Dodge', 
    'Ferrari', 'Ford', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar',
    'Jeep', 'Kia', 'Lamborghini', 'Lexus', 'Lincoln', 'Maserati', 'Mazda',
    'Mercedes-Benz', 'Mitsubishi', 'Nissan', 'Porsche', 'Ram', 'Subaru',
    'Tesla', 'Toyota', 'Volkswagen', 'Volvo'
]

VEHICLE_YEARS = list(range(1990, 2026))  # 1990 to 2025

def initialize_sample_data():
    """Initialize sample data if database is empty"""
    # Check if admin exists
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin()
        admin.username = 'admin'
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Check if products exist
    if Product.query.count() == 0:
        sample_products = [
            {
                'name': 'Forged Aluminum Racing Wheel',
                'description': 'Premium lightweight forged aluminum wheel designed for high-performance vehicles. Features advanced spoke design for optimal strength and heat dissipation.',
                'price': 1299.99,
                'sizes': ['18x8.5', '19x9.5', '20x10.5'],
                'bolt_pattern': '5x114.3',
                'widths': ['8.5"', '9.5"', '10.5"'],
                'main_image': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=600&h=600&fit=crop&crop=center',
                'additional_images': []
            },
            {
                'name': 'Carbon Fiber Sport Rim',
                'description': 'Ultra-lightweight carbon fiber construction with titanium hardware. Perfect for track days and performance driving.',
                'price': 2499.99,
                'sizes': ['19x9.0', '20x10.0', '21x11.0'],
                'bolt_pattern': '5x120',
                'widths': ['9.0"', '10.0"', '11.0"'],
                'main_image': 'https://images.unsplash.com/photo-1609096334421-5b4b9fdccce6?w=600&h=600&fit=crop&crop=center',
                'additional_images': []
            },
            {
                'name': 'Chrome Luxury Wheel',
                'description': 'Stunning chrome finish luxury wheel with intricate spoke pattern. Perfect for premium sedans and luxury vehicles.',
                'price': 899.99,
                'sizes': ['20x8.5', '22x9.0', '24x10.0'],
                'bolt_pattern': '5x115',
                'widths': ['8.5"', '9.0"', '10.0"'],
                'main_image': 'https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?w=600&h=600&fit=crop&crop=center',
                'additional_images': []
            }
        ]
        
        for product_data in sample_products:
            product = Product(**product_data)
            db.session.add(product)
    
    db.session.commit()
