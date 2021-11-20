# First Responder Sites

## Running code from this repository

**The recommended setup uses MacOS / Linux operating systems, Windows has not been tested**

1. Setup the conda environment using the conda_env.yml and Python version 3.8.11.  
2. Clone the repository
3. Download the [SQLite database](https://gtvault-my.sharepoint.com/:u:/g/personal/manderson334_gatech_edu/EUCVCElcpSFLswnJB7sPHowB0fpm7eIoBumUq0avyfNFIw?e=lFwjYc) that we've compiled for this project **into the "/data" subdirectory** of the cloned repository.

## Repository Overview

* **[data.md](data.md)** - Descriptions and sources of data used in this project, and the schema for the SQLite file.

* **data/** - Scripts to load and prepare data the analytics database (SQLite file)
 * *query_travel_times.py* fetches travel times (including estimated traffic impacts) between points in San Francisco from the BingMaps API.  Requires an API key.
 * *import_data.py* prepares the SQLite database from 

* **notebooks/**
 * *2SFCA Response Time Correlations.ipynb* - Modeling work for the kernel density estimates and Two-step floating catchment algorithm (2SFCA)

## Team Members:
* Jude Yakamavage
* Dalton Schling
* Mike McPhee Anderson (manderson334)
* Eric Fitchwell
* Mike Good
* Everton Sehnem
