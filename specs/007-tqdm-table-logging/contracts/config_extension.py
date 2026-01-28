"""
Contract: VPGConfig Logging Extension

This file defines the logging-related fields to be added to VPGConfig.
"""

from pydantic import Field

# Fields to add to VPGConfig class:

LOGGING_FIELDS = {
    "progress_bar": Field(
        default=True,
        alias="progress-bar",
        description="Show TQDM progress bar during training",
    ),
    "table_log_freq": Field(
        default=0,
        ge=0,
        alias="table-log-freq",
        description="Log metrics table every N epochs (0 to disable)",
    ),
}

# CLI options to add to training scripts:

CLI_OPTIONS = """
@click.option(
    "--progress-bar/--no-progress-bar",
    default=True,
    help="Show TQDM progress bar during training.",
)
@click.option(
    "--table-log-freq",
    default=0,
    type=int,
    help="Log metrics table every N epochs (0 to disable).",
)
"""
