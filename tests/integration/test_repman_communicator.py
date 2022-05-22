import pytest

from lunch_and_learn.models.replicator import Replicator
from lunch_and_learn.repman_communicator import RepManCommunicator
from tests.integration.data import sample_replicator
from tests.integration.integration_utils.mysql import (
    insert_sample_data,
    local_engine,
    wipe_mysql,
)

INITIAL_ACTIVE_REPLICATORS_COUNT = 2
INITIAL_REPLICATORS_COUNT = 3


@pytest.fixture(autouse=True)
def init_repman_replicator_table(is_docker_ready: bool) -> None:
    assert is_docker_ready
    wipe_mysql()

    insert_sample_data(Replicator, sample_replicator.sample)


@pytest.fixture(name="local_repman_communicator")
def local_repman_communicator_fixture(is_docker_ready: bool) -> RepManCommunicator:
    assert is_docker_ready
    return RepManCommunicator(engine=local_engine())


def test_get_replicator_count(local_repman_communicator: RepManCommunicator) -> None:
    assert local_repman_communicator.get_replicators_count() == INITIAL_REPLICATORS_COUNT


def test_get_activereplicator_count(local_repman_communicator: RepManCommunicator) -> None:
    assert local_repman_communicator.get_active_replicators_count() == INITIAL_ACTIVE_REPLICATORS_COUNT


def test_add_new_replicator(local_repman_communicator: RepManCommunicator) -> None:
    local_repman_communicator.add_new_replicator(replicator_name="NewReplicator")
    assert local_repman_communicator.get_replicators_count() == INITIAL_REPLICATORS_COUNT + 1
    assert local_repman_communicator.get_active_replicators_count() == INITIAL_ACTIVE_REPLICATORS_COUNT + 1


def test_activate_replicator(local_repman_communicator: RepManCommunicator) -> None:
    local_repman_communicator.toggle_replicator("Replicator3", active=True)
    assert local_repman_communicator.get_replicators_count() == INITIAL_REPLICATORS_COUNT
    assert local_repman_communicator.get_active_replicators_count() == INITIAL_ACTIVE_REPLICATORS_COUNT + 1


def test_deactivate_replicator(local_repman_communicator: RepManCommunicator) -> None:
    local_repman_communicator.toggle_replicator("Replicator2", active=False)
    assert local_repman_communicator.get_replicators_count() == INITIAL_REPLICATORS_COUNT
    assert local_repman_communicator.get_active_replicators_count() == INITIAL_ACTIVE_REPLICATORS_COUNT - 1


def test_deactivate_replicator_not_present(local_repman_communicator: RepManCommunicator) -> None:
    local_repman_communicator.toggle_replicator("ReplicatorNotPresent", active=False)
    assert local_repman_communicator.get_replicators_count() == INITIAL_REPLICATORS_COUNT
    assert local_repman_communicator.get_active_replicators_count() == INITIAL_ACTIVE_REPLICATORS_COUNT
