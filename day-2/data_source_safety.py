"""Shared security boundaries for MDSP CSV loading and spreadsheet export."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd


ALLOWED_REMOTE_HOSTS = frozenset({"raw.githubusercontent.com"})
ENCODING_ATTEMPTS = ("utf-8", "utf-8-sig", "cp1252", "latin-1")
FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


class DataSourceSafetyError(RuntimeError):
    """Raised when a CSV source violates the workshop safety policy."""


def validate_remote_url(url: str) -> None:
    """Allow only direct HTTPS downloads from approved public dataset hosts."""
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise DataSourceSafetyError("Remote CSV sources must use HTTPS.")
    if parsed.username or parsed.password:
        raise DataSourceSafetyError("Credentials are not permitted in dataset URLs.")
    if parsed.hostname not in ALLOWED_REMOTE_HOSTS:
        approved = ", ".join(sorted(ALLOWED_REMOTE_HOSTS))
        raise DataSourceSafetyError(
            f"Remote host is not approved. Download the CSV locally or use: {approved}."
        )
    try:
        port = parsed.port
    except ValueError as exc:
        raise DataSourceSafetyError("The dataset URL contains an invalid port.") from exc
    if port not in (None, 443):
        raise DataSourceSafetyError("Remote CSV sources must use the standard HTTPS port.")
    if not parsed.path or parsed.path.endswith("/"):
        raise DataSourceSafetyError("Use a direct CSV file URL, not a directory URL.")


def _decode_csv_bytes(raw_bytes: bytes) -> str:
    for encoding in ENCODING_ATTEMPTS:
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise DataSourceSafetyError("The CSV could not be decoded with an approved encoding.")


def _fetch_remote_bytes(url: str, max_bytes: int, timeout_seconds: int) -> bytes:
    validate_remote_url(url)
    try:
        import requests
    except ImportError as exc:
        raise DataSourceSafetyError("Install the reviewed workshop requirements first.") from exc

    try:
        with requests.get(
            url,
            stream=True,
            timeout=(5, timeout_seconds),
            allow_redirects=False,
        ) as response:
            if 300 <= response.status_code < 400:
                raise DataSourceSafetyError("Remote redirects are not followed; use the final approved URL.")
            if response.status_code != 200:
                raise DataSourceSafetyError(
                    f"The remote source returned HTTP {response.status_code}."
                )
            content_length = response.headers.get("Content-Length")
            if content_length:
                try:
                    if int(content_length) > max_bytes:
                        raise DataSourceSafetyError("The remote CSV exceeds the byte limit.")
                except ValueError as exc:
                    raise DataSourceSafetyError("The remote Content-Length is invalid.") from exc
            if "text/html" in response.headers.get("Content-Type", "").lower():
                raise DataSourceSafetyError("The remote source returned HTML, not CSV data.")

            chunks = []
            total = 0
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                total += len(chunk)
                if total > max_bytes:
                    raise DataSourceSafetyError("The remote CSV exceeds the byte limit.")
                chunks.append(chunk)
    except DataSourceSafetyError:
        raise
    except requests.exceptions.RequestException as exc:
        raise DataSourceSafetyError("The remote CSV request failed safely.") from exc

    raw_bytes = b"".join(chunks)
    if not raw_bytes:
        raise DataSourceSafetyError("The remote CSV is empty.")
    return raw_bytes


def load_csv_safely(
    data_source: str,
    *,
    max_remote_mb: int = 100,
    max_local_mb: int = 500,
    timeout_seconds: int = 30,
) -> pd.DataFrame:
    """Load a bounded local CSV or an approved direct remote CSV."""
    if not data_source or not data_source.strip():
        raise DataSourceSafetyError("Set a local CSV path or an approved direct HTTPS URL.")

    parsed = urlparse(data_source)
    if parsed.scheme in ("http", "https"):
        raw_bytes = _fetch_remote_bytes(
            data_source,
            max_bytes=max_remote_mb * 1024 * 1024,
            timeout_seconds=timeout_seconds,
        )
    else:
        if parsed.scheme and "://" in data_source:
            raise DataSourceSafetyError(
                "Use a local filesystem path or an approved HTTPS URL."
            )
        try:
            path = Path(data_source).expanduser().resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise DataSourceSafetyError("The local CSV could not be found safely.") from exc
        if not path.is_file() or path.suffix.lower() != ".csv":
            raise DataSourceSafetyError("The local source must be an existing regular .csv file.")
        size = path.stat().st_size
        if size == 0 or size > max_local_mb * 1024 * 1024:
            raise DataSourceSafetyError("The local CSV is empty or exceeds the byte limit.")
        try:
            raw_bytes = path.read_bytes()
        except OSError as exc:
            raise DataSourceSafetyError("The local CSV could not be read safely.") from exc

    text = _decode_csv_bytes(raw_bytes)
    try:
        dataframe = pd.read_csv(StringIO(text), engine="python", on_bad_lines="error")
    except Exception as exc:
        raise DataSourceSafetyError("The CSV is malformed or could not be parsed safely.") from exc
    if dataframe.empty or len(dataframe.columns) == 0:
        raise DataSourceSafetyError("The CSV contains no data rows or columns.")
    return dataframe


def spreadsheet_safe_copy(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a copy whose string cells cannot be interpreted as formulas."""
    safe = dataframe.copy()
    for column in safe.columns:
        safe[column] = safe[column].map(
            lambda value: "'" + value
            if isinstance(value, str) and value.startswith(FORMULA_PREFIXES)
            else value
        )
    return safe
