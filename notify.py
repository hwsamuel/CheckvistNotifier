#!/usr/bin/python

import requests, json, time, re, pytz, datetime, webbrowser
from win10toast import ToastNotifier

from settings import *

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

def get_lists(auth_token):
	ping_url = 'https://checkvist.com/checklists.json'
	response = requests.get(ping_url, {'token': auth_token})
	all_lists = json.loads(response.text)
	list_ids = []
	for list in all_lists:
		list_ids.append(str(list['id']))
	return list_ids
	
def get_tasks(auth_token, list_id):
	ping_url = 'https://checkvist.com/checklists/'+list_id+'/tasks.json'
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
		list_id = str(task['checklist_id'])
		
		if status != 0 or due == None or due != today: continue
		
		due_time = re.findall('[0-9]+h', tags)
		due_time = due_time[0] if len(due_time) > 0 else DUE_DEFAULT
		due_time = due_time.zfill(3)
		
		today_tasks.append({'title': title, 'due_time': due_time, 'list_id': list_id, 'id': id})

	return today_tasks
	
def win10_send(id, list_id, title):
	action_url = 'https://checkvist.com/checklists/%s/tasks/%s' % (list_id, id)
	toaster = ToastNotifier()
	toaster.show_toast('Checkvist', title, icon_path='F:\\Checkvist Notifier\\checkvist.ico', duration=0, callback_on_click=lambda: webbrowser.open_new_tab(action_url))

def wirepusher_send(id, list_id, title):
	ping_url = 'https://wirepusher.com/send'
	action_url = 'checkvist.https://m.checkvist.com/app/list/%s/item/%s' % (list_id, id)
	data = {'id': DEVICE_ID, 'title': title, 'message': title, 'action': action_url}
	response = requests.post(ping_url, data)
	print '[' + str(response.status_code) + '] ' + title

def onesignal_send(id, list_id, title, app_id, api_key):
	header = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Basic '+api_key}

	ping_url = 'https://onesignal.com/api/v1/notifications'
	action_url = 'https://m.checkvist.com/app/list/%s/item/%s' % (list_id, id)
	data = {'app_id': app_id, 'included_segments': ["Active Users"], 'contents': {'en': title}, 'url': action_url}
	response = requests.post(ping_url, headers=header, data=json.dumps(data))
	print '[' + str(response.status_code) + '] ' + title

def main():
	auth_token = get_auth(USER_NAME, API_KEY)
	all_lists = get_lists(auth_token)
	today_tasks = []
	for list_id in all_lists:
		list_tasks = get_tasks(auth_token, list_id)
		todays = get_today_tasks(list_tasks)
		today_tasks.extend(todays)

	on_date = get_today_date(USER_TIMEZONE)
	current_hour = str(on_date.strftime("%H"))+'h'
	current_hour = current_hour.zfill(3)
	
	for task in today_tasks:
		id = task['id']
		due_time = task['due_time']
		title = task['title']
		list_id = task['list_id']
		
		if current_hour != due_time: continue
		win10_send(id, list_id, title)

if __name__ == "__main__" :
	main()