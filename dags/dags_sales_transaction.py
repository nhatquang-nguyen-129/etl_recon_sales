import os
import sys
from pathlib import Path

ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_FOLDER_LOCATION))

from etl.extract_sales_transaction import extract_sales_transaction
from etl.transform_sales_transaction import transform_sales_transaction
from etl.load_sales_transaction import load_sales_transaction

import pandas as pd

def dags_sales_transaction(
    *,
    extract_backend: str,
    extract_direction: str,
    load_backend: str,
    load_direction: str,
    start_date: str,
    end_date: str,
):
    """
    DAG Orchestration for sales transaction
    ---
    Principles:
        1. Trigger sales transaction extraction
        2. Transform Google Ads campaign insights into validated schema
        3. Load transformed Google Ads campaing insights records into Google BigQuery
        4. Set Google Ads API cooldown between each day
        5. Execute dbt models for materialization
    ---
    Returns:
        1. None
    """

    print(
        "🔄 [DAGS] Trigger to update sales transaction from "
        f"{start_date} to "
        f"{end_date}..."
    )

    # Extract
    df = extract_sales_transaction(
        backend=extract_backend,
        direction=extract_direction,
        start_date=start_date,
        end_date=end_date,
    )

    if df.empty:
        print("⚠️ [DAGS] No data → stop.")
        return

    # Transform
    df = transform_sales_transaction(df=df)

    if df.empty:
        print("⚠️ [DAGS] Transform empty → stop.")
        return

    # Load
    year = pd.to_datetime(df["transaction_date"].iloc[0]).year
    
    month = pd.to_datetime(df["transaction_date"].iloc[0]).month

    _sales_transaction_direction = (
        f"{load_direction}."
        f"kids_dataset_sales_transaction_raw."
        f"kids_table_erp_lsretail_sales_transaction_m{month:02d}{year}"
    )

    print(
        "🔄 [DAGS] Loading sales transaction to "
        f"{_sales_transaction_direction}..."
    )

    load_sales_transaction(
        df=df,
        backend=load_backend,
        direction=_sales_transaction_direction,
    )

    print(
        "✅ [DAGS] Completed sales transaction pipeline with "
        f"{len(df):,} row(s)."
    )