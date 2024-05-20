import logging

class NotFound(Exception):
    logging.error("DADOS NÃO ENCONTRADOS NO BANCO DE DADOS")
    """Exceção levantada quando não encontrado no banco de dados."""
