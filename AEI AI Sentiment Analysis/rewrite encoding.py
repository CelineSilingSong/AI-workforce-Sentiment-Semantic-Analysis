

import pandas as pd
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(1000000)  # Read up to 1,000,000 bytes
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        return encoding, confidence

file_path = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/AEI AI Sentiment Analysis/AI Job To Fetch Meta 2020 Jan/AI_Job2020-01-09 copy 1.csv'
encoding, confidence = detect_encoding(file_path)
print(f"Detected encoding: {encoding} (confidence: {confidence * 100:.2f}%)")

try:
    # Open the file with the detected encoding and read the contents
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        file_content = f.read()

    # Write the content to a temporary file with utf-8 encoding
    temp_file_path = 'temp_file.csv'
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)

    # Read the temporary file into a pandas DataFrame
    df = pd.read_csv(temp_file_path)

    # Save the DataFrame to a new CSV file with utf-8 encoding
    output_path = '/Users/LindaSong/Desktop/AI-workforce-Sentiment-Semantic-Analysis/AEI AI Sentiment Analysis/AI Job To Fetch Meta 2020 Jan/AI_Job2020-01-09 copy 2.csv'
    df.to_csv(output_path, encoding='utf-8', index=False)
    df_2 = pd.read_csv(output_path)
    print(df_2)

    print(f"File has been re-encoded to UTF-8 and saved as {output_path}")
except Exception as e:
    print(f"An error occurred: {e}")