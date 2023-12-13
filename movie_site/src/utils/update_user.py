import requests
import pandas as pd
import json
from .utils import is_user_in_user_table, get_user_data, post_user_into, post_a_movie_info
from .generate_topster import main_generate
import logging

def update_user(user: str):
    '''
    Given a user we should create their data if they're new to the system or
    update their data if they're already 
    '''
    try:
        # Read in our hydrated data
        r = requests.get("http://127.0.0.1:8000/endpoint/hydrated_data/", auth=('username1', 'password1'))
        df = pd.DataFrame(json.loads(r.content))
    except Exception as e:
        logging.info("Table probably empty")
        logging.info(e)

    if is_user_in_user_table(user):
        # get full user data from lbox
        full_user_data = get_user_data(user)
        full_user_data = full_user_data[[
            "name",
            "day",
            "month",
            "year",
            "film",
            "released",
            "rating",
            "review_link",
            "film_link"]]
        # limit our db to that user
        our_user_data = df[df["name"] == user]
        our_user_data = our_user_data[[
            "name",
            "day",
            "month",
            "year",
            "film",
            "released",
            "rating",
            "review_link",
            "film_link"]]

        # we have to do this to find difference
        # each time you watch a film a new film_link is generated
        # covers instances when you can watch the same film on the same day with different ratings
        # and reviews and details
        difference = full_user_data[~(full_user_data["film_link"]).isin(our_user_data["film_link"].unique())]
        post_user_into(difference)
    else:
        full_user_data = get_user_data(user)
        full_user_data = full_user_data[[
            "name",
            "day",
            "month",
            "year",
            "film",
            "released",
            "rating",
            "review_link",
            "film_link"]]
        r = requests.post("http://127.0.0.1:8000/endpoint/user_table_post/", data={"name": user}, auth=('username1', 'password1'))
        post_user_into(full_user_data)
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
    
    # Generate a topster for our user:
    main_generate(user, True)

    return


def is_valid_username(username):
    '''
    Checks to see if a username exists with letterboxd
    '''
    url = f"https://letterboxd.com/{username}/"
    r = requests.get(url)
    if r.status_code == 200:
        logging.info("Valid username supplied")
        return True
    logging.info("Invalid username supplied")
    return False
