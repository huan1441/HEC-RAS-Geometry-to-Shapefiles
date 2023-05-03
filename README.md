# HEC-RAS Geometry to Shapefiles
These Python scripts are developed for converting the river centerlines and cross-sections of multiple geometry files (*.g or *.g.hdf) in HEC-RAS models to the corresponding polyline shapefiles (ESRI vector data).

A brief introduction to the features of each Python script is as follows.

(1) [1-HEC-RAS_FindAllGeo.py](https://github.com/huan1441/HEC-RAS-Geometry-to-Shapefiles/blob/main/1-HEC-RAS_FindAllGeo.py) is developed to find and copy all geometry files (*.g) from HEC-RAS model folders.

(2) [2-HEC-RAS_river2shp.py](https://github.com/huan1441/HEC-RAS-Geometry-to-Shapefiles/blob/main/2-HEC-RAS_river2shp.py) is developed to extract river centerlines (*.g or *.g.hdf) from HEC-RAS and save them as shapefiles and merge multiple shapefiles into one.

(3) [3-HEC-RAS_CountingShp.py](https://github.com/huan1441/HEC-RAS-Geometry-to-Shapefiles/blob/main/3-HEC-RAS_CountingShp.py) is developed to count the number of shapefiles from each folders.

(4) [4-HEC-RAS_CountingFolders.py](https://github.com/huan1441/HEC-RAS-Geometry-to-Shapefiles/blob/main/4-HEC-RAS_CountingFolders.py) is developed to count the number of folders.

(5) [5-HEC-RAS_CS2shp.py](https://github.com/huan1441/HEC-RAS-Geometry-to-Shapefiles/blob/main/5-HEC-RAS_CS2shp.py) is developed to extract river centerlines and cross-section (*.g or *.g.hdf) from HEC-RAS; save them as shapefiles; merge multiple shapefiles into one; and calculate the river length in each polyline shapefiles.

