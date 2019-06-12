# Lyrics Classifier & Scraper
Lyrics Predictor that adjudicates lyrical input from the user to pop songs from the 90s along with a link to the song. The application runs on a Flask server that interacts with a model that uses CountVectorisation, Tf-idf Transform and a Multinomial Naïve Bayes Classifier to make predictions. The model is not trained on a large corpus, therefore the predictions the model gives are not optimal. This project was mainly created to get a Machine Learning project up and running on Flask, with a presentable interface that is hosted online.


[Link to the Hosted Application](http://nicolaiai.pythonanywhere.com/)


## Using the Scraping Part of the Application
With the scraping part of the application it is possible to directly get lyrics of your choosing onto your computer in clean, individual text files.

In order to do this:

1. **Clone** this repository.
2. Run "**lyric_retrieval.py**".
3. Your IDE or command line will ask you if you want to **input your own list of artists** or retrieve a standard list.
4. Enter how many songs you would like to scrape per individual artist.
5. The script will create a directory in the same folder as the local repository and tell you what this directory is called.
6. The script will start to scrape the lyrics from Lyrics.com, show you which songs are being scraped, and where they are stored once the scraping is finished.
7. You now have clean text files of the lyrics of your chosen artists!
