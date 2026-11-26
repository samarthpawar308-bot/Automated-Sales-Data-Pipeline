
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

PIPELINE_STEPS = [
    "data_cleaning.py",
    "data_validation.py",
    "business_transformation.py",
    "load_payments.py",
    "load_products.py",
    "load_product_data.py",
    "load_to_mysql.py"
]


def run_step(script_name):
    script_path = SRC_DIR / script_name

    print(f"\n{'=' * 60}")
    print(f"Running: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline failed at {script_name}. "
            f"Exit code: {result.returncode}"
        )

    print(f"Completed: {script_name}")


def main():
    print("Starting Olist ETL Pipeline...")

    try:
        for step in PIPELINE_STEPS:
            run_step(step)

        print("\nPipeline completed successfully!")

    except Exception as error:
        print(f"\nPipeline failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
