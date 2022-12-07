import re
import traceback

from tools import *

config = read_config()
developer_chat_id = config["developer_chat_id"]
bot_id = f'bot{config["bot_token"]}'
chat_id = config["chat_id"]
wsid = config["wsid"]

try:
    appointments = run_request("GET",
                               'https://terminvereinbarung.leipzig.de/m/leipzig-ba/extern/calendar/search_result?'
                               'search_mode=earliest&'
                               'uid=b76cab25-49bd-44e3-950d-aab715881ea7&'
                               f'wsid={wsid}',
                               num_of_tries=1,
                               decode_json=False)

    if appointments.find("Session abgelaufen") != -1:
        send_message(bot_id, developer_chat_id, "Session abgelaufen")

    result = [_.start() for _ in re.finditer("\"date_time\"", appointments)]
    result_units = [_.start() for _ in re.finditer("\"unit\"", appointments)]
    full_message = ""
    for d, u in zip(result, result_units):
        end = appointments[d + 14:d + 31].find("\"") + d + 14
        collected_date, collected_time = appointments[d + 14:end].split(" ")
        end_unit = appointments[u + 9:].find("\"") + u + 9
        collected_unit = appointments[u + 9:end_unit]
        if full_message != "":
            full_message = full_message + "\n"
        full_message = full_message + \
                       f"{collected_date} {collected_time} - {collected_unit}"
    if full_message != "":
        send_message(bot_id, chat_id, full_message, num_of_tries=1, timestamp=False)
except Exception as exc:
    print(exc)
    traceback.print_exc()
    send_message(bot_id, developer_chat_id, str(exc)[0:500])
