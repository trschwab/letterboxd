import re
import sqlite3
import requests
import statistics

from utility.utility import *

def get_genres(username):
	all_genres = ''
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = "select genre from (select distinct * from " + username + "_diary a join t1_movie_info b on a.expected_url = b.url where a.view_str like '%2021') a;"
		cur.execute(q)
		rows = cur.fetchall()
	rows = str(rows)
	for i in range(len(rows)):
		if rows[i] in " asdfghjklzxcvbnmqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM":
			all_genres += rows[i]
			
	all_genres = all_genres.split(" ")

	all_genres_unique = []
	for i in range(len(all_genres)):
		if all_genres[i] not in all_genres_unique:
			all_genres_unique += [all_genres[i]]
	
	#print(all_genres_unique)

	occur = []
	for i in range(len(all_genres_unique)):
		occur += [[all_genres.count(all_genres_unique[i]), all_genres_unique[i]]]
	
	#print(occur)
	top = 0
	store = []
	for i in range(len(occur)):
		if occur[i][0] > top:
			#print(top)
			top = occur[i][0]
			#print(top)
			store = [occur[i]]
		elif occur[i][0] == top:
			store += [occur[i]]

	#print(store)

	top_two = 0
	store_two = []
	for i in range(len(occur)):
		if occur[i][0] > top_two and occur[i][0] < top:
			top_two = occur[i][0]
			store_two = [occur[i]]
		elif occur[i][0] == top_two:
			store_two += [occur[i]]
	#print(store_two)
	a_format(store + store_two)

	return 1



def get_actors(username):
	all_genres = ''
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = "select actors from (select distinct * from " + username + "_diary a join t1_movie_info b on a.expected_url = b.url where a.view_str like '%2021') a;"
		cur.execute(q)
		rows = cur.fetchall()
	rows = str(rows)
	for i in range(len(rows)):
		if rows[i] in " asdfghjklzxcvbnmqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM123456789-":
			all_genres += rows[i]
			
	all_genres = all_genres.split(" ")

	all_genres_unique = []
	for i in range(len(all_genres)):
		if all_genres[i] not in all_genres_unique:
			all_genres_unique += [all_genres[i]]
	
	#print(all_genres_unique)

	occur = []
	for i in range(len(all_genres_unique)):
		occur += [[all_genres.count(all_genres_unique[i]), all_genres_unique[i]]]
	
	#print(occur)

	top = 0
	store = []
	for i in range(len(occur)):
		if occur[i][0] > top:
			#print(top)
			top = occur[i][0]
			#print(top)
			store = [occur[i]]
		elif occur[i][0] == top:
			store += [occur[i]]

	#print(store)
	#print(store)
	#a_format(store)

	top_two = 0
	store_two = []
	for i in range(len(occur)):
		if occur[i][0] > top_two and occur[i][0] < top:
			top_two = occur[i][0]
			store_two = [occur[i]]
		elif occur[i][0] == top_two:
			store_two += [occur[i]]
	a = store + store_two
	a_format(a)

	
	return 1

def get_countries(username):
	all_genres = ''
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = "select country_of_origin from (select distinct * from " + username + "_diary a join t1_movie_info b on a.expected_url = b.url where a.view_str like '%2021') a;"
		cur.execute(q)
		rows = cur.fetchall()
	rows = str(rows)
	for i in range(len(rows)):
		if rows[i] in " asdfghjklzxcvbnmqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM123456789-":
			all_genres += rows[i]
			
	all_genres = all_genres.split(" ")

	all_genres_unique = []
	for i in range(len(all_genres)):
		if all_genres[i] not in all_genres_unique:
			all_genres_unique += [all_genres[i]]
	
	#print(all_genres_unique)

	occur = []
	for i in range(len(all_genres_unique)):
		occur += [[all_genres.count(all_genres_unique[i]), all_genres_unique[i]]]
	
	#print(occur)

	top = 0
	store = []
	for i in range(len(occur)):
		if occur[i][0] > top:
			#print(top)
			top = occur[i][0]
			#print(top)
			store = [occur[i]]
		elif occur[i][0] == top:
			store += [occur[i]]

	#print(store)

	top_two = 0
	store_two = []
	for i in range(len(occur)):
		if occur[i][0] > top_two and occur[i][0] < top:
			top_two = occur[i][0]
			store_two = [occur[i]]
		elif occur[i][0] == top_two:
			store_two += [occur[i]]
	#print(store_two)

	a_format(store + store_two)

	return 1

def get_studios(username):
	all_genres = ''
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = "select studios from (select distinct * from " + username + "_diary a join t1_movie_info b on a.expected_url = b.url where a.view_str like '%2021') a;"
		cur.execute(q)
		rows = cur.fetchall()
	rows = str(rows)
	for i in range(len(rows)):
		if rows[i] in " asdfghjklzxcvbnmqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM123456789-":
			all_genres += rows[i]
			
	all_genres = all_genres.split(" ")

	all_genres_unique = []
	for i in range(len(all_genres)):
		if all_genres[i] not in all_genres_unique:
			all_genres_unique += [all_genres[i]]
	
	#print(all_genres_unique)

	occur = []
	for i in range(len(all_genres_unique)):
		occur += [[all_genres.count(all_genres_unique[i]), all_genres_unique[i]]]
	
	#print(occur)

	top = 0
	store = []
	for i in range(len(occur)):
		if occur[i][0] > top:
			#print(top)
			top = occur[i][0]
			#print(top)
			store = [occur[i]]
		elif occur[i][0] == top:
			store += [occur[i]]

	#print(store)

	top_two = 0
	store_two = []
	for i in range(len(occur)):
		if occur[i][0] > top_two and occur[i][0] < top:
			top_two = occur[i][0]
			store_two = [occur[i]]
		elif occur[i][0] == top_two:
			store_two += [occur[i]]
	#print(store_two)
	
	a_format(store + store_two)

	return 1

def get_studios_top_movies(username):
	all_genres = ''
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = "select studios from (select distinct * from " + username + "_diary a join t1_movie_info b on a.expected_url = b.url where a.view_str like '%2021' and rating = (select max(rating) from " + username + "_diary)) a;"
		cur.execute(q)
		rows = cur.fetchall()
	rows = str(rows)
	for i in range(len(rows)):
		if rows[i] in " asdfghjklzxcvbnmqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM123456789-":
			all_genres += rows[i]
			
	all_genres = all_genres.split(" ")

	all_genres_unique = []
	for i in range(len(all_genres)):
		if all_genres[i] not in all_genres_unique:
			all_genres_unique += [all_genres[i]]
	
	#print(all_genres_unique)

	occur = []
	for i in range(len(all_genres_unique)):
		occur += [[all_genres.count(all_genres_unique[i]), all_genres_unique[i]]]
	
	#print(occur)

	top = 0
	store = []
	for i in range(len(occur)):
		if occur[i][0] > top:
			#print(top)
			top = occur[i][0]
			#print(top)
			store = [occur[i]]
		elif occur[i][0] == top:
			store += [occur[i]]

	a_format(store)
	return 1

def get_studios_top_directors(username):
	all_genres = ''
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = "select director from (select distinct * from " + username + "_diary a join t1_movie_info b on a.expected_url = b.url where a.view_str like '%2021' and rating = (select max(rating) from " + username + "_diary)) a;"
		cur.execute(q)
		rows = cur.fetchall()
	rows = str(rows)
	for i in range(len(rows)):
		if rows[i] in " asdfghjklzxcvbnmqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM123456789-":
			all_genres += rows[i]
			
	all_genres = all_genres.split(" ")

	all_genres_unique = []
	for i in range(len(all_genres)):
		if all_genres[i] not in all_genres_unique:
			all_genres_unique += [all_genres[i]]
	
	#print(all_genres_unique)

	occur = []
	for i in range(len(all_genres_unique)):
		occur += [[all_genres.count(all_genres_unique[i]), all_genres_unique[i]]]
	
	#print(occur)

	top = 0
	store = []
	for i in range(len(occur)):
		if occur[i][0] > top:
			#print(top)
			top = occur[i][0]
			#print(top)
			store = [occur[i]]
		elif occur[i][0] == top:
			store += [occur[i]]

	a_format(store)
	return 1

def get_studios_top_actors(username):
	all_genres = ''
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = "select actors from (select distinct * from " + username + "_diary a join t1_movie_info b on a.expected_url = b.url where a.view_str like '%2021' and rating = (select max(rating) from " + username + "_diary)) a;"
		cur.execute(q)
		rows = cur.fetchall()
	rows = str(rows)
	for i in range(len(rows)):
		if rows[i] in " asdfghjklzxcvbnmqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM123456789-":
			all_genres += rows[i]
			
	all_genres = all_genres.split(" ")

	all_genres_unique = []
	for i in range(len(all_genres)):
		if all_genres[i] not in all_genres_unique:
			all_genres_unique += [all_genres[i]]
	
	#print(all_genres_unique)

	occur = []
	for i in range(len(all_genres_unique)):
		occur += [[all_genres.count(all_genres_unique[i]), all_genres_unique[i]]]
	
	#print(occur)

	top = 0
	store = []
	for i in range(len(occur)):
		if occur[i][0] > top:
			#print(top)
			top = occur[i][0]
			#print(top)
			store = [occur[i]]
		elif occur[i][0] == top:
			store += [occur[i]]

	a_format(store)
	return 1


def get_frequent_directors(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = """select director, director_count from ( select director, count(director) as director_count, row_number() over (order by count(director) desc) up from (select distinct * from """ + username + """_diary a join t1_movie_info b on a.expected_url = b.url where a.view_str like "%2021") a group by director) a where up <= 3;"""
		cur.execute(q)
		rows = cur.fetchall()
	#print(rows)
	a_format(rows)
	return


def get_avg_rating(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = """select round(avg(rating),2) from (
		select
		distinct *
		from """ + username + """_diary a
		join t1_movie_info b
		on a.expected_url = b.url
		where a.view_str like "%2021"
		and a.rating != 0) a;""" 
		cur.execute(q)
		rows = cur.fetchall()
	#print(rows)
	get_numbers(rows)
	return

def get_stdev_rating(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = """select rating from (
		select
		distinct *
		from """ + username + """_diary a
		join t1_movie_info b
			on a.expected_url = b.url
		where a.view_str like "%2021"
		and a.rating != 0) a;"""
		cur.execute(q)
		rows = cur.fetchall()
	ratings = ''
	for i in range(len(str(rows))):
		#print(str(rows)[i])
		if str(rows)[i] in " 1234567890":
			ratings += str(rows)[i]
	#print(ratings)
	#print(ratings)
	ratings = ratings.split(" ")
	for i in range(len(ratings)):
		ratings[i] = int(ratings[i])
	#get_numbers(
	print(round(statistics.pstdev(ratings), 2))
	return

def get_frequency_reviews(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = """
select count(review) from (
                select
                        distinct *
                from """ + username + """_diary a
                join t1_movie_info b
                        on a.expected_url = b.url
                where a.view_str like "%2021"
                        and review != "") a;
"""
		cur.execute(q)
		rows = cur.fetchall()
	get_numbers(rows)
	return

def get_reviewed_percent(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = """
select
        round(
                cast(sum(review is not "") as float)
                /
                cast(count(review) as float) * 100.0
        ,2)
from """ + username + """_diary 
where
        view_str like "%2021";
"""
		cur.execute(q)
		rows = cur.fetchall()
	#print(rows)
	get_numbers(rows)
	return

def get_years(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = """
select
        "year",
        year_count
from (
        select
                "year",
                count("year") as year_count,
                row_number() over (order by count("year") desc) up
        from (
                select
                        distinct *
                from """ + username + """_diary a
                join t1_movie_info b
                        on a.expected_url = b.url
                where a.view_str like "%2021"
                ) a
        group by "year") a
where up <= 3;
"""
		cur.execute(q)
		rows = cur.fetchall()
	b_format(rows)
	return

def get_decades(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = """
select
        decade || '0',
        decade_count
from (
        select
                decade,
                count(decade) as decade_count,
                row_number() over (order by count(decade) desc) up
        from (
                select *, substr("year",1,3) as decade
                from ( 
                select
                        distinct *
                from """ + username + """_diary a
                join t1_movie_info b
                        on a.expected_url = b.url
                where a.view_str like "%2021"
                )
                ) a
        group by decade) a
where up <= 3;
"""
		cur.execute(q)
		rows = cur.fetchall()
	#print(rows)
	a_format(rows)
	return

def get_hot_takes(username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		q = """
select * from ( 
select
        title,
        rating as rating,
        cast(substr(rating_value,13,4) as float)*2 as movie
        from (
                select
                        distinct *
                from """ + username + """_diary a
                join t1_movie_info b
                        on a.expected_url = b.url
                where a.view_str like "%2021"
                        and a.rating != 0
        ) a
        ) a
where a.rating > movie + 3.0
or a.rating < movie - 3.0;
"""
		cur.execute(q)
		rows = cur.fetchall()
	#print(rows)
	c_format(rows)
	return


def a_format(a):
	''' takes in [[6, 'warner-bros-pictures-1'], [6, 'columbia-pictures']] and formats it as
		warner bros pictures, 6
		columbia pictures, 6
	'''
	for i in range(len(a)):
		print(str(a[i][1]).replace("'", "").replace("-", " ") + " " + str(a[i][0]))
	return

def get_numbers(a):
	''' gets just the numbers and decimals from a string
	'''
	r_string = ''
	for i in range(len(str(a))):
		if str(a)[i] in '1234567890.':
			r_string += str(a)[i]
	print(r_string)
	return


def b_format(a):
	''' takes in [(2007, 11), (2021, 7), (2018, 6)] and formats it
	'''
	a_string = ''
	for i in range(len(str(a))):
		if str(a)[i] in '1234567890 ':
			a_string += str(a)[i]
	a = a_string.split(" ")
	for i in range(1, len(a), 2):
		print(str(a[i]) + " " + str(a[i - 1]))
	return

def c_format(a):
	for i in range(len(a)):
		print(str(a[i][1]).replace("'", "").replace("-", " ") + " against " + str(a[i][2]).replace("'","") + " " + str(a[i][0]))
	return


def get_ugly_stats(username):
	print("The actors you watched most in 2021 were:")
	get_actors(username)
	print("The genres you watched most in 2021 were:")
	get_genres(username)
	print("You watched movies mostly from these countries in 2021:")
	get_countries(username)
	print("You watched movies mostly from these studios in 2021:")
	get_studios(username)
	print("These studios made your highest rated movies in 2021:")
	get_studios_top_movies(username)
	print("These directors made your highest rated movies in 2021:")
	get_studios_top_directors(username)
	#get_studios_top_actors("trschwab")
	print("You watched these directors the most in 2021:")
	get_frequent_directors(username)
	print("The average rating you gave in 2021:")
	get_avg_rating(username)
	print("Your rating standard deviation in 2021:")
	get_stdev_rating(username)
	print("You gave this many reviews in 2021:")
	get_frequency_reviews(username)
	print("The percent of movies you reviewed in 2021:")
	get_reviewed_percent(username)
	print("You watched mostly from these years in 2021:")
	get_years(username)
	print("You watched mostly from these decades in 2021:")
	get_decades(username)
	print("These ratings are your hot takes. Where your rating differs from the movie's average rating by more than 3 points:")
	get_hot_takes(username)

#get_ugly_stats("trschwab")
#get_ugly_stats("nrg004")
#get_ugly_stats("marvelfan69")
#get_ugly_stats("grahamgearhart")
#get_ugly_stats("_jelvin")
#get_ugly_stats("captainronfan44")
#get_ugly_stats("jlucien")
get_ugly_stats("timco")
