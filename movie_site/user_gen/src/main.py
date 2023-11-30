import pandas as pd
from utils import is_valid_user, get_user_set

def main(user: str) -> int or None:
    '''
    Given a username we should populate our endpoint with it
    '''
    print(user)
    # We need to ensure that user is a valid username
    if not is_valid_user(user):
        return -1
    user_list = get_user_set()
    if user in user_list:
        # If user is already in our system we need to update
        print("User is already in our system")
    else:
        # If user is not in our system we need to fully create it
        print("User not in our system")
    return

main("trschwab")
