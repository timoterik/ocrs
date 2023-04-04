# OCRS - Obsolete Content Removal System
OCRS is a command-line tool designed to remove obsolete content from specified folders by deleting files 
that are older than a specified time period. It is useful for ensuring that folders remain free of clutter 
and that valuable storage space is not occupied by obsolete files. 
This project allows users to enter a comma-separated list of folders to be cleaned, and will remove all files 
and folders (including sub-folders) that have not been modified within a specified number of days.

### Install OCRS
- Clone this repository to your local machine:
```sh
https://github.com/timoterik/ocrs.git
```
- Open a terminal and navigate to the project directory.
  - Run the main.py file to start the virtual assistant:
    ```sh
    python io.dcctech.ocrs/main.py
    ```
  - Enter a comma-separated list of folders to be cleaned when prompted. For example: folder1,folder2,folder3.
  - For each folder entered, you will be prompted to enter the number of days of inactivity after which files should be deleted.
  - Finally, you will be prompted to enter the number of seconds to sleep between cleaning operations.

The application will then start cleaning the specified folders and log the results in a file named ocrs.log found in
the same directory as the main script.
**To stop the application, you can press Ctrl + C or create an exit_file.txt file in any of the folders mentioned in 
the cleaning process** (it is sufficient to create it in just one of the folders). 
This file will trigger the application to stop running. The application will exit gracefully and log a message to the ocrs.log file.

## Notes
- If a file or folder cannot be deleted, the application will log an error message and continue with the cleaning process.
- The application will sleep for the specified number of seconds between each cleaning operation to prevent overwhelming the system with too many requests.
- <font color="red" >Be careful when using this tool as it will delete all files and folders that have not been modified within the specified number of days.</font>
