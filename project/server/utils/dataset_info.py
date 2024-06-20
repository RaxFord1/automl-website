import csv
import json
import logging
import os.path


def get_desc(dataset_full_path):
    try:
        file_path = os.path.join(dataset_full_path, "description.json")
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        logging.log(logging.ERROR, f"Exception: {e}")
        return {}


def get_description(dataset_name, datasets_path):
    file_path = os.path.join(datasets_path, dataset_name)
    return get_desc(file_path)


def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size


def get_few_file_names_from_each_category(dataset_path: str, max_amount: int = 5):
    category_files = {}
    for category in os.listdir(dataset_path):
        category_path = os.path.join(dataset_path, category)

        # Check if the item is a directory (category)
        if os.path.isdir(category_path):
            # List all files in the category directory
            files = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]

            selected_files = files[:max_amount]

            category_files[category] = selected_files

    return category_files


def get_csv_dimensions(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)

        num_rows = 0
        num_cols = 0

        for i, row in enumerate(reader):
            if i == 0:
                num_cols = len(row)
            num_rows += 1

        return num_cols, num_rows


def find_first_csv_file(folder_path: str):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            return file_name


def count_files_in_dir_total(path):
    files_count = 0
    for directory in os.listdir(path):
        dir_path = os.path.join(path, directory)
        files_count += len(
            [name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])

    return files_count


def count_files_in_dir_by_category(path):
    files_count = {}
    for directory in os.listdir(path):
        dir_path = os.path.join(path, directory)
        files_count[directory] = len(
            [name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])

    return files_count
