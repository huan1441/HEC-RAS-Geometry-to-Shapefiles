# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Created by Tao Huang, March 2022, in Python 3.7
#
# Script to count the number of shapefiles from each folders
#
# Version 1.0        
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
import numpy as np

# function to create a folder to store the results if it does not exist

def ResultsFolder(Folder):
    if os.path.exists(Folder) == False:
        os.mkdir(Folder)

# function to find and copy all *.g files from HEC-RAS model folders

def HR_CountShp(input_folder,output_folder):

    Folder_Name = os.listdir(input_folder)
    County_Name = []
    No_Shapefiles = []

    # create a folder for river centerline geometry files
    ResultsFolder(output_folder)

    # Counting number of geometry files
    for folder in Folder_Name:
        
        County_Name.append(folder.split(sep='_')[2])
        
        path = os.path.join(input_folder, folder)

        file_list = os.listdir(path)

        # there are five sub-files for each shapefile, and exclude the merge shapefile
        number_file = len(file_list)/5 -1
        No_Shapefiles.append(number_file)
    
    Counting = np.column_stack((County_Name,No_Shapefiles))
    np.savetxt(output_folder+'Counting_shp.csv', Counting, fmt='%s',delimiter = ',')

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.

if __name__ == '__main__':
        
        input_all_folder = './River_shp/River_shp_TX'

        output_folder = './Counting/'

        HR_CountShp(input_all_folder,output_folder)

        print("Done!")
    
    
