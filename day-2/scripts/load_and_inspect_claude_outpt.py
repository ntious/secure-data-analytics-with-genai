"""
MDSP Step 1: Load and Inspect a Dataset Locally
================================================

This script loads a CSV dataset (local path or direct public HTTP/HTTPS URL)
into a pandas DataFrame named `mydata`, inspects it locally without exposing
raw values, and produces a LOCAL-ONLY metadata review file for a student to
manually review and sanitize before any GenAI-assisted analysis.

IMPORTANT: The output file (LOCAL_ONLY_mdsp_metadata_review.csv) contains the
ORIGINAL column names and is NOT safe to upload to a GenAI system. It must be
reviewed and sanitized by a student before use in later MDSP steps.
"""

from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from typing import Any, Tuple
from urllib.parse import urlparse

import pandas as pd

DAY2_ROOT = Path(__file__).resolve().parents[1]
if str(DAY2_ROOT) not in sys.path:
    sys.path.insert(0, str(DAY2_ROOT))

from data_source_safety import spreadsheet_safe_copy, validate_remote_url

# ---------------------------------------------------------------------------
# Configuration - the student changes only this value.
# ---------------------------------------------------------------------------

DATA_SOURCE = r"<LOCAL_PATH_OR_DIRECT_CSV_URL>"

OUTPUT_FILE = Path.cwd() / "LOCAL_ONLY_mdsp_metadata_review.csv"

MAX_LOCAL_FILE_SIZE_MB = 500
REMOTE_TIMEOUT_SECONDS = 30
MAX_DOWNLOAD_SIZE_MB = 100
ENCODING_ATTEMPTS = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------

class DataSourceError(RuntimeError):
    """Raised when DATA_SOURCE cannot be safely located, downloaded, or parsed."""


def _sanitize_exception(exc: Exception) -> str:
    return f"{type(exc).__name__}: an error occurred while processing the data source."


# ---------------------------------------------------------------------------
# 1. Source detection and loading
# ---------------------------------------------------------------------------

def identify_source_type(data_source: str) -> str:
    """Classify DATA_SOURCE as 'remote_url' or 'local_path'."""
    if not data_source or not data_source.strip():
        raise DataSourceError("DATA_SOURCE is empty. Please set a local path or a direct CSV URL.")
    parsed = urlparse(data_source)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return "remote_url"
    return "local_path"


def _check_github_blob(url: str) -> None:
    parsed = urlparse(url)
    if parsed.netloc.lower() == "github.com" and "/blob/" in parsed.path:
        raise DataSourceError(
            "This looks like a GitHub file-view page, which normally returns an "
            "HTML page rather than CSV data. Open the file on GitHub, click "
            "'Raw', and copy that Raw URL into DATA_SOURCE instead."
        )


def _validate_remote_url(url: str) -> None:
    try:
        validate_remote_url(url)
    except RuntimeError as exc:
        raise DataSourceError(str(exc)) from exc


def _decode_bytes(raw_bytes: bytes) -> Tuple[str, str]:
    last_error: Exception | None = None
    for encoding in ENCODING_ATTEMPTS:
        try:
            return raw_bytes.decode(encoding), encoding
        except (UnicodeDecodeError, LookupError) as exc:
            last_error = exc
            continue
    raise DataSourceError(
        "The dataset could not be decoded using any of the approved encodings."
    ) from last_error


def _fetch_remote_csv_bytes(url: str) -> bytes:
    _validate_remote_url(url)
    try:
        import requests
    except ImportError as exc:
        raise DataSourceError(
            "The 'requests' library is required to load a remote CSV URL. "
            "Install it with: pip install requests"
        ) from exc

    max_bytes = MAX_DOWNLOAD_SIZE_MB * 1024 * 1024
    try:
        with requests.get(
            url,
            stream=True,
            timeout=(5, REMOTE_TIMEOUT_SECONDS),
            allow_redirects=False,
        ) as response:
            if 300 <= response.status_code < 400:
                raise DataSourceError(
                    "Remote redirects are not followed; use the final approved URL."
                )
            if response.status_code != 200:
                raise DataSourceError(
                    f"The remote source returned an unsuccessful HTTP status ({response.status_code})."
                )
            content_type = response.headers.get("Content-Type", "").lower()
            if "text/html" in content_type:
                raise DataSourceError("The remote source returned an HTML page instead of CSV content.")

            chunks = []
            total = 0
            checked_first_chunk = False
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                total += len(chunk)
                if total > max_bytes:
                    raise DataSourceError("The remote file exceeds the configured maximum download size.")
                if not checked_first_chunk:
                    lowered = chunk.lstrip()[:512].lower()
                    if lowered.startswith(b"<!doctype html") or b"<html" in lowered[:200]:
                        raise DataSourceError("The remote source content appears to be HTML, not CSV.")
                    checked_first_chunk = True
                chunks.append(chunk)
            data = b"".join(chunks)
            if len(data) == 0:
                raise DataSourceError("The remote source returned an empty response.")
            return data
    except requests.exceptions.Timeout as exc:
        raise DataSourceError("The remote request timed out.") from exc
    except requests.exceptions.ConnectionError as exc:
        raise DataSourceError("A connection error occurred while contacting the remote source.") from exc
    except requests.exceptions.RequestException as exc:
        raise DataSourceError(_sanitize_exception(exc)) from exc


def _validate_local_path(data_source: str) -> Path:
    try:
        path = Path(data_source).expanduser()
        resolved = path.resolve(strict=False)
    except Exception as exc:
        raise DataSourceError("The local path could not be parsed or resolved.") from exc

    if not resolved.exists():
        raise DataSourceError("The specified local file could not be found.")
    if not resolved.is_file():
        raise DataSourceError("The specified local path is not a regular file.")
    if resolved.suffix.lower() != ".csv":
        raise DataSourceError("The specified file does not have a .csv extension.")
    try:
        size = resolved.stat().st_size
    except OSError as exc:
        raise DataSourceError("The specified file could not be accessed.") from exc
    if size == 0:
        raise DataSourceError("The specified file is empty.")
    if size > MAX_LOCAL_FILE_SIZE_MB * 1024 * 1024:
        raise DataSourceError("The specified file exceeds the configured maximum local file size.")
    return resolved


def load_dataset(data_source: str) -> pd.DataFrame:
    """Determine source type, fetch, decode, and parse DATA_SOURCE into a DataFrame."""
    source_type = identify_source_type(data_source)

    if source_type == "remote_url":
        _validate_remote_url(data_source)
        raw_bytes = _fetch_remote_csv_bytes(data_source)
        text, _encoding = _decode_bytes(raw_bytes)
    else:
        resolved_path = _validate_local_path(data_source)
        try:
            raw_bytes = resolved_path.read_bytes()
        except PermissionError as exc:
            raise DataSourceError("The specified file could not be read due to a permissions error.") from exc
        except OSError as exc:
            raise DataSourceError("The specified file could not be read.") from exc
        text, _encoding = _decode_bytes(raw_bytes)

    try:
        dataframe = pd.read_csv(StringIO(text), engine="python", on_bad_lines="error")
    except pd.errors.EmptyDataError as exc:
        raise DataSourceError("The CSV source contains no parsable data.") from exc
    except pd.errors.ParserError as exc:
        raise DataSourceError("The CSV source is malformed and could not be parsed.") from exc
    except Exception as exc:
        raise DataSourceError(_sanitize_exception(exc)) from exc

    if len(dataframe.columns) == 0:
        raise DataSourceError("The dataset does not contain any columns.")
    if len(dataframe) == 0:
        raise DataSourceError("The dataset does not contain any data rows.")

    return dataframe


# ---------------------------------------------------------------------------
# 2. Local, privacy-safe dataset inspection (console output only)
# ---------------------------------------------------------------------------

def print_local_review_warning() -> None:
    print(
        "LOCAL REVIEW ONLY: Do not copy or upload this output to a GenAI system "
        "until the metadata has been reviewed and sanitized."
    )
    print()


def display_dataset_dimensions(mydata: pd.DataFrame) -> None:
    print("DATASET DIMENSIONS")
    print("-" * 40)
    print(f"Rows: {mydata.shape[0]}")
    print(f"Columns: {mydata.shape[1]}")
    print()


def display_numbered_column_list(mydata: pd.DataFrame) -> None:
    print("COLUMN LIST (for local review)")
    print("-" * 40)
    for index, column_name in enumerate(mydata.columns, start=1):
        print(f"{index}. {column_name}")
    print()


def display_dataframe_info(mydata: pd.DataFrame) -> None:
    print("DATAFRAME INFO")
    print("-" * 40)
    buffer = StringIO()
    mydata.info(buf=buffer)
    print(buffer.getvalue())


def _missing_summary_table(mydata: pd.DataFrame) -> pd.DataFrame:
    rows = []
    total_rows = len(mydata)
    for column_name in mydata.columns:
        series = mydata[column_name]
        non_null_count = int(series.notna().sum())
        missing_count = int(series.isna().sum())
        missing_pct = round(100.0 * missing_count / max(total_rows, 1), 2)
        unique_count = int(series.nunique(dropna=True))
        rows.append(
            {
                "original_column": column_name,
                "dtype": str(series.dtype),
                "non_null_count": non_null_count,
                "missing_count": missing_count,
                "missing_percentage": missing_pct,
                "unique_count": unique_count,
            }
        )
    return pd.DataFrame(rows)


def display_missing_data_summary(mydata: pd.DataFrame) -> pd.DataFrame:
    print("MISSING-DATA SUMMARY")
    print("-" * 40)
    summary = _missing_summary_table(mydata)
    print(summary.to_string(index=False))
    print()
    return summary


def display_duplicate_row_summary(mydata: pd.DataFrame) -> None:
    print("DUPLICATE-ROW SUMMARY")
    print("-" * 40)
    duplicate_count = int(mydata.duplicated().sum())
    duplicate_pct = round(100.0 * duplicate_count / max(len(mydata), 1), 2)
    print(f"Duplicate rows: {duplicate_count}")
    print(f"Duplicate-row percentage: {duplicate_pct}%")
    print()


def display_numerical_summary(mydata: pd.DataFrame) -> None:
    print("NUMERICAL SUMMARY (numeric columns only)")
    print("-" * 40)
    numeric_columns = mydata.select_dtypes(include="number").columns
    if len(numeric_columns) == 0:
        print("No numerical columns were found in this dataset.")
        print()
        return

    rows = []
    for column_name in numeric_columns:
        series = mydata[column_name].dropna()
        if len(series) == 0:
            rows.append(
                {
                    "column": column_name,
                    "count": 0,
                    "mean": None,
                    "std_dev": None,
                    "q25": None,
                    "median": None,
                    "q75": None,
                }
            )
            continue
        rows.append(
            {
                "column": column_name,
                "count": int(series.count()),
                "mean": round(float(series.mean()), 2),
                "std_dev": round(float(series.std(ddof=0)), 2),
                "q25": round(float(series.quantile(0.25)), 2),
                "median": round(float(series.median()), 2),
                "q75": round(float(series.quantile(0.75)), 2),
            }
        )
    summary_df = pd.DataFrame(rows)
    print(summary_df.to_string(index=False))
    print()


def display_categorical_summary(mydata: pd.DataFrame) -> None:
    print("CATEGORICAL-DATA SUMMARY (non-numerical columns only)")
    print("-" * 40)
    categorical_columns = mydata.select_dtypes(exclude="number").columns
    if len(categorical_columns) == 0:
        print("No non-numerical columns were found in this dataset.")
        print()
        return

    rows = []
    total_rows = len(mydata)
    for column_name in categorical_columns:
        series = mydata[column_name]
        non_null_count = int(series.notna().sum())
        missing_count = int(series.isna().sum())
        missing_pct = round(100.0 * missing_count / max(total_rows, 1), 2)
        unique_count = int(series.nunique(dropna=True))
        rows.append(
            {
                "column": column_name,
                "dtype": str(series.dtype),
                "non_null_count": non_null_count,
                "missing_count": missing_count,
                "missing_percentage": missing_pct,
                "unique_count": unique_count,
            }
        )
    summary_df = pd.DataFrame(rows)
    print(summary_df.to_string(index=False))
    print()


# ---------------------------------------------------------------------------
# 3. Local metadata-review file
# ---------------------------------------------------------------------------

def build_metadata_review(mydata: pd.DataFrame, missing_summary: pd.DataFrame) -> pd.DataFrame:
    """Build the LOCAL-ONLY metadata_review DataFrame (contains original names)."""
    rows = []
    for index, column_name in enumerate(mydata.columns, start=1):
        summary_row = missing_summary.loc[missing_summary["original_column"] == column_name].iloc[0]
        rows.append(
            {
                "original_column": column_name,
                "default_alias": f"column_{index:03d}",
                "data_type": summary_row["dtype"],
                "non_null_count": int(summary_row["non_null_count"]),
                "missing_count": int(summary_row["missing_count"]),
                "missing_percentage": float(summary_row["missing_percentage"]),
                "unique_count": int(summary_row["unique_count"]),
                "student_pii_decision": "Unsure",
                "risk_type": "",
                "recommended_action": "Review",
                "safe_to_share": "No",
                "student_notes": "",
            }
        )
    metadata_review = pd.DataFrame(
        rows,
        columns=[
            "original_column",
            "default_alias",
            "data_type",
            "non_null_count",
            "missing_count",
            "missing_percentage",
            "unique_count",
            "student_pii_decision",
            "risk_type",
            "recommended_action",
            "safe_to_share",
            "student_notes",
        ],
    )
    return metadata_review


def save_metadata_review(metadata_review: pd.DataFrame, output_file: Path) -> None:
    if output_file.exists():
        print(
            f"WARNING: '{output_file.name}' already exists in the current directory "
            "and will be overwritten."
        )
    try:
        spreadsheet_safe_copy(metadata_review).to_csv(
            output_file, index=False, encoding="utf-8"
        )
    except OSError as exc:
        raise DataSourceError("The local metadata review file could not be written.") from exc


def print_next_steps() -> None:
    print()
    print("NEXT MDSP STEP")
    print("-" * 40)
    print(
        "1. Open LOCAL_ONLY_mdsp_metadata_review.csv locally.\n"
        "2. Review every original column name.\n"
        "3. Identify direct identifiers, quasi-identifiers, sensitive attributes,\n"
        "   confidential fields, and free-text fields.\n"
        "4. Review or replace each default alias.\n"
        "5. Select an appropriate recommended action.\n"
        "6. Change safe_to_share to Yes only for metadata that is safe to disclose.\n"
        "7. Do not upload this local review file to a GenAI system because it still\n"
        "   contains the original column names.\n"
        "8. Create a separate sanitized metadata file before prompting a GenAI model."
    )


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------

def main() -> None:
    try:
        mydata = load_dataset(DATA_SOURCE)

        print_local_review_warning()
        display_dataset_dimensions(mydata)
        display_numbered_column_list(mydata)
        display_dataframe_info(mydata)
        missing_summary = display_missing_data_summary(mydata)
        display_duplicate_row_summary(mydata)
        display_numerical_summary(mydata)
        display_categorical_summary(mydata)

        metadata_review = build_metadata_review(mydata, missing_summary)
        save_metadata_review(metadata_review, OUTPUT_FILE)

        print(f"Local metadata review file saved to: {OUTPUT_FILE.name}")
        print_next_steps()

    except DataSourceError as exc:
        print(f"[FAILED] {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001 - final sanitized safety net
        print(f"[FAILED] {_sanitize_exception(exc)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
