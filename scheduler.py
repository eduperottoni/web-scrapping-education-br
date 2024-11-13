"""Módulo com a definição do escalonador de tarefas do Crawler"""

from dataclasses import dataclass
from queue import Queue
from typing import Callable


@dataclass
class RequestOrder:
    """Classe que abstrai um pedido de requisição"""
    url: str
    action: Callable


class Scheduler:
    """Escalonador de requisições"""
    def __init__(self):
        self.__queue: Queue[RequestOrder] = Queue()

    def queue_request(self, order: RequestOrder):
        """Enfileira um pedido de requisição"""
        self.__queue.put(order)

    def __process_request_order(self):
        request_order = self.__queue.get()
        request_order.action(self, request_order.url)

    def run(self):
        """Executa o loop até que tenham RequestOrderes a serem processadas"""
        while not self.__queue.empty():
            print(self.__queue.qsize())
            self.__process_request_order()
