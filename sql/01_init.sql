CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;
CREATE SCHEMA IF NOT EXISTS monitoring;

CREATE TABLE IF NOT EXISTS raw.usgs_earthquakes (
    id          SERIAL PRIMARY KEY,
    event_id    TEXT UNIQUE,
    raw_json    JSONB NOT NULL,
    loaded_at   TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS monitoring.daily_logs (
    id              SERIAL PRIMARY KEY,
    run_date        DATE NOT NULL,
    dag_id          TEXT NOT NULL,
    events_loaded   INTEGER,
    dbt_status      TEXT,
    finished_at     TIMESTAMPTZ DEFAULT now()
);