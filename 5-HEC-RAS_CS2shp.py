# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Created by Tao Huang, March 2022, in Python 3.7
#
# Script to (1)extract river centerlines and cross-section (.g or .g.hdf) from HEC-RAS;
#           (2)save them as shapefiles;
#           (3)merge multiple shapefiles into one; and
#           (4)calculate the river length in each polyline shapefiles
#
# Version 1.0        
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
import h5py
import numpy as np
import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd

# function to create a folder to store the results if it does not exist

def ResultsFolder(Folder):
    if os.path.exists(Folder) == False:
        os.mkdir(Folder)


# function to extract river centerlines (*.g.hdf) from HEC-RAS and save them as shapefiles

def HR_ghdf2shp(input_folder,output_folder,projection):
  # obtain the g.hdf files' names in the input folder
  filenames = os.listdir(input_folder)

  # create a folder for river centerline shapefiles
  ResultsFolder(output_folder)

  for file in filenames:      
    # extract results from HDF file(e.g.,PlanName.g01.hdf)
    # read the datasets and groups in the HDF5 file

    hdf = h5py.File(input_folder+file, 'r')

    # extract the x and y coordinates of all the polyline points
    River_xy = np.array(hdf.get('Geometry').get('River Centerlines').get('Polyline Points'))

    # converting the xy data format
    xy_List = [xy for xy in zip(River_xy[:,0], River_xy[:,1])]
    
    River_line = LineString(xy_List)

    #geo_River = gpd.GeoDataFrame(geometry = River_line)
    geo_River = gpd.GeoSeries(River_line)

    # save the river centerlines as shapefiles

    shp_path = output_folder + file + ".shp"
    geo_River.to_file(shp_path, driver="ESRI Shapefile",encoding="utf-8")

    # create the corresponding projection file
    f_in = open(projection)
    f_out = open(output_folder + file + ".prj","w")

    f_out.writelines(f_in.read())

    f_in.close()
    f_out.close()

  print(str(len(filenames))+" geometry HDF files have been converted to shapefiles!")


# function to extract river centerlines (*.g) from HEC-RAS and save them as shapefiles

def HR_Ri2shp(input_folder,output_folder,projection):

  # obtain the .g files' names in the input folder
  filenames = os.listdir(input_folder)

  # create a folder for river centerline shapefiles
  ResultsFolder(output_folder)

  for file in filenames:
      River_xy = np.array([[]]*2).T

      line_no = -1

      f = open(input_folder+file)

      geometry = f.readlines()

      f.close()

      # 4 numbers or 2 numbers in each row and 16 placeholders for x or y coordinate
      for line in geometry:

          line_no+=1
          
          if "Reach XY=" in line:
              No_points = int(line.split("=")[1])

              points_line = int(np.ceil(No_points/2))

              for i in range(1,points_line+1):
                  temp_line = geometry[line_no+i]

                  if len(temp_line) == 65:
                      River_xy = np.row_stack((River_xy,[float(temp_line[0:16]),float(temp_line[16:32])]))
                      River_xy = np.row_stack((River_xy,[float(temp_line[32:48]),float(temp_line[48:64])]))

                  elif len(temp_line) == 33:
                      River_xy = np.row_stack((River_xy,[float(temp_line[0:16]),float(temp_line[16:32])]))
                                
      # converting the xy data format
      xy_List = [xy for xy in zip(River_xy[:,0], River_xy[:,1])]
    
      River_line = LineString(xy_List)

      #geo_River = gpd.GeoDataFrame(geometry = River_line)
      geo_River = gpd.GeoSeries(River_line)

      # save the river centerlines as shapefiles

      shp_path = output_folder + file + ".shp"
      geo_River.to_file(shp_path, driver="ESRI Shapefile",encoding="utf-8")

      # create the corresponding projection file
      f_in = open(projection)
      f_out = open(output_folder + file + ".prj","w")

      f_out.writelines(f_in.read())

      f_in.close()
      f_out.close()

  print(str(len(filenames))+" geometry files have been converted to shapefiles!")


# function to extract river cross-sections (*.g) from HEC-RAS and save them as shapefiles

def HR_CS2shp(input_folder,output_folder,projection):

  # obtain the .g files' names in the input folder
  filenames = os.listdir(input_folder)

  # create a folder for river cross-section shapefiles
  ResultsFolder(output_folder)

  for file in filenames:
      CS_line = []

      line_no = -1
      
      f = open(input_folder+file)

      geometry = f.readlines()

      f.close()

      # 4 numbers or 2 numbers in each row and 16 placeholders for x or y coordinate
      for line in geometry:
          
          line_no+=1
          
          if "XS GIS Cut Line=" in line:
              No_points = int(line.split("=")[1])

              points_line = int(np.ceil(No_points/2))

              CS_xy = np.array([[]]*2).T

              for i in range(1,points_line+1):
                  temp_line = geometry[line_no+i]
                  if len(temp_line) == 65:
                      CS_xy = np.row_stack((CS_xy,[float(temp_line[0:16]),float(temp_line[16:32])]))
                      CS_xy = np.row_stack((CS_xy,[float(temp_line[32:48]),float(temp_line[48:64])]))

                  elif len(temp_line) == 33:
                      CS_xy = np.row_stack((CS_xy,[float(temp_line[0:16]),float(temp_line[16:32])]))

              # converting the xy data format
              xy_List = [xy for xy in zip(CS_xy[:,0], CS_xy[:,1])]
              
              CS_line.append(LineString(xy_List))

      geo_CS = gpd.GeoSeries(CS_line)

      # save the river cross-sections as shapefiles

      shp_path = output_folder + file + ".shp"
      geo_CS.to_file(shp_path, driver="ESRI Shapefile",encoding="utf-8")

      # create the corresponding projection file
      f_in = open(projection)
      f_out = open(output_folder + file + ".prj","w")

      f_out.writelines(f_in.read())

      f_in.close()
      f_out.close()

  print(str(len(filenames))+" geometry files have been converted to cross-section shapefiles!")


# function to merge multiple shapefiles into one

def HR_mul2one(input_folder,output_folder,projection):

    file = os.listdir(input_folder)

    path = [os.path.join(input_folder,i) for i in file if ".shp" in i]

    muli_rivers = gpd.GeoDataFrame(pd.concat([gpd.read_file(i) for i in path], ignore_index=True))

    muli_rivers.to_file(output_folder + "Merge.shp", driver="ESRI Shapefile",encoding="utf-8")

    # create the corresponding projection file
    f_in = open(projection)
    f_out = open(output_folder + "Merge.prj","w")

    f_out.writelines(f_in.read())

    f_in.close()
    f_out.close()

    print(str(len(path))+" shapefiles have been merged into one!")


# function to calculate the length of multiple polyline shapefiles

def HR_RiverLength(input_folder,output_folder):

    Folder_Name = os.listdir(input_folder)

    # create a folder for river centerline geometry files
    ResultsFolder(output_folder)

    # number of shapefiles
    count=0

    # Counting number of geometry files
    for file in Folder_Name:
        if file.endswith(".shp"):
            
            count+=1
            
            path = os.path.join(input_folder, file)
            # river length in miles (ft to mi)
            RL = gpd.read_file(path).length/5280

            RL_shp = np.column_stack((range(len(RL)),RL))

            filename = file.split(".")[0]

            np.savetxt(output_folder+filename+'_River_Length.csv', RL_shp, fmt="%s", header="Index,River length (miles)",delimiter = ',',comments='')

    print("The river length of "+str(count)+" shapefiles has been calculated!")


# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.

if __name__ == '__main__':

        CountyName = 'Lake'
##        
##        input_ghdf_folder = './Geo_HDF_input/'
##
        #input_g_folder = './Geo_input/River_Geo_'+CountyName+'/'

        output_ri_folder = './River_shp/'

        output_cs_folder = './CS_shp/CS_shp_'+CountyName+'_IN/'

        #input_ri_folder = './River_shp/River_shp_'+CountyName+'_TX/'
        input_ri_folder = './River_shp/RiverCenterline_East_IN/'

        input_cs_folder = './CS_shp/CS_shp_'+CountyName+'_IN/'
          
        input_shp_folder = './River_shp/Merge_HUC-8_TX/'
        output_RL_folder = './River_Length/'

##        input_g_folder = './Geo_input/'
##
##        output_folder = './CS_shp/'
        projection = "Projection_Indiana_East_FIPS_1301_Feet.prj"

        #projection = "Projection_Indiana_West_FIPS_1302_Feet.prj"
                                     
        #projection = "Projection_Texas_South_Central_FIPS_4204_Ft_US.prj"

        #projection = "Projection_Texas_Central_FIPS_4203_Ft_US.prj"

##        projection = "Projection_Texas_N_Central_FIPS_4202_Ft_US.prj"
##
##        #HR_ghdf2shp(input_ghdf_folder,output_folder,projection)
##
##        HR_Ri2shp(input_g_folder,output_ri_folder,projection)
##
##        HR_mul2one(input_ri_folder,output_ri_folder,projection)

        #HR_RiverLength(input_shp_folder,output_RL_folder)

        #HR_CS2shp(input_g_folder,output_cs_folder,projection)

        HR_mul2one(input_ri_folder,output_ri_folder,projection)
    
    
