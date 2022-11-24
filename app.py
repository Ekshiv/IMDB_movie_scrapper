from logClass import scrapLogger
from scrapper import MovieScrapper
from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app= Flask(__name__)

log= scrapLogger.scrap_logger()
scrape_obj= MovieScrapper().get_movie_details()
# download_obj= MovieScrapper().saving_into_csv(scrape_obj)

@cross_origin()
@app.route('/', methods=['GET'])
def homePage():
    try:
        print("App running fine ....")
        return render_template("homepage.html")
    except Exception as e:
        print(e)

@cross_origin()
@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        print("Scrape is working and results are shown !!!")
        return render_template("result.html", m_list=scrape_obj)
    except Exception as e:
        print(e)

# @app.route('/saving', methods=['GET'])
# def save_file():
#     try:
#         return render_template('result.html', download_obj=download_obj)
#     except Exception as e:
#         print(e)

if __name__== "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
