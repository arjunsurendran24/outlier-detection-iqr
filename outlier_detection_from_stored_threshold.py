import argparse
import glob
import numpy as np
import os
import pandas as pd
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-folder", type=str, help="Path to the folder containing data")
    parser.add_argument("--low-threshold-file", type=str, help="Path to threshold for lower quantile")
    parser.add_argument("--high-threshold-file", type=str, help="Path to threshold for higher quantile")
    return parser.parse_args()

def collect_args():
    args = parse_args()
    data_folder = args.data_folder
    low = args.low_threshold_file
    high = args.high_threshold_file
    data_files = glob.glob(data_folder + "/*.txt")
    return data_files, [low, high]

def read_threshold_from_file(filename):
    df = pd.read_csv(filename, sep="\t", index_col = 0, squeeze=True, header=None)
    return df

def find_outliers():
    data_files, threshold_files = collect_args()
    df_list = []
    for data_file in data_files:
        try:
            df = pd.read_csv(data_file, sep="\t")
            df_list.append(df)
        except pd.errors.EmptyDataError:
            print(f"No data found in {data_file}. Skipped")
        except UnicodeDecodeError:
            print(f"Invalid data in {data_file}. Skipped")
        except Exception as err:
            raise err

    data = pd.concat(df_list)
    data = data.fillna(0)

    ids = data['ROI_ID']
    data = data.drop('ROI_ID', axis=1)

    low, high = threshold_files
    Q1 = read_threshold_from_file(low)
    Q3 = read_threshold_from_file(high)

    Out1 = data[data > Q3]
    Out2 = data[data < Q1]

    Out1 = Out1.dropna('rows', how='any')
    Out2 = Out2.dropna('rows', how='any')

    outlier_ids =  [ids[Out1.index], ids[Out2.index]]
    
    outliers = pd.concat(outlier_ids)

    outliers.to_csv('outlier_ids.txt', sep='\t', index=False)

if __name__ == '__main__':
    find_outliers()
