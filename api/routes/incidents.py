"""
Incidents API Routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import desc, text
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database.models import Incident
from api.database import get_db

incidents_bp = Blueprint('incidents', __name__, url_prefix='/api/incidents')


@incidents_bp.route('/active', methods=['GET'])
def get_active_incidents():
    """Get active incidents"""
    db = next(get_db())
    
    try:
        # Use the view
        result = db.execute(text("SELECT * FROM v_active_incidents")).fetchall()
        
        incidents = []
        for row in result:
            incidents.append({
                'id': row[0],
                'incident_id': row[1],
                'created_at': row[2].isoformat(),
                'severity': row[3],
                'category': row[4],
                'title': row[5],
                'description': row[6],
                'status': row[7],
                'assigned_to': row[8],
                'age_minutes': row[9]
            })
        
        return jsonify({
            'count': len(incidents),
            'incidents': incidents
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidents_bp.route('/all', methods=['GET'])
def get_all_incidents():
    """Get all incidents with filters"""
    db = next(get_db())
    
    try:
        status = request.args.get('status')
        severity = request.args.get('severity')
        limit = int(request.args.get('limit', 100))
        
        query = db.query(Incident)
        
        if status:
            query = query.filter(Incident.status == status)
        
        if severity:
            query = query.filter(Incident.severity == severity)
        
        query = query.order_by(desc(Incident.created_at)).limit(limit)
        
        incidents = query.all()
        
        result = {
            'count': len(incidents),
            'incidents': [
                {
                    'id': i.id,
                    'incident_id': i.incident_id,
                    'created_at': i.created_at.isoformat(),
                    'resolved_at': i.resolved_at.isoformat() if i.resolved_at else None,
                    'severity': i.severity.value,
                    'category': i.category,
                    'title': i.title,
                    'description': i.description,
                    'status': i.status.value,
                    'assigned_to': i.assigned_to
                }
                for i in incidents
            ]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
