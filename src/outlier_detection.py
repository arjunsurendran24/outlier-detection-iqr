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
        df = df.drop('ROI_ID', axis=1)

        low_file_name = "./thresholds/" + str(id) + "_" + str(low) + "_lower_threshold.txt"
        high_file_name = "./thresholds/" + str(id) + "_" + str(high) +  "_higher_threshold.txt"

        try:
            Q1 = read_threshold_from_file(low_file_name)
            Q3 = read_threshold_from_file(high_file_name)
            IQR = Q3 - Q1

        except FileNotFoundError:
            Q1 = df.quantile(low)
            Q3 = df.quantile(high)
            Q1.to_csv(low_file_name, sep="\t")
            Q3.to_csv(high_file_name, sep="\t")
            IQR = Q3 - Q1

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
                
            subject_id = data_file.split("\\")
            subject_id = subject_id[-1]
            subject_id = subject_id.split(".")
            subject_id = subject_id[:-1]
            subject_id = ''.join(subject_id)
            out_file = "./outliers/" + subject_id + ".report.txt"
            
            df2 = data[data['ROI_ID'] == id]
            df2 = df2.drop('ROI_ID', axis=1)

            Out1 = df2[df2 > Q3 + 1.5 * IQR]
            Out2 = df2[df2 < Q1 - 1.5 * IQR]
            Out1 = Out1.dropna('rows', how='all')
            Out2 = Out2.dropna('rows', how='all')
            Out1 = Out1.dropna('columns', how='all')
            Out2 = Out1.dropna('columns', how='all')

            out_list = [Out1, Out2]
            out = pd.concat(out_list)
            
            out = out.drop_duplicates()
            if out.empty:
                pass
            else:
                if os.path.exists(out_file):
                    val = "a"
                    
                    with open(out_file, val) as outfile:
                        columns = out.columns
                        for col in columns:
                            outfile.write(str(id))
                            outfile.write("\t")
                            outfile.write(col)
                            outfile.write("\t")
                            outfile.write(str(np.round(out[col].values[0])))
                            outfile.write("\t")
                            outfile.write(str(np.round(Q1[col])))
                            outfile.write("\t")
                            outfile.write(str(np.round(Q3[col])))
                            outfile.write("\n")
                        
                else:
                    val = "w"
                    with open(out_file, val) as outfile:
                        outfile.write("ROI_ID")
                        outfile.write("\t")
                        outfile.write("Measure")
                        outfile.write("\t")
                        outfile.write("Value")
                        outfile.write("\t")
                        outfile.write("Lower Bound")
                        outfile.write("\t")
                        outfile.write("Higher Bound")
                        outfile.write("\n")
                        columns = out.columns
                        for col in columns:
                            outfile.write(str(id))
                            outfile.write("\t")
                            outfile.write(col)
                            outfile.write("\t")
                            outfile.write(str(np.round(out[col].values[0])))
                            outfile.write("\t")
                            outfile.write(str(np.round(Q1[col])))
                            outfile.write("\t")
                            outfile.write(str(np.round(Q3[col])))
                            outfile.write("\n")

if __name__ == '__main__':
    find_outliers()
