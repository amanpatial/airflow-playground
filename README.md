# Airflow Playground

A local development environment for Apache Airflow using Docker Compose. This setup runs Airflow 2.8.1 with CeleryExecutor, Redis, and PostgreSQL for orchestrating and executing data pipelines.

> **Warning:** This configuration is for local development only. Do not use it in a production deployment.

## Architecture

- **Executor:** CeleryExecutor (distributed task execution)
- **Broker:** Redis
- **Metadata Database:** PostgreSQL 13
- **Airflow Version:** 2.8.1

## Services

| Service           | Port | Description                    |
|-------------------|------|--------------------------------|
| airflow-webserver | 8080 | Airflow web UI                 |
| postgres          | 5432 | Metadata database              |
| redis             | 6379 | Message broker (internal)      |
| flower            | 5555 | Celery monitoring (optional)   |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- At least 4GB RAM and 2 CPUs recommended for Docker

## Quick Start

### 1. Set AIRFLOW_UID (Linux/macOS)

On Linux, set the user ID so files are not owned by root:

```bash
echo -e "AIRFLOW_UID=$(id -u)" >> .env
```

On macOS, you can create an `.env` file with:

```
AIRFLOW_UID=50000
```

### 2. Initialize and Start

```bash
docker compose up -d
```

The first run will initialize the database and create an admin user. This may take a few minutes.

### 3. Access the Web UI

Open [http://localhost:8080](http://localhost:8080) in your browser.

- **Username:** `airflow`
- **Password:** `airflow`

## DAGs

### simple_docker_dag

A minimal DAG that demonstrates basic task chaining:

- `start` → prints a message
- `wait` → sleeps for 5 seconds
- `end` → prints completion message

Trigger manually (schedule is `None`).

### weather_etl_pipeline

An ETL pipeline that:

1. **Extract** – Fetches weather data from the [Open-Meteo API](https://open-meteo.com/) for London
2. **Transform** – Extracts temperature, windspeed, wind direction, and weather code
3. **Load** – Inserts the data into PostgreSQL

**Required Connections** (configure in Airflow UI → Admin → Connections):

- `open_meteo_api` – HTTP connection to `https://api.open-meteo.com`
- `postgres_default` – PostgreSQL connection (host: `postgres`, login: `airflow`, password: `airflow`, schema: `airflow`)

Runs daily (`@daily`).

## Project Structure

```
airflow-playground/
├── dags/                 # DAG definitions (mounted into containers)
│   ├── simple_docker_dag.py
│   └── weather_dag.py
├── logs/                 # Airflow logs
├── config/               # Airflow config (optional)
├── plugins/              # Custom plugins (optional)
├── docker-compose.yaml
└── README.md
```

## Optional: Flower

To run [Flower](https://flower.readthedocs.io/) for Celery monitoring:

```bash
docker compose --profile flower up -d
```

Then open [http://localhost:5555](http://localhost:5555).

## Environment Variables

| Variable                    | Default                     | Description                          |
|----------------------------|-----------------------------|--------------------------------------|
| `AIRFLOW_IMAGE_NAME`       | `apache/airflow:2.8.1`      | Docker image for Airflow             |
| `AIRFLOW_UID`              | `50000`                     | User ID in containers (set on Linux) |
| `AIRFLOW_PROJ_DIR`         | `.`                         | Base path for mounted volumes        |
| `_AIRFLOW_WWW_USER_USERNAME` | `airflow`                 | Admin username                       |
| `_AIRFLOW_WWW_USER_PASSWORD` | `airflow`                 | Admin password                       |

## Stopping

```bash
docker compose down
```

To remove volumes (database data):

```bash
docker compose down -v
```

## Resources

- [Airflow Docker Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Airflow Documentation](https://airflow.apache.org/docs/)
