DESCRIPTION

INSTALLATION

** python environment **
    1. download and install anaconda
    2. setup a conda environment using the below code
        > cd CODE
        > conda env create -f env.yml
    Troubleshooting:
        If the script fails ensure that you are using Python 3.9.7 in your conda env and the latest
        version of conda.  The geospatial extensions to pandas has extensive binary dependencies, 
        and we've experienced sporadic platform-specific issues installing them.

For the downloads below, be sure you are logged into your Georgia Tech account for OneDrive / Microsoft.
If you have problems, please contact me manderson334@gatech.edu 

** data scripts (/data/*.py) **
    1. download the raw data files: https://gtvault-my.sharepoint.com/:u:/g/personal/manderson334_gatech_edu/ETCk3Ey_l41Li4T-14fe6VMBWlDFLkEYGgcfSNXvofvDEg?e=bwAe8T
    2. Register for a bing maps API developer account (https://www.bingmapsportal.com/.  Create a new API key and copy it into "/data/.bingapikey"

** notebooks **
    1. download the SQLite database (v5): https://gtvault-my.sharepoint.com/:u:/g/personal/manderson334_gatech_edu/EVnVHSvdyo5FtSR-KQUh-J8BlvCaycqBEWYNy9luH4gpcA?e=d5MFcC
    2. Run the following commands
        > conda activate geo
        > conda install jupyter
        > cd <to the CODE/notebooks directory>
        > jupyter notebook

** visualization **
    1. ensure that your python environment has the http.server module installed.  You can test this as follows:
        > python -m http.server 8080

EXECUTION

** data scripts **
    1. 


