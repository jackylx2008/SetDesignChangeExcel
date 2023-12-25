import csv
import os
from datetime import datetime

import INIT
from FileFolderSearch import FileSearch, FolderSearch, PatternMaker, Which_OS


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

    def __init__(self, root_folder: str, pattern_list: list):
        self._root_folder = root_folder
        self._pattern = pattern_list
        self._file_data = []

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
        for p in self._pattern:
            pattern = PatternMaker("biad", p).get_pattern()
            temp_path_list = INIT.BIAD_folder_obj.find_folders_with_pattern(pattern)
            for path in temp_path_list:
                creation_date = self._get_creation_date(path)
                self._file_data.append({"File": path, "Creation Date": creation_date})

    # Step 1: Create a csv to save history of dirs
    def save_to_csv(self, csv_filename):
        """
        Save the collected file data to a CSV file.

        Args:
            csv_filename (str): Filename for the CSV file.
        """
        keys = self._file_data[0].keys() if self._file_data else []
        with open(csv_filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self._file_data)


class FolderComparator:
    """
    A class to compare folders, retrieve their creation dates,
    and update data in a CSV file accordingly.

    Args:
        root_folder (str): The root folder path to start the comparison.
        csv_filename (str): Filename of the CSV file to load/store data.
        pattern_list (list): A list of patterns to identify folders.

    Attributes:
        _root_folder (str): The root folder path.
        _csv_filename (str): Filename of the CSV file.
        _pattern_list (list): A list of patterns for folder identification.
        _folder_data (dict): Dictionary to store folder data with creation dates.
        _new_folders (list): List to store paths of newly found folders.

    Methods:
        get_creation_date(folder_path): Retrieve creation date of a folder.
        load_csv(): Load existing folder data from a CSV file.
        update_csv(): Update the CSV file with new folder data.
        compare_folders(): Compare folders based on patterns and update data.
        get_new_folders(): Retrieve paths of newly found folders.
    """

    def __init__(self, root_folder, csv_filename, pattern_list: list):
        self._root_folder = root_folder
        self._pattern_list = pattern_list
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
        with open(self._csv_filename, "r") as csvfile:
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
        for p in self._pattern_list:
            pattern = PatternMaker("biad", p).get_pattern()
            temp_path_list = INIT.BIAD_folder_obj.find_folders_with_pattern(pattern)
            for path in temp_path_list:
                if path not in self._folder_data:
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
    root_folder_path = INIT.CNCC2_ROOT + "12 北京院-主体/415设计变更/"
    # Example usage:
    # file_info = InitFolderCreationDates(root_folder_path, INIT.pattern_biad_list)
    # file_info.iterate_folders()
    # file_info.save_to_csv("file_creation_dates.csv")

    # Example usage:
    csv_file_path = "./file_creation_dates.csv"

    folder_comparator = FolderComparator(
        root_folder_path, csv_file_path, INIT.pattern_biad_list
    )
    folder_comparator.compare_folders()
    new_folders_info = folder_comparator.get_new_folders()
    print(new_folders_info)
    folder_comparator.update_csv()
