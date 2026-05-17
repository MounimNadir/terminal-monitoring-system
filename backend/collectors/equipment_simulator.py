"""
Port Terminal Equipment Simulator
Simulates STS Cranes, ARMG Cranes, Shuttle Carriers, and Gate Systems
Based on APM Terminals MedPort Tangier operations
"""

import random
import time
from datetime import datetime, timedelta
from typing import List, Dict
import logging
import json

logger = logging.getLogger(__name__)


class EquipmentSimulator:
    """Simulates port terminal equipment"""
    
    def __init__(self, num_sts_cranes=12, num_armg_cranes=42, num_shuttle_carriers=30):
        self.num_sts_cranes = num_sts_cranes
        self.num_armg_cranes = num_armg_cranes
        self.num_shuttle_carriers = num_shuttle_carriers
        
        self.sts_cranes = []
        self.armg_cranes = []
        self.shuttle_carriers = []
        self.gate_systems = []
        
        self._initialize_equipment()
    
    def _initialize_equipment(self):
        """Initialize all equipment with default states"""
        
        for i in range(1, self.num_sts_cranes + 1):
            self.sts_cranes.append({
                'equipment_id': f'STS-{i:02d}',
                'equipment_type': 'STS_CRANE',
                'equipment_name': f'STS Crane {i}',
                'status': 'OPERATIONAL',
                'location': f'Berth-{(i-1)//4 + 1}',
                'utilization_rate': random.uniform(70, 95),
                'current_task': 'Container loading',
                'last_heartbeat': datetime.now(),
                'metrics': {
                    'moves_per_hour': random.uniform(30, 40),
                    'idle_time_seconds': random.randint(0, 300),
                    'total_moves_today': random.randint(200, 350),
                    'energy_consumption_kwh': random.uniform(150, 200)
                }
            })
        
        for i in range(1, self.num_armg_cranes + 1):
            self.armg_cranes.append({
                'equipment_id': f'ARMG-{i:03d}',
                'equipment_type': 'ARMG_CRANE',
                'equipment_name': f'ARMG Crane {i}',
                'status': 'OPERATIONAL',
                'location': f'Yard-Block-{(i-1)//6 + 1}',
                'utilization_rate': random.uniform(75, 90),
                'current_task': 'Container stacking',
                'last_heartbeat': datetime.now(),
                'metrics': {
                    'stack_moves_per_hour': random.uniform(20, 30),
                    'position_accuracy_cm': random.uniform(1, 3),
                    'total_moves_today': random.randint(150, 250),
                    'energy_consumption_kwh': random.uniform(80, 120)
                }
            })
        
        for i in range(1, self.num_shuttle_carriers + 1):
            self.shuttle_carriers.append({
                'equipment_id': f'SC-{i:03d}',
                'equipment_type': 'SHUTTLE_CARRIER',
                'equipment_name': f'Shuttle Carrier {i}',
                'status': 'OPERATIONAL',
                'location': f'Zone-{random.randint(1, 5)}',
                'utilization_rate': random.uniform(65, 85),
                'current_task': 'Transport to yard',
                'last_heartbeat': datetime.now(),
                'metrics': {
                    'trips_per_hour': random.uniform(8, 12),
                    'battery_level_percent': random.uniform(60, 100),
                    'total_trips_today': random.randint(80, 150),
                    'average_speed_kmh': random.uniform(15, 25)
                }
            })
        
        for i in range(1, 6):
            gate_type = 'Entry' if i <= 3 else 'Exit'
            self.gate_systems.append({
                'equipment_id': f'GATE-{gate_type[0]}{i}',
                'equipment_type': 'GATE_SYSTEM',
                'equipment_name': f'Gate {gate_type} {i}',
                'status': 'OPERATIONAL',
                'location': f'Gate-{gate_type}',
                'utilization_rate': random.uniform(50, 80),
                'current_task': f'Processing {gate_type.lower()}',
                'last_heartbeat': datetime.now(),
                'metrics': {
                    'trucks_per_hour': random.uniform(40, 70),
                    'avg_processing_time_sec': random.uniform(60, 120),
                    'ocr_success_rate_percent': random.uniform(95, 99.5),
                    'total_trucks_today': random.randint(400, 800)
                }
            })
        
        logger.info(f"Initialized {len(self.sts_cranes)} STS cranes, {len(self.armg_cranes)} ARMG cranes, {len(self.shuttle_carriers)} shuttle carriers, {len(self.gate_systems)} gate systems")
    
    def simulate_operational_patterns(self, equipment: Dict) -> Dict:
        current_hour = datetime.now().hour
        peak_factor = 1.2 if 8 <= current_hour < 20 else 0.7
        
        base_utilization = equipment['utilization_rate']
        equipment['utilization_rate'] = min(100, base_utilization * peak_factor)
        
        if equipment['status'] == 'OPERATIONAL':
            if random.random() < 0.001:
                equipment['status'] = 'FAULT'
                logger.warning(f"Equipment {equipment['equipment_id']} status changed to FAULT")
            elif random.random() < 0.005:
                equipment['status'] = 'IDLE'
        elif equipment['status'] == 'FAULT':
            if random.random() < 0.2:
                equipment['status'] = 'MAINTENANCE'
        elif equipment['status'] == 'MAINTENANCE':
            if random.random() < 0.1:
                equipment['status'] = 'OPERATIONAL'
        elif equipment['status'] == 'IDLE':
            if random.random() < 0.5:
                equipment['status'] = 'OPERATIONAL'
        
        equipment['last_heartbeat'] = datetime.now()
        
        if 'moves_per_hour' in equipment['metrics']:
            equipment['metrics']['moves_per_hour'] += random.uniform(-2, 2)
            equipment['metrics']['moves_per_hour'] = max(0, equipment['metrics']['moves_per_hour'])
        
        if 'battery_level_percent' in equipment['metrics']:
            if equipment['status'] == 'OPERATIONAL':
                equipment['metrics']['battery_level_percent'] -= random.uniform(0.1, 0.5)
            else:
                equipment['metrics']['battery_level_percent'] += random.uniform(0.5, 2)
            equipment['metrics']['battery_level_percent'] = max(0, min(100, equipment['metrics']['battery_level_percent']))
        
        return equipment
    
    def get_all_equipment_status(self) -> List[Dict]:
        all_equipment = []
        for crane in self.sts_cranes:
            crane_copy = crane.copy()
            crane_copy['metrics'] = crane['metrics'].copy()
            all_equipment.append(self.simulate_operational_patterns(crane_copy))
        for crane in self.armg_cranes:
            crane_copy = crane.copy()
            crane_copy['metrics'] = crane['metrics'].copy()
            all_equipment.append(self.simulate_operational_patterns(crane_copy))
        for carrier in self.shuttle_carriers:
            carrier_copy = carrier.copy()
            carrier_copy['metrics'] = carrier['metrics'].copy()
            all_equipment.append(self.simulate_operational_patterns(carrier_copy))
        for gate in self.gate_systems:
            gate_copy = gate.copy()
            gate_copy['metrics'] = gate['metrics'].copy()
            all_equipment.append(self.simulate_operational_patterns(gate_copy))
        return all_equipment
    
    def get_equipment_metrics(self) -> List[Dict]:
        metrics = []
        timestamp = datetime.now()
        all_equipment = self.get_all_equipment_status()
        
        for equip in all_equipment:
            metrics.append({
                'metric_type': 'equipment',
                'metric_name': f"{equip['equipment_id']}_utilization",
                'value': round(equip['utilization_rate'], 2),
                'unit': 'percent',
                'timestamp': timestamp,
                'host': 'equipment_simulator',
                'meta_data': {
                    'equipment_id': equip['equipment_id'],
                    'equipment_type': equip['equipment_type'],
                    'status': equip['status']
                }
            })
            
            for metric_name, metric_value in equip['metrics'].items():
                metrics.append({
                    'metric_type': 'equipment',
                    'metric_name': f"{equip['equipment_id']}_{metric_name}",
                    'value': round(metric_value, 2),
                    'unit': self._get_metric_unit(metric_name),
                    'timestamp': timestamp,
                    'host': 'equipment_simulator',
                    'meta_data': {
                        'equipment_id': equip['equipment_id'],
                        'equipment_type': equip['equipment_type']
                    }
                })
        
        logger.debug(f"Generated {len(metrics)} equipment metrics")
        return metrics
    
    def _get_metric_unit(self, metric_name: str) -> str:
        unit_map = {
            'moves_per_hour': 'moves/h',
            'stack_moves_per_hour': 'moves/h',
            'trips_per_hour': 'trips/h',
            'trucks_per_hour': 'trucks/h',
            'idle_time_seconds': 'seconds',
            'total_moves_today': 'moves',
            'total_trips_today': 'trips',
            'total_trucks_today': 'trucks',
            'energy_consumption_kwh': 'kWh',
            'battery_level_percent': 'percent',
            'position_accuracy_cm': 'cm',
            'average_speed_kmh': 'km/h',
            'avg_processing_time_sec': 'seconds',
            'ocr_success_rate_percent': 'percent'
        }
        return unit_map.get(metric_name, 'unit')
