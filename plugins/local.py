import os
import logging
import pandas as pd

class LocalExtractor:
    """
    Internal Local File Loader
    ---------
    Workflow:
        1. Detect file extension
        2. Map extension -> pandas reader
        3. Read file into DataFrame
        4. Raise ValueError if unsupported    
    ---
    Returns:
        DataFrame
    """

# 1.1 Supported formats
    SUPPORTED_FORMATS = {
        ".csv": pd.read_csv,
        ".parquet": pd.read_parquet,
        ".json": pd.read_json,
        ".xlsx": pd.read_excel,
    }

# 1.2 Initialize
    def __init__(self, direction: str) -> None:
        self.direction = direction


# 1.3 Entrypoint
    def fetch(self) -> pd.DataFrame:

        path = self.direction

        try:

            msg = (
                "🔍 [FETCH] Fetching local file from path "
                f"{path}."
            )
            print(msg)
            logging.info(msg)

            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"Local file not found: {path}"
                )

            ext = os.path.splitext(path)[1].lower()

            reader = self.SUPPORTED_FORMATS.get(ext)

            if not reader:
                raise ValueError(
                    "Unsupported file format "
                    f"{ext}. Supported formats: "
                    f"{list(self.SUPPORTED_FORMATS.keys())}"
                )

            df = reader(path)

            msg = (
                "✅ [FETCH] Successfully fetched "
                f"{len(df):,} row(s) from local file "
                f"{path}."
            )
            print(msg)
            logging.info(msg)

            return df

        except Exception as e:

            msg = (
                "❌ [FETCH] Failed to fetch local file from path "
                f"{path} due to error {e}."
            )
            print(msg)
            logging.exception(msg)

            raise