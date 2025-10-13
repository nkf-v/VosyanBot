import sys

from dependency_injector.wiring import Provide, inject

from .services import TestService
from .containers import Container


@inject
def main(
        test: TestService = Provide[Container.test_service]
    # logger = Provide[Container.logging],
):
    test.print()
    # logger.info('Test DI SUCCESS')

    # try:
    #     db.connect(reuse_if_open=True)
    #     app()
    # finally:
    #     db.close()

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])