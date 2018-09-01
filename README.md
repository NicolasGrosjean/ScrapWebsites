# Scrap the statistics about RGS AARs

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

## Get the top of replies and views between the 2 last scrapping

Run the following script to get top n threads according to new views and replies between the 
2 latest scrapping dates.

```
python Analysis/Tops.py RGS_AAR.json <n>
python Analysis/Tops.py Paradox_AAR.json <n>
```

*n* is the size of the top (for example 5).

#### Known issue
UnicodeEncodeError: 'charmap' codec can't encode character

In that case, run the analyze in debug mode.
