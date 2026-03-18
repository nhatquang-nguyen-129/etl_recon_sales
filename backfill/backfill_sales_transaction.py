import os
import sys
from pathlib import Path

ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[0]
sys.path.append(str(ROOT_FOLDER_LOCATION))

import argparse
from datetime import datetime

from dags.dags_sales_transaction import dags_sales_transaction

EXTRACT_BACKEND = os.getenv("EXTRACT_BACKEND")

EXTRACT_DIRECTION = os.getenv("EXTRACT_DIRECTION")

LOAD_BACKEND = os.getenv("LOAD_BACKEND", "bigquery")

LOAD_DIRECTION = os.getenv("LOAD_DIRECTION", "seer-retail-sales")

if not all([
    EXTRACT_BACKEND,
    EXTRACT_DIRECTION,
    LOAD_BACKEND,
    LOAD_DIRECTION
    ]):
    
    raise EnvironmentError(
        "❌ [MAIN] Missing required environment variables (MODE, PROJECT)."
    )

def main():
    """
    Main Sales Transaction Entrypoint
    ---
    Principles:
        1. Resolve execution time window from MODE
        2. Read & validate environment variables
        3. Dispatch execution to DAG
    ---
    Returns:
        None
    """

# CLI arguments parser for manual date range
    parser = argparse.ArgumentParser(
        description="Manual Google Ads ETL executor"
    )
    
    parser.add_argument(
        "--start_date",
        required=True,
        help="Start date in YYYY-MM-DD format"
    )
    
    parser.add_argument(
        "--end_date",
        required=True,
        help="End date in YYYY-MM-DD format"
    )
    
    args = parser.parse_args()

    try:
    
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    
    except ValueError:
    
        raise ValueError(
            "❌ [BACKFILL] Failed to execute Google Ads backfill due to start_date and end_date must be in YYYY-MM-DD format."
        )

    if start_date > end_date:
        
        raise ValueError(
            "❌ [BACKFILL] Failed to execute Google Ads backfill due to start_date must be less than or equal to end_date."
        )

    print(
        "🔄 [BACKFILL] Triggering to execute sales transaction backfill from "
        f"{start_date} to "
        f"{end_date}..."
    )

    # Execute DAG
    dags_sales_transaction(
        extract_backend=EXTRACT_BACKEND,
        extract_direction=EXTRACT_DIRECTION,
        load_backend=LOAD_BACKEND,
        load_direction=LOAD_DIRECTION,
        start_date=start_date,
        end_date=end_date,
    )

    # Entrypoint
if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print(f"❌ [MAIN] Pipeline failed due to: {e}")

        sys.exit(1)