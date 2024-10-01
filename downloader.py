"""Módulo com definições do componente Downloader"""

import requests

class Downloader:
    """Classe que define o componente Downloader"""

    @staticmethod
    def download(url: str) -> bytes:
        """Faz o download do conteúdo da URL

        Args:
            url: URL para realizar a requisição
        """
        response = requests.get(url, timeout=100)
        return response.content
