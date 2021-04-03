"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import threading
from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        self.current_producer_id = 0
        self.current_cart_id = 0

        self.producer_capacity = {}
        self.producer_furniture = {}
        self.carts = {}
        self.current_products = []

        self.producers_lock = Lock()
        self.consumers_lock = Lock()
        self.cart_lock = Lock()


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        # We start with an id of 0 and increment it for each new producer
        # We also send it as a string. Requirement of the assignment
        with self.producers_lock:
            producer_id = str(self.current_producer_id)
            self.current_producer_id += 1
            self.producer_capacity[producer_id] = self.queue_size_per_producer

            return producer_id


    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # If the producer has available slots to publish his product, he will do
        # so. We decrement his associated available capacity, send his product
        # to the market and map the product to his id.
        if self.producer_capacity[producer_id] > 0:
            self.producer_capacity[producer_id] -= 1
            self.current_products.append(product)
            self.producer_furniture[product] = producer_id

            return True

        return False


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        # We start with a base cart id of 0 and increment it for each new cart.
        # We also map the new cart's id to a list which represents the products
        # that are in the cart. We start with an empty list.
        with self.consumers_lock:
            cart_id = self.current_cart_id
            self.current_cart_id += 1
            self.carts[cart_id] = []

            return cart_id


    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        # If the required product is available on the market, we take it and add
        # it in our cart. We also give the respective producer an opportunity to
        # publish a new product in exchange, so he can make even more money.
        with self.cart_lock:
            if product in self.current_products:
                self.current_products.remove(product)
                self.carts[cart_id].append(product)

                producer_id = self.producer_furniture[product]
                self.producer_capacity[producer_id] += 1

                return True

            return False


    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # We found out that we don't need this product anymore (or we found it
        # cheaper on another marketplace :) ). We remove the product from the
        # cart and put it back on sale, updating the seller's publishing
        # capacity.
        with self.cart_lock:
            self.carts[cart_id].remove(product)
            self.current_products.append(product)

            producer_id = self.producer_furniture[product]
            self.producer_capacity[producer_id] -= 1


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        # We made up our mind about what we will buy. Now everyone will know.
        # We changed the print format to include the newline in the string and
        # not as the ending character to make it thread-safe (ordering is not
        # guaranteed, but concatenation of two lines will not occur.
        for product in self.carts[cart_id]:
            print(f'{threading.current_thread().getName()} bought {product}\n', end='')
