import arcpy
import os

arcpy.env.workspace = r"M:\MapCom\Shapefiles_M4\2023-11-01"
shpLocation = arcpy.env.workspace
gdbPath = r"M:\MapCom\Data\GeoDB\General-OSP.gdb"

# list shpfiles in the workspace
shpFiles = arcpy.ListFeatureClasses("*.shp")


# iterate through shpfiles and update geoDB
if shpFiles:
    for shp in shpFiles:

        shpPath = os.path.join(shpLocation, shp)
        # extract the feature class name by excluding extension
        featClassName = os.path.splitext(shp)[0]
        featClassPath = os.path.join(gdbPath, featClassName)
        # check if featclass in geoDG exist first only existing feature class are "updated"
        if arcpy.Exists(featClassPath):
            arcpy.Append_management(shpPath, os.path.join(gdbPath, featClassName), "No_Test")
            # arcpy.FeatureClassToFeatureClass_conversion(shpPath, gdbPath, featClassName)
            print(f"Updated {featClassName} in geodatabase")
        else:
            print(f"{featClassName} does not exist in the geodatabase")

    print("Geodatabase update complete")
else:
    print("No shapefiles found in workspace")
