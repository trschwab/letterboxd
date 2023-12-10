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

    # TODO
    if is_user_in_user_table(user):
        # We only want to fetch new values to update our hydrate for a given user
        # TODO
        print("TODO")
    else:
        r = requests.post("http://127.0.0.1:8000/endpoint/user_table_post/", data={"name": user})
        post_user_into(user)
        # Let's get the data we just posted


    # # We want to update our tables and ingest new data
    # user_df = get_user_diary_info(user)

    # c_names = ["month", "day", "film", "released", "rating", "like", "rewatch", "review", "edityou", "film_url"]  # , "img_url", "small_img_url"]

    # for i in range(len(c_names)):
    #     user_df.rename(columns={ user_df.columns[i]: c_names[i] }, inplace=True)

    # user_df["name"] = user
    r = requests.get("http://127.0.0.1:8000/endpoint/hydrated_data/")
    df = pd.DataFrame(json.loads(r.content))
    user_df = df[df["name"] == user]
    print(user_df)
    print(user_df.columns)
    print(len(user_df))
    movie_list = user_df["film_link"].unique()
    print(movie_list)
    for movie_link in movie_list:
        movie_url = f"https://letterboxd.com/{'/'.join(movie_link.split('/')[2:4])}"
        r = post_a_movie_info(movie_url)
        print(r)

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


    user_df = user_df.head(25)

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
                print(e)
    new.save(f"./image_generation/static/media/{user}.png")


def is_user_in_user_table(user: str) -> bool:
    '''
    Checks to see if a user is already contained within our user_table
    '''
    r = requests.get("http://127.0.0.1:8000/endpoint/user_table/")
    df = pd.DataFrame(json.loads(r.content))
    if user in df["name"].values:
        return True
    return False


def post_user_into(user):
    user_df = get_user_diary_info(user)

    c_names = ["month", "day", "film", "released", "rating", "like", "rewatch", "review", "edityou", "film_url"]  # , "img_url", "small_img_url"]

    for i in range(len(c_names)):
        user_df.rename(columns={ user_df.columns[i]: c_names[i] }, inplace=True)

    user_df.to_csv("expected.csv")
    # explode tuple values into new cols:

    user_df[["month", "month_none"]] = pd.DataFrame(user_df['month'].tolist(), index=user_df.index)
    user_df[["day", "day_none"]] = pd.DataFrame(user_df['day'].tolist(), index=user_df.index)
    user_df[["film", "film_link"]] = pd.DataFrame(user_df['film'].tolist(), index=user_df.index)
    user_df[["released", "released_none"]] = pd.DataFrame(user_df['released'].tolist(), index=user_df.index)
    user_df[["rating", "rating_none"]] = pd.DataFrame(user_df['rating'].tolist(), index=user_df.index)
    user_df[["review", "review_link"]] = pd.DataFrame(user_df['review'].tolist(), index=user_df.index)

    # Convert to dict for iterative processing.. TODO fix this
    dict_df = user_df.to_dict('records')

    for count, item in enumerate(dict_df):
        if item["month"] == '':
            item["month"] = dict_df[count-1]["month"]

    dated_df = pd.DataFrame(dict_df)
    dated_df[["month", "year"]] = dated_df['month'].str.split(' ', expand=True)

    dated_df_dict = dated_df.to_dict('records')

    # Issue posts
    for item in dated_df_dict:
        data = {
        "name": user, 
        "day": item["day"],
        "month": item["month"],
        "year": item["year"],
        "film": item["film"],
        "released": item["released"],
        "rating":  item["rating"],
        "review_link": item["review_link"],
        "film_link" : item["film_link"]
        }

        r = requests.post("http://127.0.0.1:8000/endpoint/hydrated_data_post/", data=data)

    return dated_df


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


### Need to redo imports 
###

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
    try:
        df = get_a_movie_info(url)
        post_df = df[["image", "director", "dateModified", "productionCompany", "releasedEvent", "url",
                    "actors", "dateCreated", "name", "aggregateRating.reviewCount",
                    "aggregateRating.ratingValue", "aggregateRating.ratingCount"]]
        post_df = post_df.rename(columns={"aggregateRating.reviewCount": "reviewCount",
                                        "aggregateRating.ratingValue": "ratingValue",
                                        "aggregateRating.ratingCount": "ratingCount"})
        # We don't want to post a movie that already exists in our endpoint
        get_r = requests.get("http://127.0.0.1:8000/endpoint/movie_table/")
        movie_table = pd.DataFrame(get_r.json())
        post_data = post_df.to_dict('records')[0]
        for k in post_data.keys():
            post_name = post_data["name"]
            post_date = post_data["dateCreated"]
            match = len(movie_table[(movie_table["name"] == post_name) & (movie_table["dateCreated"] == post_date)])
            if match > 0:
                print("Do not post something already in our database")
                return
            post_data[k] = str(post_data[k])
        r = requests.post("http://127.0.0.1:8000/endpoint/movie_table_post/", data=post_data)
        print(r)
        print(r.content)
        return r
    except Exception as e:
        print("FAIL")
        print(url)
        print(e)
        


def main_generate(user):
    if user:
        generate_topster(user)
    return





