import pandas as pd
from __future__ import print_function
import logging
import grpc
import fet_pb2
import fet_pb2_grpc



def run():
    creds = grpc.ssl_channel_credentials()
    client_id = '8282'
    with grpc.insecure_channel(f'localhost:{client_id}') as channel:
        # Fet service client test
        stub = fet_pb2_grpc.MasterClientCommunicationServiceStub(channel)
        response = stub.GetRandomSplitValueFromClient(fet_pb2.GetRandomSplitValueFromClientRequest(feature="", clientId=client_id))
        channel.close()

        stub = fet_pb2_grpc.MasterClientCommunicationServiceStub(channel)
        response = stub.GetAggregatedValuesFromClient(fet_pb2.GetAggregatedValuesFromClientRequest(feature="", clientId=client_id, splitValue=0))
        channel.close()

        stub = fet_pb2_grpc.MasterClientCommunicationServiceStub(channel)
        response = stub.BroadcastTreeNodesBasedOnBestSplit(
            fet_pb2.BroadcastTreeNodesBasedOnBestSplitRequest(feature="", splitValue=0, treeHeight=0))
        channel.close()


        # # Feedback service client test
        # stub = feedback_pb2_grpc.FeedbackServiceStub(channel)
        # request_question = common_pb2.QuestionDto()
        # request_question.question = "Is the ride bumpy ?"
        # request_question.options.extend(["Yes", "No"])
        # response = stub.SaveFeedback(feedback_pb2.FeedbackRequest(question=request_question, answer="No"))
        # print(f'Feedback response received: {response.timeStamp}')




if __name__ == '__main__':
    logging.basicConfig()
    run()
