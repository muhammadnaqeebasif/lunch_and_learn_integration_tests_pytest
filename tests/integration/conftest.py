import os

import pytest
from _pytest.config import Config  # noqa: WPS436
from pytest_docker.plugin import Services

from tests.integration.integration_utils.mysql import (
    MYSQL_READY_TIMEOUT,
    is_mysql_ready,
)
from tests.integration.integration_utils.presto import (
    PRESTO_READY_TIMEOUT,
    create_presto_schema,
    is_presto_ready,
)


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Config) -> str:
    if os.environ.get("PRESTO_DOCKER", default="false") == "true":
        return os.path.join(
            str(pytestconfig.rootdir),
            "tests",
            "integration",
            "docker_environment",
            "docker-compose-presto.yml",
        )

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

    if os.environ.get("PRESTO_DOCKER", default="false") == "true":
        docker_services.wait_until_responsive(
            timeout=PRESTO_READY_TIMEOUT,
            pause=1,
            check=is_presto_ready,
        )
        create_presto_schema("delta", "replicatormanager")
    return True
