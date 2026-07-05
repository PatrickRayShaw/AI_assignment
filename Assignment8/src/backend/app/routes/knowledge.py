from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.database import News, NewsTag

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route('/list', methods=['GET'])
@jwt_required()
def list_news():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    source_type = request.args.get('source_type')
    tag = request.args.get('tag')
    keyword = request.args.get('keyword')
    
    result, total = News.get_all(page, per_page, source_type, tag, keyword)
    return jsonify({
        'data': result,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }), 200

@knowledge_bp.route('/<int:news_id>', methods=['GET'])
@jwt_required()
def get_news(news_id):
    item = News.get_by_id(news_id)
    if item:
        return jsonify(item), 200
    return jsonify({'error': '新闻不存在'}), 404

@knowledge_bp.route('/create', methods=['POST'])
@jwt_required()
def create_news():
    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    
    if not title:
        return jsonify({'error': '标题不能为空'}), 400
    
    news_id = News.create(
        title=title,
        content=content,
        source=data.get('source', 'manual'),
        source_type=data.get('source_type', 'manual'),
        url=data.get('url'),
        summary=data.get('summary'),
        tags=data.get('tags', [])
    )
    
    return jsonify({'message': '创建成功', 'id': news_id}), 201

@knowledge_bp.route('/<int:news_id>', methods=['PUT'])
@jwt_required()
def update_news(news_id):
    item = News.get_by_id(news_id)
    if not item:
        return jsonify({'error': '新闻不存在'}), 404
    
    data = request.get_json()
    News.update(news_id, **data)
    return jsonify({'message': '更新成功'}), 200

@knowledge_bp.route('/<int:news_id>', methods=['DELETE'])
@jwt_required()
def delete_news(news_id):
    item = News.get_by_id(news_id)
    if not item:
        return jsonify({'error': '新闻不存在'}), 404
    
    News.delete(news_id)
    return jsonify({'message': '删除成功'}), 200

@knowledge_bp.route('/batch-delete', methods=['POST'])
@jwt_required()
def batch_delete_news():
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return jsonify({'error': '请提供要删除的ID列表'}), 400
    
    News.batch_delete(ids)
    return jsonify({'message': f'成功删除{len(ids)}条新闻'}), 200

@knowledge_bp.route('/tags', methods=['GET'])
@jwt_required()
def get_tags():
    tags = NewsTag.get_all_tags()
    return jsonify(tags), 200
