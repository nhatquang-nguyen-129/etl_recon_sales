import os
import sys
from pathlib import Path
ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_FOLDER_LOCATION))

import pandas as pd

class LocalExtractor:
    """
    Internal Local File Loader
    ---
    Principles:
        1. Detect file extension
        2. Map extension to Python pandas reader
        3. Read file into Python DataFrame
        4. Raise ValueError if unsupported    
    ---
    Returns:
        DataFrame
    """

    # 1.1. Initialize
    def __init__(self, direction: str) -> None:
        self.direction = direction

    # 1.2. Entrypoint
    def fetch(self) -> pd.DataFrame:

        SUPPORTED_LOCAL_FORMATS = {
            ".csv": pd.read_csv,
            ".parquet": pd.read_parquet,
            ".json": pd.read_json,
            ".xlsx": pd.read_excel,
        }

        path = self.direction

        try:

            print(
                "🔍 [FETCH] Extracting local file from path "
                f"{path}..."
            )

            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"❌ [FETCH] Failed to extract local file from path "
                    f"{path} due to file not found."
                )

            extension = os.path.splitext(path)[1].lower()

            reader = self.SUPPORTED_LOCAL_FORMATS.get(extension)

            if not reader:
                
                raise ValueError(
                    "❌ [FETCH] Failed to extract local file from path "
                    f"{path} due to extension "
                    f"{extension} is not one of supported formats "
                    f"{list(self.SUPPORTED_LOCAL_FORMATS.keys())}"
                )

            df = reader(path)

            print(
                "✅ [FETCH] Successfully extracted "
                f"{len(df)} row(s) from local file path "
                f"{path}."
            )

            return df

        except Exception as e:

            error = RuntimeError(
                "❌ [FETCH] Failed to fetch local file from path "
                f"{path} due to error {e}."
            )
            
            raise error from e