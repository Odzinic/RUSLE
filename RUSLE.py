arcpy.CheckOutExtension("Spatial")

import arcpy, os

arcpy.env.overwriteOutput = True

# Determine file I/O
rFactor = arcpy.GetParameterAsText(0)
kFactor = arcpy.GetParameterAsText(1)
lsFactor = arcpy.GetParameterAsText(2)
cFactor = arcpy.GetParameterAsText(3)
pFactor = 1
outDir = arcpy.GetParameterAsText(4)

rusle_output = os.path.join(outDir, "RUSLE_Output.tif")

# Multiply the factors
rusle = rFactor * kFactor * lsFactor * cFactor * pFactor

# Save the raster
rusle.save(rusle_output)
