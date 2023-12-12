import requests
import json
import pandas as pd
import logging
from bs4 import BeautifulSoup

BASE_URL = "https://letterboxd.com"


def is_user_in_user_table(user: str) -> bool:
    '''
    Checks to see if a user is already contained within our user_table
    '''
    r = requests.get("http://127.0.0.1:8000/endpoint/user_table/", auth=('username1', 'password1'))
    df = pd.DataFrame(json.loads(r.content))
    if user in df["name"].values:
        return True
    return False


def get_user_data(user: str) -> pd.DataFrame:
    '''
    Gets a df of user data ready to be posted to our model
    '''
    user_df = get_user_diary_info(user)

    c_names = ["month", "day", "film", "released", "rating", "like", "rewatch", "review", "edityou", "film_url"]  # , "img_url", "small_img_url"]

    for i in range(len(c_names)):
        user_df.rename(columns={ user_df.columns[i]: c_names[i] }, inplace=True)

    # user_df.to_csv("expected.csv")
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

    dated_df["name"] = user

    dated_df = dated_df[[
        "name",
        "day",
        "month",
        "year",
        "film",
        "released",
        "rating",
        "review_link",
        "film_link"]]

    return dated_df


def post_user_into(user_info):
    print(user_info)
    print(user_info.columns)
    # dated_df = get_user_data(user)

    user_info_dict = user_info.to_dict('records')

    # # Issue posts
    # for item in dated_df_dict:
    #     data = {
    #     "name": user, 
    #     "day": item["day"],
    #     "month": item["month"],
    #     "year": item["year"],
    #     "film": item["film"],
    #     "released": item["released"],
    #     "rating":  item["rating"],
    #     "review_link": item["review_link"],
    #     "film_link" : item["film_link"]
    #     }


    for item in user_info_dict:
        for key in item.keys():
            # We need to make sure all our data types abide by what the serializer expects
            # So if a user does not post a review and that field is None, it cannot be a nonetype
            item[key] = str(item[key])
        print("ATTEMPT TO POST:")
        print(item)
        r = requests.post("http://127.0.0.1:8000/endpoint/hydrated_data_post/", data=item, auth=('username1', 'password1'))
        print(item["film"])
        print(r)

    return


def post_a_movie_info(url: str):
    '''
    actually posts movie info to our endpoint
    '''
    # We don't want to post a movie that already exists in our endpoint
    # TODO this takes way too long to check on a per URL basis
    # TODO We need to switch to a join so that we immediately know exactly which
    # TODO records we need to insert and can do that in a bulk action
    get_r = requests.get("http://127.0.0.1:8000/endpoint/movie_table/", auth=('username1', 'password1'))
    movie_table = pd.DataFrame(get_r.json())
    # Maybe we want to hand this a url with a backslash already on the end? Something to think about
    if f"{url}/" in movie_table["url"].unique():
        logging.info("Cannot insert duplicate %s into movie table", url)
        return
    try:
        df = get_a_movie_info(url)
        post_df = df[["image", "director", "dateModified", "productionCompany", "releasedEvent", "url",
                    "actors", "dateCreated", "name", "aggregateRating.reviewCount",
                    "aggregateRating.ratingValue", "aggregateRating.ratingCount"]]
        post_df = post_df.rename(columns={"aggregateRating.reviewCount": "reviewCount",
                                        "aggregateRating.ratingValue": "ratingValue",
                                        "aggregateRating.ratingCount": "ratingCount"})
        
        post_data = post_df.to_dict('records')[0]
        for k in post_data.keys():
            # post_name = post_data["name"]
            # post_date = post_data["dateCreated"]
            # match = len(movie_table[(movie_table["name"] == post_name) & (movie_table["dateCreated"] == post_date)])
            # if match > 0:
            #     print("Do not post something already in our database")
            #     return
            post_data[k] = str(post_data[k])
        r = requests.post("http://127.0.0.1:8000/endpoint/movie_table_post/", data=post_data, auth=('username1', 'password1'))
        print(r)
        print(r.content)
        return r
    except Exception as e:
        print("FAIL")
        print(url)
        print(e)

def get_user_diary_info(a_user):
    '''
    returns a DF of a user's diary information

    # TOOD need to be able to handle users that do not exist
    '''
    print(a_user)
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


def get_diary(a_user):
    return f"{BASE_URL}/{a_user}/films/diary/"


def gen_film_url(a_str):
    return f"https://letterboxd.com/film/{a_str[1].split('/')[3]}/"

def get_page(url):
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup