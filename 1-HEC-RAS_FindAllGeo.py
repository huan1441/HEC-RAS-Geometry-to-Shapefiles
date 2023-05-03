# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Created by Tao Huang, Feb 2022, in Python 3.7
#
# Script to find and copy all *.g files from HEC-RAS model folders
#
# Version 1.0        
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
import shutil


# function to create a folder to store the results if it does not exist

def ResultsFolder(Folder):
    if os.path.exists(Folder) == False:
        os.mkdir(Folder)


# function to find and copy all *.g files from HEC-RAS model folders

def HR_FindGeo(input_folder,output_folder,target_suffix = ".g0"):

    # create a folder for river centerline geometry files
    ResultsFolder(output_folder)

    # Counting number of geometry files
    n=1

    walk_generator = os.walk(input_folder)
    
    for root_path, dirs, files in walk_generator:
        # root_path : current path
        # dirs : directory list in the folder
        # files : file list in the folder
        
        if len(files) < 1:
            continue
        
        for file in files:
            file_name, suffix_name = os.path.splitext(file)
            
            #if suffix_name == target_suffix:
            if  target_suffix in suffix_name:
                
                old_file_path = os.path.join(root_path, file)
                new_file_path = os.path.join(output_folder, str(n)+"-"+file)
                
                shutil.copy(old_file_path,new_file_path)

                n+=1

    print(str(n-1)+" geometry files have been found in "+input_folder+"!")


# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.

if __name__ == '__main__':
        
        input_all_folder = './Indiana_HEC_RAS_Models/'

        for folder in os.listdir(input_all_folder):

            if os.path.isdir(input_all_folder+folder):

                #input_HR_folder = os.path.join(input_all_folder, folder)
                input_HR_folder = input_all_folder+folder

                output_folder = './River_Geo_'+folder+'/'

                HR_FindGeo(input_HR_folder,output_folder)
    
    
