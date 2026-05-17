# 🚢 Intelligent Terminal Operations Monitoring System

> **Automated System Monitoring Dashboard with Incident Detection for Port Terminal Operations**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.2+-61DAFB.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)

## 📋 Project Context

This project was developed to demonstrate proficiency in **intelligent incident detection**, **backup status monitoring**, and **interactive business dashboards** — aligned with APM Terminals Tangier's IT internship requirements for their world-class automated container terminal operations.

**APM Terminals MedPort Tangier** is one of the most technologically advanced port terminals globally, featuring:
- 20+ remote-controlled Ship-to-Shore (STS) cranes
- 42 Automated Rail-Mounted Gantry (ARMG) cranes  
- 30+ shuttle carriers for container transport
- Fully automated gate systems

This monitoring system simulates real-world IT infrastructure monitoring with a focus on port terminal KPIs and equipment tracking.

---

## ✨ Key Features

### 🔍 **Intelligent Incident Detection**
- Real-time system metrics monitoring (CPU, memory, disk, network)
- Threshold-based anomaly detection with configurable rules
- Multi-channel alerting (Email, Slack, SMS simulation)
- Automated incident logging and severity classification

### 💾 **Backup Status Monitoring**
- Automated database backup verification
- File integrity checks (checksums, restore tests)
- Backup success rate tracking
- Storage capacity monitoring

### 📊 **Interactive KPI Dashboards**
- **Equipment Monitoring**: STS cranes, ARMG cranes, shuttle carriers
- **Operational KPIs**: Vessel turnaround time, crane productivity, gate throughput
- **System Health**: Uptime, response time, error rates
- **Real-time Updates**: WebSocket-powered live data streaming

### 🏗️ **Port Terminal Equipment Simulation**
- Realistic equipment behavior modeling
- Random fault injection for incident testing
- Operational patterns (peak hours, seasonal trends)
- Equipment utilization tracking

---

## 🏛️ System Architecture
┌────────────────────────────────────────────────────────┐
│              React Dashboard (Port 3000)                │
│  Equipment Status | KPI Analytics | Alert Management   │
└──────────────────────┬─────────────────────────────────┘
│ HTTP/WebSocket
┌──────────────────────▼─────────────────────────────────┐
│              Flask REST API (Port 5000)                 │
│  /api/metrics | /api/alerts | /api/equipment           │
└──────────────────────┬─────────────────────────────────┘
│
┌──────────────┼──────────────┐
│              │              │
┌───────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
│ MySQL DB     │ │  Redis   │ │  Monitor   │
│ (Port 3306)  │ │ (6379)   │ │  Service   │
└──────────────┘ └──────────┘ └────────────┘


---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- 4GB RAM minimum
- 10GB free disk space

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/terminal-monitoring-system.git
cd terminal-monitoring-system
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
nano .env
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the dashboard**
- Dashboard: http://localhost:3000
- API: http://localhost:5000
- API Docs: http://localhost:5000/docs

5. **View logs**
```bash
docker-compose logs -f
```

---

## 📊 Port Terminal KPIs Tracked

| KPI Category | Metrics | Target |
|--------------|---------|--------|
| **Equipment** | Crane moves/hour | 30-40 |
| **Equipment** | Utilization rate | >85% |
| **Vessel Ops** | Turnaround time | <24 hours |
| **Yard Ops** | Container dwell time | <5 days |
| **Gate Ops** | Truck throughput | >60/hour |
| **System** | Backup success rate | >99% |
| **System** | API response time | <200ms |

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11+** - Core language
- **Flask** - REST API framework
- **psutil** - System metrics collection
- **APScheduler** - Task scheduling
- **PyMySQL** - Database connector
- **Redis** - Caching & real-time data

### Frontend
- **React 18+** - UI framework
- **Material-UI** - Component library
- **Chart.js / Recharts** - Data visualization
- **Socket.IO Client** - Real-time updates
- **React Query** - Data fetching

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **MySQL 8.0** - Relational database
- **Nginx** - Reverse proxy & static files

---

## 📁 Project Structure
terminal-monitoring-system/
├── backend/              # Monitoring service
│   ├── collectors/       # System & equipment monitors
│   ├── alerts/           # Alert management
│   ├── database/         # Models & migrations
│   └── utils/            # Helper functions
├── api/                  # Flask REST API
│   ├── routes/           # API endpoints
│   ├── websocket/        # Real-time communication
│   └── middleware/       # Auth & rate limiting
├── frontend/             # React dashboard
│   └── src/
│       ├── components/   # UI components
│       ├── pages/        # Application pages
│       └── services/     # API clients
├── config/               # Configuration files
├── scripts/              # Utility scripts
├── docs/                 # Documentation
└── tests/                # Test suites

---

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/ -v --cov

# Frontend tests
cd frontend
npm test -- --coverage

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## 📖 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [User Manual](docs/USER_MANUAL.md)

---

## 🎯 Future Enhancements

- [ ] Machine learning anomaly detection
- [ ] Predictive maintenance alerts
- [ ] Mobile app (React Native)
- [ ] Integration with real Terminal Operating Systems (TOS)
- [ ] Advanced analytics with Grafana
- [ ] Multi-tenant support
- [ ] RBAC (Role-Based Access Control)

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Name](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by **APM Terminals Tangier MedPort** operations
- Port terminal KPIs based on industry standards
- Built for the APM Terminals IT Internship application

---

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the author.

---

**⭐ If you find this project useful, please consider giving it a star!**

