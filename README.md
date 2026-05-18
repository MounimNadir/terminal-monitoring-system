# Terminal Monitoring System

A production-ready real-time monitoring system for port terminal operations. Tracks 89+ equipment units with automated alerting, interactive dashboards, and full Docker deployment.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

[![React 18](https://img.shields.io/badge/react-18.2-61DAFB.svg)](https://reactjs.org/)

[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)

## 📋 Overview

A full-stack monitoring system demonstrating real-time data processing, equipment simulation, alerting, and containerized deployment. Built as a portfolio project to showcase modern DevOps and full-stack development practices.

**Key Capabilities:**

- Real-time monitoring of system metrics and equipment status

- Automated incident detection with email notifications

- Interactive dashboard with live data visualization

- RESTful API with 11 endpoints

- One-command Docker deployment

## 🎯 Features

### Real-Time Monitoring

- System metrics: CPU, Memory, Disk, Network

- Equipment simulation: 89 units (cranes, carriers, gates)

- 470+ metrics collected every 10 seconds

- Automatic data cleanup (7-day retention)

### Alert System

- Threshold-based monitoring

- Configurable alert rules stored in database

- Email notifications via SMTP (Gmail)

- Automatic incident creation and tracking

- Multiple severity levels: CRITICAL, HIGH, MEDIUM, LOW

### Interactive Dashboard

- Real-time KPI cards (CPU, Memory, Disk, Equipment %)

- Live line charts with 30-point history

- Equipment summary by type

- Paginated equipment status table

- Auto-refresh every 10-15 seconds

### REST API

- 11 endpoints for metrics, equipment, and incidents

- Time-range filtering and aggregation

- Equipment filtering by type and status

- Health check endpoint

- CORS-enabled for frontend integration

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+

- Docker Compose 2.0+

- 4GB RAM minimum

- 10GB disk space

### Installation

```bash

# Clone the repository

git clone https://github.com/MounimNadir/terminal-monitoring-system.git

cd terminal-monitoring-system

# Start all services (builds and starts 5 containers)

docker-compose up -d

# Wait 30 seconds for initialization

sleep 30

# Access the system

open http://localhost:8080

```

**That's it!** The system is now running with:

- Dashboard at http://localhost:8080

- API at http://localhost:5000

- MySQL at localhost:3307

- Redis at localhost:6379

### Stopping the System

```bash

# Stop all services

docker-compose down

# Stop and remove all data (WARNING: deletes database)

docker-compose down -v

```

## 🏗️ Architecture
┌─────────────────────────────────────────────────┐
│              Docker Host                        │
│                                                 │
│  ┌──────────────┐      ┌──────────────┐         │
│  │  Dashboard   │◄─────┤     API      │         │
│  │  (Nginx)     │      │   (Flask)    │         │
│  │  Port 8080   │      │   Port 5000  │         │
│  └──────────────┘      └───────┬──────┘         │
│                                 │               │
│  ┌──────────────┐      ┌───────▼──────┐         │
│  │  Monitoring  │─────►│    MySQL     │         │
│  │  (Python)    │      │   Port 3307  │         │
│  └──────┬───────┘      └──────────────┘         │
│         │                                       │
│         │              ┌──────────────┐         │
│         └─────────────►│    Redis     │         │
│                        │   Port 6379  │         │
│                        └──────────────┘         │
└─────────────────────────────────────────────────┘


**Services:**
- **MySQL 8.0**: Database with 8 tables, 4 views
- **Redis 7**: Caching layer
- **Monitoring Service**: Python-based data collector
- **API Service**: Flask REST API
- **Dashboard**: React + Nginx production build

## 🔧 Technology Stack

### Backend
- **Python 3.12** - Core language
- **Flask** - REST API framework
- **SQLAlchemy** - ORM for database operations
- **PyMySQL** - MySQL database driver
- **psutil** - System metrics collection
- **smtplib** - Email notifications

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Material-UI (MUI)** - Component library
- **Recharts** - Data visualization
- **Axios** - HTTP client

### Infrastructure
- **MySQL 8.0** - Relational database
- **Redis 7** - In-memory cache
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy & static file server

## 📡 API Endpoints

| Method |         Endpoint             | Description                        |
|--------|------------------------------|------------------------------------|
| GET    | `/health`                    | API health check                   |
| GET    | `/api/metrics/current`       | Latest metrics (last minute)       |
| GET    | `/api/metrics/historical`    | Historical metrics with time range |
| GET    | `/api/metrics/summary`       | Aggregated metrics (avg/max/min)   |
| GET    | `/api/metrics/types`         | Available metric types             |
| GET    | `/api/equipment/status`      | All equipment with filters         |
| GET    | `/api/equipment/summary`     | Equipment summary by type          |
| GET    | `/api/equipment/<id>`        | Specific equipment details         |
| GET    | `/api/equipment/types`       | Equipment types list               |
| GET    | `/api/incidents/active`      | Active incidents                   |
| GET    | `/api/incidents/all`         | All incidents with filters         |


**Example Request:**
```bash
curl http://localhost:5000/api/equipment/summary
```

## 🗄️ Database Schema

### Tables (8)
- **metrics** - Time-series system and equipment metrics
- **equipment_status** - Current state of all equipment
- **incidents** - Alert incidents history
- **backup_logs** - System backup records
- **alert_rules** - Configurable alert thresholds
- **alert_history** - Alert trigger history
- **kpi_snapshots** - Daily KPI summaries
- **system_config** - System configuration

### Views (4)
- **v_active_incidents** - Currently open incidents
- **v_equipment_summary** - Equipment summary by type
- **v_recent_backups** - Recent backup status
- **v_kpi_current** - Current KPI values

## 🚨 Alert System

### Production Alert Rules

| Alert            | Condition | Severity |
|------------------|-----------|----------|
| CPU Critical     | > 90%     | CRITICAL |
| CPU High         | > 80%     | HIGH     |
| Memory Critical  | > 95%     | CRITICAL |
| Memory High      | > 90%     | HIGH     |
| Disk Critical    | > 95%     | CRITICAL |

### Email Configuration

Edit `.env` file:
```env
EMAIL_ALERTS_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
ALERT_FROM_EMAIL=monitoring@terminal.com
ALERT_TO_EMAILS=recipient@example.com
```

**Getting Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Enable 2-Step Verification
3. Generate app password for "Mail"
4. Copy 16-character password to `.env`

## 🛠️ Development

### Project Structure
terminal-monitoring-system/
├── backend/                # Monitoring service
│   ├── collectors/         # Metrics collectors
│   ├── database/           # Models & connection
│   ├── alerts/             # Alert management
│   └── utils/              # Utility functions
├── api/                    # Flask REST API
│   └── routes/             # API endpoints
├── frontend/               # React dashboard
│   └── src/
│       ├── components/     # React components
│       ├── services/       # API client
│       └── types/          # TypeScript types
├── docker-compose.yml      # Docker orchestration
└── .env                    # Environment variables

### Running Locally (Without Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**API:**
```bash
cd api
pip install -r ../backend/requirements.txt
pip install flask flask-cors
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 📊 System Performance

- **Metrics Collection**: 470 metrics per 10-second cycle
- **Database Writes**: ~1.5 MB/hour
- **Storage Growth**: ~36 MB/day (auto-cleanup after 7 days)
- **API Response Time**: 50-200ms
- **Dashboard Load Time**: 2-3 seconds

## 🔍 Monitoring

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f monitoring
docker-compose logs -f api
docker-compose logs -f dashboard
```

### Check Service Status
```bash
docker-compose ps
```

### Access Database
```bash
docker exec -it terminal-mysql mysql -u root -p
# Password: rootpassword (default)
```

## 🐛 Troubleshooting

### Dashboard shows no data
```bash
# Check API health
curl http://localhost:5000/health

# Check API data
curl http://localhost:5000/api/equipment/summary

# Hard refresh browser (Ctrl+F5)
```

### Monitoring service not collecting
```bash
# Check logs
docker-compose logs monitoring

# Verify database connection
docker exec terminal-monitoring env | grep DB_
```

### Port conflicts
Edit `docker-compose.yml`:
```yaml
# Change dashboard port
ports:
  - "8081:80"  # Change 8080 to 8081

# Change MySQL port
ports:
  - "3308:3306"  # Change 3307 to 3308
```

## 📈 Equipment Simulated

- **12 STS Cranes** - Ship-to-Shore cranes at 3 berths
- **42 ARMG Cranes** - Automated Rail-Mounted Gantry cranes in 7 yard blocks
- **30 Shuttle Carriers** - Container transport in 5 zones
- **5 Gate Systems** - 3 entry gates, 2 exit gates

Each equipment unit has:
- Unique ID and location
- Operational status (OPERATIONAL, FAULT, MAINTENANCE, IDLE)
- Utilization percentage
- Current task
- Realistic fault injection (random failures)

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Full-stack development (Python backend, React frontend)
- ✅ RESTful API design and implementation
- ✅ Real-time data processing and visualization
- ✅ Database design and optimization
- ✅ Docker containerization and orchestration
- ✅ Alert systems and notifications
- ✅ System monitoring and metrics collection
- ✅ Production-ready deployment practices

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mounim Nadir**
- GitHub: [@MounimNadir](https://github.com/MounimNadir)
- LinkedIn: [Mounim Nadir](https://www.linkedin.com/in/mounimnadir/)
- Email: mounimnadir7@gmail.com

## 🙏 Acknowledgments

- Built with modern web technologies and DevOps best practices
- Inspired by industrial IoT monitoring systems
- Created as a portfolio project to demonstrate full-stack capabilities

---

**⭐ If you find this project useful, please consider giving it a star!**
