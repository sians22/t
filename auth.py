from flask import Blueprint, request, jsonify
from src.models.user import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or user.password != password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is disabled'}), 401
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        role = data.get('role', 'customer')
        
        if not username or not password or not name:
            return jsonify({'error': 'Username, password and name are required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        new_user = User(
            username=username,
            password=password,
            name=name,
            email=email,
            phone=phone,
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/init-demo-users', methods=['POST'])
def init_demo_users():
    try:
        # Demo kullanıcıları oluştur
        demo_users = [
            {
                'username': 'admin',
                'password': 'admin123',
                'name': 'Admin User',
                'email': 'admin@example.com',
                'phone': '+90 555 123 4567',
                'role': 'admin'
            },
            {
                'username': 'customer',
                'password': 'customer123',
                'name': 'Test Customer',
                'email': 'customer@example.com',
                'phone': '+90 555 234 5678',
                'role': 'customer'
            },
            {
                'username': 'courier',
                'password': 'courier123',
                'name': 'Test Courier',
                'email': 'courier@example.com',
                'phone': '+90 555 345 6789',
                'role': 'courier'
            }
        ]
        
        created_users = []
        for user_data in demo_users:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                new_user = User(**user_data)
                db.session.add(new_user)
                created_users.append(user_data['username'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Demo users initialized',
            'created_users': created_users
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

