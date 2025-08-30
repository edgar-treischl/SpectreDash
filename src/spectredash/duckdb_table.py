# src/spectredash/duckdb_table.py
import duckdb
import pandas as pd
import os

def duckdb_table(table):
    """
    Fetch data from the DuckDB database.

    Args:
    - table (str): The name of the table to fetch.

    Returns:
    - pd.DataFrame: Data from the specified table.
    """
    db_path = os.path.join(os.getcwd(), "data", "meta.duckdb")  # Adjust path as needed
    con = duckdb.connect(db_path, read_only=True)
    try:
        query = f"SELECT * FROM {table}"
        return con.execute(query).fetchdf()  # Return data as pandas DataFrame
    finally:
        con.close()
