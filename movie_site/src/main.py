from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from PIL import Image, ImageEnhance
import urllib.request
from io import BytesIO
import numpy as np

BASE_URL = "https://letterboxd.com"

def generate_topster(user):
    # Generate topster for user

    user_df = get_user_diary_info(user)

    c_names = ["month", "day", "film", "released", "rating", "like", "rewatch", "review", "edityou", "film_url"]  # , "img_url", "small_img_url"]

    for i in range(len(c_names)):
        user_df.rename(columns={ user_df.columns[i]: c_names[i] }, inplace=True)

    # Sort by rating
    user_df = user_df.sort_values("rating", ascending=False).drop_duplicates('film_url', keep="first")

    # Sort by rating
    # user_df = user_df.sort_values("rating", ascending=False)

    # delete duplicates
    # user_df.drop_duplicates(subset='film', keep="last", inplace=True)


    user_df = user_df.head(25)

    user_df["img_url"] = user_df["film_url"].apply(lambda x: add_img(x))
    user_df["small_img_url"] = user_df["film_url"].apply(lambda x: add_small_img(x))

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
                print(e)
    new.save(f"./image_generation/static/media/{user}.png")


def add_img(x):
    r = requests.get(x)
    soup = BeautifulSoup(r.content)
    img = soup.find("meta", property="og:image")
    return img["content"]

def add_small_img(x):
    try:
        r = requests.get(x)
        soup = BeautifulSoup(r.content)
        s = soup.find("script", attrs={"type": "application/ld+json"})
        split_str = s.string.split("/* <![CDATA[ */")[-1].split("/* ]]> */")[0]
        info = json.loads(split_str)
        return info["image"]
    except Exception as e:
        print(e)
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
    print(diary_url)
    while diary_url:
        # print(diary_url)
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

def main_generate(user):
    if user:
        generate_topster(user)
    return

# main("mamief")