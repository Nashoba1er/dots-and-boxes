# dots_and_boxes/logger.py

import logging


# Configuration du logger
def setup_logger():
    logger = logging.getLogger('dots_and_boxes')  # Nom du logger
    # Définir le niveau de log (DEBUG pour tout afficher)
    logger.setLevel(logging.DEBUG)

    # Créer un format de log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    # Créer un handler pour afficher les logs dans la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Ajouter le handler au logger
    logger.addHandler(console_handler)

    # Optionnel : Créer un handler pour écrire les logs dans un fichier
    file_handler = logging.FileHandler('game.log')  # Logs dans un fichier 'game.log'
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Initialiser le logger
logger = setup_logger()
