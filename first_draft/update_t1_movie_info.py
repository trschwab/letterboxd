import re
import sqlite3
import requests
from utility.utility import *

#from requests import session
from bs4 import BeautifulSoup

def create_movie_db():
	''' takes in a list of movies of format ['movie 1', 'movie2', ... ,'movien']
		populates movie_info table
	'''
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		#execute_task(conn, "drop table if exists t1_movie_info;")
		#execute_task(conn, "drop table if exists movie_info;")
		execute_task(conn, "create table if not exists t1_movie_info (title string, director string, poster string, desc string, cover_image string, studios string, year string, url string, actors string, genre string, country_of_origin string, review_count string, rating_value string, rating_count string, date_added date);")
		#select_all_tasks(conn, "movie_info")
	close_connection(conn)
	return 1

#create_movie_db()

def get_unformatted_info():
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cursor = conn.cursor()
		cursor.execute("select a.url, a.a_info, a.b_info  from t0_movie_info a left join t1_movie_info b on a.url = b.url where b.url is null;")
		
		#cursor.execute("select user.expected_url from " + user_db + " user left join t0_movie_info movie on user.title = movie.title and user.year = movie.year where movie.title is null and movie.year is null;")
		info = cursor.fetchall()
	close_connection(conn)
	return str(info)

#print(list(get_unformatted_info()))

def test_get_list():
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		conn.row_factory = lambda cursor, row: row[0:5]
		c = conn.cursor()
		ids = c.execute('select * from t0_movie_info').fetchall()
	return ids


def get_numbers(s):
	''' takes in a string like
		"test":1532
		or
		"another":4.60
		and returns 1532 and 4.60 respectively
	'''
	allowed = "1234567890."
	r_string = ''
	for i in range(len(s)):
		if s[i] in allowed:
			r_string += s[i]
	return r_string


def parse_movie_info(info):
	''' takes in a string of format:
		* <![CDATA[ */
		{"image":"https://a.ltrbxd.com/resized/film-poster/5/1/9/4/2/51942-three-colors-blue-0-230-0-345-crop.jpg?k
		...
		members.","ratingCount":80845,"worstRating":0}}
		/* ]]> */
		
		and parse out the image, director, organization, year (startdate), cast, genre, rating, ratingCount
	'''

	title = None
	director = None
	poster = None
	description = None
	cover_image = None
	#studio_list
	year = None
	#url
	#actor_list
	#genre_list
	#country_list
	review_count = None
	rating_value = None
	rating_count = None




	#print(info)
	s = info[1]
	b_info = info[2]
	url = info[0]

	b_info = b_info[1:-1].split(", https://")
	description = b_info[0]
	cover_image = "https://" + b_info[1]
	title = (url.split('/')[-2])#.replace('-', ' ')

	
	a = s.split(",")
	
	actor_list = []
	studio_list = []
	genre_list = []
	country_list = []
	#print(a)	
	for i in range(len(a)):
		#if "film-poster" in a[i]:
		if "resized" in a[i]:
			poster = a[i].split("image:")[-1]#[-2]
		elif "/director/" in a[i]:
			director = a[i].split('/')[-2]
		elif "/studio/" in a[i]:
			studio_list += [a[i].split('/')[-2]]
		elif "startDate" in a[i]:
			year = get_numbers(a[i])
		elif "/actor/" in a[i]:
			actor_list += [a[i].split('/')[-2]]
		elif "genre:[" in a[i]:
			#print(a[i])
			j = i
			flag = True
			while flag:
				add_one = a[j].replace("genre:[","").replace("]","")
				if "https" not in add_one and "Country" not in add_one and "name" not in add_one:
					genre_list += [add_one]
				if "]" in a[j + 1]:
					add_two = a[j + 1].replace("genre:[","").replace("]","")
					if "https" not in add_two and "Country" not in add_two and "name" not in add_two:
						genre_list += [add_two]
					#print([a[j + 1].replace("genre:[","").replace("]","")])
					flag = False
				j += 1
		elif "countryOfOrigin" in a[i]:
			j = i
			flag = True
			while flag:
				country_list += [a[j].replace("name:","").replace("}","").replace("]","")]
				if "]" in a[j + 1]:
					country_list += [a[j + 1].replace("name:","").replace("}","").replace("]","")]
					flag = False
				j += 1
		elif "reviewCount" in a[i]:
			review_count = a[i]
		elif "ratingCount" in a[i]:
			rating_count = a[i]
		elif "ratingValue" in a[i]:
			rating_value = a[i]
	
	country_list = country_list[1::2]

	#print(genre_list)

	r_list = [title, director, poster, description, cover_image, studio_list, year, url, actor_list, genre_list, country_list, review_count, rating_value, rating_count]


	return r_list



def format_movie_info(a):
	''' takes in the output from get_a_movie_info() and get_b_movie_info() and formats for sql execution and db entry
	'''
	for i in range(len(a)):
		a[i] = remove_apos(str(a[i]))
		#print(a[i])
	organized = "('" + a[0] + "', '" +  a[1] + "', '" + a[2] + "', '" +  a[3] + "', '" +  a[4] + "', '" + a[5] + "', '" + a[6] + "', '" + a[7] + "', '" + a[8] + "', '" + a[9] + "', '" + a[10] + "', '" + a[11] + "', '" + a[12] + "', '" + a[13] + "'),"
	#print(organized)
	return organized

def remove_apos(s):
	''' takes in a string and removes all ' or "
	'''
	#try escaping instead..
	return str(s).replace("'","").replace('"',"")

def populate_movie_info_sqlite(s):
	''' takes in a list of movies of format ['movie 1', 'movie2', ... ,'movien']
		populates movie_info table
	'''
	s = s[:-1]
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		q = "insert into t1_movie_info(title, director, poster, desc, cover_image, studios, year, url, actors, genre, country_of_origin, review_count, rating_value, rating_count) values" + s + ';'
		execute_task(conn, q)
	close_connection(conn)
	return

def delete_duplicate_rows(table_name):
        database = "./letterbox.db"
        conn = create_connection(database)
        with conn:
                execute_task(conn, "delete from " + table_name + " where rowid not in (select min(rowid) from " + table_name + " group by title, director, poster, desc, cover_image, studios, year, url, actors, genre, country_of_origin);")
                #select_all_tasks(conn, table_name) #would print a select * from the table
        close_connection(conn)

def main_update_t1_movie_info():
	create_movie_db()
	t = test_get_list()
	movies_to_add = ''
	for i in range(len(t)):
		a = parse_movie_info(t[i])
		#print(a)
		new_movie = format_movie_info(a)
		movies_to_add = movies_to_add + new_movie
	populate_movie_info_sqlite(movies_to_add)
	#stupid delete duplicates
	delete_duplicate_rows("t1_movie_info")


#t = test_get_list()
#movies_to_add = ''
#for i in range(len(t)):
#	#print(t[i])
#	a = parse_movie_info(t[i])
#	new_movie = format_movie_info(a)
#	movies_to_add = movies_to_add + new_movie

#populate_movie_info_sqlite(movies_to_add)

main_update_t1_movie_info()

