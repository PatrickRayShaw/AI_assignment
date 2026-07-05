from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from app.models.database import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    email = data.get('email', '').strip()
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    if User.find_by_username(username):
        return jsonify({'error': '用户名已存在'}), 409
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_id = User.create(username, password_hash, email)
    
    return jsonify({'message': '注册成功', 'user_id': user_id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    user = User.find_by_username(username)
    if not user:
        return jsonify({'error': '用户名或密码错误'}), 401
    
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    access_token = create_access_token(identity=str(user['id']))
    return jsonify({
        'message': '登录成功',
        'access_token': access_token,
        'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())
    conn = __import__('app.models.database', fromlist=['get_db']).get_db()
    row = conn.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row)), 200
    return jsonify({'error': '用户不存在'}), 404
