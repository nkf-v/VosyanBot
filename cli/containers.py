import logging.config

from dependency_injector import containers, providers

from cli.services import TestService

from . import services

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    test_service = providers.Singleton(
        services.TestService,
        text=config.test.text,
    )
