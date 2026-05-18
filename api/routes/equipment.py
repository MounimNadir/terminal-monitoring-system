"""
Equipment API Routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import func, and_, text
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database.models import EquipmentStatusModel, EquipmentType, EquipmentStatus
from api.database import get_db

equipment_bp = Blueprint('equipment', __name__, url_prefix='/api/equipment')


@equipment_bp.route('/status', methods=['GET'])
def get_equipment_status():
    """Get current status of all equipment"""
    db = next(get_db())
    
    try:
        equipment_type = request.args.get('type')
        status = request.args.get('status')
        
        query = db.query(EquipmentStatusModel)
        
        if equipment_type:
            query = query.filter(EquipmentStatusModel.equipment_type == equipment_type)
        
        if status:
            query = query.filter(EquipmentStatusModel.status == status)
        
        equipment = query.all()
        
        result = {
            'count': len(equipment),
            'equipment': [
                {
                    'equipment_id': e.equipment_id,
                    'equipment_type': e.equipment_type.value,
                    'equipment_name': e.equipment_name,
                    'status': e.status.value,
                    'location': e.location,
                    'utilization_rate': float(e.utilization_rate) if e.utilization_rate else 0,
                    'current_task': e.current_task,
                    'last_heartbeat': e.last_heartbeat.isoformat() if e.last_heartbeat else None,
                    'metrics': e.metrics
                }
                for e in equipment
            ]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipment_bp.route('/summary', methods=['GET'])
def get_equipment_summary():
    """Get equipment summary by type"""
    db = next(get_db())
    
    try:
        # Use the view
        result = db.execute(text("SELECT * FROM v_equipment_summary")).fetchall()
        
        summary = []
        for row in result:
            summary.append({
                'equipment_type': row[0],
                'total_count': row[1],
                'operational': row[2],
                'idle': row[3],
                'fault': row[4],
                'maintenance': row[5],
                'avg_utilization': float(row[6]) if row[6] else 0
            })
        
        return jsonify({'summary': summary}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipment_bp.route('/<equipment_id>', methods=['GET'])
def get_equipment_detail(equipment_id):
    """Get detailed information for specific equipment"""
    db = next(get_db())
    
    try:
        equipment = db.query(EquipmentStatusModel).filter_by(
            equipment_id=equipment_id
        ).first()
        
        if not equipment:
            return jsonify({'error': 'Equipment not found'}), 404
        
        result = {
            'equipment_id': equipment.equipment_id,
            'equipment_type': equipment.equipment_type.value,
            'equipment_name': equipment.equipment_name,
            'status': equipment.status.value,
            'location': equipment.location,
            'utilization_rate': float(equipment.utilization_rate) if equipment.utilization_rate else 0,
            'current_task': equipment.current_task,
            'last_heartbeat': equipment.last_heartbeat.isoformat() if equipment.last_heartbeat else None,
            'metrics': equipment.metrics,
            'created_at': equipment.created_at.isoformat(),
            'updated_at': equipment.updated_at.isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipment_bp.route('/types', methods=['GET'])
def get_equipment_types():
    """Get list of equipment types"""
    return jsonify({
        'types': [
            {'value': t.value, 'name': t.name} 
            for t in EquipmentType
        ]
    }), 200
