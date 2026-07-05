from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.search_service import SearchService
from app.models.database import SearchLog

search_bp = Blueprint('search', __name__)

@search_bp.route('/semantic', methods=['POST'])
@jwt_required()
def semantic_search():
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': '请输入搜索内容'}), 400
    
    user_id = int(get_jwt_identity())
    search_service = SearchService()
    results = search_service.search(query)
    
    source = 'local' if results.get('source') == 'local' else 'web'
    SearchLog.create(user_id, query, len(results.get('items', [])), source)
    
    return jsonify(results), 200

@search_bp.route('/history', methods=['GET'])
@jwt_required()
def search_history():
    user_id = int(get_jwt_identity())
    conn = __import__('app.models.database', fromlist=['get_db']).get_db()
    rows = conn.execute(
        "SELECT * FROM search_logs WHERE user_id = ? ORDER BY created_at DESC LIMIT 50",
        (user_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200
