import ibmmq
import time

class Vendor:
    def __init__(self, name = 'vendor', address = 'localhost'):
        self.name = name
        self.address = address

    def connect(self):
        qmanager = ibmmq.connect("QM1", "DEV.APP.SVRCONN", "localhost(1414)", user="app", password="passw0rd")
        queue = ibmmq.Queue(qmanager, "DEV.QUEUE.1")
        return queue
    
    def get_message(self):
        queue = self.connect()
        while True:
            try:
                message = queue.get()
                print('=' * 60)
                print(f"Received message: {message}")
            except ibmmq.MQMIError as e:
                if e.reason == 2033:
                    print("No message available, waiting...")
                    time.sleep(5)  # Wait for 5 seconds before checking again
                else:
                    print(f"An error occurred: {e}")
                    break

def main():
    vendor = Vendor()
    vendor.get_message()

if __name__ == "__main__":
    main()
