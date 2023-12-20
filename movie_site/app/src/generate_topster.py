from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from PIL import Image, ImageEnhance
import urllib.request
from io import BytesIO
import numpy as np
import os
from config import ROOT
import logging

BASE_URL = "https://letterboxd.com"

def generate_topster(user):
    # Generate topster for user
    # Read in our hydrated data
    r = requests.get(f"{ROOT}endpoint/hydrated_data/", auth=('username1', 'password1'))
    df = pd.DataFrame(json.loads(r.content))
    user_df = df[df["name"] == user]


    ###
    ### This is where we want to update the movie table
    ### post_a_movie_info(movie_url)
    ###

    # Sort by rating
    user_df = user_df.sort_values("rating", ascending=False).drop_duplicates('film_link', keep="first")

    # Sort by rating
    # user_df = user_df.sort_values("rating", ascending=False)

    # delete duplicates
    # user_df.drop_duplicates(subset='film', keep="last", inplace=True)

    # We want to use the top 25 rated movies, but we need to remove duplicate movies that have the same rating
    user_df = user_df.drop_duplicates(["film_link", "rating"])
    user_df = user_df.head(25)
    # if we want variability for our topster, we'd want to shuffle it by groups
    # That imnplementation would probably be answered here
    # https://stackoverflow.com/questions/45585860/shuffle-a-pandas-dataframe-by-groups

    # Terrible logic here
    # New film_link references the user review page, so the username is appended at the start
    # and if it's a re watch then there are "2/" ints appended at the end
    # For now we just grab the middle of that string, but this film_link val should really be fixed in the future
    user_df["img_url"] = user_df["film_link"].apply(lambda x: add_img("/".join(x.split("/")[2:4])))
    user_df["small_img_url"] = user_df["film_link"].apply(lambda x: add_small_img("/".join(x.split("/")[2:4])))

    head_test = user_df

    a_list = list(head_test["small_img_url"])

    b_list = np.reshape(a_list, (-1, 5))

    new = Image.new("RGBA", (1150,1725))
    for row in range(len(b_list)):
        for col in range(len(b_list[row])):
            try:
                response = requests.get(b_list[row][col])
                img = Image.open(BytesIO(response.content))
                img = img.resize((230,345))
                new.paste(img, (col * 230, row * 345))
            except Exception as e:
                logging.info(e)
    new.save(f"./image_generation/static/media/{user}.png")

def add_img(x):
    r = requests.get(f"https://letterboxd.com/{x}")
    soup = BeautifulSoup(r.content)
    img = soup.find("meta", property="og:image")
    return img["content"]

def add_small_img(x):
    try:
        r = requests.get(f"https://letterboxd.com/{x}")
        soup = BeautifulSoup(r.content)
        s = soup.find("script", attrs={"type": "application/ld+json"})
        split_str = s.string.split("/* <![CDATA[ */")[-1].split("/* ]]> */")[0]
        info = json.loads(split_str)
        return info["image"]
    except Exception as e:
        logging.info(e)
        return None

def gen_film_url(a_str):
    return f"https://letterboxd.com/film/{a_str[1].split('/')[3]}/"


def get_diary(a_user):
    return f"{BASE_URL}/{a_user}/films/diary/"

def get_user_diary_info(a_user):
    '''
    returns a DF of a user's diary information

    # TOOD need to be able to handle users that do not exist
    '''
    df_list = []
    # Get diary URL
    diary_url = get_diary(a_user)
    while diary_url:
        r = requests.get(diary_url)
        soup = BeautifulSoup(r.content)

        # Extract the table as a df
        table = soup.find_all('table')
        df_list.append(pd.read_html(str(table), extract_links="all")[0])

        # Find out if there are any subsequent pages
        older_link = soup.find_all("a", text="Older")

        if older_link:
            new_page = older_link[0]['href']
            diary_url = f"{BASE_URL}{new_page}"
        else:
            diary_url = False
    return_df = pd.concat(df_list)

    return_df["film_url"] = return_df[('Film', None)].apply(lambda x: gen_film_url(x))

    return return_df


def main_generate(user, assert_generation=False):
    # We want to check to see if a topster already exists.
    # If this gets called and assert_generation is True we will generate an image
    if assert_generation == False:
        if os.path.isfile(f"./image_generation/static/media/{user}.png"):
            return
    if user:
        # We need to ensure there is data to generate topster here
        # If for example, we hit a user that is not in our database here an empty PNG gets generated
        generate_topster(user)
    return
