from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.cluster_service import ClusterService

cluster_bp = Blueprint('cluster', __name__)

@cluster_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    service = ClusterService()
    result = service.analyze(top_n=10)
    return jsonify(result), 200

@cluster_bp.route('/report', methods=['GET'])
@jwt_required()
def get_report():
    service = ClusterService()
    result = service.get_latest_report()
    return jsonify(result), 200
