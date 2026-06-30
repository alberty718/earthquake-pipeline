# Earthquake Pipeline

End-to-end data pipeline for ingesting and analyzing real-time seismic data from the USGS Earthquake API.

---

## Architecture

**Data source:** USGS Earthquake API

```
GET https://earthquake.usgs.gov/fdsnws/event/1/query
```

```
USGS API
   │
   ▼
[Python producer]
   │  upsert by event_id
   ▼
raw.earthquakes_raw           ← raw JSON + loaded_at
   │
   ▼  dbt run
staging.stg_earthquakes       ← typed columns, region parsed from place
   │
   ▼  dbt run
marts.mart_daily_stats        ← aggregated by day
marts.mart_region_stats       ← aggregated by region
marts.mart_significant_events ← mag >= 5.0 or alert is not null
```

**Orchestration — 3 Airflow DAGs:**

- `earthquake_ingest` — every 15 min, fetches events and loads to raw
- `earthquake_transform` — hourly, triggers dbt run + dbt test
- `earthquake_daily_report` — daily, full dbt rebuild + writes to monitoring log

---

## Stack

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL_15-4169E1?style=flat&logo=postgresql&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow_2.9-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt_1.11-FF694B?style=flat&logo=dbt&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)

---

## Getting Started

### Prerequisites

- Docker + Docker Compose
- Git
- Python 3.11 or 3.12 (3.14 is not supported by dbt)

### Installation

1. Clone the repo

```bash
git clone https://github.com/alberty718/earthquake-pipeline.git
cd earthquake-pipeline
```

2. Create `.env` from example

```bash
cp .env.example .env
```

3. Fill in all values in `.env`. Generate Airflow Fernet key:

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

4. Build and start the stack

```bash
docker compose up -d --build
```

5. Open Airflow UI at `http://localhost:8080` and enable the DAGs

---

## Data Model

| Table | Layer | Description |
|---|---|---|
| `raw.earthquakes_raw` | Raw | Raw JSON from USGS API, upsert by event_id |
| `staging.stg_earthquakes` | Staging | Typed columns, region extracted from place field |
| `marts.mart_daily_stats` | Mart | Events count, avg/max magnitude per day |
| `marts.mart_region_stats` | Mart | Events count, avg magnitude and depth per region |
| `marts.mart_significant_events` | Mart | Events with mag >= 5.0 or alert level set |
| `monitoring.daily_run_log` | Monitoring | Daily DAG run log |

---

## Data Quality

dbt tests are configured for all models:

| Test | Models |
|---|---|
| `not_null` | `event_id`, `magnitude`, `origin_time` in staging; `day`, `events_count` in daily stats; `region` in region stats; `event_id` in significant events |
| `unique` | `event_id` in staging; `day` in daily stats; `event_id` in significant events |

---

## Project Structure

```
earthquake-pipeline/
├── docker-compose.yml
├── .env.example
├── airflow/
│   ├── Dockerfile
│   └── dags/
│       ├── earthquake_ingest.py
│       ├── earthquake_transform.py
│       └── earthquake_daily_report.py
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/
│       │   ├── stg_earthquakes.sql
│       │   └── schema.yml
│       └── marts/
│           ├── mart_daily_stats.sql
│           ├── mart_region_stats.sql
│           ├── mart_significant_events.sql
│           └── schema.yml
├── ingestion/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── fetch_earthquakes.py
└── sql/
    └── init.sql
```

---

## License

MIT

---

## Contact

Albert — Telegram [@thealberty](https://t.me/thealberty)

Project: [github.com/alberty718/earthquake-pipeline](https://github.com/alberty718/earthquake-pipeline)
