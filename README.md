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

If the thresholds are already calculated and stored in file `outlier_detection_from_stored_threshold.py` can be used for outlier detection

`
python .\outlier_detection_from_stored_threshold.py --data-folder .\Edited\ --low-threshold-file .\lower_threshold.txt --high-threshold-file .\higher_threshold.txt
`
Threshold files for `0.1 and 0.9` thresholds are available in `theshold_01_09` directory.
Threshold files for `0.25 and 0.75` thresholds are available in `theshold_025_075` directory.

