"""
Tools for handling census data acessed from NOMIS

Author: William Jay, November 2025
"""

import geopandas as gpd
import pandas as pd

from glob import glob


class Census(object):
    """ """

    def __init__(self, csv_glob: str):
        """
        Initiate class with a Unix-style glob to all NOMIS CSV files containing census
        data
        """

        print("Initialising census object")

        csv_list = glob(csv_glob)

        if csv_list == []:
            raise FileNotFoundError(
                f"Input glob to CSV files does not direct to any files: '{csv_glob}'"
            )

        # Read CSV files as one pandas DataFrame
        self.data = self.nomis_csv_to_dataframe(csv_list)

        # Define column names of output area IDs
        self.oa_id_col_nomis = "2021 output area"
        self.oa_id_col_polygons = "OA21CD"

    def nomis_csv_to_dataframe(
        self,
        csv_list: list[str],
        header: int = 8,
        names_line: int = 7,
        dataset_name_line: int = 1,
    ) -> pd.DataFrame:
        """
        Returns a pandas DataFrame from an input list of CSV files containing census
        data from NOMIS
        """

        # Create list to populate dataframes with
        df_list = []

        for csv_path in csv_list:

            print(f"Reading CSV: '{csv_path}'")

            with open(csv_path, "r") as csv_file:

                csv_lines = csv_file.readlines()
                # Get the name of this dataset
                dataset_name = eval(csv_lines[dataset_name_line])
                # Get the field names
                names = csv_lines[names_line]

            # FIXME: Some CSV field names contain commas!
            # Convert field names to a list
            names = names.split(",")

            # Remove any double quotations and new line escape charecters
            names = [name.replace('"', "") for name in names]
            names = [name.replace("\n", "") for name in names]

            # Open as a pandas DataFrame
            dataframe = pd.read_csv(csv_path, header=header, names=names)

            # Add dataset name to dataframe
            dataframe.name = dataset_name.replace(" ", "_")

            # Add dataframe to list
            df_list.append(dataframe)

        for n, df in enumerate(df_list):

            # The first dataframe in the list will be the main dataframe. Other
            # dataframes will be added to the main dataframe
            if n == 0:
                print(f"Designating main dataframe: '{df.name}'")
                main_df = df

            # For the second dataframe, add a suffix for the main dataframe's fields so
            # the dataset they are from is identifiable
            elif n == 1:
                print(f"Joining {df.name}")
                main_df.join(df, lsuffix=main_df.name, rsuffix=df.name)

            else:
                print(f"Joining {df.name}")
                main_df.join(df, rsuffix=df.name)

        return main_df

    def map_data_to_polygons(
        self,
        gpkg_path: str,
    ):
        """
        Returns a geopandas DataFrame that contains geospatial polygons for each
        geographic entry such as output areas or super output areas.
        """

        # Open output areas as GeoDataFrame
        gdf = gpd.read_file(gpkg_path)

        # Join the census data to the output area polygons
        mapped_df = gdf.merge(
            self.data,
            left_on=self.oa_id_col_polygons,
            right_on=self.oa_id_col_nomis,
            how="left",
        )

        # Open the joined data as a GeoDataFrame
        mapped_gdf = gpd.GeoDataFrame(mapped_df)

        # Assign to attribute
        self.mapped_data = mapped_gdf
