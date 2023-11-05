from __future__ import annotations

from typing import Annotated

import typer

# from .cluster_app import cluster_app
# from .data_app import data_app
# from .model_app import model_app
# from .tools import SHOW_OUTPUT_OPTION
# from .tools import SHOW_TRACEBACK_OPTION
# from ..various import do_login
# from ..various import healthcheck as api_healthcheck


app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    rich_markup_mode="rich",
    help="Observer: Scrape and access observation data",
)
# app.add_typer(cluster_app, name="cluster")
# app.add_typer(data_app, name="data")
# app.add_typer(model_app, name="model")


@app.command()
def main(
    a: Annotated[str, typer.Option(help="This is option a")],
    # timeout: Annotated[int, typer.Option( help="The timeout countdown. If it expires, you probably haven't setup the managed identity correctly.")] = 5,
    # no_attempts: Annotated[int, typer.Option(help="How many times to retry to login")] = 3,
    # show_output: Annotated[bool, SHOW_OUTPUT_OPTION] = True,
    # show_traceback: Annotated[bool, SHOW_TRACEBACK_OPTION] = True,
) -> None:  ## fmt: skip
    """
    Login to [blue]azure-cli[/blue] and [blue]azcopy[/blue] using [italic]system-managed-identity[/italic].

    """
