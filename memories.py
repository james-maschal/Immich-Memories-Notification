import sys
import os
import logging
import requests
from datetime import date
from requests.exceptions import ConnectionError, RequestException, HTTPError
from dotenv import load_dotenv

#Loads logging functions, saving all logs to ./memories.log
logging.basicConfig(
    filename='memories.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#Loads ./.env file with credentials and host information
load_dotenv()
API_KEY = os.getenv("API_KEY")
HOST = os.getenv("HOST")
CONTAINER = os.getenv("CONTAINER")
NOTIFY_URL = os.getenv("NOTIFY_URL")


def rest_connect(host, container, headers):
    #Main function for connection to Immich's API
    url = f"http://{host}{container}"
    response = None
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=3)
        if response.status_code == 200:
            return response.json(), True

        response.raise_for_status()

    except HTTPError as http_err:
        if response.status_code == 401:
            logger.error(f"Immich HTTP error occurred, likely a bad API key: {http_err}")
            return f"Server Response: {response.status_code}", False
        else:
            logger.error(f"Immich HTTP error occurred: {http_err} - Status Code: {response.status_code}")
            return f"Server Response: {response.status_code}", False
    except ConnectionError as e:
        logger.error(f"Immich Connection Error: {e}")
    except RequestException as e:
        logger.error(f"Immich Request Failed: {e}")


def notify(message):
    #Function to send messages (good or bad!) to your notification server
    response = None
    try:
        response = requests.post(NOTIFY_URL, json={
            "message": message,
            "priority": 2,
            "title": "Memories"
        }, headers={"Content-Type": "application/json"})

        response.raise_for_status()

    except HTTPError as http_err:
        if response.status_code == 401:
            logger.error(f"Notification Server HTTP error occurred, likely a bad token: {http_err}")
        else:
            logger.error(f"Notification Server HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except ConnectionError as e:
        logger.error(f"Notification Server Connection error: {e}")
    except RequestException as e:
        logger.error(f"Failed to send notification: {e}")


def check_memories(server_output):
    #Checks JSON output for memories with "showAt" that match the current date
    memory_state = False
    for record in server_output:
        if str(date.today()) in record["showAt"]:
            memory_state = True
    return memory_state


def main():
    """This script will connect to Immich's API and collect all Memory related data.
    It will then check to see if any memories are set to be shown on the current
    date, and if so, send you a notification. If there are no memories today,
    the script exits. It will also send you a notification on some connection
    errors."""

    headers = {"Content-Type": "application/json", "x-api-key": API_KEY}
    server_output, result = rest_connect(HOST, CONTAINER, headers)

    if result:
        memory_state = check_memories(server_output)
        if memory_state:
            message = (
                "Good Morning, You have memories to review!")
        else:
            sys.exit()
    else:
        message = (
            "Bad News!\nThe Immich server was unresponsive!"
            if server_output == "unsuccessful connection" else
            f"Bad News! \nThe Immich server is angry, it said {server_output}"
        )

    notify(message)

if __name__ == "__main__":
    main()
