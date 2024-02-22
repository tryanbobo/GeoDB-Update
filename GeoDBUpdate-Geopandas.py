import geopandas as gpd
import os

def update_geodatabase(shp_directory, gdb_directory, id_field):
    # list shpfiles in the workspace
    shpFiles = [f for f in os.listdir(shp_directory) if f.endswith('.shp')]

    # iterate through shpfiles and update geoDB
    if shpFiles:
        for shp in shpFiles:
            shpPath = os.path.join(shp_venv-Arcpydirectory, shp)
            # extract the feature class name by excluding extension
            featClassName = os.path.splitext(shp)[0]
            featClassPath = os.path.join(gdb_directory, featClassName + '.shp')
            # check if featclass in geoDG exist first only existing feature class are "updated"
            if os.path.exists(featClassPath):
                # load shapefile and geodatabase feature class into GeoDataFrames
                shp_gdf = gpd.read_file(shpPath)
                gdb_gdf = gpd.read_file(featClassPath)

                # perform a left join to find records in gdb that are not in shp
                merged_gdf = gdb_gdf.merge(shp_gdf, how='left', indicator=True, on=id_field)
                merged_gdf = merged_gdf[merged_gdf['_merge'] == 'left_only']

                # drop the _merge column and save the result back to the geodatabase
                merged_gdf.drop(columns='_merge', inplace=True)
                merged_gdf.to_file(featClassPath, driver='FileGDB')

                print(f"Updated {featClassName} in geodatabase")
            else:
                print(f"{featClassName} does not exist in the geodatabase")

        print("Geodatabase update complete")
    else:
        print("No shapefiles found in workspace")

# Ask the user for inputs
shp_directory = input("Enter the shapefile directory: ")
gdb_directory = input("Enter the geodatabase directory: ")
id_field = input("Enter the ID field: ")

update_geodatabase(shp_directory, gdb_directory, id_field)