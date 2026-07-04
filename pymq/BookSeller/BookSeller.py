import ibmmq
import random
import time
import json

class Record:
    def __init__(self, title, price, store):
        self.title = title
        self.price = price
        self.store = store

class BookSeller:
    def __init__(self, name):
        self.name = name
        self.books = {}

        self.add_book("The Great Gatsby", 10.99 )
        self.add_book("To Kill a Mockingbird", 8.99)
        self.add_book("1984", 12.99)
        self.add_book("Pride and Prejudice", 9.99)
        self.add_book("The Catcher in the Rye", 11.99)
        self.add_book("The Hobbit", 14.99)
        self.add_book("Fahrenheit 451", 13.99)

        self.connect()

    def connect(self):
        self.qManager = ibmmq.connect("QM1", "DEV.APP.SVRCONN", "localhost(1414)", user="app", password="passw0rd")
        self.queque = ibmmq.Queue(self.qManager, "DEV.QUEUE.1")

    def add_book(self, title, price):
        self.books[title] = price

    def get_price(self, title):
        return self.books.get(title, None)

    def list_books(self):
        return self.books
    
    def send_message(self, message):
        self.queque.put(json.dumps(message))
        print('Message sent to queue: ', message)

    # def __del__(self):
    #     if self.queque:
    #         self.queque.close()
    #     if self.qManager:
    #         self.qManager.disconnect()

def main():
    seller = BookSeller("My Book Store")
    seller2 = BookSeller("My Book Store 2")

    sold = 0
    while sold < 10:
        time.sleep(random.randint(0, 10))  # Simulate time taken to sell a book
        book_title = random.choice(list(seller.books.keys()))
        price = seller.get_price(book_title)
        record = Record(book_title, price, seller.name)
        #message = f"Seller1 Sold '{book_title}' for ${price:.2f}"
        seller.send_message(record.__dict__)

        book_title2 = random.choice(list(seller2.books.keys()))
        price2 = seller2.get_price(book_title2)
        #message2 = f"Seller2 Sold '{book_title2}' for ${price2:.2f}"
        record2 = Record(book_title2, price2, seller2.name)
        seller2.send_message(record2.__dict__)

        sold += 1


if __name__ == "__main__":
    main()