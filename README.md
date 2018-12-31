# Scrap the statistics about RGS AARs

## Installation
Install [Miniconda](https://conda.io/miniconda.html).

Create a conda environment with the following command.

````
conda env create --file environment.yml
````

## Activate the environment to run code
### Windows
````
activate scrap_websites
````

### Linux
````
source activate scrap_websites
````

## Update the data

Run the following command to scrap the RGS and Paradoxwebsite to get the new statistics about the
AARs.

```
cd AAR
scrapy crawl rgs_aar -o ./Data/RGS_AAR.json
scrapy crawl paradox_aar -o ./Data/Paradox_AAR.json
```

## Fix the file

In *Data/RGS_AAR.json* and *Data/Paradox_AAR.json*, search the line with **][**,
remove it and add a comma at the end of the previous line.

## Write the top of replies and views between the 2 last scrapping

Run the following script to get top n threads according to new views and replies between the 
2 latest scrapping dates.

```
python Analysis/Tops.py RGS_AAR.json <n>
python Analysis/Tops.py Paradox_AAR.json <n>
```

*n* is the size of the top (for example 10).

The results are written in the ARR/Results/RGS and ARR/Results/Paradox directories

## Write the top of replies and views for the latest year

Run the following script to get top n threads according to new views and replies in latest year.

```
python Analysis/Tops.py RGS_AAR.json <n> --year
python Analysis/Tops.py Paradox_AAR.json <n> --year
```

*n* is the size of the top (for example 100).

The results are written in the ARR/Results/RGS and ARR/Results/Paradox directories
