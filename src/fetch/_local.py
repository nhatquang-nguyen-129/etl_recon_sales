import os
import sys
import logging
import pandas as pd
from src.fetch._base import BaseFetch
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../../"
        )
    )
)

class LocalFetch(BaseFetch):
    """
    Implementation of BaseFetch for local files
    ---------
    Workflow:
        1. Uses pd.read_(format) to fetch CSV, Parquet, JSON, and XLSX files
        2. Raises ValueError if file format is unsupported or fetch fails
    ----------
    Parameters
        1. backend : str
            Must be 'local' for this class
        2. direction : str
            Path to the local file (CSV, Parquet, JSON, XLSX)
    """

# 1.1. Entrypoint
    def _fetch(self) -> pd.DataFrame:

        try:
            path = self.direction

            msg = (
                "🔍 [FETCH] Fetching local file from path"
                f"{path}."
            )
            print(msg)
            logging.info(msg)   

            if path.lower().endswith(".csv"):
                df = pd.read_csv(path)

            elif path.lower().endswith(".parquet"):
                df = pd.read_parquet(path)

            elif path.lower().endswith(".json"):
                df = pd.read_json(path)

            elif path.lower().endswith(".xlsx"):
                df = pd.read_excel(path)

            else:
                raise ValueError(
                    "❌ [FETCH] Failed to fetch local file due to unsupported file format for path "
                    f"{path}."
                )

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
                f"{path} due to error "
                f"{e}."
            )
            print(msg)
            logging.exception(msg)