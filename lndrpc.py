import logging
import sys
sys.path.insert(0, 'googleapis')

import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc

from google.protobuf.json_format import MessageToJson


class LndWrapper:
    """API for Lightning gRPC client
    """
    def __init__(self, cert, config):
        creds = grpc.ssl_channel_credentials(cert)
        channel = grpc.secure_channel(config.LND_HOST, creds)
        self.stub = lnrpc.LightningStub(channel)
        self.DEFAULT_PRICE = config.DEFAULT_PRICE
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
                value=self.DEFAULT_PRICE
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
            return stub.SubscribeInvoices(request)
        except grpc.RpcError as e:
           logging.error(e)
           return e.details()    
