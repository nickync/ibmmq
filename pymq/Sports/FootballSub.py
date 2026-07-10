import ibmmq
import json
import time

class FootballSub:
    def __init__(self, queue_name="GOLF.SUB.QUEUE"):
        self.queue_name = queue_name
        self.qmgr = None
        self.queue = None
        self.running = True
        self.connect()

    def connect(self): 
        """ Connect to QM_FOOTBALL and open the queue for subscription """
        try:
            self.qmgr = ibmmq.connect(
                "QM_FOOTBALL",
                'DEV.APP.SVRCONN',
                "localhost(1415)",
                user="app",
                password="password"
            )
            self.queue = ibmmq.Queue(self.qmgr, self.queue_name)
            print(f"✅ Connected to QM_FOOTBALL, queue: {self.queue_name}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise

    def process_message(self, msg):
        """ Process a single message """
        try:
            data = json.loads(msg)
            print("== Received message ==")
            print("=" * 60)
            print(f"🏌️  Golf Update Received!")
            print(f"   Player: {data.get('player', 'Unknown')}")
            print(f"   Score:  {data.get('score', 'N/A')}")
            print(f"   Course: {data.get('course', 'Unknown')}")
            print(f"   Time:   {data.get('timestamp', 'N/A')}")
            print("=" * 60)
        except json.JSONDecodeError:
            print("❌ Failed to decode message:", msg)

    def receive_messages(self, timeout=5000):
        """ Continuously receive messages from the queue """
        while self.running:
            try:
                # Wait up to timeout milliseconds for a message
                msg = self.queue.get(timeout=timeout)
                if msg:
                    self.process_message(msg)
            except Exception as e:
                if e.reason == 2033:  # MQRC_NO_MSG_AVAILABLE
                    # No message available, just continue
                    continue
                else:
                    print(f"⚠️  Error: {e}")
                    break
            except KeyboardInterrupt:
                print("\n🛑 Stopped by user")
                self.stop()
                break
            except Exception as e:
                print(f"⚠️  Unexpected error: {e}")
                break
    
    def get_one_message(self):
        """Get a single message (useful for testing)"""
        try:
            msg = self.queue.get(timeout=5000)
            if msg:
                self.process_message(msg)
                return msg
        except Exception as e:
            if e.reason == 2033:
                print("📭 No messages available")
            else:
                print(f"⚠️  Error: {e}")
        return None
    
    def stop(self):
        self.running = False
    
    def close(self):
        if self.queue:
            self.queue.close()
        if self.qmgr:
            self.qmgr.disconnect()
        print("🔌 Disconnected from QM_FOOTBALL")

if __name__ == "__main__":
    subscriber = FootballSub()
    try:
        # Check if there are any messages first
        print("🔍 Checking for existing messages...")
        subscriber.get_one_message()
        
        # Then start listening for new messages
        subscriber.receive_messages()
    finally:
        subscriber.close()