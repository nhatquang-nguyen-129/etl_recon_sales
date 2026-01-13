import os
import sys
import logging
import pandas as pd
from src.fetch._local import LocalFetch
from src.fetch._gspread import GSpreadFetch
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../../"
        )
    )
)

class Fetch:
    """
    Orchestrator for fetching data from various backends
    ---------
    Workflow:
        1. Trigger fetch   : Logs and routes the request to the correct backend fetcher
        2. Validate config : Delegates validation to backend fetcher
        3. Retrieve data   : Delegates actual data fetching to backend fetcher
        4. Apply FetchQL   : WHERE, SELECT, AGGREGATE, ORDER BY, LIMIT, SAMPLE
    ----------
    Parameters:
        backend : str
            The type of backend to fetch data from (e.g., 'local', 'gspread')
        direction : str
            The source location or identifier, such as a file path or spreadsheet ID
    ----------
    Returns:
        pd.DataFrame
            The fetched DataFrame from the selected backend
    """

# 1.1. Initialize
    def __init__(
        self,
        backend: str,
        direction: str,
    ):
        
        self.backend = backend.lower()
        self.direction = direction

# 1.2. Entrypoint
    def fetch(
        self,
        config: dict | None = None,
    ) -> pd.DataFrame:

        msg = (
            "🔄 [FETCH] Triggering to fetch with backend "
            f"{self.backend.lower()} from direction "
            f"{self.direction}..."
        )
        print(msg)
        logging.info(msg)

        if self.backend == "local":
            fetcher = LocalFetch(
                backend=self.backend,
                direction=self.direction,
            )

        elif self.backend == "gspread":
            fetcher = GSpreadFetch(
                backend=self.backend,
                direction=self.direction,
            )

        else:
            raise ValueError(
                "❌ [FETCH] Failed to trigger fetch due to unsupported backend "
                f"{self.backend}."
            )

        return fetcher.fetch(config=config)