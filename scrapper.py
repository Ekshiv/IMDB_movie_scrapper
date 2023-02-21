from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
from logClass import scrapLogger


class MovieScrapper:
    
    def __init__(self):

        ## Creating constructor
        self.log= scrapLogger.scrap_logger()
    
    
    def get_movie_details(self):
        ## Scraping code 
        self.log.info("-> Scrapping Module initiated.....")
        self.log.info("-> Parsing IMDB movie site")
        try:
            url = 'http://www.imdb.com/chart/top'
            response = requests.get(url)
            soup= BeautifulSoup(response.text, 'html.parser')
            self.log.info("-> Parsing done successfull !!!")
        except Exception as e:
            self.log.error(f"!! Error while parsing due to error:->\n{e}")

        try:
            self.log.info(f"{'='*60}")
            self.log.info("-> Started scrapping data from Html page....\n")
            # titlebox contain rank, movie_title, and release_date
            titlebox = soup.select('td.titleColumn')
            movie_rank=[c.attrs.get('data-value') for c in soup.select('td.posterColumn span[name=rk]')]
            star_cast = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
            IMDBratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

        except Exception as e:
            self.log.error(f"!! Error while scrapping Html page due to error:->\n{e}")

        try:
            self.log.info("-> Started cleaning and fetching info from scrapped data....\n")
            # m_list to store all movies dict
            m_list=[]

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
                m_list.append(data)
            self.log.info("## Movie details like rank, movie_name, star_cast, year_of_release and IMDBratings has been fetched successfully and stored in m_list of dictionary.\n")
            self.log.info("## Scrapping done successfully !!! ")
            self.log.info(f"{'='*60}\n")
            self.log.info(f"{' '*35}*** E N D ***\n")
            return m_list
        
        except Exception as e:
            self.log.error(f"!! Error while scrapping Html page due to error:->\n{e}")


    def saving_into_csv(self, m_list):
        ## Saving Top 250 movie m_list as Dataframe and CSV format
        try:
            self.log.info("-> Saving movie m_list as Dataframe and CSV file ...")
            
            ## creating dataframe out of m_list
            IMDBmoviem_list= pd.DataFrame(m_list)
            ## changing the dtypes of feature 'Ranking' 'Rating' and 'Year' into numeric
            IMDBmoviem_list["Ranking"]= IMDBmoviem_list.Ranking.astype('int')
            IMDBmoviem_list["Rating"]= IMDBmoviem_list.Rating.astype('float')
            IMDBmoviem_list["Year"]= IMDBmoviem_list.Year.astype('int')
            ## rounding off numbers after decimal for Rating
            IMDBmoviem_list['Rating']= IMDBmoviem_list['Rating'].round(2)
            ## saving to csv format
            csv_file= IMDBmoviem_list.to_csv("Top-250-movies.csv")
            self.log.info("-> Saving file successfully done !!!")
            return csv_file
        except Exception as e:
            self.log.error(f"Error while saving csv-file due to ->: {e}")