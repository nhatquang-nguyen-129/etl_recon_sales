import sys
from pathlib import Path

ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_FOLDER_LOCATION))

import pandas as pd

from plugins.local import InternalLocalExtractor
from plugins.gspread import InternalGoogleSheetExtractor

def extract_sales_fact(
    *,
    backend: str,
    direction: str,
) -> pd.DataFrame:
    """
    Extract sales fact
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
        "🔄 [EXTRACT] Triggering to extract sales fact with "
        f"{backend} backend from "
        f"{direction}..."
    )

    if backend == "local":
        extractor = InternalLocalExtractor(direction)

    elif backend == "gspread":
        extractor = InternalGoogleSheetExtractor(direction)

    else:

        raise ValueError(
            "❌ [EXTRACT] Failed to trigger sales fact extraction due to unsupported backend "
            f"{backend}."
        )

    df = extractor.fetch()

    print(
        "✅ [EXTRACT] Successfully triggered sales fact extraction with "
        f"{len(df):,} row(s)."
    )

    return df