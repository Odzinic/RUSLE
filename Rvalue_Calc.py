arcpy.CheckOutExtension("Spatial")

import arcpy, os
import arcpy.sa as arcsa

arcpy.env.overwriteOutput = True

# Determine file I/O
rInput = arcpy.GetParameterAsText(0)
zField = arcpy.GetParameterAsText(1)
boundaryIn = arcpy.GetParameterAsText(2)
outDir = arcpy.GetParameterAsText(3)
resolutionIn = arcpy.GetParameterAsText(4)
rvalRaster = os.path.join(outDir, "RValue_Raster.tif")

# Interpolate R Factor values
rFactor = arcsa.Idw(rInput, zField, resolutionIn)

# Extract by mask the interpolated raster to the study area
rFactorClip = arcsa.ExtractByMask(rFactor, boundaryIn)

# Save the raster 
rFactorClip.save(rvalRaster)

