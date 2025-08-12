import os
import pandas as pd

# Folder containing the CSV files
folder_path = r" "
output_file = os.path.join(folder_path, "merger_all_users.csv")

# List to store DataFrames
all_data = []

# Loop through and merge matching files
for filename in os.listdir(folder_path):
    if filename.startswith(" ") and filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path, header=None)  # No headers
        all_data.append(df)
        print(f"📥 Merged: {filename}")

# Combine all into one DataFrame
merged_df = pd.concat(all_data, ignore_index=True)

# Save the merged file (no headers)
merged_df.to_csv(output_file, index=False, header=False)
print(f"\n✅ Merged file saved as: {output_file}")
