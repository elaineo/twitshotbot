from tweet import TweetClient
import config as cfg

from lndrpc import LndWrapper
import os, logging

def main():
    logging.basicConfig(level=logging.INFO)

    cert = open(os.path.expanduser(cfg.LND_CERT_PATH)).read()
    ln = LndWrapper(cert, cfg)

    tweet = TweetClient(cfg.twitter, ln)
    tweet.watch()

if __name__ == "__main__":
    main()
