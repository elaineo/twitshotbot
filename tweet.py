from TwitterAPI import TwitterAPI
import json
import logging
from screenshot import screenshot
import threading, glob

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
                    'media_ids': media_id }
        tweet = self.api.request('statuses/update', options).json()
        logging.info(tweet)
        return tweet.get('id_str')

    def _send_invoice(self, reply_sid):
        memo = "ScreenshotBot #%s" % reply_sid 
        msg = self.lnrpc.get_invoice(memo)
        sid = self._post(msg, reply_sid)
        return sid

    def _return_image(self, file, reply_sid):
        img = open(file, "rb").read()
        r = self.api.request('media/upload', None, {'media': img })
        logging.info(r.json())
        if r.status_code == 200:
            media_id = r.json()['media_id']
            self._post('Here you go:', reply_sid, media_id)
        else:
            logging.info("Media upload failed: %s" % file)
            self._post('Error', reply_sid)

    def _send_receipt(self, memo):
        id_str = memo.split('#')[-1]
        file = glob.glob('%s-*.png' % id_str)[0]
        reply_sid = file[file.find('-')+1 : file.find('.')]
        self._return_image(file, reply_sid)

    def watch(self):  
        """
        Filter tweets based on bot's screen name
        """
        msgs = self.api.request('statuses/filter', { 'track': self.bot.get('screen_name') })

        for m in msgs:
            logging.info(m)
            urls = m.get('entities').get('urls')
            if len(urls)==0:
                continue
            tweet_url = urls[0]
            sid = m.get('id_str')
            r = self._send_invoice(sid)
            logging.info(r)
            screenshot(tweet_url.get('expanded_url'), '%s-%s' % (sid, r))
            continue

    def get_invoices(self):
        invoices = self.lnrpc.subscribe_invoices()
        for invoice in invoices:
            logging.info(invoice)
            if invoice.settled:
                self._send_receipt(invoice.memo)

    def go(self):
        watch = threading.Thread(target=self.watch)
        get_invoices = threading.Thread(target=self.get_invoices)
        watch.daemon = True
        get_invoices.daemon = True
        watch.start()
        get_invoices.start()