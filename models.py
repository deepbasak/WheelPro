from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    sizes: List[str]
    bolt_pattern: str
    widths: List[str]
    main_image: str
    additional_images: List[str]
    created_at: datetime

@dataclass
class Quote:
    id: int
    # Customer info
    first_name: str
    last_name: str
    email: str
    phone: str
    city: str
    state: str
    country: str
    # Vehicle info
    vehicle_make: str
    vehicle_year: int
    vehicle_model: str
    # Additional info
    remarks: str
    product_id: Optional[int]
    created_at: datetime
    status: str = "pending"  # pending, contacted, completed

@dataclass
class Admin:
    username: str
    password_hash: str
