import json
import logging

import pandas as pd
import requests


def is_valid_user(user: str) -> bool:
    '''
    Returns True if the user string is a valid letterboxd user
    '''
    # TODO
    return True


def get_user_set() -> list:
    '''
    Gets all users currently in our system
    '''
    test_url = "http://host.docker.internal:8000/endpoint/user_table/"
    original_test_url = "http://127.0.0.1:8000/endpoint/user_table/"
    r = requests.get(test_url)
    logging.info("Request status code: %s", r.status_code)
    df = pd.DataFrame(json.loads(r.content))
    return df["name"].unique()