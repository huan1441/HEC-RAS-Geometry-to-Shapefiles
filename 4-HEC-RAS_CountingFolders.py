# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Created by Tao Huang, March 2022, in Python 3.7
#
# Script to count the number of folders
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

def HR_CountFolder(input_folder,output_folder):

    Folder_Name = os.listdir(input_folder)

    No_Folder = []

    # create a folder for river centerline geometry files
    ResultsFolder(output_folder)

    # Counting number of geometry files
    for folder in Folder_Name:
        count=0
        
        path = os.path.join(input_folder, folder)

        file_list = os.listdir(path)

        for file in file_list:
            if os.path.isdir(os.path.join(path, file)):
                count+=1

        No_Folder.append(count)
    
    Counting = np.column_stack((Folder_Name,No_Folder))
    
    np.savetxt(output_folder+'Counting_folder.csv', Counting, fmt='%s',delimiter = ',')

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.

if __name__ == '__main__':
        
        #input_all_folder = './Indiana_HEC_RAS_Models/'
    
        input_all_folder = './River_shp/'
        
        output_folder = './Counting/'

        HR_CountFolder(input_all_folder,output_folder)

        print("Done!")
    
    
