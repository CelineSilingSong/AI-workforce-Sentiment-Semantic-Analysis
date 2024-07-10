import os

def get_filenames(folder):
    return set(os.listdir(folder))

def process_filenames(filenames, remove_str):
    processed_filenames = set()
    for filename in filenames:
        if remove_str in filename:
            new_filename = filename.replace(remove_str, '').strip()
            processed_filenames.add(new_filename)
        else:
            processed_filenames.add(filename)
    return processed_filenames

def compare_folders(folder1, folder2, remove_str):
    # Get filenames from both folders
    folder1_filenames = get_filenames(folder1)
    folder2_filenames = get_filenames(folder2)
    
    # Process filenames from folder1
    processed_folder1_filenames = process_filenames(folder1_filenames, remove_str)
    
    # Find unique filenames
    unique_to_folder1 = processed_folder1_filenames - folder2_filenames
    unique_to_folder2 = folder2_filenames - processed_folder1_filenames
    
    return unique_to_folder1, unique_to_folder2

folder1 = '/Users/LindaSong/Desktop/macroed'
folder2 = '/Users/LindaSong/Desktop/test 2 Fr fetched'
remove_str = 'macro.csv'

unique_to_folder1, unique_to_folder2 = compare_folders(folder1, folder2, remove_str)

print("Files unique to folder1:")
for filename in unique_to_folder1:
    print(filename)

print("\nFiles unique to folder2:")
for filename in unique_to_folder2:
    print(filename)