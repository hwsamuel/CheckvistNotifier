#!/usr/bin/python

import requests, json, time, re, pytz, datetime
from settings import *

DUE_DEFAULT = '10h'

def get_today_date(time_zone):
	my_zone = pytz.timezone(time_zone)
	my_date = datetime.datetime.now(my_zone)
	return my_date
	
def get_auth(USER_NAME, API_KEY):
	ping_url = 'https://checkvist.com/auth/login.json'
	post_data = {'username': USER_NAME, 'remote_key': API_KEY}
	response = requests.post(ping_url, post_data)
	token = response.text.replace('"', '').strip()
	return token
	
def get_tasks(auth_token, list_id):
	ping_url = 'https://checkvist.com/checklists/'+str(list_id)+'/tasks.json'
	response = requests.get(ping_url, {'token': auth_token})
	all_tasks = json.loads(response.text)
	return all_tasks

def get_today_tasks(all_tasks):
	on_date = get_today_date(USER_TIMEZONE)
	today = on_date.strftime("%Y/%m/%d")
	
	today_tasks = []
	
	for task in all_tasks:
		id = str(task['id'])
		status = task['status']
		title = task['content']
		tags = task['tags_as_text']
		due = task['due']
		
		if status != 0 or due == None or due != today: continue
		
		due_time = re.findall('[0-9]+h', tags)
		due_time = due_time[0] if len(due_time) > 0 else DUE_DEFAULT
		due_time = due_time.zfill(3)
		
		today_tasks.append({'title': title, 'due_time': due_time})
		
	return today_tasks
	
def send_push(title, message):
	ping_url = 'https://wirepusher.com/send'
	data = {'id': DEVICE_ID, 'title': title, 'message': message, 'action': 'https://m.checkvist.com/app/list/'+str(LIST_ID)}
	response = requests.post(ping_url, data)
	print '[' + str(response.status_code) + '] ' + title

def main():
	auth_token = get_auth(USER_NAME, API_KEY)
	all_tasks = get_tasks(auth_token, LIST_ID)
	today_tasks = get_today_tasks(all_tasks)

	on_date = get_today_date(USER_TIMEZONE)
	current_hour = str(on_date.strftime("%H"))+'h'
	current_hour = current_hour.zfill(3)
	
	for task in today_tasks:
		due_time = task['due_time']
		title = task['title']
		
		if current_hour != due_time: continue
		send_push(title, title)

if __name__ == "__main__" :
	main()