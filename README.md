# Scrap the statistics about RGS AARs

## Update the data

Run the following command to scrap the RGS website to get the new statistics about the
"Récits de parties".

```
cd RGS
scrapy crawl recits_parties -o ./Data/Recits_parties.json
```

## Fix the file

In *Data/Recits_parties.json*, search the line with ][,
remove it and add a comma at the end of the previous line.
