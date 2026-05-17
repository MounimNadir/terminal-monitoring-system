-- Terminal Monitoring System - Initial Schema
-- Version: 1.0.0
-- Description: Core tables for metrics, incidents, equipment, and backups

-- ============================================
-- 1. METRICS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME(6) NOT NULL,
    metric_type ENUM('cpu', 'memory', 'disk', 'network', 'equipment', 'custom') NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(20),
    host VARCHAR(100) DEFAULT 'localhost',
    metadata JSON,
    created_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX idx_timestamp (timestamp),
    INDEX idx_type_name (metric_type, metric_name),
    INDEX idx_created (created_at),
    INDEX idx_host (host)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 2. INCIDENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS incidents (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    incident_id VARCHAR(50) UNIQUE NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    resolved_at DATETIME(6),
    severity ENUM('critical', 'high', 'medium', 'low', 'info') NOT NULL,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    metric_snapshot JSON,
    status ENUM('open', 'acknowledged', 'investigating', 'resolved', 'closed') DEFAULT 'open',
    assigned_to VARCHAR(100),
    resolution_notes TEXT,
    updated_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX idx_incident_id (incident_id),
    INDEX idx_status (status),
    INDEX idx_severity (severity),
    INDEX idx_created (created_at),
    INDEX idx_category (category),
    INDEX idx_status_severity (status, severity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 3. EQUIPMENT STATUS TABLE (Port Terminal Simulation)
-- ============================================
CREATE TABLE IF NOT EXISTS equipment_status (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    equipment_id VARCHAR(50) UNIQUE NOT NULL,
    equipment_type ENUM('STS_crane', 'ARMG_crane', 'shuttle_carrier', 'gate_system', 'other') NOT NULL,
    equipment_name VARCHAR(100) NOT NULL,
    status ENUM('operational', 'idle', 'maintenance', 'fault', 'offline') NOT NULL DEFAULT 'operational',
    location VARCHAR(100),
    utilization_rate DECIMAL(5, 2) DEFAULT 0.00,
    current_task VARCHAR(255),
    last_heartbeat DATETIME(6),
    metrics JSON,
    created_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX idx_equipment_id (equipment_id),
    INDEX idx_type_status (equipment_type, status),
    INDEX idx_status (status),
    INDEX idx_last_heartbeat (last_heartbeat)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 4. BACKUP LOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS backup_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    backup_id VARCHAR(100) UNIQUE NOT NULL,
    backup_type ENUM('full', 'incremental', 'differential', 'snapshot') NOT NULL,
    target VARCHAR(255) NOT NULL,
    started_at DATETIME(6) NOT NULL,
    completed_at DATETIME(6),
    status ENUM('running', 'success', 'failed', 'partial', 'cancelled') NOT NULL,
    size_bytes BIGINT,
    verification_status ENUM('pending', 'verified', 'corrupted', 'skipped'),
    checksum VARCHAR(64),
    error_message TEXT,
    backup_path VARCHAR(500),
    retention_days INT DEFAULT 30,
    created_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX idx_backup_id (backup_id),
    INDEX idx_status (status),
    INDEX idx_started (started_at),
    INDEX idx_verification (verification_status),
    INDEX idx_type (backup_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 5. ALERT RULES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS alert_rules (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rule_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    rule_type VARCHAR(50) NOT NULL,
    condition_expression TEXT NOT NULL,
    severity ENUM('critical', 'high', 'medium', 'low', 'info') NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    cooldown_seconds INT DEFAULT 600,
    channels JSON,
    metadata JSON,
    created_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX idx_rule_id (rule_id),
    INDEX idx_enabled (enabled),
    INDEX idx_rule_type (rule_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 6. ALERT HISTORY TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS alert_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    alert_id VARCHAR(100) UNIQUE NOT NULL,
    rule_id VARCHAR(50) NOT NULL,
    triggered_at DATETIME(6) NOT NULL,
    resolved_at DATETIME(6),
    severity ENUM('critical', 'high', 'medium', 'low', 'info') NOT NULL,
    message TEXT NOT NULL,
    channels_notified JSON,
    incident_id BIGINT,
    metadata JSON,
    created_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX idx_alert_id (alert_id),
    INDEX idx_rule_id (rule_id),
    INDEX idx_triggered (triggered_at),
    INDEX idx_incident (incident_id),
    FOREIGN KEY (incident_id) REFERENCES incidents(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 7. KPI SNAPSHOTS TABLE (Aggregated Data)
-- ============================================
CREATE TABLE IF NOT EXISTS kpi_snapshots (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    snapshot_time DATETIME(6) NOT NULL,
    kpi_category VARCHAR(50) NOT NULL,
    kpi_name VARCHAR(100) NOT NULL,
    kpi_value DECIMAL(12, 2) NOT NULL,
    unit VARCHAR(20),
    aggregation_period ENUM('1min', '5min', '15min', '1hour', '1day') NOT NULL,
    metadata JSON,
    created_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
    
    INDEX idx_snapshot_time (snapshot_time),
    INDEX idx_category_name (kpi_category, kpi_name),
    INDEX idx_period (aggregation_period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 8. SYSTEM CONFIG TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS system_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    value_type ENUM('string', 'integer', 'float', 'boolean', 'json') NOT NULL,
    description TEXT,
    is_sensitive BOOLEAN DEFAULT FALSE,
    created_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    
    INDEX idx_config_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- INSERT DEFAULT CONFIGURATIONS
-- ============================================
INSERT INTO system_config (config_key, config_value, value_type, description) VALUES
('collection_interval_seconds', '10', 'integer', 'Metrics collection interval in seconds'),
('alert_cooldown_seconds', '600', 'integer', 'Default cooldown period between alerts'),
('backup_retention_days', '30', 'integer', 'Default backup retention period'),
('max_incidents_display', '100', 'integer', 'Maximum incidents to display in dashboard'),
('enable_equipment_simulation', 'true', 'boolean', 'Enable port equipment simulation'),
('num_sts_cranes', '12', 'integer', 'Number of STS cranes to simulate'),
('num_armg_cranes', '42', 'integer', 'Number of ARMG cranes to simulate'),
('num_shuttle_carriers', '30', 'integer', 'Number of shuttle carriers to simulate')
ON DUPLICATE KEY UPDATE config_value=VALUES(config_value);

-- ============================================
-- INSERT DEFAULT ALERT RULES
-- ============================================
INSERT INTO alert_rules (rule_id, name, description, rule_type, condition_expression, severity, channels) VALUES
('RULE_CPU_CRITICAL', 'Critical CPU Usage', 'CPU usage exceeds 85% for 5 minutes', 'threshold', 'cpu_percent > 85 AND duration > 300', 'critical', '["email", "slack"]'),
('RULE_MEMORY_HIGH', 'High Memory Usage', 'Memory usage exceeds 80% for 3 minutes', 'threshold', 'memory_percent > 80 AND duration > 180', 'high', '["email", "slack"]'),
('RULE_DISK_CRITICAL', 'Critical Disk Space', 'Disk usage exceeds 90%', 'threshold', 'disk_percent > 90', 'critical', '["email", "slack", "sms"]'),
('RULE_BACKUP_FAILED', 'Backup Failure', 'Backup job failed', 'status', 'backup_status == "failed"', 'high', '["email", "slack"]'),
('RULE_EQUIPMENT_FAULT', 'Equipment Fault Detected', 'Equipment status changed to fault', 'status', 'equipment_status == "fault"', 'high', '["slack"]'),
('RULE_CRANE_IDLE', 'Crane Idle Too Long', 'STS Crane idle for more than 30 minutes', 'threshold', 'crane_idle_time > 1800', 'medium', '["slack"]')
ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description);

-- ============================================
-- CREATE VIEWS FOR COMMON QUERIES
-- ============================================

-- Active Incidents View
CREATE OR REPLACE VIEW v_active_incidents AS
SELECT 
    i.id,
    i.incident_id,
    i.created_at,
    i.severity,
    i.category,
    i.title,
    i.description,
    i.status,
    i.assigned_to,
    TIMESTAMPDIFF(MINUTE, i.created_at, NOW()) as age_minutes
FROM incidents i
WHERE i.status IN ('open', 'acknowledged', 'investigating')
ORDER BY i.severity DESC, i.created_at DESC;

-- Equipment Summary View
CREATE OR REPLACE VIEW v_equipment_summary AS
SELECT 
    equipment_type,
    COUNT(*) as total_count,
    SUM(CASE WHEN status = 'operational' THEN 1 ELSE 0 END) as operational_count,
    SUM(CASE WHEN status = 'idle' THEN 1 ELSE 0 END) as idle_count,
    SUM(CASE WHEN status = 'fault' THEN 1 ELSE 0 END) as fault_count,
    SUM(CASE WHEN status = 'maintenance' THEN 1 ELSE 0 END) as maintenance_count,
    AVG(utilization_rate) as avg_utilization
FROM equipment_status
GROUP BY equipment_type;

-- Recent Backups View
CREATE OR REPLACE VIEW v_recent_backups AS
SELECT 
    backup_id,
    backup_type,
    target,
    started_at,
    completed_at,
    status,
    ROUND(size_bytes / 1024 / 1024, 2) as size_mb,
    verification_status,
    TIMESTAMPDIFF(SECOND, started_at, completed_at) as duration_seconds
FROM backup_logs
WHERE started_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY started_at DESC;

-- KPI Summary View
CREATE OR REPLACE VIEW v_kpi_current AS
SELECT 
    kpi_category,
    kpi_name,
    kpi_value,
    unit,
    snapshot_time
FROM kpi_snapshots k1
WHERE snapshot_time = (
    SELECT MAX(snapshot_time)
    FROM kpi_snapshots k2
    WHERE k2.kpi_category = k1.kpi_category
    AND k2.kpi_name = k1.kpi_name
);

-- ============================================
-- SUCCESS MESSAGE
-- ============================================
SELECT 'Database schema created successfully!' as message;
