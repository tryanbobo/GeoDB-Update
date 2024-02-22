import arcpy
import os


def update_geodatabase(shp_directory, gdb_directory, id_field):
    arcpy.env.workspace = shp_directory
    shpLocation = arcpy.env.workspace
    gdbPath = gdb_directory

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
                # below section checks for each shpfiles feature ID. If it is not found in the corresponding geoDB feature it is removed.
                # create a list of unique identifiers in the shapefile
                shpIds = [row[0] for row in arcpy.da.SearchCursor(shpPath, id_field)]
                # create edit session
                with arcpy.da.Editor(gdbPath) as Edit:
                    # iterate over the features in the geodatabase feature class
                    with arcpy.da.UpdateCursor(featClassPath, [id_field]) as cursor:
                        for row in cursor:
                            # if the feature's identifier is not in the list, delete the feature
                            if row[0] not in shpIds:
                                cursor.deleteRow()

                # append new features from the list of shapefiles to the geodatabase
                arcpy.Append_management(shpPath, featClassPath, "NO_TEST")

                print(f"Updated {featClassName} in geodatabase")
            else:
                print(f"{featClassName} does not exist in the geodatabase")

        print("Geodatabase update complete")
    else:
        print("No shapefiles found in workspace")

# user input
shp_directory = input("Enter the shapefile directory: ")
gdb_directory = input("Enter the geodatabase directory: ")
id_field = input("Enter the ID field name: ")

update_geodatabase(shp_directory, gdb_directory, id_field)