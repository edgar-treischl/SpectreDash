import os
import pandas as pd
import emoji
from great_tables import GT, md, pct, google_font, style, loc
from spectredash.getduck import duckdb_table


def table_overview(df: pd.DataFrame) -> GT:
    """
    Generate a styled table overview of the latest runs per table with clickable links.

    Args:
        df (pd.DataFrame): Input dataframe containing columns
            - 'table': table name
            - 'version': datetime string (possibly malformed)
            - 'status': status string
            - 'report_path': path strings used to extract basename for link text
            - 'validated_by': agent or validator name

    Returns:
        GT: great_tables GT object representing the styled summary table
    """
    # Extract basename from 'report_path' to use as link text
    df["report_path"] = df["report_path"].apply(os.path.basename)

    # Fix datetime string format if needed (convert Txx-xx-xx to Txx:xx:xx)
    df["version"] = df["version"].str.replace(
        r"T(\d+)-(\d+)-(\d+)", r"T\1:\2:\3", regex=True
    )

    # Convert 'version' to datetime
    df["version"] = pd.to_datetime(df["version"])

    # Filter to keep only the latest version per 'table'
    df_latest = df.loc[df.groupby("table")["version"].idxmax()].copy()

    # Create markdown links using 'report_path' as link text
    df_latest["html_link"] = df_latest["report_path"].apply(
        lambda t: f"[{t}](https://gitlab.lrz.de/edgar-treischl/OddJob/-/tree/main/{t}/pointers?ref_type=heads)"
    )

    # Select and rename columns for display with emojis
    df_display = df_latest[
        ["table", "version", "status", "html_link", "validated_by"]
    ].copy()

    # deleted {emoji.emojize(':compass:')}
    df_display.columns = [
        "Table",
        "Version",
        "Status",
        f"{emoji.emojize(':link:')} Link",
        f"{emoji.emojize(':detective:')} Agent",
    ]

    # Build and style the great_tables GT table
    gt_table = (
        GT(df_display)
        .tab_header(title=md(f"{emoji.emojize(':man_running:')} Summary Last Run"))
        .fmt_datetime(
            columns=[f"{emoji.emojize(':compass:')} Version"], date_style="iso"
        )
        .cols_align("left", columns=df_display.columns.tolist())
        .opt_table_font(font=google_font("IBM Plex Sans"))
        .fmt_markdown(columns=[f"{emoji.emojize(':link:')} Link"])
    )

    return gt_table


def table_pointer(pointer_name="penguins", date="2025-08-20T13-52-15"):
    """
    Generate a formatted summary table of metadata for a specific dataset version.

    This function retrieves metadata and pointer information from DuckDB-backed tables,
    filters them by dataset name and version (timestamp), and returns a beautifully styled
    HTML-renderable table using the `great_tables` library.

    Args:
        pointer_name (str): The name of the dataset/pointer to query. Defaults to "penguins".
        date (str): The version timestamp to filter by (in ISO format, e.g. "2025-08-20T13-52-15").

    Returns:
        GT: A `great_tables.GT` table object containing the metadata summary with
        labels, types, descriptions, and validation information.

    Raises:
        ValueError: If no matching row is found in the pointers table for the provided
        dataset name and date.

    Example:
        >>> table = table_pointer("penguins", "2025-08-20T13-52-15")
        >>> table.show()  # In Jupyter or render in Shiny via .as_raw_html()
    """

    # Load data from DuckDB
    pointers_df = duckdb_table(table="pointers")
    meta_df = duckdb_table(table="columns")

    # Filter pointer info
    pointer_row = pointers_df[
        (pointers_df["table"] == pointer_name) & (pointers_df["version"] == date)
    ].copy()

    if pointer_row.empty:
        raise ValueError(f"No pointer found for '{pointer_name}' on '{date}'")

    # Prepare metadata table
    meta_filtered = (
        meta_df[(meta_df["table"] == pointer_name) & (meta_df["version"] == date)][
            ["column_name", "label", "type", "levels", "description"]
        ]
        .rename(columns={"column_name": "column"})
        .copy()
    )

    # Titles and notes
    table_title = f"**Data:** {pointer_name}"
    table_subtitle = (
        f"{emoji.emojize(':package:')} **Build:** {pointer_row['version'].iloc[0]}<br>"
        f"{emoji.emojize(':check_mark_button:')} **Validation:** {pointer_row['status'].iloc[0]}"
    )
    table_caption = f"{emoji.emojize(':detective:')} **Agent:** {pointer_row['validated_by'].iloc[0]}"

    # Build the table using great_tables
    gt_table = (
        GT(meta_filtered)
        .tab_header(title=md(table_title), subtitle=md(table_subtitle))
        .cols_label(
            column=md("**Column**"),
            label=md("**Label**"),
            type=md("**Type**"),
            levels=md("**Levels**"),
            description=md("**Description**"),
        )
        .fmt_markdown(columns=meta_filtered.columns.tolist())
        .tab_style(
            style=style.text(size="22px", weight="500", align="left", color="#444444"),
            locations=loc.title(),
        )
        .tab_style(
            style=style.text(size="18px", align="left"), locations=loc.subtitle()
        )
        .tab_options(table_width="100%", table_font_size=pct(110))
        .opt_table_font(font=google_font("IBM Plex Sans"))
        .tab_source_note(source_note=md(table_caption))
    )

    return gt_table
