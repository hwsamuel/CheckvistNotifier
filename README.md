## Checkvist Notifier [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This script lets you get push notifications about your [Checkvist](https://checkvist.com) tasks on your Android phone. It uses the Checkvist [Open API](https://checkvist.com/auth/api) and the [WirePusher API](http://wirepusher.com/help).

## Requirements

- Checkvist account and the ID of the list you want notifications from (i.e. the number after `https://checkvist.com/checklists/` in your URL)
- [WirePusher installed](https://play.google.com/store/apps/details?id=com.mrivan.wirepusher) on your Android phone
- [Cron](https://www.howtogeek.com/101288/how-to-schedule-tasks-on-linux-an-introduction-to-crontab-files) or [Task Scheduler](https://www.howtogeek.com/123393/how-to-automatically-run-programs-and-set-reminders-with-the-windows-task-scheduler) to run this script every hour via `python run.py` (tested with Python 2.7, requires `pytz` via `pip install pytz`)

## Setup

- Edit `settings.py` to add your Checkvist username (the email you registered with), list ID, Open API key (under your [Profile](https://checkvist.com/auth/profile), WirePusher ID (shows in the app when you open it on your phone), and your [timezone string](http://www.timezoneconverter.com/cgi-bin/findzone.tzc), e.g. "America/Toronto".
- Only tasks with a due date will trigger notifications. The default notification time is 10:00AM.
- If you want notifications to trigger at certain times, then use the time estimate tag to configure the time, e.g. `13h` will trigger a notification at 1PM, `0h` will trigger at midnight, and so on.

## Roadmap

- Support for all user lists instead of only one by manually setting ID.
- Auto-detection of timezone in user's Checkvist account instead of manually setting.
- Enhanced documentation with demo screenshots.
- Review of the notification click actions (currently just opens Checkvist mobile page).
- Testing with other push APIs such as [OneSignal](https://onesignal.com) and [PushOver](http://pushover.net).