from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Sipariş bilgileri
    description = db.Column(db.Text, nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    
    # Konum bilgileri
    pickup_lat = db.Column(db.Float, nullable=False)
    pickup_lng = db.Column(db.Float, nullable=False)
    pickup_address = db.Column(db.String(500), nullable=True)
    
    delivery_lat = db.Column(db.Float, nullable=False)
    delivery_lng = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(500), nullable=True)
    
    # Fiyat ve mesafe
    distance = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=True)
    
    # Promosyon kodu
    promo_code = db.Column(db.String(50), nullable=True)
    
    # Durum
    status = db.Column(db.String(20), default='pending')  # pending, accepted, in-transit, delivered, cancelled
    
    # Tarihler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    # İlişkiler
    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_orders')
    courier = db.relationship('User', foreign_keys=[courier_id], backref='courier_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'courier_id': self.courier_id,
            'description': self.description,
            'customer_phone': self.customer_phone,
            'pickupLocation': {
                'lat': self.pickup_lat,
                'lng': self.pickup_lng,
                'address': self.pickup_address
            },
            'deliveryLocation': {
                'lat': self.delivery_lat,
                'lng': self.delivery_lng,
                'address': self.delivery_address
            },
            'distance': self.distance,
            'price': self.price,
            'original_price': self.original_price,
            'promo_code': self.promo_code,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'customer': {
                'id': self.customer.id,
                'username': self.customer.username,
                'name': self.customer.name
            } if self.customer else None,
            'courier': {
                'id': self.courier.id,
                'username': self.courier.username,
                'name': self.courier.name,
                'phone': self.courier.phone
            } if self.courier else None
        }

class PromoCode(db.Model):
    __tablename__ = 'promo_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_type = db.Column(db.String(20), nullable=False)  # percentage, fixed
    discount_value = db.Column(db.Float, nullable=False)
    min_order_amount = db.Column(db.Float, default=0)
    max_discount = db.Column(db.Float, nullable=True)
    usage_limit = db.Column(db.Integer, nullable=True)
    used_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'min_order_amount': self.min_order_amount,
            'max_discount': self.max_discount,
            'usage_limit': self.usage_limit,
            'used_count': self.used_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

