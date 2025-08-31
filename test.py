# import os
# import pandas as pd

# # Assuming duckdb_table function is already defined
# from spectredash.getduck import duckdb_table

# # Hardcoded dataset and version (for testing purposes)
# ds = "penguins"  # Replace with actual dynamic dataset
# ver = "2025-08-20T13-52-15"  # Replace with actual dynamic version

# # Debugging: Print the selected dataset and version
# print(f"Selected dataset: {ds}, version: {ver}")

# if not ds or not ver:
#     print("No dataset or version selected.")
#     # Return early or raise an error as per your requirements
#     exit()

# try:
#     # Pull pointer data from duckdb
#     pointer_df = duckdb_table(table="pointers")
    
#     # Debugging: Print the pointer dataframe before any filtering
#     print(f"Pointer DataFrame before filtering:\n{pointer_df}")

#     # Filter the dataframe based on the dataset and version
#     pointer_df = pointer_df[pointer_df["table"] == ds]
#     pointer_df = pointer_df[pointer_df["version"] == ver]

#     # Debugging: Print the filtered pointer dataframe
#     print(f"Filtered pointer_df:\n{pointer_df}")

#     # Ensure pointer_df is not empty
#     if pointer_df.empty:
#         print(f"No matching report found for dataset '{ds}' and version '{ver}'.")
#         exit()  # Or handle the error as needed

#     # Get the report path from the first row
#     report_path = os.path.join("src", "spectredash", "data", pointer_df.iloc[0]["report_path"])

#     # Debugging: Print the constructed report path
#     print(f"Constructed report path: {report_path}")

#     # Check if the report file exists at the constructed path
#     if os.path.exists(report_path):
#         print(f"Report file found at {report_path}")
        
#         # Loading the content of the report
#         with open(report_path, "r", encoding="utf-8") as f:
#             content = f.read()

#         # Debugging: Print the first 500 characters of the content to confirm
#         print(f"Loaded report content (first 500 characters): {content[:500]}")

#     else:
#         print(f"Report file not found at: {report_path}")
#         exit()  # Or handle the error as needed

# except Exception as e:
#     print(f"Error occurred: {str(e)}")
#     exit()  # Or handle the error as needed
