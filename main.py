#!/usr/bin/env python3

from tweet import TweetClient
import config as cfg

from lndrpc import LndWrapper
import os, logging

def main():
    logging.basicConfig(level=logging.INFO)

    cert = open(os.path.expanduser(cfg.LND_CERT_PATH), 'rb').read()
    ln = LndWrapper(cert, cfg)

    tweet = TweetClient(cfg.twitter, ln)
    tweet.watch()
    invoices = ln.subscribe_invoices()
    for invoice in invoices:
    	logging.info(invoice)
    	tweet.send_receipt(invoice.get('memo'))

if __name__ == "__main__":
    main()
