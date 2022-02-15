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
		#execute_task(conn, "drop table if exists t0_movie_info;")
		#execute_task(conn, "drop table if exists movie_info;")
		execute_task(conn, "create table if not exists t0_movie_info (url string, a_info string, b_info string, c_info string, date_added date);")
		#select_all_tasks(conn, "movie_info")
	close_connection(conn)
	return 1

#create_movie_db()

def get_unformatted_diary_info(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	user_db = username + "_diary"
	with conn:
		cursor = conn.cursor()
		cursor.execute("select user.expected_url from " + user_db + " user left join t0_movie_info movie on user.expected_url = movie.url where movie.url is null;")
		
		#cursor.execute("select user.expected_url from " + user_db + " user left join t0_movie_info movie on user.title = movie.title and user.year = movie.year where movie.title is null and movie.year is null;")
		info = cursor.fetchall()
	close_connection(conn)
	return str(info)

#print(get_unformatted_diary_info("marvelfan69"))

def format_diary_urls(a):
	''' takes in the urls from diary not in movie info (based on title and year)
		formats them into a list
	'''
	a = str(a).replace(",), (", '\n').replace("(","").replace(")","").replace("'","").replace(",","").replace("]","").replace("[","")
	a = a.split('\n')
	#print(a)
	return a
		
def get_a_movie_info(url):
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
	return [str(soup).split('\n')[begin:end], url]

	
def get_b_movie_info(url):
	soup = get_page(url)
	#title = str(soup.find_all(property="og:title"))
	desc = str(soup.find_all(property="og:description"))
	cover_image = str(soup.find_all(property="og:image"))
	#title = title.split('"')[1][:-7]
	desc = desc.split('"')[1]
	cover_image = cover_image.split('"')[1]
	#r_list = [remove_apos(title), remove_apos(desc), remove_apos(cover_image)]
	r_list = [remove_apos(desc), remove_apos(cover_image)]
	#print("b movie info")
	#print(r_list)
	return str(r_list)

def populate_movie_info_sqlite(a, b, c):
	''' takes in a list of movies of format ['movie 1', 'movie2', ... ,'movien']
		populates movie_info table
	'''
	a = remove_apos(str(a))
	b = remove_apos(str(b))
	c = remove_apos(str(c))
	s = "('" + a + "', '" + b + "', '" + c + "', date('now'))"
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		q = "insert into t0_movie_info(url, a_info, b_info, date_added) values" + s + ';'
		#print(q)
		execute_task(conn, q)
	close_connection(conn)
	return

def remove_apos(s):
	''' takes in a string and removes all ' or "
	'''
	#try escaping instead..
	return str(s).replace("'","").replace('"',"")

def check_movie_info():
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		select_all_tasks(conn, "t0_movie_info")
	close_connection(conn)

def check_titles():
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		cur.execute("select count(*) from t0_movie_info;")
		rows = cur.fetchall()
	for row in rows:
		print(row)
	return 1

#urls = get_unformatted_diary_info("marvelfan69")
#urls = get_unformatted_diary_info("trschwab")
#urls = get_unformatted_diary_info("_jelvin")
#valid_pages = format_diary_urls(urls)

#print(valid_pages)

#if valid_pages != ['']:
#	for i in range(len(valid_pages)):
#		test_url = valid_pages[i]
		#print(test_url)
#		a = get_a_movie_info(test_url)
		#some_info = parse_a_movie_info(a)
#		b = get_b_movie_info(test_url)
		#formatted_info = format_movie_info(some_info, other_info)
		#print(a)
		#print(b)
		#print(test_url)
#		populate_movie_info_sqlite(test_url, a, b)

#check_movie_info()
#check_titles()


def main_update_t0_movie_info(username):
	''' takes in a username
		(assuming the username has a relative [username]_diary database created)
	'''
	create_movie_db()
	urls = get_unformatted_diary_info(username)
	valid_pages = format_diary_urls(urls)
	if valid_pages != ['']:
		for i in range(len(valid_pages)):
			test_url = valid_pages[i]
			a = get_a_movie_info(test_url)
			b = get_b_movie_info(test_url)
			populate_movie_info_sqlite(test_url, a, b)

#main("_jelvin")
#main("trschwab")
#main("marvelfan69")
#main("davidehrlich")
