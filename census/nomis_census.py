"""
Tools for handling census data acessed from NOMIS

Author: William Jay, November 2025
"""

import folium

import geopandas as gpd
import pandas as pd

from glob import glob


class Census(object):
    """
    Class object for handling census data from CSV files acessed from NOMIS
    """

    def __init__(self, csv_glob: str):
        """
        Initiate class with a Unix-style glob to all NOMIS CSV files containing census
        data.

        """

        csv_list = glob(csv_glob)

        if csv_list == []:
            raise FileNotFoundError(
                f"Input glob to CSV files does not direct to any files: '{csv_glob}'"
            )

        # Read CSV files as one pandas DataFrame
        self.data = self.nomis_csv_to_dataframe(csv_list)

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
                main_df = df

            # For the second dataframe, add a suffix for the main dataframe's fields so
            # the dataset they are from is identifiable
            elif n == 1:
                main_df = main_df.join(df, lsuffix=main_df.name, rsuffix=df.name)

            else:
                main_df = main_df.join(df, rsuffix=df.name)

        return main_df

    def calc_percent_of_variable(self, variable_name: str, total_name: str):
        """
        Create new series within the self.mapped_data GeoDataFrame containing the
        percentage of a given variable of another.

        Returns name of new variable
        """

        # Create standard name for new series
        variable_percent_name = f"{variable_name}_percent"

        # Calculate percent from sum values if percent is required
        self.mapped_data[variable_percent_name] = (
            self.mapped_data[variable_name] / self.mapped_data[total_name]
        ) * 100

        return variable_percent_name

    def map_data_to_polygons(
        self,
        gpkg_path: str,
        geometry_field_nomis: str = "2021 output area",
        geometry_field_gpkg: str = "OA21CD",
    ):
        """
        Returns a geopandas DataFrame that contains geospatial polygons for each
        geographic entry such as output areas or super output areas. A GeoPackage file
        must be input containing these output areas at the resolution that matches the
        census data.
        """

        # Open output areas as GeoDataFrame
        gdf = gpd.read_file(gpkg_path)

        # Add geometry fields ass attributes
        self.geometry_field_gpkg = geometry_field_gpkg

        # Check that the datatypes of the join columns match
        nomis_dtype = self.data[geometry_field_nomis].dtype
        gpkg_dtype = gdf[self.geometry_field_gpkg].dtype
        if nomis_dtype != gpkg_dtype:
            raise ValueError(
                "Datatype mismatch for join columns. NOMIS field "
                f"'{geometry_field_nomis}' is '{nomis_dtype}' and GeoPackage field "
                f"'{self.geometry_field_gpkg}' is '{gpkg_dtype}'"
            )

        # Join the census data to the output area polygons
        gdf = gdf.merge(
            self.data,
            left_on=self.geometry_field_gpkg,
            right_on=geometry_field_nomis,
            how="left",
        )

        # Open the joined data as a GeoDataFrame
        mapped_gdf = gpd.GeoDataFrame(gdf)

        # Assign to attribute
        self.mapped_data = mapped_gdf

    def create_choropleth_map(
        self,
        value_field: str,
        output_map: str,
        start_coords: list[float],
        zoom_level: int,
    ):
        """
        Create a Leaflet choropleth map using the folium.Choropleth method
        """

        # Create map centered over Plymouth
        folium_map = folium.Map(start_coords, zoom_start=zoom_level)

        # Create choropleth features
        choropleth = folium.Choropleth(
            geo_data=self.mapped_data,
            data=self.mapped_data,
            columns=[self.geometry_field_gpkg, value_field],
            key_on=f"feature.properties.{self.geometry_field_gpkg}",
            legend_name=value_field,
            highlight=True,
        ).add_to(folium_map)

        # Write as HTML
        folium_map.save(output_map)
