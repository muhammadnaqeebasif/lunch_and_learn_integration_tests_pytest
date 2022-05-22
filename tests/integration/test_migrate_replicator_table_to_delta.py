import os

import pytest
from pytest_mock import MockerFixture

from lunch_and_learn.migrate_replicator_table_to_delta import (
    migrate_replicator_table_to_presto,
)
from lunch_and_learn.models.replicator import Replicator
from tests.integration.data import sample_replicator
from tests.integration.integration_utils.mysql import insert_sample_data, wipe_mysql
from tests.integration.integration_utils.presto import (
    execute_presto_sql,
    wipe_presto_schema,
)


@pytest.fixture(name="initialise_repman_and_delta")
def initialise_repman_and_delta_fixture(is_docker_ready: bool) -> bool:
    assert is_docker_ready
    wipe_mysql()
    wipe_presto_schema("delta", "replicatormanager")

    insert_sample_data(Replicator, sample_replicator.sample)

    return True


@pytest.fixture(autouse=True)
def apply_presto_patch(mocker: MockerFixture) -> None:
    mocker.patch("lunch_and_learn.migrate_replicator_table_to_delta.execute_presto_sql", execute_presto_sql)


@pytest.mark.skipif(
    os.environ.get("PRESTO_DOCKER", default="false") == "false",
    reason="Skip when not using presto docker",
)
def test_migrate_table_to_presto(initialise_repman_and_delta: bool) -> None:
    assert initialise_repman_and_delta

    migrate_replicator_table_to_presto()
