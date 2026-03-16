import logging
import pandas as pd
import gspread
from google.auth import default

class GoogleSheetExtractor:
    """
    Internal Google Sheets Loader
    ---
    Principles:
        1. Parse direction <spreadsheet_id>.<worksheet_name>
        2. Authenticate using Google default credentials
        3. Fetch worksheet data using gspread
        4. Convert records -> pandas DataFrame
    ---
    Returns:
        DataFrame
    """

    # 1.1 Initialize
    def __init__(self, direction: str):

        self.direction = direction

        creds, _ = default(
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly"
            ]
        )

        self.client = gspread.authorize(creds)


# 1.2 Entrypoint
    def fetch(self) -> pd.DataFrame:

        try:

            try:
                
                spreadsheet_id, worksheet_name = self.direction.split(".", 1)

            except ValueError:
                
                raise ValueError(
                    "❌ [FETCH] Failed to extract Invalid Google Sheets direction format "
                    f"{self.direction}. Expected <spreadsheet_id>.<worksheet_name>."
                )

            print(
                "🔍 [FETCH] Fetching Google Sheets "
                f"{spreadsheet_id}.{worksheet_name}..."
            )

            spreadsheet = self.client.open_by_key(spreadsheet_id)
            worksheet = spreadsheet.worksheet(worksheet_name)

            records = worksheet.get_all_records()

            df = pd.DataFrame(records)

            msg = (
                "✅ [FETCH] Successfully fetched "
                f"{len(df):,} row(s) from Google Sheets "
                f"{spreadsheet_id}.{worksheet_name}."
            )
            print(msg)
            logging.info(msg)

            return df

        except Exception as e:

            msg = (
                "❌ [FETCH] Failed to fetch Google Sheets "
                f"{self.direction} due to {e}."
            )
            print(msg)
            logging.exception(msg)

            raise