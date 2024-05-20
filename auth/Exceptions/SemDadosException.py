import logging

class SemDadosException(Exception):
    logging.error("SEM DADOS NO BANCO DE DADOS")
    """Exceção levantada quando não há dados no banco de dados."""
