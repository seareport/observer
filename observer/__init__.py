from __future__ import annotations

import importlib.metadata

import fastparquet  # noqa: F401=unused import

from .azclients import get_credential_aio
from .azclients import get_credential
from .azclients import get_obs_client
from .azclients import get_obs_fs
from .azclients import get_storage_options
from .ioc import get_ioc_metadata
from .ioc import get_ioc_parquet_file
from .ioc import read_ioc_df
from .ioc import scrape_ioc_station
from .ioc import write_ioc_df
from .settings import get_settings
from .settings import Settings

__version__ = importlib.metadata.version(__name__)


__all__: list[str] = [
    "get_credential_aio",
    "get_credential",
    "get_ioc_metadata",
    "get_ioc_parquet_file",
    "get_obs_client",
    "get_obs_fs",
    "get_settings",
    "get_storage_options",
    "read_ioc_df",
    "Settings",
    "scrape_ioc_station",
    "write_ioc_df",
    "__version__",
]
