from datetime import datetime
from app import db
from sqlalchemy import String, Integer, Float, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

class Product(db.Model):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    bolt_pattern: Mapped[str] = mapped_column(String(20), nullable=False)
    sizes: Mapped[list] = mapped_column(JSON, nullable=False)
    widths: Mapped[list] = mapped_column(JSON, nullable=False)
    main_image: Mapped[str] = mapped_column(String(500), nullable=False)
    additional_images: Mapped[list] = mapped_column(JSON, default=lambda: [])
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Quote(db.Model):
    __tablename__ = 'quotes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Customer information
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    # Vehicle information
    vehicle_make: Mapped[str] = mapped_column(String(50), nullable=False)
    vehicle_year: Mapped[int] = mapped_column(Integer, nullable=False)
    vehicle_model: Mapped[str] = mapped_column(String(50), nullable=False)
    # Additional information
    remarks: Mapped[str] = mapped_column(Text, nullable=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default='pending')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
