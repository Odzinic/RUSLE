#Calculate the SPI
arcpy.CheckOutExtension("Spatial")

import arcpy
import arcpy.sa as arcsa
import os
import numpy as np

#OVERWRITE command
arcpy.env.overwriteOutput = True

#Input Parameters
inRaster = arcpy.GetParameterAsText(0)
outDir = arcpy.GetParameterAsText(1)
percentileNum = float(arcpy.GetParameterAsText(2))

slopedegRaster = os.path.join(outDir, "SlopeValue_Raster.tif")
flowdirRaster = os.path.join(outDir, "FlowDirValue_Raster.tif")
flowaccumRaster = os.path.join(outDir, "FlowAccumValue_Raster.tif")

spiRaster = os.path.join(outDir, "SPIValue_Raster.tif")
spipercRaster = os.path.join(outDir, "SPIPercentile_Raster.tif")



# calculate and save the slope
slopedeg = arcsa.Slope(inRaster, "DEGREE", 1)

# calculate flow direction
flowdir = arcsa.FlowDirection(inRaster)


# calculate flow accumulation
flowaccum = arcsa.FlowAccumulation(flowdir, "", "FLOAT")


# Equation to get the SPI is SPI = ln(flow accum * slope)
SPI = arcsa.Ln(flowaccum * slopedeg)
SPI.save(spiRaster)


spiArray = arcpy.RasterToNumPyArray(spiRaster)
percentileVal = np.percentile(spiArray, percentileNum)
maxpercentileVal = np.percentile(spiArray, 100.0)

spipercentileRaster = arcsa.Con(spiRaster, spiRaster, None, "VALUE >= {0} AND VALUE <= {1}".format(percentileVal, maxpercentileVal))
spipercentileRaster.save(spipercRaster)
