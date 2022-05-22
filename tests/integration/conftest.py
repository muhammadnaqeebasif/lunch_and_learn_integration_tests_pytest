import os

import pytest
from _pytest.config import Config  # noqa: WPS436
from pytest_docker.plugin import Services

from tests.integration.integration_utils.mysql import (
    MYSQL_READY_TIMEOUT,
    is_mysql_ready,
)


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Config) -> str:
    return os.path.join(
        str(pytestconfig.rootdir),
        "tests",
        "integration",
        "docker_environment",
        "docker-compose.yml",
    )


@pytest.fixture(scope="session")
def is_docker_ready(docker_services: Services) -> bool:
    docker_services.wait_until_responsive(
        timeout=MYSQL_READY_TIMEOUT,
        pause=1,
        check=is_mysql_ready,
    )
    return True
