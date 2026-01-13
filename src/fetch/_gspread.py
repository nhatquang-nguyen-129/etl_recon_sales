import os
import sys
import logging
import pandas as pd
from google.auth import default
import gspread
from src.fetch._base import BaseFetch
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../../"
        )
    )
)

class GSpreadFetch(BaseFetch):
    """
    Implementation of BaseFetch for Google Spreadsheets files
    ---------
    Workflow:
        1. Uses gspread API to fetch Google Spreadsheets files
        2. Raises ValueError if file format is unsupported or fetch fails
    ----------
    Parameters
        1. backend : str
            Must be 'local' for this class
        2. direction : str
            Path to the Google Spreadsheets file with spreadsheets.worksheet format
    """
# 1.1. Initialize
    def __init__(
        self,
        backend: str,
        direction: str,
    ):
        
        super().__init__(
            backend=backend,
            direction=direction,
        )

        creds, _ = default(scopes=[
            "https://www.googleapis.com/auth/spreadsheets.readonly"
        ])
        self.client = gspread.authorize(creds)

# 1.2. Entrypoint
    def _fetch(self) -> pd.DataFrame:

        try:
            spreadsheet_id, worksheet_name = self.direction.split(".", 1)
        except ValueError:
            raise ValueError(
                "❌ [FETCH] Failed to fetch Google Spreadsheets due to invalid gspread direction against expected format "
                "<spreadsheet_id>.<worksheet_name>."
            )

        try:
            msg = (
                "🔍 [FETCH] Fetching Google Spreadsheets "
                f"{spreadsheet_id}.{worksheet_name}..."
            )
            print(msg)
            logging.info(msg)

            spreadsheet = self.client.open_by_key(spreadsheet_id)
            worksheet = spreadsheet.worksheet(worksheet_name)

            records = worksheet.get_all_records()
            df = pd.DataFrame(records)

            msg = (
                "✅ [FETCH] Successfully fetched "
                f"{len(df):,} row(s) from Google Spreadsheets "
                f"{spreadsheet_id}.{worksheet_name}."
            )
            print(msg)
            logging.info(msg)

            return df

        except Exception as e:
            msg = (
                "❌ [FETCH] Failed to fetch Google Spreadsheets "
                f"{spreadsheet_id}.{worksheet_name} due to "
                f"{e}."
            )
            print(msg)
            logging.exception(msg)