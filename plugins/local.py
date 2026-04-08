import os
import sys
from pathlib import Path
ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_FOLDER_LOCATION))

import pandas as pd

class InternalLocalExtractor:
    """
    Internal Local File Loader
    ---
    Principles:
        1. Detect file extension
        2. Map extension to supported file formats
        3. Check extension to call appropriate reader
        3. Read file into Python DataFrame
        4. Raise ValueError if unsupported    
    ---
    Returns:
        pandas.DataFrame
    """

    SUPPORTED_LOCAL_FORMATS = {
        ".csv": pd.read_csv,
        ".parquet": pd.read_parquet,
        ".json": pd.read_json,
        ".xlsx": pd.read_excel,
    }

    # 1.1. Initialize
    def __init__(self, direction: str) -> None:
        self.direction = direction

    # 1.2. Entrypoint
    def extract(self) -> pd.DataFrame:

        path = self.direction

        try:

            print(
                "🔍 [PLUGIN] Extracting local file from path "
                f"{path}..."
            )

            if not os.path.exists(path):

                raise FileNotFoundError(
                    f"❌ [PLUGIN] Failed to extract local file from path "
                    f"{path} due to file not found."
                )

            extension = os.path.splitext(path)[1].lower()

            reader = self.SUPPORTED_LOCAL_FORMATS.get(extension)

            if not reader:
                
                raise ValueError(
                    "❌ [PLUGIN] Failed to extract local file from path "
                    f"{path} due to extension "
                    f"{extension} is not one of supported formats "
                    f"{list(self.SUPPORTED_LOCAL_FORMATS.keys())}"
                )

            df = reader(path)

            print(
                "✅ [PLUGIN] Successfully extracted "
                f"{len(df)} row(s) from local file path "
                f"{path}."
            )

            return df

        except Exception as e:

            error = RuntimeError(
                "❌ [PLUGIN] Failed to extract local file from path "
                f"{path} due to "
                f"{e}."
            )
            
            raise error from e