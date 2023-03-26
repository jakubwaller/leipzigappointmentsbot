import re
import traceback
from datetime import datetime

import tweepy as tweepy

from tools import *

config = read_config()
developer_chat_id = config["developer_chat_id"]
bot_id = f'bot{config["bot_token"]}'
chat_id = config["chat_id"]
wsid = config["wsid"]
sent_day = 0

try:
    # auth = tweepy.OAuth1UserHandler(
    #     config['twitter_key'],
    #     config['twitter_secret'],
    #     config['twitter_token_key'],
    #     config['twitter_token_secret']
    # )
    #
    # api = tweepy.API(auth)

    appointments = run_request("GET",
                               'https://terminvereinbarung.leipzig.de/m/leipzig-ba/extern/calendar/search_result?'
                               'search_mode=earliest&'
                               'uid=b76cab25-49bd-44e3-950d-aab715881ea7&'
                               f'wsid={wsid}',
                               num_of_tries=1,
                               decode_json=False)

    if appointments.find("Session abgelaufen") != -1 and sent_day != datetime.now().day:
        send_message(bot_id, developer_chat_id, "Session abgelaufen")
        sent_day = datetime.now().day

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
        # if len(full_message) <= 280:
        #     api.update_status(full_message)
        # else:
        #     last_newline = full_message.rfind("\n", 0, 280)
        #     if last_newline == -1:
        #         last_newline = 280
        #     tweet = api.update_status(full_message[0:last_newline])
        #     full_message = full_message[last_newline:]
        #     remaining_length = len(full_message)
        #     while remaining_length > 0:
        #         last_newline = full_message.rfind("\n", 0, 280)
        #         if last_newline == -1 or len(full_message) <= 280:
        #             last_newline = 280
        #         tweet = api.update_status(status=full_message[0:last_newline],
        #                                   in_reply_to_status_id=tweet.id,
        #                                   auto_populate_reply_metadata=True)
        #         full_message = full_message[last_newline:]
        #         remaining_length = len(full_message)
except Exception as exc:
    error_message = str(exc)[0:100]
    if "Status is a duplicate" not in error_message:
        print(exc)
        traceback.print_exc()
        send_message(bot_id, developer_chat_id, error_message)
