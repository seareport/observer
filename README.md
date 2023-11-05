# `observer`

`observer` is a library/application for:

- scraping observation data and storing them on Azure
- accessing the scraped data directly from Azure

Its main purpose is to support `seareport`.
The code may be open source but you won't find it useful since
you won't have access to the Azure Storage Accounts.

## Usage

You must define the following env variables (preferably using direnv):

- `export STORAGE_ACCOUNT=`
- `export CONTAINER_NAME=`

```python
import observer

# Parse IOC metadata
ioc = observer.get_ioc_metadata()

# Create a `pd.DataFrame` containing the last 2 years of a specific station:
acap2 = observer.read_ioc_df("acap2")

# Create a `pd.DataFrame` containing the last 5 years of a specific station:
acap = observer.read_ioc_df("acap", no_years=5)
```
