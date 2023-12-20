import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import ROOT


def get_page(url):
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def get_a_movie_info(url: str) -> pd.DataFrame:
    '''
    Takes in a movie URL like "https://letterboxd.com/film/goon/"
    return the Dataframe of the movie's info
    '''
    soup = get_page(url)
    i = 0
    begin = 0
    end = 0
    for item in str(soup).split('\n'):
        if ("* <![CDATA[ */" in item):
            begin = i
        if ("/* ]]> */" in item):
            end = i + 1
        i += 1
    info_list = [str(soup).split('\n')[begin:end], url]
    movie_df = pd.json_normalize(json.loads(info_list[0][1]))
    return movie_df


def post_a_movie_info(url: str):
    '''
    actually posts movie info to our endpoint
    '''
    df = get_a_movie_info(url)
    post_df = df[["image", "director", "dateModified", "productionCompany", "releasedEvent", "url",
                  "actors", "dateCreated", "name", "aggregateRating.reviewCount",
                  "aggregateRating.ratingValue", "aggregateRating.ratingCount"]]
    post_df = post_df.rename(columns={"aggregateRating.reviewCount": "reviewCount",
                                      "aggregateRating.ratingValue": "ratingValue",
                                      "aggregateRating.ratingCount": "ratingCount"})
    post_data = post_df.to_dict('records')[0]
    for k in post_data.keys():
        post_data[k] = str(post_data[k])
    r = requests.post(f"{ROOT}endpoint/movie_table_post/", data=post_data, auth=('username1', 'password1'))
    return r


# columns:
# Index(['image', '@type', 'director', 'dateModified', 'productionCompany',
#        'releasedEvent', '@context', 'url', 'actors', 'dateCreated', 'name',
#        'genre', '@id', 'countryOfOrigin', 'aggregateRating.bestRating',
#        'aggregateRating.reviewCount', 'aggregateRating.@type',
#        'aggregateRating.ratingValue', 'aggregateRating.description',
#        'aggregateRating.ratingCount', 'aggregateRating.worstRating'],
#       dtype='object')
