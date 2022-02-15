import re
import sqlite3
import requests


#from requests import session
from bs4 import BeautifulSoup
from utility.utility import *


def get_user_url(username):
	''' takes in a username, returns the user URL.. if the user does not exist, return -1
	'''
	raw_url = "https://letterboxd.com"
	user_url = raw_url + "/" + username + "/"
	page = get_page(user_url)
	if "Sorry, we can’t find the page you’ve requested." in str(page):
		print("Error: User not found. Return code -1")
		return -1
	return user_url

def get_numbers(a):
	allowed = "1234567890"
	r = ''
	for i in range(len(a)):
		if a[i] in allowed:
			r += a[i]
	return r

#needs to be fixed to ensure the diary pages are in order.. this assume diary, 2, 3, ..45
def get_diary_pages(url):
	''' takes in a user url and returns the amount of diary pages the user has.
	'''
	#print(url) = https://letterboxd.com/[username]/
	username = url.split("/")[-2]
	raw_url = "https://letterboxd.com"
	diary_url = url + "films/diary/"
	page = get_page(diary_url)
	info = str(page.find_all("div", {"class": "pagination"}))
	info = info.split('"')
	diary_urls = [diary_url]
	page_count = []
	for i in range(len(info)):
		if "/films/diary/page/" in info[i] and info[i] not in diary_urls:
			page_count += [int(get_numbers(info[i].replace(username,"")))]
	if page_count == []:
		return diary_urls
	for i in range(2,max(page_count)+1):
		diary_urls += [str(url + "films/diary/page/" + str(i) + "/")]
	#print(diary_urls)
	return diary_urls

def create_user_db(username):
	sql_query = "create table if not exists " + username + "_diary (title string, year string, rating string, review string, rewatch string, view string, view_str string, poster_url string, expected_url string);"
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		#execute_task(conn, "drop table if exists " + username + "_diary;")
		execute_task(conn, sql_query)
	close_connection(conn)
	return 1

def handle_quotes(a):
	''' takes in a string and prefaces any apostraphes or quotes with a \
		TODO
	'''
	r_string = a
	r_string = r_string.replace("'", "")
	r_string = r_string.replace('"', '')
	return r_string

def get_info(soup):
	''' takes the info of a diary page and formats for sql insertion
	'''
	titles = soup.find_all("a", "edit-review-button has-icon icon-16 icon-edit")
	name = ""
	value_list = []
	#print(titles)
	for tag in titles:
		#print(name)
		#print(str(tag.get("data-film-name")))
		name = handle_quotes(str(tag.get("data-film-name")))
		year = handle_quotes(str(tag.get("data-film-year")))
		rating = handle_quotes(str(tag.get("data-rating")))
		review = handle_quotes(str(tag.get("data-review-text")))
		rewatch = handle_quotes(str(tag.get("data-rewatch")))
		date = handle_quotes(str(tag.get("data-viewing-data")))
		date_str = handle_quotes(str(tag.get("data-viewing-date-str")))
		poster_url = handle_quotes(str(tag.get("data-film-poster")))
		expected_url = "https://letterboxd.com" + poster_url[:-10]
		value = "('" + name + "', '" + year + "', '" + rating + "', '" + review + "', '" + rewatch + "', '" + date + "', '" + date_str + "', '" + poster_url + "', '" + expected_url+ "'),"
		value_list += [value]
	if name != "":
		return value_list
	return -1

def get_diary_page_info(url):
	page = get_page(str(url))
	page_info = get_info(page)
	return page_info

def get_all_watched(username):
	u = get_user_url(username)
	if u == -1:
		print("Exit")
		exit(1)
	diary_urls = get_diary_pages(u)
	all_page_info = []
	for i in range(len(diary_urls)):
		#print(type(diary_urls))
		#print(type(get_diary_page_info(diary_urls[i])))
		all_page_info += get_diary_page_info(diary_urls[i])
	#print(all_page_info)
	return all_page_info
		

def format_watched(a):
	''' takes in the output list from get_all_watched
		formats the string for sql execution and db entry
	'''
	r_string = ""
	for i in range(len(a)):
		r_string += a[i]
	r_string = r_string[:-1] # last element cannot be a ','
	encode = r_string.encode("ascii", "ignore")
	decode = encode.decode() #remove non ascii characters
	r_string = decode.replace('\n', "") # remove newlines
	return r_string


def populate_diary_sqlite(s, username):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		q = "insert into " + username + "_diary(title, year, rating, review, rewatch, view, view_str, poster_url, expected_url) values" + s + ";"
		execute_task(conn, q)
	close_connection(conn)

def delete_duplicate_rows(table_name):
	database = "./letterbox.db"
	conn = create_connection(database)
	with conn:
		execute_task(conn, "delete from " + table_name + " where rowid not in (select min(rowid) from " + table_name + " group by title, year, rating, review, rewatch, view, view_str, poster_url, expected_url);")
		#select_all_tasks(conn, table_name) #would print a select * from the table
	close_connection(conn)

def main_populate_user_diary(username):
	#username = "trschwab"
	#username = "_jelvin"
	#username = "mamief"
	#username = "marvelfan69"
	#username = "davidehrlich"
	#username = "nrg004"
	create_user_db(username)
	watched = get_all_watched(username)
	formatted_data = format_watched(watched)
	populate_diary_sqlite(formatted_data, username)
	#delete_duplicate_rows("trschwab_diary")
	#delete_duplicate_rows("_jelvin_diary")
	#delete_duplicate_rows("mamief_diary")
	#delete_duplicate_rows("marvelfan69_diary")
	#delete_duplicate_rows("davidehrlich_diary")
	delete_duplicate_rows(username + "_diary")

#main_populate_user_diary("trschwab")

#utility_test()
