import sys
from pathlib import Path
ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_FOLDER_LOCATION))

import pandas as pd

from plugins.google_bigquery import internalGoogleBigqueryLoader

def load_sales_transaction(
    *,
    df: pd.DataFrame,
    backend: str,
    direction: str,
) -> None:

    """
    Load sales transaction
    ---
    Principles:
        1. Validate input DataFrame
        2. Validate output direction for Google BigQuery
        3. Set primary key(s) to date
        4. Use UPSERT mode with parameterized query for deduplication
        5. Make internalGoogleBigQueryLoader API call
    ---
    Returns:
        None
    """

    if df.empty:

        print(
            "⚠️ [LOADER] Empty sales transaction DataFrame then loading will be suspended."
        )
        
        return


    print(
        "🔄 [LOADER] Loading sales transaction with "
        f"{len(df):,} row(s) to "
        f"{backend} direction "
        f"{direction}..."
    )

    if backend == "bigquery":

        loader = internalGoogleBigqueryLoader()

        loader.load(
            df=df,
            direction=direction,
            mode="upsert",
            keys=["transaction_date"],
            partition={"field": "transaction_date"},
            cluster=["store_id", "product_id"],
        )

    else:
        
        raise ValueError(
            f"❌ [LOADER] Failed to load sales transaction with "
            f"{len(df):,} row(s) to "
            f"{direction} direction due to unsupported backend {backend}."
        )