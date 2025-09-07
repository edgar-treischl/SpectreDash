# from shiny import App, Inputs, Outputs, Session, render, ui
import pandas as pd
from spectredash.getduck import duckdb_table
from shiny import reactive

# Shared reactive values
shared_first_choice = reactive.Value(None)
shared_second_choice = reactive.Value(None)


def filter_and_sort_versions(dataset_name: str) -> pd.DataFrame:
    """
    Fetches the 'pointers' table via duckdb_table(),
    filters for rows where 'table' == dataset_name,
    extracts and parses timestamps from the 'version' column,
    sorts by timestamp descending, and returns the resulting DataFrame.
    """
    df = duckdb_table(table="pointers")
    filtered_df = df[df["table"] == dataset_name].copy()

    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})"
    filtered_df["timestamp_str"] = filtered_df["version"].str.extract(pattern)

    filtered_df["timestamp_iso"] = filtered_df["timestamp_str"].str.replace(
        r"(\d{4}-\d{2}-\d{2}T)(\d{2})-(\d{2})-(\d{2})",
        lambda m: f"{m.group(1)}{m.group(2)}:{m.group(3)}:{m.group(4)}",
        regex=True,
    )

    filtered_df["timestamp"] = pd.to_datetime(
        filtered_df["timestamp_iso"], utc=True, errors="coerce"
    )
    filtered_df = filtered_df.dropna(subset=["timestamp"])
    filtered_df = filtered_df.sort_values("timestamp", ascending=False)

    return filtered_df


def datasets():
    df = duckdb_table(table="pointers")
    tables = df["table"].unique().tolist()
    return tables
