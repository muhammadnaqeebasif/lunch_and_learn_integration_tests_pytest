from sqlalchemy import Boolean, Column, Integer, String

from lunch_and_learn.models.base import Base

STRING_COLUMN_DEFAULT_LENGTH = 128


class Replicator(Base):  # type: ignore
    __tablename__ = "replicator"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(STRING_COLUMN_DEFAULT_LENGTH), nullable=False)
    active = Column(Boolean, nullable=False)
