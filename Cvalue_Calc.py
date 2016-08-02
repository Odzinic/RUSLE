arcpy.CheckOutExtension("Spatial")

import arcpy, os
import arcpy.sa as arcsa

arcpy.env.overwriteOutput = True

agriIn = arcpy.GetParameterAsText(0)
boundaryIn = arcpy.GetParameterAsText(1)
outDir = arcpy.GetParameterAsText(2)

cvalRaster = os.path.join(outDir, "CValue_Raster.tif")
remapValues = []

convtillDic ={147.000000:0.41, # Grain Corn
              167.000000:0.56, # Beans
              136.000000:0.43, # Oats
              140.000000:0.43, # Wheat
              138.000000:0.43, # Spelt
              139.000000:0.43, # Triticale
              133.000000:0.43, # Barley
              162.000000:0.43, # Peas
              137.000000:0.34, # Rye
              195.000000:0.34, # Buckwheat
              157.000000:0.34, # Sunflower
              154.000000:0.34, # Flax
              122.000000:0.02, # Pasture/Forages
              192.000000:0.02, # Sod
              148.000000:0.47, # Tobacco
              181.000000:0.28, # Berries
              190.000000:0.36, # Vineyards/Grapes
              188.000000:0.38, # Fruit Trees/Orchards
              194.000000:0.20, # Nurseries
              177.000000:0.44, # Potatoes
              131.000000:0.50, # Fallow
              199.000000:0.46, # Other Crops
              158.000000:0.46, # Soybean (From Quebec)
			  200.000000:0.03, # Trees (undifferentiated)
			  210.000000:0.03, # Coniferous Trees
			  220.000000:0.03, # Broadleaf Trees
			  230.000000:0.03} # Mixedwood Trees

for key in convtillDic.keys():
    remapValues.append([key, int(convtillDic[key] * 100)])  # Creates the reclassify values that will be turned into a RemapValue (multiplies by 100 to
                                                            # turn the float values into integers temporarily (limitation of reclassify)

remap = arcsa.RemapValue(remapValues)			    # Creates a RemapValue object with the set reclassification values

arcpy.AddMessage(remapValues)
                                       

maskedAgri = arcsa.ExtractByMask(agriIn, boundaryIn)	    # Extracts the upper nith data from the agri
#maskedAgri.save(maskagriOut)

reclassedAgri = arcsa.Reclassify(maskedAgri, "VALUE",       # Reclassifies the crop types to their respective C value and changes crops that weren't
                                 remap, "NODATA")	    # specified to NoData
#reclassed.save(reclassedAgri)

arcsa.Divide(arcsa.Float(reclassedAgri), 100).save(cvalRaster)



