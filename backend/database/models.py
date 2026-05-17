"""
Database Models for Terminal Monitoring System
Using SQLAlchemy ORM
"""

from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, DECIMAL, 
    DateTime, Enum, Boolean, JSON, ForeignKey, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()


# ============================================
# ENUMS
# ============================================

class MetricType(enum.Enum):
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    EQUIPMENT = "equipment"
    CUSTOM = "custom"


class IncidentSeverity(enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IncidentStatus(enum.Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class EquipmentType(enum.Enum):
    STS_CRANE = "STS_crane"
    ARMG_CRANE = "ARMG_crane"
    SHUTTLE_CARRIER = "shuttle_carrier"
    GATE_SYSTEM = "gate_system"
    OTHER = "other"


class EquipmentStatus(enum.Enum):
    OPERATIONAL = "operational"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    FAULT = "fault"
    OFFLINE = "offline"


class BackupType(enum.Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"


class BackupStatus(enum.Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    CANCELLED = "cancelled"


class VerificationStatus(enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    CORRUPTED = "corrupted"
    SKIPPED = "skipped"


# ============================================
# MODELS
# ============================================

class Metric(Base):
    __tablename__ = 'metrics'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(6), nullable=False, index=True)
    metric_type = Column(Enum(MetricType), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False, index=True)
    value = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(String(20))
    host = Column(String(100), default='localhost', index=True)
    meta_data = Column('metadata', JSON)
    created_at = Column(DateTime(6), default=func.now())
    
    __table_args__ = (
        Index('idx_type_name', 'metric_type', 'metric_name'),
    )
    
    def __repr__(self):
        return f"<Metric(id={self.id}, type={self.metric_type.value}, name={self.metric_name}, value={self.value})>"


class Incident(Base):
    __tablename__ = 'incidents'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    incident_id = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(6), nullable=False, default=func.now(), index=True)
    resolved_at = Column(DateTime(6))
    severity = Column(Enum(IncidentSeverity), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    metric_snapshot = Column(JSON)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN, index=True)
    assigned_to = Column(String(100))
    resolution_notes = Column(Text)
    updated_at = Column(DateTime(6), default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_status_severity', 'status', 'severity'),
    )
    
    def __repr__(self):
        return f"<Incident(id={self.incident_id}, severity={self.severity.value}, status={self.status.value})>"


class EquipmentStatusModel(Base):
    __tablename__ = 'equipment_status'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    equipment_id = Column(String(50), unique=True, nullable=False, index=True)
    equipment_type = Column(Enum(EquipmentType), nullable=False, index=True)
    equipment_name = Column(String(100), nullable=False)
    status = Column(Enum(EquipmentStatus), nullable=False, default=EquipmentStatus.OPERATIONAL, index=True)
    location = Column(String(100))
    utilization_rate = Column(DECIMAL(5, 2), default=0.00)
    current_task = Column(String(255))
    last_heartbeat = Column(DateTime(6), index=True)
    metrics = Column(JSON)
    created_at = Column(DateTime(6), default=func.now())
    updated_at = Column(DateTime(6), default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_type_status', 'equipment_type', 'status'),
    )
    
    def __repr__(self):
        return f"<Equipment(id={self.equipment_id}, type={self.equipment_type.value}, status={self.status.value})>"


class BackupLog(Base):
    __tablename__ = 'backup_logs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    backup_id = Column(String(100), unique=True, nullable=False, index=True)
    backup_type = Column(Enum(BackupType), nullable=False, index=True)
    target = Column(String(255), nullable=False)
    started_at = Column(DateTime(6), nullable=False, index=True)
    completed_at = Column(DateTime(6))
    status = Column(Enum(BackupStatus), nullable=False, index=True)
    size_bytes = Column(BigInteger)
    verification_status = Column(Enum(VerificationStatus), index=True)
    checksum = Column(String(64))
    error_message = Column(Text)
    backup_path = Column(String(500))
    retention_days = Column(Integer, default=30)
    created_at = Column(DateTime(6), default=func.now())
    
    def __repr__(self):
        return f"<BackupLog(id={self.backup_id}, type={self.backup_type.value}, status={self.status.value})>"


class AlertRule(Base):
    __tablename__ = 'alert_rules'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    rule_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    rule_type = Column(String(50), nullable=False, index=True)
    condition_expression = Column(Text, nullable=False)
    severity = Column(Enum(IncidentSeverity), nullable=False)
    enabled = Column(Boolean, default=True, index=True)
    cooldown_seconds = Column(Integer, default=600)
    channels = Column(JSON)
    meta_data = Column('metadata', JSON)
    created_at = Column(DateTime(6), default=func.now())
    updated_at = Column(DateTime(6), default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<AlertRule(id={self.rule_id}, name={self.name}, enabled={self.enabled})>"


class AlertHistory(Base):
    __tablename__ = 'alert_history'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    alert_id = Column(String(100), unique=True, nullable=False, index=True)
    rule_id = Column(String(50), nullable=False, index=True)
    triggered_at = Column(DateTime(6), nullable=False, index=True)
    resolved_at = Column(DateTime(6))
    severity = Column(Enum(IncidentSeverity), nullable=False)
    message = Column(Text, nullable=False)
    channels_notified = Column(JSON)
    incident_id = Column(BigInteger, ForeignKey('incidents.id', ondelete='SET NULL'), index=True)
    meta_data = Column('metadata', JSON)
    created_at = Column(DateTime(6), default=func.now())
    
    def __repr__(self):
        return f"<AlertHistory(id={self.alert_id}, rule={self.rule_id}, severity={self.severity.value})>"


class KPISnapshot(Base):
    __tablename__ = 'kpi_snapshots'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    snapshot_time = Column(DateTime(6), nullable=False, index=True)
    kpi_category = Column(String(50), nullable=False, index=True)
    kpi_name = Column(String(100), nullable=False, index=True)
    kpi_value = Column(DECIMAL(12, 2), nullable=False)
    unit = Column(String(20))
    aggregation_period = Column(
        Enum('1min', '5min', '15min', '1hour', '1day', name='aggregation_period'),
        nullable=False,
        index=True
    )
    meta_data = Column('metadata', JSON)
    created_at = Column(DateTime(6), default=func.now())
    
    __table_args__ = (
        Index('idx_category_name', 'kpi_category', 'kpi_name'),
    )
    
    def __repr__(self):
        return f"<KPISnapshot(category={self.kpi_category}, name={self.kpi_name}, value={self.kpi_value})>"


class SystemConfig(Base):
    __tablename__ = 'system_config'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Text, nullable=False)
    value_type = Column(
        Enum('string', 'integer', 'float', 'boolean', 'json', name='value_type'),
        nullable=False
    )
    description = Column(Text)
    is_sensitive = Column(Boolean, default=False)
    created_at = Column(DateTime(6), default=func.now())
    updated_at = Column(DateTime(6), default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<SystemConfig(key={self.config_key}, type={self.value_type})>"
    
    def get_value(self):
        """Convert string value to appropriate type"""
        if self.value_type == 'integer':
            return int(self.config_value)
        elif self.value_type == 'float':
            return float(self.config_value)
        elif self.value_type == 'boolean':
            return self.config_value.lower() in ('true', '1', 'yes')
        elif self.value_type == 'json':
            import json
            return json.loads(self.config_value)
        return self.config_value
