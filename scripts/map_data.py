#!/usr/bin/env python3

import argparse
import folium

import matplotlib.pyplot as plt

# TODO: Make this a proper package
from nomis_census import Census


def main(csv_glob: str, gpkg_path: str, output_map: str):
    """ """

    # Get Census object
    census_data = Census(csv_glob)

    # Add output area geometries to census data
    census_data.map_data_to_polygons(gpkg_path)

    # Create simple plot of test variable
    census_data.mapped_data.plot(column="Total: All usual residents")

    plt.savefig(output_map)


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
