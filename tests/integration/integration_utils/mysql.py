from typing import Any, Dict, List

import pandas as pd
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm.session import Session, close_all_sessions

from lunch_and_learn.models.base import Base

MYSQL_READY_TIMEOUT = 60.0


def local_creds() -> Dict[str, Any]:
    return {
        "database": "replicatormanager",
        "password": "password",
        "username": "root",
        "port": 3305,
        "host": "localhost",
    }


def local_engine() -> Engine:
    return create_engine(
        "mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(  # noqa: FS002
            **local_creds(),
        ),
    )


def local_session() -> Session:
    return Session(bind=local_engine())


def is_mysql_ready() -> bool:
    try:
        with local_engine().connect() as con:
            sql = "SELECT 1"
            con.execute(sql)
            return True
    except:  # noqa: B001,E722  # pylint: disable=bare-except
        return False


def execute_mysql_sql(  # pylint: disable=unused-argument
    sql: str,
    *args: Any,
    **kwargs: Any,
) -> pd.DataFrame:
    engine = local_engine()
    sql = sql.replace("%", "%%")  # noqa: WPS323
    if kwargs.get("return_results"):
        to_return = pd.read_sql(sql, engine)
    else:
        engine.execute(sql)
        to_return = pd.DataFrame()
    return pd.DataFrame(to_return)


def wipe_mysql() -> None:
    engine = local_engine()
    close_all_sessions()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_sample_data(model: Base, sample: List[Dict[str, Any]]) -> None:
    session = local_session()
    for row in sample:
        row_to_be_added = model(**row)
        session.add(row_to_be_added)
    session.commit()
