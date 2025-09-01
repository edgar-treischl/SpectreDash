import pandas as pd
from plotnine import (
    ggplot, aes, geom_tile, scale_fill_manual, labs, theme_minimal,
    theme, element_text, coord_cartesian
)

from spectredash.getduck import duckdb_table

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
        [all_versions, all_columns],
        names=["version", "column_name"]
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
        how="left"
    )
    presence_data["present"] = presence_data["found"].fillna(False)

    # Handle version filtering by `skip`
    if clip_date is not None:
        if not isinstance(skip, int):
            raise ValueError("Skip must be a numeric value.")
        unique_versions = data["version"].unique()
        max_skip = len(unique_versions) - 1
        if skip > max_skip:
            raise ValueError(f"Skip value is too large! Maximum skip can only be {max_skip}")
        selected_versions = unique_versions[skip:]
        presence_data = presence_data[presence_data["version"].isin(selected_versions)]

    # Clip date if needed
    if clip_date:
        presence_data["version"] = presence_data["version"].str.replace(r"T.*", "", regex=True)

    # Sort factor levels for columns
    col_order = presence_data.sort_values("column_name", ascending=False)["column_name"].unique()
    presence_data["column_name"] = pd.Categorical(presence_data["column_name"], categories=col_order, ordered=True)

    # Step 5: Plot
    plot = (
        ggplot(presence_data, aes(x="version", y="column_name", fill="present"))
        + geom_tile(color="white", alpha=0.9)
        + scale_fill_manual(
            values={True: "#31572c", False: "#d00000"},
            labels={True: "Yes", False: "No"},
            name="Present"
        )
        + labs(x="Version", y="Column")
        + theme_minimal(base_size=16)
        + theme(
            axis_text_x=element_text(size=14, angle=45, ha="right"),
            axis_text_y=element_text(size=14),
            aspect_ratio=0.8
        )
         + coord_cartesian(expand=True)
    )

    return plot
