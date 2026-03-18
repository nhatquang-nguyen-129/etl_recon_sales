import os
import sys
from pathlib import Path

ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[0]
sys.path.append(str(ROOT_FOLDER_LOCATION))

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dags.dags_sales_transaction import dags_sales_transaction

MODE = os.getenv("MODE")

EXTRACT_BACKEND = os.getenv("EXTRACT_BACKEND")

EXTRACT_DIRECTION = os.getenv("EXTRACT_DIRECTION")

LOAD_BACKEND = os.getenv("LOAD_BACKEND", "bigquery")

LOAD_DIRECTION = os.getenv("LOAD_DIRECTION", "seer-retail-sales")

if not all([
    MODE, 
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

    print(
        "🔄 [MAIN] Triggering Sales Transaction pipeline with mode "
        f"{MODE}..."
    )

# ======================
# Resolve time range
# ======================
    ICT = ZoneInfo("Asia/Ho_Chi_Minh")

    today = datetime.now(ICT)

    if MODE == "today":

        start_date = end_date = today.strftime("%Y-%m-%d")

    elif MODE == "last3days":

        start_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
        end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")

    elif MODE == "last7days":

        start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")

    elif MODE == "thismonth":

        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")

    elif MODE == "lastmonth":

        last_month_end = today.replace(day=1) - timedelta(days=1)

        start_date = last_month_end.replace(day=1).strftime("%Y-%m-%d")
        end_date = last_month_end.strftime("%Y-%m-%d")

    else:

        raise ValueError(
            "❌ [MAIN] Unsupported MODE: "
            f"{MODE}"
        )

    print(
        "✅ [MAIN] Resolved time range from "
        f"{start_date} to {end_date}."
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