
# from spectredash.getduck import duckdb_table
# from spectredash.tables import table_pointer

# pointer_name = "penguins"
# point_df = duckdb_table(table="pointers")


# table_pointer("penguins", "2025-08-20T13-52-15")


# meta_df = duckdb_table(table="columns", name=pointer_name)

#     # Filter pointer info
#     pointer_row = pointers_df[
#         (pointers_df["table"] == pointer_name) &
#         (pointers_df["version"] == date)
#     ].copy()

#     if pointer_row.empty:
#         raise ValueError(f"No pointer found for '{pointer_name}' on '{date}'")

#     # Prepare metadata table
#     meta_filtered = (
#         meta_df[
#             (meta_df["table"] == pointer_name) &
#             (meta_df["version"] == date)
#         ]
#         [["column_name", "label", "type", "levels", "description"]]
#         .rename(columns={"column_name": "column"})
#         .copy()
#     )

#     # Titles and notes
#     table_title = f"**Data:** {pointer_name}"
#     table_subtitle = (
#         f"{emoji.emojize(':package:')} **Build:** {pointer_row['version'].iloc[0]}<br>"
#         f"{emoji.emojize(':check_mark_button:')} **Validation:** {pointer_row['status'].iloc[0]}"
#     )
#     table_caption = f"{emoji.emojize(':detective:')} **Agent:** {pointer_row['validated_by'].iloc[0]}"

#     # Build the table using great_tables
#     gt_table = (
#         GT(meta_filtered)
#         .tab_header(title=md(table_title), subtitle=md(table_subtitle))
#         .cols_label(
#             column=md("**Column**"),
#             label=md("**Label**"),
#             type=md("**Type**"),
#             levels=md("**Levels**"),
#             description=md("**Description**")
#         )
#         .fmt_markdown(columns=meta_filtered.columns.tolist())
#         .tab_style(
#             style=style.text(size="22px", weight="500", align="left", color="#444444"),
#             locations=loc.title()
#         )
#         .tab_style(
#             style=style.text(size="18px", align="left"),
#             locations=loc.subtitle()
#         )
#         .tab_options(table_font_size=pct(110), table_width="650px")
#         .opt_table_font(font=google_font("IBM Plex Sans"))
#         .tab_source_note(source_note=md(table_caption))
#     )

#     return gt_table