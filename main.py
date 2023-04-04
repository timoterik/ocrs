#  Copyright © 2022 - 2023, DCCTech. All Rights Reserved.
#  This copyright notice is the exclusive property of DCCTech and is hereby granted to users
#  for use of DCCTech's intellectual property.
#  Any reproduction, modification, distribution, or other use of DCCTech's intellectual property without prior written
#  consent is strictly prohibited.

import logging
import os
import time

# create logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to INFO
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler and set level to DEBUG
fh = logging.FileHandler('ocrs.log')
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to handlers
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

exit_file = "exit_file.txt"


def clean_folder(folder_path, inactive_days=30):
    """
    Recursively removes all files and sub-folders within the specified folder that are older than the specified
    number of days.
    """
    current_time = time.time()
    inactive_time = current_time - (inactive_days * 24 * 60 * 60)

    for root, dirs, files in os.walk(folder_path, topdown=True):
        for file in files:
            if file == exit_file:
                logger.info(f"{exit_file} file found! Shutting down program...")
                exit()  # shuts down the program
            file = check(root, file, inactive_time)
            if file:
                remove(file, False)
            else:
                logger.warning(f"unknown file: {file}")

        for dic in dirs:
            folder = check(root, dic, inactive_time)
            if dic:
                remove(folder)
            else:
                logger.warning(f"Unknown dictionary: {folder}")


def check(root, name, inactive_time):
    path = os.path.join(root, name)
    last_modified_time = os.path.getmtime(path)
    # Delete the file if it was last modified more than the specified number of days ago
    if last_modified_time < inactive_time:
        return path


def remove(path, isDir=True):
    try:
        if path is None:
            logger.warning("Path variable is None, cannot delete.")
        elif not os.path.exists(path):
            logger.warning(f"The folder/file {path} doesn't exist.")
        elif isDir:
            os.rmdir(path)
            logger.info(f"Removed directory {path}")
        else:
            os.remove(path)
            logger.info(f"Removed file {path}")
    except Exception as e:
        logger.error(f"Failed to delete {path}. Reason: {e}")


def get_args(prompt):
    while True:
        try:
            value = input(prompt)
            if value:
                return value
            else:
                raise ValueError
        except ValueError:
            logger.error("Invalid input. Please try again.")


def main():
    folders = []
    get_folders_cmd = "Enter a comma-separated list of folders to be cleaned: "
    folder_list = get_args(get_folders_cmd)
    logger.info(f"{get_folders_cmd}{folder_list}")
    folder_paths = folder_list.split(",")
    for folder_path in folder_paths:
        folder = folder_path.strip()
        get_number_of_days = f"Enter the number of days of inactivity after which files should be deleted for {folder}: "
        days = int(get_args(get_number_of_days))
        logger.info(f"{get_number_of_days}{days}")
        folders.append((folder, days))

    get_sleep_time = "Enter the number of seconds to sleep between cleaning operations: "
    sleep_time = int(get_args(get_sleep_time))
    logger.info(f"{get_sleep_time}{sleep_time} seconds")

    while True:
        for folder, days in folders:
            logger.debug(f"Clean {folder} folder by removing any sub-content that is older than {days} days.")
            clean_folder(folder, days)
            logger.debug(f"All contents of {folder} have been removed.")
        logger.debug("All specified folders have been cleaned.")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
