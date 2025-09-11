# src/spectredash/duckdb_table.py
import duckdb
import pandas as pd
import os


def duckdb_table(table):
    """
    Fetch data from the DuckDB database.

    Args:
    - table (str): The name of the table.

    Returns:
    - pd.DataFrame: Data from the specified table.
    """
    db_path = os.path.join(os.getcwd(), "src", "sp3ctrapp", "data", "meta.duckdb")

    # Check if the database file exists
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")

    con = duckdb.connect(db_path, read_only=True)
    try:
        query = f"SELECT * FROM {table}"
        df = con.execute(query).fetchdf()
        if df.empty:
            print(f"Warning: Table '{table}' is empty.")
        return df
    except Exception as e:
        print(f"Error fetching data from table '{table}': {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        con.close()
