#!/usr/bin/env python3
"""
Create a Leaflet choropleth map of a census data variable

Author: William Jay, November 2025
"""

import argparse
import folium

import geopandas as gpd

from census.nomis_census import Census

CSV_GEOMETRY = "2021 output area"
GPKG_GEOMETRY = "OA21CD"
PLYMOUTH_COORDS = [50.37, -4.14]
ZOOM_LEVEL = 12


def main(
    csv_path: str,
    gpkg_path: str,
    output_map: str,
    variable: str,
    percent_of_variable: str = None,
    csv_geometry_field: str = CSV_GEOMETRY,
    gpkg_geometry_field: str = GPKG_GEOMETRY,
):
    """
    Create a Leaflet HTML choropleth map using Folium for a chosen variable in a
    provided CSV file of census data accessed from NOMIS.

    `gpkg_path` must be input to provide the geometries used for each census data row.
    E.g. the output area of the census data can be accessed from
    https://www.data.gov.uk/dataset/4d4e021d-fe98-4a0e-88e2-3ead84538537/output-areas-december-2021-boundaries-ew-bgc-v21

    Use the `percent_of_variable` to calculate values of `variable` as a percentage of
    `variable`. E. g. for the "TS030 - Religion" dataset, if `variable` is "Christian" and `percent_of_variable` is "Total All usual residents", then the percentage of people identifying as Christian will be plotted for each output area.
    """

    # Get Census object
    census = Census(csv_path)

    # Map data onto output area polygons
    census.map_data_to_polygons(gpkg_path, csv_geometry_field, gpkg_geometry_field)

    # Calculate percent of variable
    if percent_of_variable is not None:
        
       variable = census.calc_percent_of_variable(variable, percent_of_variable)

    # Create choropleth Leaflet map
    create_choropleth_map(
        census.mapped_data,
        variable,
        gpkg_geometry_field,
        output_map,
    )


def create_choropleth_map(
    gdf: gpd.GeoDataFrame,
    value_field: str,
    geometry_field: str,
    output_map: str,
    start_coords: list[float] = PLYMOUTH_COORDS,
    zoom_level: int = ZOOM_LEVEL,
):
    """
    Create a Leaflet choropleth map using the folium.Choropleth method
    """

    # Create map centered over Plymouth
    folium_map = folium.Map(start_coords, zoom_start=zoom_level)

    # Create choropleth features
    choropleth = folium.Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=[geometry_field, value_field],
        key_on=f"feature.properties.{geometry_field}",
        legend_name=value_field,
        highlight=True,
    ).add_to(folium_map)

    # Write as HTML
    folium_map.save(output_map)


if __name__ == "__main__":
    helpstring = ""
    parser = argparse.ArgumentParser(
        description=helpstring,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input_csv",
        type=str,
        required=True,
        help="Unix-style glob to CSV files downloaded from NOMIS",
    )
    parser.add_argument(
        "--input_gpkg",
        type=str,
        required=True,
        help="Path to GeoPackage file containing census Output Area features",
    )
    parser.add_argument(
        "--output_map",
        type=str,
        required=True,
        help="Path to write output HTML map to",
    )
    parser.add_argument(
        "--variable",
        type=str,
        required=True,
        help="Name of CSV field to map",
    )
    parser.add_argument(
        "--percent_variable",
        type=str,
        required=False,
        default=None,
        help=(
            "Name of CSV field to calculate the percentage of --variable from, optional"
        ),
    )

    cmdline = parser.parse_args()

    main(
        cmdline.input_csv,
        cmdline.input_gpkg,
        cmdline.output_map,
        cmdline.variable,
        cmdline.percent_variable,
    )
