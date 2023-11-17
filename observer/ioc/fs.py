from __future__ import annotations

import logging
import typing as T

import azure.identity.aio
import fastparquet
import pandas as pd

from observer.azclients import get_obs_fs
from observer.azclients import get_storage_options
from observer.settings import get_settings


Credential: T.TypeAlias = azure.identity.aio.ChainedTokenCredential

logger = logging.getLogger(__name__)


def _get_metadata_uri() -> str:
    settings = get_settings()
    uri = f"az://{settings.container_name}/ioc/metadata.parquet"
    return uri


def _get_station_uri(ioc_code: str) -> str:
    settings = get_settings()
    uri = f"az://{settings.container_name}/ioc/{ioc_code}.parquet"
    return uri


def get_ioc_metadata(credential: Credential | None = None) -> pd.DataFrame:
    """
    Return the IOC metadata from Blob
    """
    settings = get_settings()
    storage_options = get_storage_options(credential=credential)
    df = pd.read_parquet(
        _get_metadata_uri(),
        storage_options=storage_options,
        engine=settings.engine,
    )
    return df


def write_ioc_df(
    *,
    df: pd.DataFrame,
    ioc_code: str | None = None,
    compression_level: int = 0,
    credential: Credential | None = None,
    **kwargs: dict[str, T.Any],
) -> None:
    logger.debug("%s: Starting upload", ioc_code)
    settings = get_settings()
    uri = _get_station_uri(ioc_code)
    storage_options = get_storage_options(credential=credential)
    if "year" not in df.columns:
        df = df.assign(year=df.index.year)
    df.to_parquet(
        uri,
        partition_cols=["year"],
        index=True,
        storage_options=storage_options,
        engine=settings.engine,
        compression={
            "_default": {
                "type": "zstd",
                "args": {"level": compression_level},
            },
        },
        **kwargs,
    )
    logger.info("%s: Finished upload", ioc_code)


def get_ioc_parquet_file(
    ioc_code: str,
    credential: Credential | None = None,
    **kwargs: dict[str, T.Any],
) -> fastparquet.ParquetFile:
    uri = _get_station_uri(ioc_code)
    fs = get_obs_fs(credential=credential)
    pf = fastparquet.ParquetFile(uri, fs=fs, **kwargs)
    return pf


def get_ioc_df(
    ioc_code: str,
    no_years: int = 2,
    credential: Credential | None = None,
    **kwargs: dict[str, T.Any],
) -> pd.DataFrame:
    pf = get_ioc_parquet_file(ioc_code=ioc_code, credential=credential, **kwargs)
    df = pf[-no_years:].to_pandas(columns=pf.columns)
    return df


def list_ioc_stations(
    credential: Credential | None = None,
) -> list[str]:
    fs = get_obs_fs(credential=credential)
    existing = [parquet.split("/")[-1].split(".")[0] for parquet in fs.ls("obs/ioc")]
    return existing
