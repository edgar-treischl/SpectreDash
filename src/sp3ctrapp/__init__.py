# src/sp3ctrapp/__init__.py

# Expose commonly used elements for easy access
from .getduck import duckdb_table  # Expose the DuckDB function
from .moduleAbout import about_ui, about_server
from .moduleOverview import overview_ui, overview_server
from .moduleValidation import validation_ui, validation_server
from .moduleVariables import variables_ui, variables_server
from .moduleClass import class_ui, class_server
from .moduleLabels import labels_ui, labels_server
from .modulePipe import pipe_ui, pipe_server
from .getgit import get_diff, visualize_diff


from .tables import table_overview, table_pointer
from .plots import plot_PresenceMatrixWeb, plot_TypeMatrixWeb, plot_LabelMatrix

from .utils import filter_and_sort_versions, datasets
from .utils import shared_first_choice, shared_second_choice


__all__ = [
    "duckdb_table",
    "about_ui", "about_server",
    "overview_ui", "overview_server",
    "validation_ui", "validation_server",
    "variables_ui", "variables_server",
    "class_ui", "class_server",
    "labels_ui", "labels_server",
    "pipe_ui", "pipe_server",
    "get_diff", "visualize_diff",
    "table_overview", "table_pointer",
    "plot_PresenceMatrixWeb", "plot_TypeMatrixWeb", "plot_LabelMatrix",
    "filter_and_sort_versions", "datasets",
    "shared_first_choice", "shared_second_choice",
]