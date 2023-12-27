import csv
import os
import sys
from datetime import datetime

sys.path.append(r"./FileFolderSearchZipCopy")
from FileFolderSearch import PatternMaker

import FileFolderSearchZipCopy.INIT as INIT


class InitFolderCreationDates:
    """
    A class to iterate through folders, retrieve their creation dates, and save the data to a CSV file.

    Args:
        root_folder (str): The root folder path to start the iteration.
        pattern_list (list): A list of patterns to identify folders.

    Attributes:
        _root_folder (str): The root folder path.
        _pattern (list): A list of patterns for folder identification.
        _file_data (list): List to store file data with creation dates.

    Methods:
        get_creation_date(file_path): Retrieve creation date of a file.
        iterate_folders(): Iterate through folders, retrieve creation dates, and store data.
        save_to_csv(csv_filename): Save the collected data to a CSV file.
    """

    def __init__(self, path_list: list):
        self._pattern = pattern_list
        self._file_data = []
        self._path_list = path_list

    def _get_creation_date(self, file_path):
        """
        Retrieve the creation date of a file.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Formatted creation date string.
        """
        creation_time = os.path.getctime(file_path)
        return datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")

    # Step 0: Get list of DesignChanges
    def iterate_folders(self):
        """
        Iterate through folders based on patterns, retrieve creation dates,
        and store the data in _file_data attribute.
        """
        for path in self._path_list:
            creation_date = self._get_creation_date(path)
            split_string = path.split(
                "CloudStation", 1
            )  # Split at the first occurrence

            result = split_string[1].lstrip()  # Removing leading spaces if any
            self._file_data.append({"File": result, "Creation Date": creation_date})

    # Step 1: Create a csv to save history of dirs
    def save_to_csv(self, csv_filename):
        """
        Save the collected file data to a CSV file.

        Args:
            csv_filename (str): Filename for the CSV file.
        """
        keys = self._file_data[0].keys() if self._file_data else []
        try:
            # Try opening the file in read mode
            with open(csv_filename, "r", encoding="utf-8") as file:
                # If the file exists, perform operations
                print(csv_filename + " is existed. Don't operate the file")

        except FileNotFoundError:
            # If the file doesn't exist, create it
            with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self._file_data)


class FolderComparator:
    def __init__(
        self,
        path_list: list,
        csv_filename: str,
    ):
        self.path_list = path_list
        self._csv_filename = csv_filename
        self._folder_data = self._load_csv() if os.path.exists(csv_filename) else {}
        self._new_folders = []

    def _get_creation_date(self, folder_path):
        """
        Retrieve the creation date of a folder.

        Args:
            folder_path (str): Path to the folder.

        Returns:
            str: Formatted creation date string.
        """
        creation_time = os.path.getctime(folder_path)
        return datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")

    def _load_csv(self):
        """
        Load existing folder data from a CSV file.

        Returns:
            dict: Folder data with creation dates.
        """
        folder_data = {}
        with open(self._csv_filename, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                folder_data[row[0]] = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        return folder_data

    def update_csv(self):
        """
        Update the CSV file with new folder data.
        """
        if self._new_folders:
            sorted_keys = sorted(self._folder_data.keys())
            with open(self._csv_filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Folder", "Creation Date"])
                for key in sorted_keys:
                    writer.writerow([key, self._folder_data[key]])

    def compare_folders(self):
        """
        Compare folders based on patterns and update data in _folder_data.
        """
        # print(self._folder_data)
        for path in []:
            path_last_name = path.split(r"/")[-1].split(r" ")[0]
            is_found_in_dict = any(
                path_last_name in key for key in self._folder_data.keys()
            )
            # print(path_last_name)
            if not is_found_in_dict:
                # if self._folder_data.get(path) is not None:
                print(path)
                creation_date = self._get_creation_date(path)
                self._new_folders.append(path)
                self._folder_data[path] = creation_date

    def get_new_folders(self):
        """
        Retrieve paths of newly found folders.

        Returns:
            list: Paths of newly found folders.
        """
        return self._new_folders


if __name__ == "__main__":
    # TODO: Make a func or class to do these
    root_folder_path = INIT.CNCC2_ROOT + "12 北京院-主体/415设计变更/"
    pattern_list = INIT.pattern_biad_list
    path_list_list = []
    path_list = []
    for pattern in pattern_list:
        pattern = PatternMaker("biad", pattern).get_pattern()
        path_list_list.append(INIT.BIAD_folder_obj.find_folders_with_pattern(pattern))
    for temp_path_list in path_list_list:
        for path in temp_path_list:
            path_list.append(path)

    root_folder_path = INIT.CNCC2_ROOT + "12 主体精装/主体精装变更/"
    pattern_list = INIT.pattern_decoration_list
    for pattern in pattern_list:
        pattern = PatternMaker("decoration", pattern).get_pattern()
        path_list_list.append(
            INIT.Decoration_folder_obj.find_folders_with_pattern(pattern)
        )
    for temp_path_list in path_list_list:
        for path in temp_path_list:
            path_list.append(path)

    for p in path_list:
        print(p)
    # Example usage:
    # file_info = InitFolderCreationDates(path_list)
    # file_info.iterate_folders()
    # file_info.save_to_csv("./csv_txt/file_creation_dates.csv")

    # Example usage:
    csv_file_path = "./csv_txt/file_creation_dates.csv"

    # new_folders_info = folder_comparator.get_new_folders()
    # print(new_folders_info)
    # folder_comparator.update_csv()
