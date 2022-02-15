from update_t0_movie_info import *
from update_t1_movie_info import *
from populate_user_diary import *


#username = "nrg004"
#username = "trschwab"
#username = "marvelfan69"
#username = "_jelvin"
#username = "grahamgearhart"
#username = "captainronfan44"
#username = "jlucien"
username = "timco"

def set_up(username):
	main_populate_user_diary(username)
	main_update_t0_movie_info(username)	
	main_update_t1_movie_info()
	#main_create_user_genre()

#def get_top_directors(username):

set_up(username)
