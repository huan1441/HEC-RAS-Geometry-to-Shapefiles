# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Created by Tao Huang, Jan 2022, in Python 3.7
#
# Script to extract river centerlines (.g or .g.hdf) from HEC-RAS and save them as shapefiles
#           and merge multiple shapefiles into one
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

def HR_g2shp(input_folder,output_folder,projection):

  # obtain the .g files' names in the input folder
  filenames = os.listdir(input_folder)

  # create a folder for river centerline shapefiles
  ResultsFolder(output_folder)

  for file in filenames:
      River_xy = np.array([[]]*2).T
      # create the corresponding projection file
      f = open(input_folder+file)

      # 4 numbers or 2 numbers in each row and 16 placeholders for x or y coordinate
      for line in f.readlines():
          if "Reach XY=" in line:
              No_points = int(line.split("=")[1])

          if len(line) == 65 and len(River_xy) < No_points and "Junct X Y & Text" not in line and "Viewing Rectangle" not in line:
              River_xy = np.row_stack((River_xy,[float(line[0:16]),float(line[16:32])]))
              River_xy = np.row_stack((River_xy,[float(line[32:48]),float(line[48:64])]))

          if len(line) == 33 and len(River_xy) > 1 and len(River_xy) < No_points:
              River_xy = np.row_stack((River_xy,[float(line[0:16]),float(line[16:32])]))

      f.close()
                                
      # converting the xy data format
      xy_List = xy_List = [xy for xy in zip(River_xy[:,0], River_xy[:,1])]
    
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


# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.

if __name__ == '__main__':

        CountyName = 'Ohio'
        
        input_ghdf_folder = './Geo_HDF_input/'

        input_g_folder = './Geo_input/River_Geo_'+CountyName+'/'

        output_folder = './River_shp/River_shp_'+CountyName+'_IN/'

        input_shp_folder = './River_shp/River_shp_'+CountyName+'_IN/'
        
        projection = "Projection_Indiana_East_FIPS_1301_Feet.prj"

        #HR_ghdf2shp(input_ghdf_folder,output_folder,projection)

        HR_g2shp(input_g_folder,output_folder,projection)

        HR_mul2one(input_shp_folder,output_folder,projection)
    
    
