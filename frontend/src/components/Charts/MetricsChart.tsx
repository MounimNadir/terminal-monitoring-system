import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { metricsAPI } from '../../services/api';
import { format } from 'date-fns';

const MetricsChart: React.FC = () => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      // Fetch each metric type separately
      const [cpuRes, memoryRes, diskRes] = await Promise.all([
        metricsAPI.getHistorical({ name: 'cpu_percent', hours: 1, limit: 50 }),
        metricsAPI.getHistorical({ name: 'memory_percent', hours: 1, limit: 50 }),
        metricsAPI.getHistorical({ name: 'disk_percent', hours: 1, limit: 50 }),
      ]);

      // Combine all metrics
      const allMetrics = [
        ...cpuRes.data.metrics,
        ...memoryRes.data.metrics,
        ...diskRes.data.metrics,
      ];

      // Group by timestamp
      const grouped: { [key: string]: any } = {};

      allMetrics.forEach((metric: any) => {
        const time = format(new Date(metric.timestamp), 'HH:mm:ss');
        
        if (!grouped[time]) {
          grouped[time] = { time };
        }

        if (metric.name === 'cpu_percent') {
          grouped[time].cpu = Number(metric.value);
        } else if (metric.name === 'memory_percent') {
          grouped[time].memory = Number(metric.value);
        } else if (metric.name === 'disk_percent') {
          grouped[time].disk = Number(metric.value);
        }
      });

      // Convert to array and sort by time
      const chartData = Object.values(grouped)
        .sort((a: any, b: any) => a.time.localeCompare(b.time))
        .slice(-30); // Last 30 data points

      setData(chartData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching metrics:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading chart...</div>;
  }

  if (data.length === 0) {
    return <div>No data available yet. Collecting metrics...</div>;
  }

  return (
    <ResponsiveContainer width="100%" height="90%">
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="time" 
          tick={{ fontSize: 12 }}
        />
        <YAxis 
          domain={[0, 100]} 
          tick={{ fontSize: 12 }}
        />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="cpu"
          stroke="#1976d2"
          name="CPU %"
          strokeWidth={2}
          dot={false}
          connectNulls
        />
        <Line
          type="monotone"
          dataKey="memory"
          stroke="#2e7d32"
          name="Memory %"
          strokeWidth={2}
          dot={false}
          connectNulls
        />
        <Line
          type="monotone"
          dataKey="disk"
          stroke="#ed6c02"
          name="Disk %"
          strokeWidth={2}
          dot={false}
          connectNulls
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default MetricsChart;
