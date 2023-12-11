import ast

import pandas as pd
import requests

# Deviations? I want to see when a rating of a user varied from a rating of movie by more than 3 points

def get_deviation(joined_table):
    joined_table = joined_table[joined_table["year"] == "2023"]
    mapping = {'×': 0,
               "× ★★★★½": 9,
               "× ★★½": 5,
               "× ★★★★": 8,
               "× ★★★": 6,
               "× ★★★½": 7
               }
    joined_table['numeric_rating'] = joined_table.rating.map(mapping)
    joined_table = joined_table[joined_table["numeric_rating"] != 0]
    joined_table["ratingValue"] = joined_table["ratingValue"].astype('float64')
    joined_table["deviation"] = abs(joined_table["numeric_rating"] - (joined_table["ratingValue"]*2))
    deviation = joined_table[joined_table["deviation"] >= 2.5]
    return deviation[["film", "ratingValue", "numeric_rating", "deviation"]]


# Top production companies?
def get_production_companies(joined_table):
    joined_table = joined_table[joined_table["year"] == "2023"]
    production = joined_table["productionCompany"]
    production_list = list(production)
    production_set = []
    for element in production_list:
        try:
            production_set += ast.literal_eval(element)
        except Exception as e:
            print(e)
            print("director likely NA type")
    df = pd.DataFrame.from_dict(production_set)
    actor_stats = df.groupby(["name"]).size().reset_index(name='counts')
    top_10 = actor_stats.sort_values("counts", ascending=False).head(10)
    return top_10


# Top actors
def get_actors(joined_table):
    joined_table = joined_table[joined_table["year"] == "2023"]
    actors = joined_table["actors"]
    actor_list = list(actors)
    actor_set = []
    for element in actor_list:
        try:
            actor_set += ast.literal_eval(element)
        except Exception as e:
            print(e)
            print("actor likely NA type")
    # print(actor_set)
    df = pd.DataFrame.from_dict(actor_set)
    actor_stats = df.groupby(["name"]).size().reset_index(name='counts')
    top_10 = actor_stats.sort_values("counts", ascending=False).head(10)
    return top_10


# Top Directors?
def get_directors(joined_table):
    joined_table = joined_table[joined_table["year"] == "2023"]
    directors = joined_table["director"]
    director_list = list(directors)
    director_set = []
    for element in director_list:
        try:
            director_set += ast.literal_eval(element)
        except Exception as e:
            print(e)
            print("director likely NA type")
    df = pd.DataFrame.from_dict(director_set)
    actor_stats = df.groupby(["name"]).size().reset_index(name='counts')
    top_10 = actor_stats.sort_values("counts", ascending=False).head(10)
    return top_10


# How many movies did the user watch in 2023?
def get_watch_per_year(df):
    return len(df[df["year"] == "2023"])


def get_reviews_per_year(df):
    return len(df[(df["review_link"] != "None") &
                  (df["year"] == "2023")])


def get_average_rating(df):
    df = df[df["year"] == "2023"]
    mapping = {'×': 0,
               "× ★★★★½": 9,
               "× ★★½": 5,
               "× ★★★★": 8,
               "× ★★★": 6,
               "× ★★★½": 7
               }
    df['numeric_rating'] = df.rating.map(mapping)
    df = df[df["numeric_rating"] != 0]
    return df["numeric_rating"].mean()


def coordinator(user):
    get_r = requests.get("http://127.0.0.1:8000/endpoint/movie_table/")
    movie_table = pd.DataFrame(get_r.json())

    get_r = requests.get("http://127.0.0.1:8000/endpoint/hydrated_data/")
    hyd_table = pd.DataFrame(get_r.json())

    user_info = hyd_table[hyd_table["name"] == user]

    movie_count = get_watch_per_year(user_info)
    print(f"User watched {movie_count} movies in 2023")

    review_count = get_reviews_per_year(user_info)
    print(f"User reviewed {review_count} of those movies in 2023")

    print(f"Only {review_count / movie_count * 100}% of movies watched in 2023 were reviewed")

    average_rating = get_average_rating(user_info)
    print(f"On average, you rated movies at {average_rating} in 2023, excluding the 0 star entries")

    user_info["film_url"] = user_info.apply(lambda x: f"https://letterboxd.com/{'/'.join(x['film_link'].split('/')[2:4])}/", axis=1)

    join_info = pd.merge(user_info, movie_table, how="left", left_on="film_url", right_on="url")

    print("User top watched actors were the following:")
    print(get_actors(join_info))

    print("User top watched directors were the following: ")
    print(get_directors(join_info))

    print("User top watched production companies were the following: ")
    print(get_production_companies(join_info))

    print("User deviated from mainstream ratings: ")
    print(get_deviation(join_info))
