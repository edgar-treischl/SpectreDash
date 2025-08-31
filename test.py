import pandas as pd
from great_tables import GT, md
import emoji
import os
from spectredash.duckdb_table import duckdb_table

# Example data - replace with your duckdb_table call
df = duckdb_table(table = "pointers")

df['report_path'] = df['report_path'].apply(os.path.basename)


df['version'] = df['version'].str.replace(r'T(\d+)-(\d+)-(\d+)', r'T\1:\2:\3', regex=True)
df['version'] = pd.to_datetime(df['version'])
df_latest = df.loc[df.groupby('table')['version'].idxmax()].copy()

df_latest['html_link'] = df_latest['report_path'].apply(
    lambda t: f"[{t}](https://gitlab.lrz.de/edgar-treischl/OddJob/-/tree/main/{t}/pointers?ref_type=heads)"
)

df_display = df_latest[['table', 'version', 'status', 'html_link', 'validated_by']].copy()
df_display.columns = [
    f"{emoji.emojize(':bar_chart:')} Latest Run",
    f"{emoji.emojize(':compass:')} Version",
    f"{emoji.emojize(':check_mark_button:')} Status",
    f"{emoji.emojize(':link:')} Link",
    f"{emoji.emojize(':detective:')} Agent"
]

gt_table = (
    GT(df_display)
    .tab_header(
        title=md(f"{emoji.emojize(':brain:')} Latest Run (According to OddJob)")
    )
    .fmt_datetime(
        columns=[f"{emoji.emojize(':compass:')} Version"],
        date_style="iso"
    )
    .cols_align("left", columns=df_display.columns.tolist())
    .fmt_markdown(columns=[f"{emoji.emojize(':link:')} Link"])  # <-- here
    .tab_source_note(
        source_note=md(
            f"{emoji.emojize(':top_hat:')} [Visit the OddJob Repository](https://gitlab.lrz.de/edgar-treischl/OddJob)"
        )
    )
)


gt_table
