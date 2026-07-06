import ibmmq

qmgr = ibmmq.connect("QM_GOLF", "DEV.APP.SVRCONN", "localhost(1414)", user="app", password="password")

q = ibmmq.Queue(qmgr, "DEV.QUEUE.1")

#q.put("Hello 12323")


go = input("have you recieved the message in the MQ console? (y/n): ")

if go.lower() == "y":
    qmgr = ibmmq.connect("QM_GOLF", "DEV.APP.SVRCONN", "localhost(1414)", user="app", password="password")

    q = ibmmq.Queue(qmgr, "DEV.QUEUE.1")

    msg = q.get()
    print("Received message:", msg)