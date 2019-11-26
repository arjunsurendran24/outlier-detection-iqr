import argparse
import glob
import numpy as np
import os
import pandas as pd
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-folder", type=str, help="Path to the folder containing data")
    parser.add_argument("--low-threshold", type=float, help="Threshold for lower quantile")
    parser.add_argument("--high-threshold", type=float, help="Threshold for higher quantile")
    return parser.parse_args()

def collect_args():
    args = parse_args()
    data_folder = args.data_folder
    low = args.low_threshold
    high = args.high_threshold
    data_files = glob.glob(data_folder + "/*.txt")
    return data_files, [low, high]

def find_outliers():
    data_files, thresholds = collect_args()
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

    low, high = thresholds
    Q1 = data.quantile(low)
    Q3 = data.quantile(high)

    Q1.to_csv('lower_threshold.txt', sep='\t')
    Q3.to_csv('higher_threshold.txt', sep='\t')

    Out1 = data[data > Q3]
    Out2 = data[data < Q1]

    Out1 = Out1.dropna('rows', how='any')
    Out2 = Out2.dropna('rows', how='any')

    outlier_ids =  [ids[Out1.index], ids[Out2.index]]
    
    outliers = pd.concat(outlier_ids)

    outliers.to_csv('outlier_ids.txt', sep='\t', index=False)

if __name__ == '__main__':
    find_outliers()
