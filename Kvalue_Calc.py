arcpy.CheckOutExtension("Spatial")

import arcpy, os
import arcpy.sa as arcsa

arcpy.env.overwriteOutput = True

soilIn= arcpy.GetParameterAsText(0)
boundaryIn = arcpy.GetParameterAsText(1)
outDir = arcpy.GetParameterAsText(2)
resolutionIn = arcpy.GetParameterAsText(3)

clippedSoil = os.path.join(outDir, "Clipped_Soil.shp")
kvalRaster = os.path.join(outDir, "KValue_Raster.tif")

kvalDic = {"C":0.49,    # Clay
		   "CL":0.67,   # Clay loam
		   "CSL":0.16,  # Coarse sandy loam
		   "FS":0.18,   # Fine sand
		   "FSL":0.40,  # Fine sandor loam
		   "L":0.67,    # Loam
		   "LS":0.09,   # Loamy sand
		   "LFS":0.25,  # Loamy fine sand
		   "LVFS":0.87, # Loamy very fine sand
		   "S":0.04,    # Sand
		   "SL":0.29,   # Sandy loam
		   "SIL":0.85,  # Silt loam
		   "SIC":0.58,	# Silty clay
		   "SICL":0.72,	# Silty clay loam
		   "VFSL":0.79	# Very fine sandy loam
		   }

arcpy.Clip_analysis(soilIn, boundaryIn, clippedSoil)

arcpy.AddField_management(clippedSoil, "K_Val", "FLOAT")

with arcpy.da.UpdateCursor(clippedSoil, ["ATEXTURE1", "ATEXTURE2", "ATEXTURE3", "PERCENT1", "PERCENT2", "PERCENT3", "K_Val"]) as cursor:
	for row in cursor:
		numKval = 0.0
		soilType = []
		soilPerc = []
		
		for soilNum in range(3):
			#soilDic[row[soilNum]] = row[soilNum+3]	# Sets the key to be the soil type and makes the value the percent of that soil (adds 3 to the list index)
			if (row[soilNum] in kvalDic.keys()):
				soilType.append(kvalDic[row[soilNum]])
				soilPerc.append(row[soilNum + 3]/100.0)
			else:
				soilType.append(0)
				soilPerc.append(0)
			
		for num in range(3):
			numKval += (float(soilType[num] * soilPerc[num])) / 7.59	# Converts the unit of K values
			
		row[6] = numKval		
		cursor.updateRow(row)
		

			

arcpy.PolygonToRaster_conversion(clippedSoil, "K_Val", kvalRaster, "CELL_CENTER", "", float(resolutionIn))


		