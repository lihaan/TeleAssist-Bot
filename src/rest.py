import requests
import datetime as dt
import time

# WEB_APP_NAME = "web"
WEB_APP_NAME = "localhost" # uncomment when running locally
WEB_URL = f"http://{WEB_APP_NAME}:5000"


def start_assist_session(reason, duration_mins):
    url = f"{WEB_URL}/startAssistSession"
    params = {"reason": reason, "duration_mins": duration_mins, }

    response = requests.post(url, json=params)
    print(f"{time.asctime()}: startAssistSession - {response.json()}")

    return response.json()


def check_assist_session():
    url = f"{WEB_URL}/checkAssistSession"
    params = {}

    response = requests.post(url, json=params)
    print(f"{time.asctime()}: checkAssistSession - {response.json()}")
    is_free, reason, end_time, duration_mins_remaining = response.json()

    if not is_free:
        end_time = dt.datetime.fromisoformat(end_time).replace(tzinfo=dt.timezone(dt.timedelta(hours=0))).astimezone(
            tz=dt.timezone(dt.timedelta(hours=8)))

    return (is_free, reason, end_time, duration_mins_remaining)


def end_assist_session():
    url = f"{WEB_URL}/endAssistSession"
    params = {}

    response = requests.post(url, json=params)
    print(f"{time.asctime()}: endAssistSession - {response.json()}")

    return response.json()


def send_message_from_me(user_id, msg):
    url = f"{WEB_URL}/sendMsgFromMe"
    userID = int(user_id)
    params = {"userID": userID, "message": msg}

    response = requests.post(url, json=params)
    print(f"{time.asctime()}: sendMsgFromMe - {response.json()}")

    return response.json()
