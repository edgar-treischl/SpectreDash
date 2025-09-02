import os
import gitlab
import pandas as pd
from datetime import datetime
import warnings
from dotenv import load_dotenv
import logging
import html
import webbrowser
import tempfile
from typing import List

# Suppress verbose HTTP logs in console (especially for Shiny apps)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("gitlab").setLevel(logging.WARNING)



def connect_gitlab():
    """
    Establish a connection to the GitLab API using a personal access token.

    This function loads the GitLab token from a `.env` file (environment variable `GITLAB_API_TOKEN`)
    and returns an authenticated `gitlab.Gitlab` client object.

    Raises:
        RuntimeError: If the token is missing or authentication fails.

    Returns:
        gitlab.Gitlab: An authenticated GitLab client instance.
    """

    load_dotenv()  # Load token from .env
    token = os.getenv("GITLAB_API_TOKEN")
    if not token:
        raise RuntimeError("GITLAB_API_TOKEN is not set in the environment")

    try:
        gl = gitlab.Gitlab(
            url="https://gitlab.lrz.de",
            private_token=token,
            api_version=4,
        )
        gl.auth()  # Will raise if token is invalid
        return gl
    except gitlab.exceptions.GitlabAuthenticationError as e:
        raise RuntimeError(f"GitLab authentication failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Could not connect to GitLab: {e}")



def get_diff(table="penguins"):
    """
    Retrieve the latest Git diff for a specific YAML file in the GitLab repository.

    This function connects to GitLab, filters commits affecting the file 
    `{table}/pipe_{table}.yml`, and returns the diff from the latest matching commit.

    The function expects commits with messages in the format:
    `spectre a/m pipe_<table>.yml`.

    Args:
        table (str): The name of the table/file to check. Defaults to "penguins".

    Returns:
        list[str]: A list of lines in the diff output.

    Raises:
        RuntimeError: If the connection, commit retrieval, or diff operation fails.
        UserWarning: If no matching commits or diffs are found.
    """

    # Compose file path and expected commit message pattern
    oddjob_path = f"{table}/pipe_{table}.yml"
    commit_message = f"spectre a/m pipe_{table}.yml"
    project_id = "216273"

    # Load .env file
    load_dotenv()

    # Connect securely using your dedicated function
    gl = connect_gitlab()

    try:
        # Load project
        project = gl.projects.get(project_id)

        # Use direct HTTP call to get commits filtered by file path
        endpoint = f"/projects/{project_id}/repository/commits"
        commits_raw = gl.http_get(endpoint, query={"path": oddjob_path, "per_page": 100})

        # Wrap raw responses into GitLab commit objects (optional but nice)
        commits = [project.commits.get(c["id"]) for c in commits_raw]
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve commits: {e}")

    if not commits:
        warnings.warn(f"No commits found for file '{oddjob_path}'")
        return []

    # Create a DataFrame for filtering
    data = [{
        "id": c.id,
        "message": c.message,
        "authored_date": datetime.strptime(c.authored_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    } for c in commits]

    df = pd.DataFrame(data)

    # Filter by the exact commit message
    filtered = df[df["message"] == commit_message].sort_values(by="authored_date", ascending=False)

    if filtered.empty:
        warnings.warn(f"No commits found with message '{commit_message}'")
        return []

    latest_commit_id = filtered.iloc[0]["id"]

    # Get diff for the latest commit
    try:
        diff = project.commits.get(latest_commit_id).diff()
    except Exception as e:
        raise RuntimeError(f"Failed to get diff for commit {latest_commit_id}: {e}")

    # Look for the specific file in the diff
    for file_diff in diff:
        if file_diff.get("new_path") == oddjob_path or file_diff.get("old_path") == oddjob_path:
            diff_text = file_diff.get("diff", "")
            return diff_text.splitlines()

    warnings.warn(f"No diff found for file '{oddjob_path}' in commit '{latest_commit_id}'")
    return []





def visualize_diff(diff: List[str], browse: bool = True) -> str:
    """
    Generate a syntax-highlighted HTML visualization of a Git diff.

    This function takes a line-by-line Git diff (as a list of strings) and renders it 
    into formatted HTML, including line numbers, color-coded changes (additions, removals, context),
    and basic styling for readability. It is useful for embedding diffs in dashboards, reports,
    or web-based applications like Shiny for Python.

    Args:
        diff (List[str]): A list of lines from a Git diff (e.g., output from `commit.diff()`).
        browse (bool): If True, attempts to render and preview the HTML in a browser.
                       If False, returns the raw HTML string for embedding. Defaults to True.

    Returns:
        str: A complete HTML string representing the formatted diff.

    Notes:
        - Additions are highlighted in green, deletions in red (with strikethrough),
          and unchanged lines in grey.
        - Chunk headers (`@@ -old,+new @@`) are styled separately.
        - Designed for embedding in `<div>` or rendering with `htmltools.HTML()` in Shiny apps.

    Example:
        >>> html_str = visualize_diff(["@@ -1,3 +1,3 @@", "-old line", "+new line"], browse=False)
        >>> print(html_str)
    """
    html_diff_lines = []

    old_line_num = 0
    new_line_num = 0

    for line in diff:
        if line.startswith("@@"):
            import re
            match = re.match(r"^@@ -(\d+),\d+ \+(\d+),\d+ @@", line)
            if match:
                old_line_num = int(match.group(1)) - 1
                new_line_num = int(match.group(2)) - 1

            html_diff_lines.append(
                f"<div class='diff-chunk-header' style='color: #999; font-style: italic;'>{html.escape(line)}</div>"
            )
            continue

        first_char = line[0] if line else ' '
        content = html.escape(line[1:] if len(line) > 1 else '')

        if first_char == "+":
            new_line_num += 1
            old_num_display = "&nbsp;"
            new_num_display = f"{new_line_num:4d}"
            line_html = (
                f"<span class='line-num old-line'>&nbsp;</span>"
                f"<span class='line-num new-line'>{new_num_display}</span> "
                f"<span class='added'>+ {content}</span>"
            )
        elif first_char == "-":
            old_line_num += 1
            old_num_display = f"{old_line_num:4d}"
            new_num_display = "&nbsp;"
            line_html = (
                f"<span class='line-num old-line'>{old_num_display}</span>"
                f"<span class='line-num new-line'>&nbsp;</span> "
                f"<span class='removed'>- {content}</span>"
            )
        else:
            old_line_num += 1
            new_line_num += 1
            old_num_display = f"{old_line_num:4d}"
            new_num_display = f"{new_line_num:4d}"
            line_html = (
                f"<span class='line-num old-line'>{old_num_display}</span>"
                f"<span class='line-num new-line'>{new_num_display}</span> "
                f"<span class='context'>  {html.escape(line)}</span>"
            )

        html_diff_lines.append(line_html)

    # Wrap in <pre><code>
    final_html = (
        "<pre><code>"
        + "\n".join(html_diff_lines)
        + "</code></pre>"
    )

    # CSS styling
    custom_css = """
    <style>
      pre {
        background-color: #f7f7f7;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
        overflow-x: auto;
        font-family: 'Courier New', monospace;
        font-size: 14px;
      }
      .line-num {
        display: inline-block;
        width: 3em;
        text-align: right;
        padding-right: 1em;
        color: #999;
        user-select: none;
      }
      .old-line {
        color: #999;
      }
      .new-line {
        color: #999;
      }
      .added {
        color: green;
      }
      .removed {
        color: red;
        text-decoration: line-through;
      }
      .context {
        color: #444;
      }
      .diff-chunk-header {
        margin-top: 1em;
      }
    </style>
    """

    html_full = custom_css + final_html

    if browse:
        # Write to a temp HTML file and open in browser
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as f:
            f.write(html_full)
            webbrowser.open("file://" + f.name)

    return html_full
