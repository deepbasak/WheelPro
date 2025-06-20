from datetime import datetime
from typing import List, Dict, Optional
from models import Product, Quote, Admin
from werkzeug.security import generate_password_hash, check_password_hash

class DataStore:
    def __init__(self):
        self.products: Dict[int, Product] = {}
        self.quotes: Dict[int, Quote] = {}
        self.admins: Dict[str, Admin] = {}
        self.next_product_id = 1
        self.next_quote_id = 1
        
        # Create default admin
        self.admins['admin'] = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        
        # Add some sample products for demo
        self._add_sample_products()
    
    def _add_sample_products(self):
        """Add some sample products for demonstration"""
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
            product = Product(
                id=self.next_product_id,
                created_at=datetime.now(),
                **product_data
            )
            self.products[self.next_product_id] = product
            self.next_product_id += 1
    
    # Product methods
    def add_product(self, product_data: dict) -> Product:
        product = Product(
            id=self.next_product_id,
            created_at=datetime.now(),
            **product_data
        )
        self.products[self.next_product_id] = product
        self.next_product_id += 1
        return product
    
    def get_product(self, product_id: int) -> Optional[Product]:
        return self.products.get(product_id)
    
    def get_all_products(self) -> List[Product]:
        return list(self.products.values())
    
    def delete_product(self, product_id: int) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
    
    # Quote methods
    def add_quote(self, quote_data: dict) -> Quote:
        quote = Quote(
            id=self.next_quote_id,
            created_at=datetime.now(),
            **quote_data
        )
        self.quotes[self.next_quote_id] = quote
        self.next_quote_id += 1
        return quote
    
    def get_quote(self, quote_id: int) -> Optional[Quote]:
        return self.quotes.get(quote_id)
    
    def get_all_quotes(self) -> List[Quote]:
        return list(self.quotes.values())
    
    def update_quote_status(self, quote_id: int, status: str) -> bool:
        if quote_id in self.quotes:
            self.quotes[quote_id].status = status
            return True
        return False
    
    # Admin methods
    def check_admin_credentials(self, username: str, password: str) -> bool:
        admin = self.admins.get(username)
        if admin and check_password_hash(admin.password_hash, password):
            return True
        return False

# Global data store instance
data_store = DataStore()

# Vehicle data
VEHICLE_MAKES = [
    'Acura', 'Audi', 'BMW', 'Cadillac', 'Chevrolet', 'Chrysler', 'Dodge', 
    'Ferrari', 'Ford', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar',
    'Jeep', 'Kia', 'Lamborghini', 'Lexus', 'Lincoln', 'Maserati', 'Mazda',
    'Mercedes-Benz', 'Mitsubishi', 'Nissan', 'Porsche', 'Ram', 'Subaru',
    'Tesla', 'Toyota', 'Volkswagen', 'Volvo'
]

VEHICLE_YEARS = list(range(1990, 2026))  # 1990 to 2025
