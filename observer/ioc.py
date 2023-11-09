from __future__ import annotations

import typing as T

import azure.identity.aio
import fastparquet
import pandas as pd

from .azclients import get_obs_fs
from .azclients import get_storage_options
from .settings import get_settings


def _get_metadata_uri() -> str:
    settings = get_settings()
    uri = f"az://{settings.container_name}/ioc/metadata.parquet"
    return uri


def _get_station_uri(ioc_code: str) -> str:
    settings = get_settings()
    uri = f"az://{settings.container_name}/ioc/{ioc_code}.parquet"
    return uri


def get_ioc_metadata(credential: azure.identity.aio.ChainedTokenCredential | None = None) -> pd.DataFrame:
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
    df: pd.DataFrame,
    ioc_code: str,
    compression_level: int = 0,
    credential: azure.identity.aio.ChainedTokenCredential | None = None,
) -> None:
    settings = get_settings()
    uri = _get_station_uri(ioc_code)
    storage_options = get_storage_options(credential=credential)
    if "year" not in df.columns:
        df = df.assign(year=df.index.year)
    df.to_parquet(
        uri,
        partition_cols="year",
        # file_scheme="hive",
        index=True,
        storage_options=storage_options,
        engine=settings.engine,
        compression={
            "_default": {
                "type": "zstd",
                "args": {"level": compression_level},
            },
        },
    )


# def read_ioc_df(
#     ioc_code: str,
#     credential: azure.identity.aio.ChainedTokenCredential | None = None,
#     **kwargs: dict[str, T.Any],
# ) -> pd.DataFrame:
#     settings = get_settings()
#     storage_options = get_storage_options(credential=credential)
#     df = pd.read_parquet(
#         path=_get_station_uri(ioc_code),
#         storage_options=storage_options,
#         engine=settings.engine,
#         **kwargs,
#     )
#     return df


def get_ioc_parquet_file(
    ioc_code: str,
    credential: azure.identity.aio.ChainedTokenCredential | None = None,
    **kwargs: dict[str, T.Any],
) -> pd.DataFrame:
    uri = _get_station_uri(ioc_code)
    fs = get_obs_fs(credential=credential)
    pf = fastparquet.ParquetFile(uri, fs=fs, **kwargs)
    return pf


def read_ioc_df(
    ioc_code: str,
    no_years: int = 2,
    credential: azure.identity.aio.ChainedTokenCredential | None = None,
    **kwargs: dict[str, T.Any],
) -> pd.DataFrame:
    pf = get_ioc_parquet_file(ioc_code=ioc_code, credential=credential)
    df = pf[-no_years:].to_pandas(columns=pf.columns)
    return df
