import sys
from pathlib import Path
ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_FOLDER_LOCATION))

import pandas as pd

from plugins.local import InternalLocalExtractor
from plugins.gspread import InternalGoogleSheetExtractor

def extract_sales_transaction(
    *,
    backend: str,
    direction: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Extract sales transaction
    ---
    Principles:
        1. Validate backend
        2. Validate extractor plugin
        3. Initialize plugin client
        4. Trigger extractor
        5. Enforce to DataFrame
    ---
    Returns:
        pandas.DataFrame
    """

    print(
        "🔄 [EXTRACT] Triggering to extract sales transaction with "
        f"{backend} backend from "
        f"{direction}..."
    )

    if backend == "local":
        extractor = InternalLocalExtractor(direction)

    elif backend == "gspread":
        extractor = InternalGoogleSheetExtractor(direction)

    else:

        raise ValueError(
            "❌ [EXTRACT] Failed to trigger sales transaction extraction due to unsupported backend "
            f"{backend}."
        )

    df = extractor.fetch()

    if "Ngày bán" not in df.columns:
        raise ValueError(
            "❌[EXTRACT] Failed to trigger sales transaction extraction due to missing column 'Ngày bán' in source data."
        )
    
    df["Ngày bán"] = pd.to_datetime(
        df["Ngày bán"],
        errors="coerce"
    )

    df = df[df["Ngày bán"].notna()]

    df = df[
        (df["Ngày bán"] >= pd.to_datetime(start_date)) &
        (df["Ngày bán"] <= pd.to_datetime(end_date))
    ]

    print(
        "✅ [EXTRACT] Successfully triggered sales transaction extraction from "
        f"{start_date} to "
        f"{end_date} with "
        f"{len(df):,} row(s)."
    )

    return df