"""
Metrics API Routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database.models import Metric, MetricType
from api.database import get_db

metrics_bp = Blueprint('metrics', __name__, url_prefix='/api/metrics')


@metrics_bp.route('/current', methods=['GET'])
def get_current_metrics():
    """Get current metrics (latest values)"""
    db = next(get_db())
    
    try:
        # Get the latest timestamp
        latest_time = db.query(func.max(Metric.timestamp)).scalar()
        
        if not latest_time:
            return jsonify({'metrics': [], 'timestamp': None}), 200
        
        # Get metrics from the last minute
        one_minute_ago = latest_time - timedelta(minutes=1)
        
        metrics = db.query(Metric).filter(
            Metric.timestamp >= one_minute_ago
        ).all()
        
        result = {
            'timestamp': latest_time.isoformat(),
            'metrics': [
                {
                    'type': m.metric_type.value,
                    'name': m.metric_name,
                    'value': float(m.value),
                    'unit': m.unit,
                    'host': m.host
                }
                for m in metrics
            ]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@metrics_bp.route('/historical', methods=['GET'])
def get_historical_metrics():
    """Get historical metrics with time range"""
    db = next(get_db())
    
    try:
        # Get query parameters
        metric_type = request.args.get('type')
        metric_name = request.args.get('name')
        hours = int(request.args.get('hours', 1))
        limit = int(request.args.get('limit', 1000))
        
        # Build query
        query = db.query(Metric)
        
        # Time filter
        time_threshold = datetime.now() - timedelta(hours=hours)
        query = query.filter(Metric.timestamp >= time_threshold)
        
        # Type filter
        if metric_type:
            query = query.filter(Metric.metric_type == metric_type)
        
        # Name filter
        if metric_name:
            query = query.filter(Metric.metric_name == metric_name)
        
        # Order and limit
        query = query.order_by(desc(Metric.timestamp)).limit(limit)
        
        metrics = query.all()
        
        result = {
            'count': len(metrics),
            'filters': {
                'type': metric_type,
                'name': metric_name,
                'hours': hours
            },
            'metrics': [
                {
                    'timestamp': m.timestamp.isoformat(),
                    'type': m.metric_type.value,
                    'name': m.metric_name,
                    'value': float(m.value),
                    'unit': m.unit,
                    'host': m.host
                }
                for m in metrics
            ]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@metrics_bp.route('/summary', methods=['GET'])
def get_metrics_summary():
    """Get aggregated metrics summary"""
    db = next(get_db())
    
    try:
        hours = int(request.args.get('hours', 1))
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        # System metrics summary
        system_metrics = {}
        
        for metric_type in ['cpu_percent', 'memory_percent', 'disk_percent']:
            result = db.query(
                func.avg(Metric.value).label('avg'),
                func.max(Metric.value).label('max'),
                func.min(Metric.value).label('min')
            ).filter(
                and_(
                    Metric.metric_name == metric_type,
                    Metric.timestamp >= time_threshold
                )
            ).first()
            
            if result and result.avg is not None:
                system_metrics[metric_type] = {
                    'avg': float(result.avg),
                    'max': float(result.max),
                    'min': float(result.min)
                }
        
        return jsonify({
            'period_hours': hours,
            'system_metrics': system_metrics
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@metrics_bp.route('/types', methods=['GET'])
def get_metric_types():
    """Get list of available metric types"""
    return jsonify({
        'types': [t.value for t in MetricType]
    }), 200
