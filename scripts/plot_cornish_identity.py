#!/usr/bin/env python3
"""

Author: William Jay, November 2025
"""

import argparse

from census.nomis_census import Census

AUTHORITY_OF_INTEREST = "Cornwall"
AUTHORITY_FIELD = "MSOA21NM"
CSV_GEOMETRY = "Area"
GPKG_GEOMETRY = "MSOA21CD"


def main(
    csv_path: str,
    gpkg_path: str,
    output_plot: str,
    #variable: str,
    #percent_of_variable: str = None,
    output_areas_to_keep: list[str] = AUTHORITY_OF_INTEREST,
    csv_geometry_field: str = CSV_GEOMETRY,
    gpkg_geometry_field: str = GPKG_GEOMETRY,
):
    """
    Middle Super Output Area polygons accessed from
    https://www.data.gov.uk/dataset/677a5164-3a9e-4752-b8e6-5744d2b280ec/middle-layer-super-output-areas-december-2021-boundaries-ew-bgc-v3
    """

    # Get Census object
    census = Census(csv_path)

    # Map data onto output area polygons
    census.map_data_to_polygons(
        gpkg_path, csv_geometry_field, gpkg_geometry_field, output_areas_to_keep
    )

    # Calculate percent of variable
    #if percent_of_variable is not None:
    #    
    #`   variable = census.calc_percent_of_variable(variable, percent_of_variable)

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
        "--output_plot",
        type=str,
        required=True,
        help="Path to write output plot to",
    )

    cmdline = parser.parse_args()

    main(cmdline.input_csv, cmdline.input_gpkg, cmdline.output_plot)
