#  Copyright © 2022 - 2023, DCCTech. All Rights Reserved.
#  This copyright notice is the exclusive property of DCCTech and is hereby granted to users
#  for use of DCCTech's intellectual property.
#  Any reproduction, modification, distribution, or other use of DCCTech's intellectual property without prior written
#  consent is strictly prohibited.

import datetime
import logging
import os
import time


def clean_folder(folder_path, inactive_days=30):
    """
    Recursively removes all files and sub-folders within the specified folder that are older than the specified
    number of days.
    """
    current_time = time.time()
    inactive_time = current_time - (inactive_days * 24 * 60 * 60)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            print(f"{path}")

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file = check(root, file, inactive_time)
            if file:
                remove(file, False)
            else:
                print(f"clean_file: {file}")

        for dir in dirs:
            folder = check(root, dir, inactive_time)
            if dir:
                remove(folder)
            else:
                print(f"clean_folder: {folder}")


def check(root, name, inactive_time):
    path = os.path.join(root, name)
    last_modified_time = os.path.getmtime(path)
    # Delete the file if it was last modified more than the specified number of days ago
    if last_modified_time < inactive_time:
        return path
    else:
        print(f"Remove: {path}")


def remove(path, isDir=True):
    try:
        if not os.path.exists(path):
            log(f"The folder/file {path} doesn't exist.", logging.WARNING)
        if isDir:
            os.rmdir(path)
            log(f"Removed directory {path}")
        else:
            os.remove(path)
            log(f"Removed file {path}")
    except Exception as e:
        log(f"Failed to delete {path}. Reason: {e}", logging.ERROR)


def log(msg, level=logging.INFO):
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('ocrs.log'),
            logging.StreamHandler()
        ]
    )
    if level is logging.ERROR:
        logging.error(msg)
    else:
        logging.info(msg)


def get_args(prompt):
    while True:
        try:
            value = input(prompt)
            return value
        except ValueError:
            print("Invalid input. Please try again.")


def main():
    folders = []
    folder_list = get_args("Enter a comma-separated list of folders to be cleaned: ")
    folder_paths = folder_list.split(",")
    for folder_path in folder_paths:
        folder = folder_path.strip()
        days = int(
            get_args(f"Enter the number of days of inactivity after which files should be deleted for {folder}: "))
        folders.append((folder, days))

    sleep_time = int(get_args("Enter the number of seconds to sleep between cleaning operations: "))

    while True:
        for folder, days in folders:
            log(f"Clean {folder} folder by removing any sub-content that is older than {days} days.")
            clean_folder(folder, days)
            log(f"All contents of {folder} have been removed.")
        log("All specified folders have been cleaned.")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
