#!/usr/bin/env python3

from tweet import TweetClient
from lndrpc import LndWrapper
import config as cfg
import os, logging

def main():
    logging.basicConfig(level=logging.INFO)

    cert = open(os.path.expanduser(cfg.LND_CERT_PATH), 'rb').read()
    ln = LndWrapper(cert, cfg)

    tweet = TweetClient(cfg.twitter, ln)
    tweet.go()

if __name__ == "__main__":
    main()
