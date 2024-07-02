import os
import pandas as pd
from collections import defaultdict

def combine_files(directory):
    # Dictionary to store file paths grouped by xx-XX_XX_Year-month
    file_groups = defaultdict(list)
    
    # List all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            # Extract the xx-XX_XX_Year-month part of the filename
            parts = filename.split('_')
            if len(parts) == 3:
                group_key = f"{parts[0]}_{parts[1]}_{parts[2][:7]}"
                file_groups[group_key].append(os.path.join(directory, filename))
    
    # Combine files in each group
    for group_key, files in file_groups.items():
        combined_df = pd.DataFrame()
        for file in files:
            df = pd.read_csv(file)
            combined_df = pd.concat([combined_df, df])
        
        # Save the combined file
        combined_filename = f"/Users/LindaSong/Desktop/test 2 reorganized/{group_key}.csv"
        combined_filepath = os.path.join(directory, combined_filename)
        combined_df.to_csv(combined_filepath, index=False)
        print(f"Combined files for {group_key} into {combined_filename}")

# Usage
directory = '/Users/LindaSong/Desktop/test 2'
combine_files(directory)