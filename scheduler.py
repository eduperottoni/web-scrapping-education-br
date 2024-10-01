from dataclasses import dataclass
from .downloader import Downloader

@dataclass
class RequestOrder:
    url: str


class Scheduler:
    """Escalonador de requisições"""
    def __init__(self):
        self.__queue: list[RequestOrder] = []
        self.__downloader: Downloader = Downloader()

    def queue_request(self, order: RequestOrder):
        """Enfileira um pedido de requisição"""
        self.__queue.append(order)