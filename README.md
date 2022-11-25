# Leipzig Appointments Bot

Tired of refreshing the page with available appointments at the Leipzig city office? The bot in this channel checks them for you and every minute sends available appointments.

[![@leipzig_appointments](https://img.shields.io/badge/Telegram%20Channel-@leipzig_appointments-blue?logo=telegram&style=plastic)](https://t.me/leipzig_appointments)

## Deployment

- Create a file `env.json`
```json
{
  "developer_chat_id": "<REPLACE WITH DEVELOPER CHAT ID>",
  "bot_token": "<REPLACE WITH BOT TOKEN>",
  "chat_id": "<REPLACE WITH CHAT ID>",
  "wsid": "<REPLACE WITH WSID>"
}
```
The wsid can be obtained here https://terminvereinbarung.leipzig.de/m/leipzig-ba/extern/calendar/?uid=b76cab25-49bd-44e3-950d-aab715881ea7

- add to crontab

```shell
* * * * * cd ~/leipzigappointmentsbot && flock -n /tmp/leipzigappointmentsbot.lockfile python3 leipzigappointmentsbot.py
```