# 🕵️ SpectreApp

**Spectre** silently infiltrates your data validation pipelines and turns raw audit logs into sleek, interactive visual intelligence.

This app is built with [`shiny`](https://shiny.posit.co/py/) for Python and wraps around validation metadata extracted from the `OddJob` repository. It provides a visual audit trail and dynamic data introspection.



## 🔍 In a Nutshell

- Extracts validation steps and metadata from a `DuckDB`-backed pipeline
- Visualizes:
  - The structure of validation flows (`Pipe`)
  - The validation results themselves (`Validation`)
  - The dataset’s variables and their types (`Variables`, `Classes`)
  - Associated labels (`Labels`)
  - The last Git Diff a given table (`Diff`)
- Enables version-aware exploration of datasets



## 🧩 Modules

Each section is modularized:

| Module       | Purpose                                                                 |
|--------------|-------------------------------------------------------------------------|
| `Overview`   | General metadata about your datasets and recent validation runs         |
| `Pipe`       | Shows which columns are validated and how                               |
| `Validation` | Displays the validation report                                          |
| `Variables`  | Lists columns and attributes                                            |
| `Classes`    | Highlights class-level (categorical) structures                         |
| `Labels`     | Shows label definitions and usage                                       |
| `Diff`       | Fetches the latest Git diff for tracking validation logic changes       |

