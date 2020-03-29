from crendentials import ACCESS_TOKEN
import requests
import time
import sys
import pandas as pd
import logging

# This is an example of retrieving most recent 30 messages given a symbol.


def get_messages_by_symbol(symbol):
    url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
    params = {
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    print("Exception")
    logging.exception("Invalid response!")
    logging.exception(response.content)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            # logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    symbol = "AAPL"
    while True:
        print("Reset")
        try:
            response_json = get_messages_by_symbol(symbol)
            messages = response_json["messages"]
            cursor = response_json["cursor"]
            logging.info("Number of messages: %d" % len(messages))
            logging.info("Cursor since:  %d, cursor max:   %d" % (cursor["since"], cursor["max"]))
            logging.info("First message: %d, last message: %d" % (messages[0]["id"], messages[-1]["id"]))
            max_timestamp = pd.to_datetime(messages[0]["created_at"])
            max_msg_text = messages[0]["body"]
            for message in messages:
                ts = pd.to_datetime(message["created_at"])
                if ts > max_timestamp:
                    max_timestamp = ts
                    max_msg_text = message["body"]
            logging.info(max_timestamp.astimezone("US/Central"))
            logging.info(max_msg_text)

            time.sleep(20)
        except Exception as ex:
            print("Exception!")
            print(ex)
            time.sleep(60)
            continue
