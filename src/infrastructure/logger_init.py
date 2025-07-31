import logging
from logging.handlers import TimedRotatingFileHandler

def logger_init():
    # TODO Инициализацию логера и перехват исключений убрать в отдельные классы
    formatter = logging.Formatter('%(asctime)s : %(levelname)s - %(message)s')

    file_handler = TimedRotatingFileHandler(
        'bot.log',
        when='midnight',
        interval=1,
        backupCount=0,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    result_logger = logging.getLogger('bot')
    result_logger.setLevel(logging.INFO)
    result_logger.addHandler(file_handler)
    result_logger.addHandler(console_handler)

    return result_logger

logger = logger_init()
