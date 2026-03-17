# Airflow DAG Orchestration for Sales Transaction

## Purpose

- Provide a standardized orchestration layer to manage `Extract`, `Transform`, `Load` to `dbt` workflows

- Ensure all data pipelines are executed in a deterministic, scheduled, and observable manner

- Support both manual trigger (testing/debugging) and scheduled execution (production)

- Decouple data processing logic (Python / dbt) from execution control (Airflow DAG)

- Enable task-level monitoring, retry, and failure handling

## Architecture

DAG Structure

Each DAG represents a logical data pipeline for a specific domain (e.g. sales, ads, promotion)

DAGs are defined using Python and must follow idempotent execution principles

DAGs define task dependencies explicitly using directed acyclic graph structure

DAGs are discovered automatically by Airflow when placed inside the dags/ directory

DAG Run Lifecycle

A DAG Run represents a single execution instance of a DAG

DAG Runs are triggered either:

Manually via UI / CLI

Automatically via schedule_interval

Each DAG Run contains multiple Task Instances

Each Task Instance:

Executes independently

Has its own state (success, failed, retry, etc.)

Produces isolated logs

Task Execution Model

Tasks are executed using operators (e.g. PythonOperator)

Each task runs in an isolated process context

Tasks do not share memory or variables directly

Data must be passed between tasks using:

Intermediate files (e.g. Parquet)

External storage (e.g. BigQuery, GCS)

Sales ELT DAG Design

The sales pipeline follows strict ELT separation:

Extract → Transform → Load → dbt
Extract Task

Responsible for retrieving raw data from source systems

Supports multiple backends:

Local file system

Google Sheets

Validates critical columns (e.g. Ngày bán)

Applies minimal filtering (e.g. date range)

Outputs raw DataFrame to intermediate storage (e.g. Parquet file)

Transform Task

Responsible for data standardization and validation

Performs:

Column renaming (Vietnamese → standardized English)

Data type casting

Column selection

Non-null constraint enforcement

Does not apply business logic or aggregation

Outputs cleaned DataFrame to intermediate storage

Load Task

Responsible for writing data into staging layer in BigQuery

Uses internal loader abstraction (internalGoogleBigqueryLoader)

Supports:

UPSERT mode with key-based deduplication

Partitioning by date

Clustering for performance optimization

Writes to staging.stg_sales instead of mart layer

dbt Task

Responsible for building analytics-ready data models

Executes dbt commands (e.g. dbt run)

Transforms staging data into:

Fact tables (e.g. fact_sales)

Dimension tables (e.g. dim_product, dim_store)

Applies:

Aggregation

Business logic

Data modeling

Task Dependency Flow
extract_sales → transform_sales → load_sales → dbt_run

Each downstream task depends strictly on upstream success

Failure in any task prevents execution of subsequent tasks

Parameterization

DAG supports dynamic configuration via params or conf

Parameters include:

backend (data source)

direction (input/output location)

start_date

end_date

Parameters can be injected during manual trigger for flexible testing

Manual Execution (Testing Mode)

DAGs can be triggered manually via:

Airflow UI (Trigger DAG)

CLI (airflow dags trigger)

Individual tasks can be tested independently using:

airflow tasks test

Manual execution is used for:

Debugging pipeline logic

Validating data transformations

Testing new integrations

Scheduling Behavior

DAGs support scheduling via schedule_interval

Common schedules:

@daily for daily batch processing

Custom cron expressions for fine-grained control

Scheduler continuously evaluates DAGs and creates DAG Runs accordingly

Scheduler must be running for automatic execution

Error Handling and Retry

Each task defines retry behavior:

retries

retry_delay

On failure:

Task is retried automatically based on configuration

Logs are captured for debugging

Hard failures propagate downstream and stop pipeline execution

Logging and Observability

All task logs are stored and accessible via Airflow UI

Logs include:

Execution steps

Row counts

Error messages

Logging should use structured logging (logging.info) instead of print

Data Flow Strategy

Intermediate data is persisted between tasks using Parquet files

This ensures:

Decoupling between tasks

Reproducibility

Fault isolation

Direct in-memory passing between tasks is not supported

Environment Modes
Local Development

Airflow runs on local machine

DAGs are triggered manually

Used for:

Development

Debugging

Pipeline validation

Production Environment

Airflow runs on:

Virtual Machine (VM)

Kubernetes cluster

Managed service

DAGs are scheduled automatically

System is always-on and monitored

Summary

Airflow DAGs orchestrate the execution order and lifecycle of data pipelines

Data transformation logic is separated into:

Python (staging layer)

dbt (mart layer)

Tasks are isolated, idempotent, and observable

The system supports both manual testing and automated scheduling

The architecture aligns with modern data stack principles:

Airflow for orchestration

BigQuery for storage

dbt for transformation

### Setup local dev mode Airflow

- Setup env for Windows
```bash
python -m venv airflow_env
airflow_env\Scripts\activate
```

- Setup env for Mac/Linux
```bash
python -m venv airflow_env
source airflow_env/bin/activate
```

- Install Airflow using constraint to prevent dependency conflict
```bash
pip install "apache-airflow==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.10.txt"
```

- Setup AIRFLOW_HOME for Windows
```bash
export AIRFLOW_HOME=~/airflow
```

- Setup AIRFLOW_HOME for Mac/Linux
```bash
set AIRFLOW_HOME=C:\airflow
```

- Initialize Airflow database
```bash
airflow db init
```

- Create user for Airflow database
```bash
airflow users create \
  --username admin \
  --password admin \
  --firstname admin \
  --lastname admin \
  --role Admin \
  --email admin@example.com
```

---

### Execute Airflow

- Terminal 1 Webserver
```bash
airflow webserver --port 8080
```

- Terminal 2 Scheduler
```bash
airflow scheduler
```

- Put dag file in folder:
```text
~/airflow/dags
```

