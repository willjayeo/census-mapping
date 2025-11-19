#!/usr/bin/env python3
"""

Author: William Jay, November 2025
"""

import argparse

from census.nomis_census import Census

AUTHORITY_OF_INTEREST = "Cornwall"
AUTHORITY_FIELD = "MSOA21NM"
CSV_GEOMETRY = "Area"
GPKG_GEOMETRY = "MSOA21NM"


def main(
    csv_path: str,
    gpkg_path: str,
    output_plot: str,
    authorities_to_keep: list[str] = AUTHORITY_OF_INTEREST,
    authority_field: str = AUTHORITY_FIELD,
    csv_geometry_field: str = CSV_GEOMETRY,
    gpkg_geometry_field: str = GPKG_GEOMETRY,
):
    """
    Middle Super Output Area polygons accessed from
    https://www.data.gov.uk/dataset/677a5164-3a9e-4752-b8e6-5744d2b280ec/middle-layer-super-output-areas-december-2021-boundaries-ew-bgc-v3
    """

    # Get Census object
    census = Census(csv_path)

    # This dataset has MSOAs named with the prefix of 'msoa2021:' which needs removing
    # in order to match the MSOA names in the GeoPackage. The following line removes
    # characters to the left of and including ':'
    census.data[csv_geometry_field] = (
        census.data[csv_geometry_field].str.split(":").str.get(1)
    )

    # Map data onto output area polygons
    census.map_data_to_polygons(
        gpkg_path, csv_geometry_field, gpkg_geometry_field, authorities_to_keep
    )

    # Remove unrequired authorities
    census.mapped_data = remove_polygons_by_authority(
        census.mapped_data, authorities_to_keep, authority_field
    )

    fields_of_interest = [
        "UK identity: British only identity",
        "UK identity: English only identity",
        "UK identity: English and British only identity",
        "UK identity: Cornish only identity",
        "UK identity: Cornish and British only identity",
    ]
    total_field = "Total: All usual residents"
    # List to populate new field names with
    percent_fields = []

    for field in fields_of_interest:

        # Calculate field as a percentage of the total per output area
        new_field_name = census.calc_percent_of_variable(field, total_field)
        # Add new field name to list
        percent_fields.append(new_field_name)


# TODO: Make this flexible and handle queries for multiple regions and add to Census class
def remove_polygons_by_authority(
    gdf, authorities_to_keep: list[str], authority_field: str
):
    """
    Remove polygons from self.output_areas GeoDataFrame by inputting a list of aurthority names to keep.
    """

    return gdf[gdf["MSOA21NM"].str.startswith("Cornwall")]


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
