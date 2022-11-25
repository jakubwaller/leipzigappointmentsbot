import json
import time
import urllib
from datetime import datetime
from typing import Dict, Union, Any

import requests


def read_config() -> Dict:
    with open("env.json") as file:
        config = json.load(file)
    return config


def send_message(bot_id, chat_id, message, num_of_tries=3, timestamp=True, disable_notification=False):
    if timestamp:
        timestamp_str = str(datetime.now()).split(".")[0] + ": "
    else:
        timestamp_str = ""
    run_request("GET",
                f"https://api.telegram.org/{bot_id}/sendMessage?disable_notification={str(disable_notification)}&"
                f"chat_id={chat_id}&text={timestamp_str}{urllib.parse.quote(message)}",
                num_of_tries=num_of_tries)


def run_request(request_type: str,
                url: str,
                request_body: Dict[str, str] = {},
                request_json: str = "",
                bearer="",
                timeout: int = 30,
                media: Dict = None,
                request_headers=None,
                num_of_tries=5,
                decode_json=True) -> Union[str, Any]:
    success = False
    response = None
    expected_status_code = None
    try_number = 1

    while not success and try_number <= num_of_tries:
        try_number = try_number + 1
        try:
            if request_type == "GET":
                expected_status_code = 200
                if request_headers is None:
                    request_headers = {'Content-Type': 'application/json',
                                       'Authorization': bearer}
                response = requests.get(url=url,
                                        headers=request_headers,
                                        params=request_body,
                                        timeout=timeout)
            elif request_type == "POST":
                expected_status_code = 200
                if media is not None:
                    response = requests.post(url,
                                             request_body,
                                             files=media,
                                             timeout=timeout)
                else:
                    response = requests.post(url=url,
                                             headers={'Content-Type': 'application/json'},
                                             json=request_body,
                                             timeout=timeout)
            elif request_type == "PATCH":
                expected_status_code = 200
                response = requests.patch(url=url,
                                          headers={'Content-Type': 'application/json'},
                                          data=request_json,
                                          timeout=timeout)
            else:
                raise Exception("Wrong request type!")
            success = True
        except Exception as e:
            print(e)
            time.sleep(1)

    if not success:
        raise Exception(f"The request failed {num_of_tries} times.")

    if response.status_code != expected_status_code:
        raise Exception(response.content.decode("UTF-8"))

    if decode_json:
        return json.loads(response.content.decode("UTF-8"))
    else:
        return response.content.decode("UTF-8")
