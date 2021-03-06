# First Responder Sites

## Running the visualization

* [Click here to start the interactive D3 visualization](https://github.gatech.edu/pages/cse6242TeamDataWranglers/firstrespondersites/visualization/)

## Running code from this repository

**Create a conda environment**

1. Make sure the conda package manager is installed and run the following command to create a new environment with all the required dependencies.
```
> conda env create -f env.yml
```
2. Clone the repository
3. Download the [SQLite database](https://gtvault-my.sharepoint.com/:u:/g/personal/manderson334_gatech_edu/EUCVCElcpSFLswnJB7sPHowB0fpm7eIoBumUq0avyfNFIw?e=lFwjYc) that we've compiled for this project **into the "/data" subdirectory** of the cloned repository.  You need to **unzip** this file.
4. Download the [raw data files](https://gtvault-my.sharepoint.com/:f:/g/personal/manderson334_gatech_edu/EqrEYtMOW6dGt85xNxecW4sBhDtIylYJRO3Lne_itGbo2Q?e=ejda7p), and unzip into the data/raw folder, so that the files are located in `data/raw` (not `data/raw/<some subfolder>`).  For example, the file `\data\raw\SF Find Neighborhoods.geojson` should exist relative to the project root directory.
5. To run the notebooks, activate the ```geo``` conda environment and run ```jupyter notebook```.
```
> conda activate geo
> cd <to the root of the cloned repository>
> jupyter notebook
```

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
