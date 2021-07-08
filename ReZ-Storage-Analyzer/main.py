import os
import sys
import time
import numpy as np
import pandas as pd

from pathlib import Path
from itertools import islice

class ReZAnalyzer:
    def __init__(self):
        self.master_dir = 'D:\\'
        self.log_lines = []

    def record_size(self, dir_path: str, curr_dir: str):
        dir_list = os.listdir(self.master_dir)
        print(dir_list)

    def iterate_dir(self, curr_dir: str, dir_layer: int):
        if dir_layer == 1:
            curr_dir = self.master_dir

        dir_list = (directory for directory in os.listdir(curr_dir) if os.path.isdir(os.path.join(curr_dir, directory)) and directory.startswith('$') == False)

        for item in dir_list:
            item_path = os.path.join(curr_dir, item)

            folder_sz = self.get_folder_sz(item_path, 1)
            self.log_lines.append(f'Master Dir: {item_path}, Size: {folder_sz}\n')
            
            # if folder_sz == 0:
            #     continue

            # with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log.tsv'), 'a', encoding='utf-8') as file_ptr:
            #     file_ptr.write(f"{item_path}, Size: {folder_sz}\n")


    def get_folder_sz(self, folder_path: str, folder_layer: int):
        log_lines = []

        if os.path.isfile(folder_path):
            print('Only folder size can be calculated with the "get_folder_sz" function!"')
            sys.exit(0)

        folder_size = os.stat(folder_path).st_size

        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)

                if folder_layer <= 3:
                    print(f"[Layer {folder_layer}] Analyzing {item}...")

                if os.path.isfile(item_path):
                    folder_size += os.path.getsize(item_path)

                elif os.path.isdir(item_path):
                    new_folder_size = self.get_folder_sz(item_path, folder_layer + 1)
                    folder_size += new_folder_size

                    self.log_lines.append(f"{'-' * folder_layer}{item}, Size: {new_folder_size}\n")
                    # print(self.log_lines)

        except PermissionError as permission_error:
            pass
        except FileNotFoundError as file_nf_error:
            pass

        return folder_size

    def write_log_lines(self):
        start = time.time()
        print("Writing into the log file...")

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log.tsv'), 'w+', encoding='utf-8') as file_ptr:
            for line in list(reversed(self.log_lines)):
                file_ptr.write(line)

        print(f'Log Time Spent: [{time.time() - start} seconds]')


    def progress_bar(self, input, prefix="", suffix="", suffix_control=False, bar_length=50, file=sys.stdout):
        '''Light-weight progress bar (generator)

        :param input: list/range input to be iterated over
        :param prefix: prefix for the progress bar
        :param suffix: suffix for the progress bar
        :param suffix control: boolean to whether the suffix should be printed
        :param bar_length: the progress bar's length
        :param file: display/storage method
        '''

        count = len(input)
        def show(curr):
            filled_length = int(bar_length * curr / count)

            filled = filled_length * '#'
            unfilled = (bar_length - filled_length) * ' '

            if curr == count and suffix_control == True:
                file.write(f"{prefix}|{filled}{unfilled}| {curr}/{count} {suffix}\r")
            else:
                file.write(f"{prefix}|{filled}{unfilled}| {curr}/{count}\r")
            file.flush()

        show(0)
        for curr, val in enumerate(input):
            yield val
            show(curr + 1)
        file.write("\n")
        file.flush()


if __name__ == '__main__':
    start_time = time.time()

    analyzer = ReZAnalyzer()
    analyzer.iterate_dir('', 1)
    analyzer.write_log_lines()

    print(f"Total Time Spent: [{time.time() - start_time} seconds]")
