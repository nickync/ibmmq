import ibmmq
import json
import time
import random

class GolfPublisher:
    def __init__(self):
        self.qmgr = None
        self.topic = None
        self.connect()
    
    def connect(self):
        """Connect to QM_GOLF and open the topic"""
        try:
            self.qmgr = ibmmq.connect(
                "QM_GOLF", 
                "DEV.APP.SVRCONN", 
                "localhost(1414)",
                user="app", 
                password="password"
            )
            # Open topic for publishing
            self.topic = ibmmq.Topic(self.qmgr, "SPORTS.GOLF")
            print("✅ Connected to QM_GOLF, topic: sports/golf")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise
    
    def publish_scores(self, player, score, course="St. Andrews"):
        """Publish a golf score update"""
        message = {
            "sport": "golf",
            "event": "score_update",
            "player": player,
            "score": score,
            "course": course,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            self.topic.put(json.dumps(message))
            print(f"📤 Published: {player} scored {score} at {course}")
        except Exception as e:
            print(f"❌ Publish failed: {e}")
    
    def run(self, num_messages=5):
        """Publish multiple messages"""
        players = ["Tiger Woods", "Rory McIlroy", "Scottie Scheffler", 
                   "Jon Rahm", "Justin Thomas", "Collin Morikawa"]
        courses = ["St. Andrews", "Augusta National", "Pebble Beach", 
                   "TPC Sawgrass", "Royal Birkdale"]
        
        for i in range(num_messages):
            player = random.choice(players)
            score = random.randint(65, 75)  # Golf scores
            course = random.choice(courses)
            self.publish_scores(player, score, course)
            time.sleep(random.randint(1, 3))
    
    def close(self):
        if self.topic:
            self.topic.close()
        if self.qmgr:
            self.qmgr.disconnect()
        print("🔌 Disconnected from QM_GOLF")

if __name__ == "__main__":
    publisher = GolfPublisher()
    try:
        publisher.run(num_messages=10)
    finally:
        publisher.close()