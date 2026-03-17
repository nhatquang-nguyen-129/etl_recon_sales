import sys
from pathlib import Path
ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_FOLDER_LOCATION))

import pandas as pd

from plugins.google_bigquery import internalGoogleBigqueryLoader

def load_sales_fact(
    *,
    df: pd.DataFrame,
    backend: str,
    direction: str,
) -> None:

    """
    Load sales Fact Table
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
            "⚠️ [LOADER] Empty sales fact DataFrame then loading will be suspended."
        )
        
        return


    print(
        "🔄 [LOADER] Loading sales fact with "
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
            keys=["date"],
            partition={"field": "date"},
            cluster=["campaign_id"],
        )

    else:
        
        raise ValueError(
            f"❌ [LOADER] Failed to load sales fact with "
            f"{len(df):,} row(s) to "
            f"{direction} direction due to unsupported backend {backend}."
        )    