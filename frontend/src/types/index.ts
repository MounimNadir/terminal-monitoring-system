export interface Metric {
  timestamp: string;
  type: string;
  name: string;
  value: number;
  unit: string;
  host: string;
}

export interface Equipment {
  equipment_id: string;
  equipment_type: string;
  equipment_name: string;
  status: string;
  location: string;
  utilization_rate: number;
  current_task: string;
  last_heartbeat: string;
  metrics: any;
}

export interface EquipmentSummary {
  equipment_type: string;
  total_count: number;
  operational: number;
  idle: number;
  fault: number;
  maintenance: number;
  avg_utilization: number;
}

export interface Incident {
  id: number;
  incident_id: string;
  created_at: string;
  severity: string;
  category: string;
  title: string;
  description: string;
  status: string;
  assigned_to: string;
}

export interface MetricsSummary {
  period_hours: number;
  system_metrics: {
    [key: string]: {
      avg: number;
      max: number;
      min: number;
    };
  };
}
