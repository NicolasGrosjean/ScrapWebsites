# Scrap the statistics about RGS AARs

## Update the data

Run the following command to scrap the RGS website to get the new statistics about the
AARs.

```
cd RGS
scrapy crawl recits_parties -o ./Data/Recits_parties.json
```

## Fix the file

In *Data/Recits_parties.json*, search the line with ][,
remove it and add a comma at the end of the previous line.

## Get the top of replies and views between the 2 last scrapping

Run the following script to get top n threads according to new views and replies between the 
2 latest scrapping dates.

```
python Analysis/Tops.py <n>
```

*n* is the size of the top (for example 5).
