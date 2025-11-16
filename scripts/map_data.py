#!/usr/bin/env python3

import argparse
import folium

import pandas as pd

# TODO: Make this a proper package
from nomis_census import Census


def main(csv_glob: str, output_map: str):
    """ """

    # Get Census object
    census_data = Census(csv_glob)


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
        "--output_map",
        type=str,
        required=True,
        help="Path to write output HTML map to",
    )

    cmdline = parser.parse_args()

    main(cmdline.input_csv, cmdline.output_map)
