from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
from logClass import scrapLogger

## Creating log object for logging
log= scrapLogger.scrap_logger()


## Scraping code 
log.info("-> Scrapping Module initiated.....")
log.info("-> Parsing IMDB movie site")
try:
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)
    soup= BeautifulSoup(response.text, 'html.parser')
    log.info("-> Parsing done successfull !!!")
except Exception as e:
    log.error(f"!! Error while parsing due to error:->\n{e}")

try:
    log.info(f"{'='*60}")
    log.info("-> Started scrapping data from Html page....\n")
    movie_rank=[c.attrs.get('data-value') for c in soup.select('td.posterColumn span[name=rk]')]
    # titlebox contain rank, movie_title, and release_date
    titlebox = soup.select('td.titleColumn')
    star_cast = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    IMDBratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

except Exception as e:
    log.error(f"!! Error while scrapping Html page due to error:->\n{e}")

try:

    log.info("-> Started cleaning and fetching info from scrapped data....\n")
    # list to store all movies dict
    list=[]

    # Extracting year and name of movie
    for index in range(0, len(titlebox)):
        movie_string = titlebox[index].get_text()
        movie_textbox= " ".join(movie_string.split())

        # Extracting release date of movie using regex
        year= re.search('\((.*?)\)', movie_textbox).group(1)

        # Extracting name of movie using regex
        match= re.search(r" [\s\S]+ ", movie_textbox).group()
        movie_name= match.strip()

        # dict for movie details
        data = {"Ranking": movie_rank[index],
        			"Movie": movie_name,
        			"Rating": IMDBratings[index],
        			"Year": year,
        			"Crew": star_cast[index],
        			}
        list.append(data)

    log.info("## Movie details like rank, movie_name, star_cast, year_of_release and IMDBratings has been fetched successfully and stored in list of dictionary.\n")
    log.info("## Srapping done successfully !!! ")
    log.info(f"{'='*60}\n")
    log.info(f"{' '*35}*** E N D ***\n")

except Exception as e:
    log.error(f"!! Error while scrapping Html page due to error:->\n{e}")



## Saving Top 250 movie list as Dataframe and CSV format
try:
    log.info("-> Saving movie list as Dataframe and CSV file ...")
    
    ## creating dataframe out of list
    IMDBmovielist= pd.DataFrame(list)
    ## changing the dtypes of feature 'Ranking' 'Rating' and 'Year' into numeric
    IMDBmovielist["Ranking"]= IMDBmovielist.Ranking.astype('int')
    IMDBmovielist["Rating"]= IMDBmovielist.Rating.astype('float')
    IMDBmovielist["Year"]= IMDBmovielist.Year.astype('int')
    ## rounding off numbers after decimal for Rating
    IMDBmovielist['Rating']= IMDBmovielist['Rating'].round(2)
    ## saving to csv format
    IMDBmovielist.to_csv("Top-250-movies.csv")
    log.info("-> Saving file successfully done !!!")

except Exception as e:
    log.error(f"Error while saving Dataframe due to ->: {e}")
