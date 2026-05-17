"""
System Metrics Collector
Collects CPU, Memory, Disk, and Network metrics using psutil
"""

import psutil
import time
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class SystemMetricsCollector:
    """Collects system metrics"""
    
    def __init__(self):
        self.hostname = "localhost"
        self.last_net_io = None
        self.last_disk_io = None
        self.last_check_time = None
        
    def collect_cpu_metrics(self) -> List[Dict]:
        """Collect CPU metrics"""
        metrics = []
        
        try:
            # Overall CPU percentage
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append({
                'metric_type': 'cpu',
                'metric_name': 'cpu_percent',
                'value': round(cpu_percent, 2),
                'unit': 'percent',
                'timestamp': datetime.now()
            })
            
            # Per-core CPU percentage
            cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
            for i, percent in enumerate(cpu_per_core):
                metrics.append({
                    'metric_type': 'cpu',
                    'metric_name': f'cpu_core_{i}',
                    'value': round(percent, 2),
                    'unit': 'percent',
                    'timestamp': datetime.now()
                })
            
            # CPU count
            metrics.append({
                'metric_type': 'cpu',
                'metric_name': 'cpu_count',
                'value': psutil.cpu_count(),
                'unit': 'count',
                'timestamp': datetime.now()
            })
            
        except Exception as e:
            logger.error(f"Error collecting CPU metrics: {e}")
        
        return metrics
    
    def collect_memory_metrics(self) -> List[Dict]:
        """Collect memory metrics"""
        metrics = []
        
        try:
            # Virtual memory
            mem = psutil.virtual_memory()
            
            metrics.append({
                'metric_type': 'memory',
                'metric_name': 'memory_percent',
                'value': round(mem.percent, 2),
                'unit': 'percent',
                'timestamp': datetime.now()
            })
            
            metrics.append({
                'metric_type': 'memory',
                'metric_name': 'memory_used',
                'value': round(mem.used / (1024**3), 2),  # GB
                'unit': 'GB',
                'timestamp': datetime.now()
            })
            
            metrics.append({
                'metric_type': 'memory',
                'metric_name': 'memory_available',
                'value': round(mem.available / (1024**3), 2),  # GB
                'unit': 'GB',
                'timestamp': datetime.now()
            })
            
            # Swap memory
            swap = psutil.swap_memory()
            metrics.append({
                'metric_type': 'memory',
                'metric_name': 'swap_percent',
                'value': round(swap.percent, 2),
                'unit': 'percent',
                'timestamp': datetime.now()
            })
            
        except Exception as e:
            logger.error(f"Error collecting memory metrics: {e}")
        
        return metrics
    
    def collect_disk_metrics(self) -> List[Dict]:
        """Collect disk metrics"""
        metrics = []
        
        try:
            # Disk usage for root partition
            disk = psutil.disk_usage('/')
            
            metrics.append({
                'metric_type': 'disk',
                'metric_name': 'disk_percent',
                'value': round(disk.percent, 2),
                'unit': 'percent',
                'timestamp': datetime.now()
            })
            
            metrics.append({
                'metric_type': 'disk',
                'metric_name': 'disk_used',
                'value': round(disk.used / (1024**3), 2),  # GB
                'unit': 'GB',
                'timestamp': datetime.now()
            })
            
            metrics.append({
                'metric_type': 'disk',
                'metric_name': 'disk_free',
                'value': round(disk.free / (1024**3), 2),  # GB
                'unit': 'GB',
                'timestamp': datetime.now()
            })
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            if disk_io:
                current_time = time.time()
                
                if self.last_disk_io and self.last_check_time:
                    time_delta = current_time - self.last_check_time
                    
                    read_rate = (disk_io.read_bytes - self.last_disk_io.read_bytes) / time_delta / (1024**2)  # MB/s
                    write_rate = (disk_io.write_bytes - self.last_disk_io.write_bytes) / time_delta / (1024**2)  # MB/s
                    
                    metrics.append({
                        'metric_type': 'disk',
                        'metric_name': 'disk_read_rate',
                        'value': round(read_rate, 2),
                        'unit': 'MB/s',
                        'timestamp': datetime.now()
                    })
                    
                    metrics.append({
                        'metric_type': 'disk',
                        'metric_name': 'disk_write_rate',
                        'value': round(write_rate, 2),
                        'unit': 'MB/s',
                        'timestamp': datetime.now()
                    })
                
                self.last_disk_io = disk_io
                self.last_check_time = current_time
                
        except Exception as e:
            logger.error(f"Error collecting disk metrics: {e}")
        
        return metrics
    
    def collect_network_metrics(self) -> List[Dict]:
        """Collect network metrics"""
        metrics = []
        
        try:
            net_io = psutil.net_io_counters()
            current_time = time.time()
            
            if self.last_net_io and self.last_check_time:
                time_delta = current_time - self.last_check_time
                
                bytes_sent_rate = (net_io.bytes_sent - self.last_net_io.bytes_sent) / time_delta / (1024**2)  # MB/s
                bytes_recv_rate = (net_io.bytes_recv - self.last_net_io.bytes_recv) / time_delta / (1024**2)  # MB/s
                
                metrics.append({
                    'metric_type': 'network',
                    'metric_name': 'network_sent_rate',
                    'value': round(bytes_sent_rate, 2),
                    'unit': 'MB/s',
                    'timestamp': datetime.now()
                })
                
                metrics.append({
                    'metric_type': 'network',
                    'metric_name': 'network_recv_rate',
                    'value': round(bytes_recv_rate, 2),
                    'unit': 'MB/s',
                    'timestamp': datetime.now()
                })
            
            self.last_net_io = net_io
            
        except Exception as e:
            logger.error(f"Error collecting network metrics: {e}")
        
        return metrics
    
    def collect_all(self) -> List[Dict]:
        """Collect all system metrics"""
        all_metrics = []
        
        all_metrics.extend(self.collect_cpu_metrics())
        all_metrics.extend(self.collect_memory_metrics())
        all_metrics.extend(self.collect_disk_metrics())
        all_metrics.extend(self.collect_network_metrics())
        
        # Add hostname to all metrics
        for metric in all_metrics:
            metric['host'] = self.hostname
        
        logger.debug(f"Collected {len(all_metrics)} system metrics")
        
        return all_metrics
