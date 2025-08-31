import pandas as pd
from great_tables import GT, md
import emoji
import os

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
    df['report_path'] = df['report_path'].apply(os.path.basename)

    # Fix datetime string format if needed (convert Txx-xx-xx to Txx:xx:xx)
    df['version'] = df['version'].str.replace(r'T(\d+)-(\d+)-(\d+)', r'T\1:\2:\3', regex=True)

    # Convert 'version' to datetime
    df['version'] = pd.to_datetime(df['version'])

    # Filter to keep only the latest version per 'table'
    df_latest = df.loc[df.groupby('table')['version'].idxmax()].copy()

    # Create markdown links using 'report_path' as link text
    df_latest['html_link'] = df_latest['report_path'].apply(
        lambda t: f"[{t}](https://gitlab.lrz.de/edgar-treischl/OddJob/-/tree/main/{t}/pointers?ref_type=heads)"
    )

    # Select and rename columns for display with emojis
    df_display = df_latest[['table', 'version', 'status', 'html_link', 'validated_by']].copy()
    df_display.columns = [
        f"{emoji.emojize(':bar_chart:')} Latest Run",
        f"{emoji.emojize(':compass:')} Version",
        f"{emoji.emojize(':check_mark_button:')} Status",
        f"{emoji.emojize(':link:')} Link",
        f"{emoji.emojize(':detective:')} Agent"
    ]

    # Build and style the great_tables GT table
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
        .fmt_markdown(columns=[f"{emoji.emojize(':link:')} Link"])  # render markdown links correctly
        .tab_source_note(
            source_note=md(
                f"{emoji.emojize(':top_hat:')} [Visit the OddJob Repository](https://gitlab.lrz.de/edgar-treischl/OddJob)"
            )
        )
    )

    return gt_table
