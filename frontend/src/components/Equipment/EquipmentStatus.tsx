import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Box,
  LinearProgress,
  TablePagination,
} from '@mui/material';
import { equipmentAPI } from '../../services/api';
import { Equipment } from '../../types';

const EquipmentStatus: React.FC = () => {
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    fetchEquipment();
    const interval = setInterval(fetchEquipment, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchEquipment = async () => {
    try {
      const response = await equipmentAPI.getStatus();
      setEquipment(response.data.equipment);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching equipment:', error);
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'operational':
        return 'success';
      case 'idle':
        return 'warning';
      case 'fault':
        return 'error';
      case 'maintenance':
        return 'info';
      default:
        return 'default';
    }
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  if (loading) {
    return <LinearProgress />;
  }

  const displayedEquipment = equipment.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <Box>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Equipment ID</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Utilization</TableCell>
              <TableCell>Current Task</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {displayedEquipment.map((eq) => (
              <TableRow key={eq.equipment_id} hover>
                <TableCell>
                  <strong>{eq.equipment_id}</strong>
                </TableCell>
                <TableCell>{eq.equipment_type.replace('_', ' ')}</TableCell>
                <TableCell>{eq.location}</TableCell>
                <TableCell>
                  <Chip
                    label={eq.status}
                    color={getStatusColor(eq.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Box width="100px">
                      <LinearProgress
                        variant="determinate"
                        value={eq.utilization_rate}
                        color={
                          eq.utilization_rate > 90
                            ? 'error'
                            : eq.utilization_rate > 70
                            ? 'warning'
                            : 'primary'
                        }
                      />
                    </Box>
                    <span>{eq.utilization_rate.toFixed(0)}%</span>
                  </Box>
                </TableCell>
                <TableCell>{eq.current_task}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={equipment.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Box>
  );
};

export default EquipmentStatus;
