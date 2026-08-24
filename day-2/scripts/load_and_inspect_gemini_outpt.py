import pandas as pd
from pathlib import Path
import sys

DAY2_ROOT = Path(__file__).resolve().parents[1]
if str(DAY2_ROOT) not in sys.path:
    sys.path.insert(0, str(DAY2_ROOT))

from data_source_safety import DataSourceSafetyError, load_csv_safely, spreadsheet_safe_copy

# ==========================================
# CONFIGURATION: Change only the value below
# ==========================================
DATA_SOURCE = r"<LOCAL_PATH_OR_DIRECT_CSV_URL>"

def main():
    print("LOCAL REVIEW ONLY: Do not copy or upload this output to a GenAI system until the metadata has been reviewed and sanitized.\n")

    if not DATA_SOURCE or DATA_SOURCE == r"<LOCAL_PATH_OR_DIRECT_CSV_URL>":
        print("Error: Please provide a valid local path or URL in the DATA_SOURCE variable.")
        return

    try:
        mydata = load_csv_safely(DATA_SOURCE)
        
        if mydata.empty or mydata.shape[1] == 0:
            print("Error: The dataset contains no data or no columns.")
            return
            
    except DataSourceSafetyError as exc:
        print(f"Error loading dataset: {exc}")
        return

    # 1. Dataset Dimensions
    print(f"Dataset Dimensions: {mydata.shape[0]} rows, {mydata.shape[1]} columns\n")

    # 2. Numbered Column List
    print("Numbered Column List:")
    for i, col in enumerate(mydata.columns, 1):
        print(f"{i}. {col}")
    
    print("\nDataFrame Information:")
    mydata.info()

    # 3. Missing Data Summary
    print("\nMissing Data Summary:")
    missing_data = pd.DataFrame({
        'data_type': mydata.dtypes,
        'non_null_count': mydata.count(),
        'missing_count': mydata.isnull().sum(),
        'missing_percentage': (mydata.isnull().sum() / len(mydata) * 100).round(2),
        'unique_count': mydata.nunique()
    })
    print(missing_data)

    # 4. Duplicate Rows
    dup_count = mydata.duplicated().sum()
    print(f"\nDuplicate-row count: {dup_count}")
    print(f"Duplicate-row percentage: {(dup_count / len(mydata) * 100):.2f}%")

    # 5. Numerical Summary
    num_cols = mydata.select_dtypes(include=['number'])
    if not num_cols.empty:
        print("\nNumerical Summary:")
        print(num_cols.describe().loc[['count', 'mean', 'std', '25%', '50%', '75%']].round(2))
    else:
        print("\nNo numerical columns detected.")

    # 6. Categorical Summary
    cat_cols = mydata.select_dtypes(exclude=['number'])
    if not cat_cols.empty:
        print("\nCategorical Data Summary:")
        print(missing_data.loc[cat_cols.columns])

    # 7. Create Metadata Review File
    output_path = Path.cwd() / "LOCAL_ONLY_mdsp_metadata_review.csv"
    if output_path.exists():
        print(f"\nWarning: Replacing existing file at {output_path}")

    metadata_review = pd.DataFrame({
        'original_column': mydata.columns,
        'default_alias': [f"column_{i:03d}" for i in range(1, len(mydata.columns) + 1)],
        'data_type': mydata.dtypes.values,
        'non_null_count': mydata.count().values,
        'missing_count': mydata.isnull().sum().values,
        'missing_percentage': (mydata.isnull().sum() / len(mydata) * 100).round(2).values,
        'unique_count': mydata.nunique().values,
        'student_pii_decision': 'Unsure',
        'risk_type': '',
        'recommended_action': 'Review',
        'safe_to_share': 'No',
        'student_notes': ''
    })

    spreadsheet_safe_copy(metadata_review).to_csv(output_path, index=False)

    print(f"\n{'='*20}")
    print("NEXT MDSP STEP")
    print(f"{'='*20}")
    print("1. Open LOCAL_ONLY_mdsp_metadata_review.csv locally.")
    print("2. Review every original column name.")
    print("3. Identify direct identifiers, quasi-identifiers, sensitive attributes,")
    print("   confidential fields, and free-text fields.")
    print("4. Review or replace each default alias.")
    print("5. Select an appropriate recommended action.")
    print("6. Change safe_to_share to Yes only for metadata that is safe to disclose.")
    print("7. Do not upload this local review file to a GenAI system because it still")
    print("   contains the original column names.")
    print("8. Create a separate sanitized metadata file before prompting a GenAI model.")

if __name__ == "__main__":
    main()
