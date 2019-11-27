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

It will add txt files for each ROI_ID in directory `outliers`. If there are no outliers for ROI_ID the file will have `No Outliers!`

If the thresholds are already calculated and stored in file it will be read from the file else under `thresholds` directory a file will be created for each ROI_ID with file name `<ROI_ID>_<low/high threshold>_<lower/higher>_threshold.txt`

