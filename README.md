### This project include the following:

1. Plain: A plain implementation of the Random forest on 40 loan request sample.
2. Client1: Client1 flask server on rest:8000 & gRPC:8282 port with 20 loan request sample.
3. Client2: Client1 flask server on rest:8001 & gRPC:8383 port with 20 loan request sample.
4. Master: Orchestrate Client1 and Client2 to build decision tree and forest.

### How to run

1. First run the app.py from both Client1 and Client2.
2. Then run the master.py from master folder.