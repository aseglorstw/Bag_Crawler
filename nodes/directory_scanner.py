import pathlib
import os


class DirectoryScanner:
    def __init__(self):
        self.task_list = []

    def create_task_list(self, root_directory):
        self.find_bag_files(root_directory)
        return self.task_list

    def find_bag_files(self, directory):
        stop_suffixes = ["_loc", "params", "no_sensors"]
        items = os.listdir(directory)
        child_directories = [os.path.join(directory, item) for item in items if
                             os.path.isdir(os.path.join(directory, item)) and ".web_server" not in item]
        for child_directory in child_directories:
            self.find_bag_files(child_directory)
        for file in pathlib.Path(directory).iterdir():
            if file.is_file() and file.suffix == ".bag" and not any(suffix in file.stem for suffix in stop_suffixes):
                if not self.find_web_folder(directory, file.name):
                    self.task_list.append(os.path.join(directory, file.name))

    @staticmethod
    def input_check(root_directory):
        if not (os.path.exists(root_directory) and os.path.isdir(root_directory)):
            print("This directory doesn't exist.")
            return False
        return True

    @staticmethod
    def create_output_folder(path_to_bag_file):
        directory, bag_file_name = path_to_bag_file.rsplit('/', 1)
        web_folder = os.path.join(directory, f".web_server_{bag_file_name}")
        if not os.path.exists(web_folder):
            os.mkdir(web_folder)
        return web_folder

    @staticmethod
    def find_loc_file(path_to_bag_file):
        directory, bag_file_name = path_to_bag_file.rsplit('/', 1)
        for file in pathlib.Path(directory).iterdir():
            if bag_file_name.replace(".bag", "_loc.bag") in file.name:
                return os.path.join(directory, file.name)
        return None

    @staticmethod
    def find_web_folder(directory, path_to_bag_file):
        web_folder = os.path.join(directory, f".web_server_{path_to_bag_file}")
        return os.path.exists(web_folder) and os.path.isdir(web_folder)
