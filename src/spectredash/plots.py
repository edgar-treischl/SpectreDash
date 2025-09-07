# ---- Imports ----
import re
import numpy as np
import pandas as pd
from textwrap import shorten

from plotnine import (
    ggplot,
    aes,
    geom_tile,
    geom_text,
    geom_point,
    geom_line,
    scale_fill_brewer,
    scale_fill_manual,
    scale_fill_gradient,
    scale_x_discrete,
    coord_cartesian,
    labs,
    theme_minimal,
    theme,
    element_text,
    element_blank,
)

from spectredash.getduck import duckdb_table


# ---- plot_PresenceMatrixWeb ----
def plot_PresenceMatrixWeb(table, skip=0, clip_date=False):
    # Step 1: Read column-level metadata in long format
    data = duckdb_table(table="columns")
    data = data[data["table"] == table]

    # Step 2: Ensure no duplicates
    data = data.drop_duplicates(subset=["version", "column_name"])

    # Step 3: Create full presence grid
    all_versions = data["version"].unique()
    all_columns = data["column_name"].unique()

    full_grid = pd.MultiIndex.from_product(
        [all_versions, all_columns], names=["version", "column_name"]
    ).to_frame(index=False)

    # Metadata for latest version and validator (not used in plot but included for parity)
    meta = duckdb_table(table="pointers")
    meta = meta[meta["table"] == table]
    latest_version = meta.sort_values("version", ascending=False).iloc[0]["version"]
    validator = meta.sort_values("version", ascending=False).iloc[0]["validated_by"]

    # Step 4: Join and compute presence
    data["found"] = True
    presence_data = pd.merge(
        full_grid,
        data[["version", "column_name", "found"]],
        on=["version", "column_name"],
        how="left",
    )
    presence_data["present"] = presence_data["found"].fillna(False)

    # Handle version filtering by `skip`
    if clip_date is not None:
        if not isinstance(skip, int):
            raise ValueError("Skip must be a numeric value.")
        unique_versions = data["version"].unique()
        max_skip = len(unique_versions) - 1
        if skip > max_skip:
            raise ValueError(
                f"Skip value is too large! Maximum skip can only be {max_skip}"
            )
        selected_versions = unique_versions[skip:]
        presence_data = presence_data[presence_data["version"].isin(selected_versions)]

    # Clip date if needed
    if clip_date:
        presence_data["version"] = presence_data["version"].str.replace(
            r"T.*", "", regex=True
        )

    # Sort factor levels for columns
    col_order = presence_data.sort_values("column_name", ascending=False)[
        "column_name"
    ].unique()
    presence_data["column_name"] = pd.Categorical(
        presence_data["column_name"], categories=col_order, ordered=True
    )

    # presence_data['version'] = presence_data['version'].apply(
    # lambda x: x[:13] + '...' if len(x) > 13 else x
    # )

    # --- Determine plot adjustments
    n_versions = presence_data["version"].nunique()
    x_label_angle = 45 if n_versions > 8 else 0
    base_font_size = 14 if n_versions > 12 else 16
    aspect = 0.6 if len(col_order) > 20 else 0.8

    # Step 5: Plot
    # plot = (
    #     ggplot(presence_data, aes(x="version", y="column_name", fill="present"))
    #     + geom_tile(color="white", alpha=0.9)
    #     + scale_fill_manual(
    #         values={True: "#31572c", False: "#d00000"},
    #         labels={True: "Yes", False: "No"},
    #         name="Present"
    #     )
    #     + labs(x="Version", y="Column")
    #     + theme_minimal(base_size=16)
    #     + theme(
    #         axis_text_x=element_text(size=14, angle=0, ha="center"),
    #         axis_text_y=element_text(size=14),
    #         aspect_ratio=0.8
    #     )
    #      + coord_cartesian(expand=True)
    # )
    # --- Plot
    plot = (
        ggplot(presence_data, aes(x="version", y="column_name", fill="present"))
        + geom_tile(color="white", alpha=0.9)
        + scale_fill_manual(
            values={True: "#31572c", False: "#d00000"},
            labels={True: "Yes", False: "No"},
            name="Present",
        )
        + labs(x="Version", y="Column")
        + theme_minimal(base_size=base_font_size)
        + theme(
            axis_text_x=element_text(
                size=base_font_size - 2, angle=x_label_angle, ha="center"
            ),
            axis_text_y=element_text(size=base_font_size - 2),
            legend_title=element_text(size=base_font_size),
            legend_text=element_text(size=base_font_size - 2),
            plot_title=element_text(size=base_font_size + 2, weight="bold"),
            legend_position="bottom",
            aspect_ratio=aspect,
        )
        + coord_cartesian(expand=True)
    )

    return plot


# ---- plot_TypeMatrixWeb ----
def plot_TypeMatrixWeb(table, skip=0, clip_date=False):
    # Step 1: Read column-level metadata in long format
    data = duckdb_table(table="columns")
    data = data[data["table"] == table]

    # Step 2: Ensure no duplicates
    data = data.drop_duplicates(subset=["version", "column_name", "type"])

    # Step 3: Create full presence grid
    all_versions = data["version"].unique()
    all_columns = data["column_name"].unique()

    full_grid = pd.MultiIndex.from_product(
        [all_versions, all_columns], names=["version", "column_name"]
    ).to_frame(index=False)

    # Metadata (used only for display or future use)
    meta = duckdb_table(table="pointers")
    meta = meta[meta["table"] == table]
    latest_version = meta.sort_values("version", ascending=False).iloc[0]["version"]
    validator = meta.sort_values("version", ascending=False).iloc[0]["validated_by"]

    # Step 4: Join grid with real data (type info)
    type_data = pd.merge(
        full_grid,
        data[["version", "column_name", "type"]],
        on=["version", "column_name"],
        how="left",
    )

    # Handle version skipping
    if clip_date is not None:
        if not isinstance(skip, int):
            raise ValueError("Skip must be a numeric value.")
        unique_versions = type_data["version"].unique()
        max_skip = len(unique_versions) - 1
        if skip > max_skip:
            raise ValueError(
                f"Skip value is too large! Maximum skip can only be {max_skip}"
            )
        selected_versions = unique_versions[skip:]
        type_data = type_data[type_data["version"].isin(selected_versions)]

    # Clip date from version string
    if clip_date:
        type_data["version"] = type_data["version"].str.replace(r"T.*", "", regex=True)

    # Ensure column_name is ordered descending for Y axis
    col_order = type_data.sort_values("column_name", ascending=False)[
        "column_name"
    ].unique()
    type_data["column_name"] = pd.Categorical(
        type_data["column_name"], categories=col_order, ordered=True
    )

    # Ensure type is categorical
    type_data["type"] = pd.Categorical(type_data["type"])

    # Plot
    plot = (
        ggplot(type_data, aes(x="version", y="column_name", fill="type"))
        + geom_tile(color="white", alpha=0.95)
        # + scale_fill_brewer(type='qual', palette='Accent', na_value="grey50", name="Type")
        # + scale_fill_viridis_d(name="Type", na_value="grey50")
        + scale_fill_manual(
            values={"factor": "#1f77b4", "integer": "#CCCCCC", "numeric": "#2ca02c"},
            na_value="#d62728",
            name="Type",
        )
        + labs(x="Version", y="Column")
        + theme_minimal(base_size=14)
        + theme(
            axis_text_x=element_text(size=14, angle=0, ha="center"),
            axis_text_y=element_text(size=14),
            legend_position="bottom",
            aspect_ratio=0.8,
        )
        + coord_cartesian(expand=True)
    )

    return plot


# ---- Helper ----
def truncate_text(s, maxlen=20):
    return s if len(s) <= maxlen else s[: maxlen - 1] + "…"


# ---- plot_LabelMatrix ----
def plot_LabelMatrix(table: str) -> ggplot:
    # Step 1: Load data
    data = duckdb_table(table="columns")
    data = data[data["table"] == table]

    # Step 2: Filter for factors and split levels into rows
    label_data = data[data["type"] == "factor"][
        ["version", "column_name", "levels"]
    ].copy()
    label_data = label_data.dropna(subset=["levels"])
    label_data["levels"] = label_data["levels"].str.split(r",\s*")
    label_data = label_data.explode("levels")

    # Step 3: Create label signature per (column, version)
    grouped = (
        label_data.groupby(["column_name", "version"])["levels"]
        .apply(lambda levels: "|".join(sorted(set(levels))))
        .reset_index(name="label_signature")
    )

    # Step 4: Detect changes across versions per column
    grouped = grouped.sort_values(["column_name", "version"])
    grouped["prev_signature"] = grouped.groupby("column_name")[
        "label_signature"
    ].shift()
    grouped["changed"] = grouped["label_signature"] != grouped["prev_signature"]
    grouped["changed"] = grouped["changed"].where(
        ~grouped["prev_signature"].isna(), False
    )

    # Step 5: Truncate label signatures for display (fix)
    grouped["label_short"] = grouped["label_signature"].apply(
        lambda s: truncate_text(s, 20)
    )

    # Step 6: Plot (fix scale_x_discrete too)
    plot = (
        ggplot(grouped, aes(x="version", y="column_name", fill="changed"))
        + geom_tile(color="white")
        + geom_text(aes(label="label_short"), size=10, color="white")
        + scale_fill_manual(
            values={True: "#d00000", False: "#31572c"},
            labels={True: "Changed", False: "No Change"},
            name="Changes",
        )
        + labs(x="Version", y="Column")
        + theme_minimal(base_size=14)
        + theme(
            axis_text_x=element_text(size=14, angle=0, ha="center"),
            axis_text_y=element_text(size=14),
            legend_position="bottom",
        )
        + scale_x_discrete(
            labels=lambda labels: [truncate_text(str(label), 14) for label in labels]
        )
    )

    return plot


def plot_pipe():
    # Read the table from duckdb
    data = duckdb_table(table="pipes")

    # Filter rows for the specified table
    # data = data[data["table"] == table]

    if not isinstance(data, pd.DataFrame):
        raise ValueError("The input is not a data frame.")

    # Expand columns so each row is one (column, validation_type) pair
    # Split the 'columns' column by comma + optional spaces
    data["cols"] = data["columns"].apply(lambda x: re.split(r",\s*", x))
    columns_expanded = data.explode("cols").reset_index(drop=True)

    # Create wide validation matrix
    distinct = (
        columns_expanded[["cols", "validation_type"]].drop_duplicates().assign(count=1)
    )

    validation_matrix = distinct.pivot(
        index="cols", columns="validation_type", values="count"
    )

    # Convert to long format
    validation_long = validation_matrix.reset_index().melt(
        id_vars="cols", var_name="validation_type", value_name="count"
    )

    # Shorten long column names for better visualization
    def shorten_label(x, max_len=9):
        if pd.isna(x):
            return x
        return x if len(x) <= max_len else x[:max_len] + "..."

    validation_long["cols_short"] = validation_long["cols"].apply(shorten_label)

    # Replace NA counts with 0 for plotting
    validation_long["count_plot"] = validation_long["count"].fillna(0)

    # Plot heatmap (points + lines)
    plot = (
        ggplot(
            validation_long, aes(x="validation_type", y="cols_short", fill="count_plot")
        )
        + geom_line(aes(group="cols_short"), size=0.5, color="lightgray")
        + geom_point(size=4, shape="o")
        + scale_fill_gradient(low="white", high="#31572c", na_value="white")
        + labs(x="Test", y="Column")
        + theme_minimal(base_size=14)
        + theme(
            legend_position="none",
            axis_text_x=element_text(angle=45, ha="center"),
            panel_grid=element_blank(),
        )
    )

    return plot
