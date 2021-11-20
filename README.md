# First Responder Sites

## Running the visualization

* [Click here to start the interactive D3 visualization](https://github.gatech.edu/pages/cse6242TeamDataWranglers/firstrespondersites/visualization/)

## Running code from this repository

**The recommended setup uses MacOS / Linux operating systems, Windows has not been tested**

1. Setup the conda environment using the conda_env.yml and Python version 3.8.11.  
2. Clone the repository
3. Download the [SQLite database](https://gtvault-my.sharepoint.com/:u:/g/personal/manderson334_gatech_edu/EUCVCElcpSFLswnJB7sPHowB0fpm7eIoBumUq0avyfNFIw?e=lFwjYc) that we've compiled for this project **into the "/data" subdirectory** of the cloned repository.

## Repository Overview

* **[data.md](data.md)** - Descriptions and sources of data used in this project, and the schema for the SQLite file.

* **data/** - Scripts to load and prepare data the analytics database (SQLite file)
  * *query_travel_times.py* - fetches travel times (including estimated traffic impacts) between points in San Francisco from the BingMaps API.  Requires a Bing Maps Developer API key to be stored in the data/.bingapikey file.
  * *import_data.py* - prepares the SQLite database from the flat files and sources described in data.md.

* **notebooks/** - Python notebooks for modeling work
  * *2SFCA* - Does all the heavy-lifting for modeling work.  The **outputs of this notebook are provided for interactive visualization by the d3 tool in the visualization/ directory**.  This notebook performs the spatial statistics modeling, including **kernel density estimates** and **two-step floating catchment algorithm (2SFCA)**.  

* **visualization/** - Visualization of the modeling work

## Team Members:
* Jude Yakamavage
* Dalton Schling
* Mike McPhee Anderson (manderson334)
* Eric Fitchwell
* Mike Good
* Everton Sehnem
