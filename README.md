# Outlier Detection Using InterQuartile Distance

IQR(Interquartile Range) is a concept from descriptive statistics. It measures the statistical dispersion, by being the difference between 75th and 25th quartiles, or upper and lower quartiles. IQR can also be called as a measure of variability, based on dividing data into quartiles.[3]

# BrainSuite

BrainSuite is a collaborative project by University of California, Los Angeles and University of Southern California for automated processing of Magnetic Resonance Images of the human brain. It provides several tools for visualization and interaction with data in addition  to functionalities for parameterization of inner and outer surfaces of cerebral cortex. [1]

# Feature Extraction

1. Open BrainSuite
2. Open MRI Image via File>Open Volume
3. Goto Cortex > Cortex Surface Extraction Sequence. This opens CSE Dialog Box
4. Verify filename and Working Directory
5. Click Step> 4 times until it says “finished skullstripping”
6. If the default parameters is not working go back and modify the required parameters and repeat the steps
7. Use the mask tool if you need to mask any part of the brain
8. Uncheck skull and scalp
9. Click Stage>> 3 times to reach Cerebellum Labelling Stage
10. Click Step> 2 times and check for alignment. If it’s not aligning modify the cost function and fix the alignment
11. Click Stage>> to complete Cerebellum Labelling
12. Click Stage>> 5 more times.
13. If you want to use custom mask at this stage click “Load Custom Mask” button for loading masks created earlier using mask tool
14. Click Stage>> 3 more times to complete all the steps
15. Now the working directory will contain a .txt file containing the features. [1]

# Algorithm

Assuming dataset contains 2n entries  
First quartile, Q1 = median of n smallest entries in dataset  
Third Quartile, Q3 = median of n largest entries in dataset [3]

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

# Explanation for Script

1. The script collects the data from all the text files
2. The data containing the following columns - ‘ROI_ID', 'Mean_Thickness(mm)', 'GM_Volume(mm^3)', 'CSF_Volume(mm^3)', WM_Volume(mm^3)', 'Total_Volume(GM+WM)(mm^3)', 'Cortical_Area_mid(mm^2)', 'Cortical_Area_inner(mm^2)', 'Cortical_Area_pial(mm^2)'
3. Collect data belonging to the same ROI_ID into a dataframe
4. Calculate Q1, Q3 for the dataframe using df.quantile()
5. Any data point that is outside  Q1(lower limit), or  Q3(upper limit) are outliers
6. Filter them out and write to an output file.
7. In the process if thresholds are already available in txt files it will be loaded from file, else threshold files will be created that contains the threshold for further usage of script

# References

1. http://brainsuite.org/, BrainSuite, Last accessed 12/08/2019
2. https://github.com/ajoshiusc/brain-reporter, Brain Reporter, Last accessed 12/08/2019
3. https://en.wikipedia.org/wiki/Interquartile_range, Interquartie Range - Wikipedia, Last accessed 12/08/2019

