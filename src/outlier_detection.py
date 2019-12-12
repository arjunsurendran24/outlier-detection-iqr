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

def read_threshold_from_file(filename):
    df = pd.read_csv(filename, sep="\t", index_col = 0, squeeze=True, header=None)
    return df
    
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

    low, high = thresholds

    ids = data['ROI_ID'].unique()
    for id in ids:
        
        df = data[data['ROI_ID'] == id]
        df.drop('ROI_ID', axis=1)
        
        low_file_name = "./thresholds/" + str(id) + "_" + str(low) + "_lower_threshold.txt"
        high_file_name = "./thresholds/" + str(id) + "_" + str(high) +  "_higher_threshold.txt"
        
        try:
            Q1 = read_threshold_from_file(low_file_name)
            Q3 = read_threshold_from_file(high_file_name)

        except FileNotFoundError:
            Q1 = df.quantile(low)
            Q3 = df.quantile(high)
            Q1.to_csv(low_file_name, sep="\t")
            Q3.to_csv(high_file_name, sep="\t")

        Out1 = data[df >= Q3]
        Out2 = data[df <= Q1]

        Out1 = Out1.dropna('rows', how='any')
        Out2 = Out2.dropna('rows', how='any')
        
        out_list = [Out1, Out2]
        out = pd.concat(out_list)
        
        outfile = "./outliers/" + str(id) + ".txt"

        if out.empty:
            with open(outfile, "w") as outfile:
                outfile.write("No Outliers!")
        else:
            print(id)
            out.to_csv(outfile, sep="\t")

if __name__ == '__main__':
    find_outliers()
