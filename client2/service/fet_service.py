import fet_pb2
import fet_pb2_grpc
import logging


class FetCommunication(fet_pb2_grpc.MasterClientCommunicationServiceServicer):

    def BroadcastRandomFeatureSet(self, request, context):
        logging.warning(f'BroadcastRandomFeatureSet requestObject: {request}')
        return super().BroadcastRandomFeatureSet(request, context)

    def GetRandomSplitValueFromClient(self, request_iterator, context):
        logging.warning(f'GetRandomSplitValueFromClient requestObject: {request_iterator}')
        return super().GetRandomSplitValueFromClient(request_iterator, context)

    def GetAggregatedValuesFromClient(self, request_iterator, context):
        logging.warning(f'GetAggregatedValuesFromClient requestObject: {request_iterator}')
        return super().GetAggregatedValuesFromClient(request_iterator, context)

    def BroadcastTreeNodesBasedOnBestSplit(self, request, context):
        logging.warning(f'BroadcastRandomFeatureSet requestObject: {request}')
        return super().BroadcastTreeNodesBasedOnBestSplit(request, context)

