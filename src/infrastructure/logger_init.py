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

    tg_logger = logging.getLogger("telegram")
    tg_logger.addHandler(file_handler)
    tg_logger.addHandler(console_handler)
    tg_logger.setLevel(logging.INFO)

    httpx_logger = logging.getLogger("httpx")
    httpx_logger.addHandler(file_handler)
    httpx_logger.addHandler(console_handler)
    httpx_logger.setLevel(logging.INFO)

    peewee_logger = logging.getLogger("peewee")
    peewee_logger.addHandler(file_handler)
    peewee_logger.addHandler(console_handler)
    peewee_logger.setLevel(logging.INFO)

    app_logger = logging.getLogger('bot')
    app_logger.addHandler(file_handler)
    app_logger.addHandler(console_handler)
    app_logger.setLevel(logging.INFO)

    return app_logger

logger = logger_init()
