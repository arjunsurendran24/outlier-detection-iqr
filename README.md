# Outlier Detection Using InterQuartile Distance

The repository contains a python script for detecting outliers in brain image using IQR

# Usage

`
python .\outlier_detection.py --data-folder <path to data folder> --low-threshold <lower threshold> --high-threshold <higher threshold>
`

Example 

`
python .\save_thresholds.py --data-folder .\Edited\ --low-threshold 0.1 --high-threshold 0.9
`
It will create 3 text files

1. lower-threshold.txt - Contains features of low threshold
2. higher-threshold.txt = Contains features of high threshold
3. outlier_ids.txt - ROI_IDs of any detected outliers
