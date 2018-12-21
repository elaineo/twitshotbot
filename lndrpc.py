import logging
import codecs
import sys, os
sys.path.insert(0, 'googleapis')

import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc

from google.protobuf.json_format import MessageToJson

def metadata_callback(context, callback):
    with open(os.path.expanduser('~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon'), 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')
    callback([('macaroon', macaroon)], None)

class LndWrapper:
    """API for Lightning gRPC client
    """
    def __init__(self, cert, config):
        cert_creds = grpc.ssl_channel_credentials(cert)
        auth_creds = grpc.metadata_call_credentials(metadata_callback)
        creds = grpc.composite_channel_credentials(cert_creds, auth_creds)

        channel = grpc.secure_channel(config.LND_HOST, creds)
        self.stub = lnrpc.LightningStub(channel)
        self.DEFAULT_PRICE = config.DEFAULT_PRICE
        self.DEFAULT_EXPIRY = config.DEFAULT_EXPIRY
        try:
            request = ln.GetInfoRequest()
            response = self.stub.GetInfo(request)
            logging.info(response)
        except grpc.RpcError as e:
           logging.error(e)    

    def get_invoice(self, memo):
        try:
            request = ln.Invoice(
                memo=memo,
                value=self.DEFAULT_PRICE,
                expiry=self.DEFAULT_EXPIRY
            )
            response = self.stub.AddInvoice(request)
            logging.info(response)
            return response.payment_request
        except grpc.RpcError as e:
           logging.error(e)
           return e.details()

    def subscribe_invoices(self):
        try:
            request = ln.InvoiceSubscription()
            return self.stub.SubscribeInvoices(request)
        except grpc.RpcError as e:
           logging.error(e)
           return e.details()    
