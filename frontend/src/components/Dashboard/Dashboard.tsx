import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
} from '@mui/material';
import {
  Memory as MemoryIcon,
  Storage as StorageIcon,
  Speed as SpeedIcon,
  Engineering as EngineeringIcon,
} from '@mui/icons-material';
import { metricsAPI, equipmentAPI } from '../../services/api';
import { MetricsSummary, EquipmentSummary } from '../../types';
import MetricsChart from '../Charts/MetricsChart';
import EquipmentStatus from '../Equipment/EquipmentStatus';

const Dashboard: React.FC = () => {
  const [metricsSummary, setMetricsSummary] = useState<MetricsSummary | null>(null);
  const [equipmentSummary, setEquipmentSummary] = useState<EquipmentSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [metricsRes, equipmentRes] = await Promise.all([
        metricsAPI.getSummary(1),
        equipmentAPI.getSummary(),
      ]);
      
      setMetricsSummary(metricsRes.data);
      setEquipmentSummary(equipmentRes.data.summary);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const getMetricValue = (key: string, stat: 'avg' | 'max' | 'min') => {
    if (!metricsSummary?.system_metrics[key]) return 0;
    return metricsSummary.system_metrics[key][stat];
  };

  const StatCard: React.FC<{
    title: string;
    value: number;
    unit: string;
    icon: React.ReactNode;
    color: string;
  }> = ({ title, value, unit, icon, color }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div">
              {value.toFixed(1)}
              <Typography variant="caption" sx={{ ml: 1 }}>
                {unit}
              </Typography>
            </Typography>
          </Box>
          <Box
            sx={{
              backgroundColor: color,
              borderRadius: '50%',
              p: 1.5,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Typography>Loading dashboard...</Typography>
      </Container>
    );
  }

  const totalEquipment = equipmentSummary.reduce((sum, e) => sum + e.total_count, 0);
  const operationalEquipment = equipmentSummary.reduce((sum, e) => sum + parseInt(e.operational.toString()), 0);


  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Terminal Monitoring Dashboard
      </Typography>
      <Typography variant="subtitle1" color="textSecondary" gutterBottom sx={{ mb: 3 }}>
        APM Terminals MedPort Tangier - Real-time Operations
      </Typography>

      {/* KPI Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="CPU Usage"
            value={getMetricValue('cpu_percent', 'avg')}
            unit="%"
            icon={<SpeedIcon sx={{ color: 'white' }} />}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Memory Usage"
            value={getMetricValue('memory_percent', 'avg')}
            unit="%"
            icon={<MemoryIcon sx={{ color: 'white' }} />}
            color="#2e7d32"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Disk Usage"
            value={getMetricValue('disk_percent', 'avg')}
            unit="%"
            icon={<StorageIcon sx={{ color: 'white' }} />}
            color="#ed6c02"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Equipment Operational"
            value={totalEquipment > 0 ? (operationalEquipment / totalEquipment) * 100 : 0}
            unit="%"
            icon={<EngineeringIcon sx={{ color: 'white' }} />}
            color="#9c27b0"
          />
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              System Metrics (Last Hour)
            </Typography>
            <MetricsChart />
          </Paper>
        </Grid>
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Equipment Summary
            </Typography>
            <Box sx={{ mt: 2 }}>
              {equipmentSummary.map((summary) => (
                <Box key={summary.equipment_type} sx={{ mb: 2 }}>
                  <Typography variant="body2" color="textSecondary">
                    {summary.equipment_type.replace('_', ' ')}
                  </Typography>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="h6">
                      {summary.operational}/{summary.total_count}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {summary.avg_utilization.toFixed(1)}% util
                    </Typography>
                  </Box>
                  {parseInt(summary.fault.toString()) > 0 && (
                    <Typography variant="caption" color="error">
                      {summary.fault} fault(s)
                    </Typography>
                  )}
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Equipment Status */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Equipment Status
            </Typography>
            <EquipmentStatus />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
