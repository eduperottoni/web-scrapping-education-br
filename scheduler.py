from dataclasses import dataclass
from .downloader import Downloader
from typing import Callable
from queue import Queue


@dataclass
class RequestOrder:
    """Classe que abstrai um pedido de requisição"""
    url: str
    action: Callable


class Scheduler:
    """Escalonador de requisições"""
    def __init__(self):
        self.__queue: Queue[RequestOrder] = Queue()
        self.__downloader: Downloader = Downloader()

    def queue_request(self, order: RequestOrder):
        """Enfileira um pedido de requisição"""
        self.__queue.put(order)

    def download(self, order: RequestOrder) -> bytes:
        """Faz o download de alguma URL chamando o Downloader"""
        return self.__downloader.download(order.url)
