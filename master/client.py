import pandas as pd
from __future__ import print_function
import logging
import fet_pb2
import fet_pb2_grpc


def run():
    df = pd.read_csv('ds_all.csv')
    
    pass


if __name__ == '__main__':
    logging.basicConfig()
    run()
