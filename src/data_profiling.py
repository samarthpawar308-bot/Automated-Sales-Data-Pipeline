
import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

# Find all CSV files
csv_files = list(RAW_DIR.glob("*.csv"))

print("Total CSV files:", len(csv_files))

for file in csv_files:
    print("\n" + "=" * 60)
    print("FILE:", file.name)

    df = pd.read_csv(file)

    print("Rows and Columns:", df.shape)
    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:", df.duplicated().sum())
