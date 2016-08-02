#Calculate the LS Factor
arcpy.CheckOutExtension("Spatial")

import arcpy
import arcpy.sa as arcsa
import os

#OVERWRITE command
arcpy.env.overwriteOutput = True

#environment settings
# env.workspace = arcpy.GetParameterAsText(0)
# env.scratchWorkspace = arcpy.GetParameterAsText(1)

#sel local variables for slope
inRaster = arcpy.GetParameterAsText(0)
outDir = arcpy.GetParameterAsText(1)

outRaster = os.path.join(outDir, "LSValue_Raster.tif")


#calculate and save the slope
slopeRaster = arcsa.Slope(inRaster, "PERCENT_RISE", 1)


#calculate flow direction
flowdirRaster = arcsa.FlowDirection(inRaster)

#calculate flow length
flowlenRaster = arcsa.FlowLength(flowdirRaster, "DOWNSTREAM", "")

#now we need to calculate the LS factor with the equation
#LS = [0.065 + 0.0456 (slope) + 0.006541 (slope)2](slope length ÷ constant)NN
#use raster calculator for this

LSFactor = (0.065 + (0.0456 * slopeRaster) + (0.006541 * (arcsa.Square(slopeRaster)))) * arcsa.SquareRoot(flowlenRaster / 72.5)
LSFactor.save(outRaster)
