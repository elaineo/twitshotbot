# -*- coding: utf-8 -*-
from collections import Counter
import json
import time
import logging

# adjust according to desired timeframe
YEAR_AGO = 916855948064333825

def sav_favs(api, user, key, reply_id):
    newest = None
    counter = Counter([])

    with open('data/ff.json', 'r+') as file:
        ff = json.load(file)

        if user in ff:
            ff[user] = { "favs": ff[user]["favs"],
                        "key": key,
                        "reply_id": reply_id }
            file.seek(0)
            json.dump(ff, file)
            file.truncate()
            return
        
        while True:
            if newest and int(newest) < YEAR_AGO:
                break

            favs_raw = api.request('favorites/list', 
                {'screen_name': user, 'count': 200, 'since_id': YEAR_AGO, 'max_id': newest, 'include_entities': False})
            favs = json.loads(favs_raw.response.text)
            
            if len(favs) == 0:
                break

            newest = favs[-1]["id"] - 1
            logging.info(newest)

            friends = [f["user"]["id_str"] for f in favs if not f["in_reply_to_status_id"]]

            counter += Counter(friends)
            logging.info(counter.most_common(50))

            logging.info(len(favs))

            # Optional; use if rate limiting is an issue
            # time.sleep(20)

        top = counter.most_common(20)
        top = [t[0] for t in top]
        friends_raw = api.request('users/lookup', {'user_id': top}) 
        friends = json.loads(friends_raw.response.text)
        ff[user] = { "favs": [f["screen_name"] for f in friends],
                    "key": key,
                    "reply_id": reply_id }
        file.seek(0)
        json.dump(ff, file)
        file.truncate()
        return

def get_favs(user, id_str):
    with open('data/ff.json', 'r+') as file:
        ff = json.load(file)
        if user in ff:
            return ff[user]["favs"]
        logging.error("Missing user %s" % user)
