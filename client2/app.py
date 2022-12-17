from concurrent import futures
import grpc

from flask import Flask, render_template

import fet_pb2_grpc
from service.fet_service import FetCommunication


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fet_pb2_grpc.add_MasterClientCommunicationServiceServicer_to_server(FetCommunication(), server)
    app.logger.error("adding insecure port 8383")
    p = server.add_insecure_port('0.0.0.0:8383')
    app.logger.error(f"opened up on port {p}")
    server.start()
    return server


if __name__ == '__main__':
    app.logger.debug("hello! starting up")
    grpc_server = serve()
    app.logger.error("serving grpc!")
    app.run(host="0.0.0.0", port=8001)
