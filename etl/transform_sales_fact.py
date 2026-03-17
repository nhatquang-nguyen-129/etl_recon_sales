import sys
from pathlib import Path
ROOT_FOLDER_LOCATION = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_FOLDER_LOCATION))

import pandas as pd

def transform_sales_fact(
    *,
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Transform sales fact
    ---
    Principles:
        1. Rename columns (Vietnamese → standardized)
        2. Select required columns only
        3. Cast dtype
        4. Enforce non-nullable constraints
    ---
    Returns:
        pandas.DataFrame
    """

    print(
        "🔄 [TRANSFORM] Transforming sales fact with "
        f"{len(df):,} row(s)..."
    )

    if df.empty:
        
        print(
            "⚠️ [TRANSFORM] Empty sales fact then transformation will be suspended."
        )
        
        return df

    COLUMN_MAPPING = {
        "store_id": "Mã CH",
        "store_name": "Tên cửa hàng",
        "invoice_no": "Số HĐ",
        "transaction_date": "Ngày bán",
        "product_id": "Mã hàng",
        "product_name": "Tên hàng",
        "category_level_1": "Nhóm C1",
        "category_level_2": "Nhóm C2",
        "quantity": "Số lượng",
        "transaction_value": "Giá trị hóa đơn",
        "discount_value": "Giá trị giảm giá",
        "promotion_code": "Mã CTKM",
        "promotion_name": "Tên CTKM",
        "discount_type": "Loại CK",
        "promotion_type": "Loại KM",
    }


    DTYPE_MAPPING = {
        "store_id": "string",
        "store_name": "string",
        "invoice_no": "string",
        "transaction_date": "datetime64[ns]",
        "product_id": "string",
        "product_name": "string",
        "category_level_1": "string",
        "category_level_2": "string",
        "quantity": "Int64",
        "transaction_value": "float",
        "discount_value": "float",
        "promotion_code": "string",
        "promotion_name": "string",
        "discount_type": "string",
        "promotion_type": "string",
    }


    NON_NULLABLE_COLUMNS = [
        "store_id",
        "invoice_no",
        "transaction_date",
        "product_id",
        "quantity",
    ]

# Rename columns
    reverse_mapping = {
        v: k for k, v in COLUMN_MAPPING.items()
    }

    df = df.rename(columns=reverse_mapping)

# Keep only needed columns
    df = df[list(COLUMN_MAPPING.keys())]

# Cast dtype
    for col, dtype in DTYPE_MAPPING.items():

        try:
            
            if dtype.startswith("datetime"):
                df[col] = pd.to_datetime(
                    df[col],
                    errors="coerce"
                )
            
            else:
                df[col] = df[col].astype(dtype)

        
        except Exception as e:
            
            raise RuntimeError(
                f"❌ Failed to cast column {col} to {dtype}: {e}"
            )

# Enforce non-nullable
    for col in NON_NULLABLE_COLUMNS:

        if df[col].isna().any():
            raise ValueError(
                f"❌ [TRANSFORM] Column {col} contains NULL but is non-nullable."
            )

    print(
        "✅ [TRANSFORM] Successfully transformed sales fact with "
        f"{len(df):,} row(s)."
    )

    return df