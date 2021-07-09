import os
import sys
import time
import numpy as np
import pandas as pd

from pathlib import Path
from itertools import islice
from datetime import datetime

class ReZAnalyzer:
    def __init__(self):
        self.master_dir = 'D:\\'
        self.log_file = 'log.tsv'
        self.date = datetime.today().strftime('%Y-%m-%d')

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
            self.log_lines.append(f'[0] {item_path}, Size: {folder_sz}\n')


    def get_folder_sz(self, folder_path: str, folder_layer: int):
        log_lines = []
        size_status = 'Complete'

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

                    self.log_lines.append(f"[{folder_layer}] {folder_path}\{item}, Size: {new_folder_size}\n")
                    # print(self.log_lines)

        except PermissionError as permission_error:
            size_status = 'Calc-Incomplete: Permission Denied'
            back_slash = '\\'
            self.log_lines.append(f"[{folder_layer}] {folder_path}\{folder_path.split(back_slash)[-1]}, Size: [{size_status}]\n")
        except FileNotFoundError as file_nf_error:
            size_status = 'Calc-Incomplete: File Error'
            back_slash = '\\'
            self.log_lines.append(f"[{folder_layer}] {folder_path}\{folder_path.split(back_slash)[-1]}, Size: [{size_status}]\n")

        return folder_size


    def log_output(self):
        start = time.time()
        print("Writing into the log file...")

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f'{self.date}_{self.log_file}'), 'w+', encoding='utf-8') as file_ptr:
            for line in list(reversed(self.log_lines)):
                file_ptr.write(line)

        print(f'Log Time Spent: [{time.time() - start} seconds]')


    def ReZ_analyzer_driver(self):
        self.iterate_dir('', 1)
        self.log_output()


class ReZCompare:
    def __init__(self):
        self.log_file = 'log.tsv'
        self.date = datetime.today().strftime('%Y-%m-%d')

        self.curr_file_data = {}
        self.compare_file_data = {}
        self.compare_file_name = sys.argv[1]

        self.compare_result_file = 'results2.tsv'

    def read_logs(self, compare_layer=-1, compare_name=''):

        if compare_layer != -1:
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f'{self.date}_{self.log_file}'), 'r', encoding='utf-8') as file_ptr:
                log_lines = file_ptr.readlines()
                for line in log_lines:
                    if line.startswith(f'[{compare_layer}]') and line.find('Calc-Incomplete') == -1:
                        data = line.replace('\n', '').split(', Size: ')
                        self.curr_file_data[data[0]] = data[1]

            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), self.compare_file_name), 'r', encoding='utf-8') as file_ptr:
                log_lines = file_ptr.readlines()
                for line in log_lines:
                    if line.startswith(f'[{compare_layer}]') and line.find('Calc-Incomplete') == -1:
                        data = line.replace('\n', '').split(', Size: ')
                        self.compare_file_data[data[0]] = data[1]

            print(self.curr_file_data)
            print('\n')
            print(self.compare_file_data)

        elif len(compare_name) > 0 and compare_layer == -1:
            print('\nError: Compare layer must be specified if compare_name is defined.\n')
            sys.exit(0)

        elif len(compare_name) > 0:
            pass


    def compare_logs(self):
        compare_results = []

        for curr_file_key in self.curr_file_data:
            if self.compare_file_data.__contains__(curr_file_key):
                size_diff = int(self.curr_file_data[curr_file_key]) - int(self.compare_file_data[curr_file_key])
                compare_results.append(f'Folder {curr_file_key} has a size change of {size_diff} bytes.')
            else:
                compare_results.append(f'Folder with size {self.curr_file_data[curr_file_key]} has been created.')



        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), self.compare_result_file), 'w', encoding='utf-8') as file_ptr:
            for line in compare_results:
                print(line)
                file_ptr.write(f'{line}\n')


    def ReZ_compare_driver(self):
        self.a = 'a'
        self.compare_log()



if __name__ == '__main__':
    start_time = time.time()    

    # if len(sys.argv) <= 1:
    #     print('\nArguemtns needs to be provided while running the program.\nExample: py -3.7 <main.py> [option] <arg1> <arg2> ...')
    #     sys.exit(0)

    # if sys.argv[1] == '-ac' or sys.argv == '--analyze-compare':
    #     pass


    # analyzer = ReZAnalyzer()
    # analyzer.ReZ_analyzer_driver()

    comparator = ReZCompare()
    comparator.read_logs(compare_layer=0)
    comparator.compare_logs()


    print(f"Total Time Spent: [{time.time() - start_time} seconds]")
