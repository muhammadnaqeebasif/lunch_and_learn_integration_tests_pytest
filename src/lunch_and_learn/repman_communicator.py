from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from lunch_and_learn.models.replicator import Replicator


class RepManCommunicator:
    def __init__(
        self: "RepManCommunicator",
        engine: Engine,
    ) -> None:
        self.engine = engine
        self.session = Session(bind=engine)

    def get_replicators_count(self: "RepManCommunicator") -> int:
        return self.session.query(Replicator).count()

    def get_active_replicators_count(self: "RepManCommunicator") -> int:
        return self.session.query(Replicator).filter(Replicator.active).count()

    def add_new_replicator(self: "RepManCommunicator", replicator_name: str) -> None:
        new_replicator = Replicator()
        new_replicator.name = replicator_name
        new_replicator.active = True

        self.session.add(new_replicator)
        self.session.commit()

    def toggle_replicator(self: "RepManCommunicator", replicator_name: str, active: bool) -> None:
        replicator_to_toggle_query = self.session.query(Replicator).filter(Replicator.name == replicator_name)
        replicator_to_toggle = replicator_to_toggle_query.first()

        if replicator_to_toggle:
            replicator_to_toggle.active = active
            self.session.add(replicator_to_toggle)
            self.session.commit()
