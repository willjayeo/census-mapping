#!/usr/bin/env python3
"""
Create a Leaflet map of census data

Author: William Jay, November 2025
"""

import argparse
import folium

import geopandas as gpd

from census.nomis_census import Census


def main(csv_glob: str, gpkg_path: str, output_map: str):
    """ """

    # Get Census object
    census_data = Census(csv_glob, gpkg_path)

    # Calculate percent from sum values
    field_name = "No religion"
    total_field_name = "Total: All usual residentsTS030_-_Religion"
    census_data.mapped_data["no_religion_percent"] = (
        census_data.mapped_data[field_name] / census_data.mapped_data[total_field_name]
    ) * 100

    create_choropleth_map(
        census_data.mapped_data, "OA21CD", "no_religion_percent", output_map
    )


def create_choropleth_map(
    geodataframe: gpd.GeoDataFrame,
    id_field: str,
    value_field: str,
    output_map: str,
):
    """ """

    # Create map centered over Plymouth
    folium_map = folium.Map([50.37, -4.14], zoom_start=12)

    # Create choropleth features
    folium.Choropleth(
        geo_data=geodataframe,
        data=geodataframe,
        columns=[id_field, value_field],
        key_on=f"feature.properties.{id_field}",
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

    cmdline = parser.parse_args()

    main(cmdline.input_csv, cmdline.input_gpkg, cmdline.output_map)
