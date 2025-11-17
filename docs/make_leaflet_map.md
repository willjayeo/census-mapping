# `make_leaflet_map.py

Create a choropleth [Leaflet](https://leafletjs.com/) map from a graduated census data field.

## Usage

```
usage: make_leaflet_map.py [-h] --input_csv INPUT_CSV --input_gpkg INPUT_GPKG --output_map OUTPUT_MAP
                           --variable VARIABLE [--percent_variable PERCENT_VARIABLE]

options:
  -h, --help            show this help message and exit
  --input_csv INPUT_CSV
                        Unix-style glob to CSV files downloaded from NOMIS
  --input_gpkg INPUT_GPKG
                        Path to GeoPackage file containing census Output Area features
  --output_map OUTPUT_MAP
                        Path to write output HTML map to
  --variable VARIABLE   Name of CSV field to map
  --percent_variable PERCENT_VARIABLE
                        Name of CSV field to calculate the percentage of --variable from, optional
```

## Examples:

1) Percent of people born in Europe

```
~/code/census-mapping/scripts/make_leaflet_map.py --input_csv data/census_plymouth/ts004_country-of-birth_plymouth.csv --input_gpkg data/census_plymouth/Output_Areas_2021_plymouth.gpkg --output_map /tmp/born_in_europe_percent_map.html --variable 'Europe' --percent_variable 'Total: All usual residents'
```

[Output Map](./maps/born_in_europe_percent_map.html)

2) Percent of people identifying with no religion

```
~/code/census-mapping/scripts/make_leaflet_map.py --input_csv data/census_plymouth/ts030_religion_plymouth.csv --input_gpkg data/census_plymouth/Output_Areas_2021_plymouth.gpkg --output_map /tmp/no_religion_percent_map.html --variable 'No religion' --percent_variable 'Total: All usual residents'
```

[Output Map](./maps/no_religion_percent_map.html)

