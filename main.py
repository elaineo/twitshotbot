#!/usr/bin/env python3

from tweet import TweetClient
from lndrpc import LndWrapper
import config as cfg
import os, sys, logging

def main():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(threadName)s - %(message)s')
    ch.setFormatter(formatter)

    cert = open(os.path.expanduser(cfg.LND_CERT_PATH), 'rb').read()
    ln = LndWrapper(cert, cfg)

    tweet = TweetClient(cfg.twitter, ln)
    tweet.go()

if __name__ == "__main__":
    main()
