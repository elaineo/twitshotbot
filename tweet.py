from TwitterAPI import TwitterAPI
import json
import logging

class TweetClient:
    """ Twitter Client
        Responds to mentions.
    """
    def __init__(self, config, lnrpc):
        self.api = TwitterAPI(config['consumer_key'], config['consumer_secret'], 
            config['access_token'], config['access_token_secret'])
        self.lnrpc = lnrpc

        bot_id = config['access_token'].split('-')[0]
        bot_raw = self.api.request('users/lookup', {'user_id': bot_id})

        try:
            self.bot = bot_raw.json()[0]
            logging.debug(self.bot)
        except KeyError:
            print("Cannot access Twitter account. Check API keys.")
            raise 

    def _post(self, msg, reply_sid, media_id=None):
        options = { 'status': msg, 
                    'in_reply_to_status_id': reply_sid, 
                    'auto_populate_reply_metadata': True,
                    'media_id': media_id }
        tweet = self.api.request('statuses/update', options).json()
        logging.info(tweet)
        return tweet.get('id_str')

    def _send_invoice(self, reply_sid):
        msg = self.lnrpc.get_invoice(amount, reply_sid)
        sid = self._post(msg, reply_sid)
        return sid

    def _return_image(self, file, reply_sid):
        img = open(file, "rb").read()
        r = self.api.request('media/upload', None, {'media': img })
        logging.info(r.json())
        if r.status_code == 200:
            media_id = r.json()['media_id']
            self.post('Thank you', reply_sid, media_id)
        else:
            logging.info("Media upload failed: %s" % file)
            self.post('Error', reply_sid)

    def watch(self):  
        """
        Filter tweets based on bot's screen name
        """
        msgs = self.api.request('statuses/filter', { 'track': self.bot.get('screen_name') })

        for m in msgs:
            logging.info(m)
            tweet = m.get('entities').get('urls')
            tweet_url = tweet[0]
            sid = m.get('id_str')
            r = self._send_invoice(tweet)
            logging.info(r)
            continue
