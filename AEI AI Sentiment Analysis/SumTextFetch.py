# Client Code fetching Summary and Text of Articles:
# 2024.07.02
# By Siling Song

import os
from DataScraper2 import MacroDataFetcher
import pandas as pd

# Path to directory:
directory_path = '/Users/LindaSong/Desktop/test 2'

def main():
    
    files = os.listdir(directory_path)

    # Filter only the files that end with .csv
    csv_files = [file for file in files if file.endswith('.csv')]
    csv_files = sorted(csv_files)

    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path)  
        all_metadata = []

        for index, row in df.iterrows():
            url = row[0]
            chrom_path = '/Users/LindaSong/Downloads/chromedriver-mac-arm64/chromedriver'
            metadatafetcher = MacroDataFetcher(chrom_path)
            meta_data = metadatafetcher.fetch_des_section(url)
            if meta_data:
                print(f"Obtained metadata successfully for {url}")
                all_metadata.append(meta_data)
            else:
                print(f"Failed to scrape {url}")

        if all_metadata:
            meta_data_df = pd.DataFrame(all_metadata)
            df = pd.concat([df, meta_data_df], axis=1)
            df.to_csv(f'/Users/LindaSong/Desktop/macroed/{file} macro.csv', index=False)
        else:
            print(f"No metadata collected for {file}")

if __name__ == "__main__":
    main()