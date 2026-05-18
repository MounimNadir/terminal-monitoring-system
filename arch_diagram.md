
## Architecture

**System Components:**
┌─────────────────────────────────────────┐
│          Docker Network                  │
│                                          │
│  ┌──────────┐         ┌──────────┐     │
│  │Dashboard │ <-----  │   API    │     │
│  │ (Nginx)  │         │ (Flask)  │     │
│  │Port 8080 │         │Port 5000 │     │
│  └──────────┘         └────┬─────┘     │
│                            │            │
│  ┌──────────┐         ┌────▼─────┐     │
│  │Monitoring│ ------> │  MySQL   │     │
│  │ (Python) │         │Port 3307 │     │
│  └────┬─────┘         └──────────┘     │
│       │                                 │
│       │               ┌──────────┐     │
│       └────────────-> │  Redis   │     │
│                       │Port 6379 │     │
│                       └──────────┘     │
└─────────────────────────────────────────┘

**Services:**
- **MySQL 8.0**: Database with 8 tables, 4 views
- **Redis 7**: Caching layer
- **Monitoring Service**: Python-based data collector
- **API Service**: Flask REST API
- **Dashboard**: React + Nginx production build
