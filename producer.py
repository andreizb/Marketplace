"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.producer_id = marketplace.register_producer()


    def run(self):
        """
        The producer tries to publish his products on the market.
        Each product is a tuple made of the product itself, the
        available quantity of that product and a waiting time if
        the product is successfully published on the market.
        """
        while True:
            for product in self.products:
                num = product[1]

                while num > 0:
                    if not self.marketplace.publish(self.producer_id, product[0]):
                        # The producer has to wait before he can try to republish
                        time.sleep(self.republish_wait_time)
                        continue

                    num -= 1
                    # The producer has to wait before he can publish another product
                    time.sleep(product[2])
