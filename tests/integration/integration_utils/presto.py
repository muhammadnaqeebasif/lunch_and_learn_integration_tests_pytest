import logging
from typing import Any

import pandas as pd
import prestodb

PRESTO_READY_TIMEOUT = 120.0
PRESTO_PORT = 8081


def is_presto_ready() -> bool:
    try:  # noqa: WPS229
        create_presto_schema("delta", "test_schema")
        execute_presto_sql(
            "CREATE TABLE IF NOT EXISTS delta.test_schema.test (primary_key INT)",
        )
    except Exception as error:  # pylint: disable=broad-except
        logging.error(str(error))
        return False

    logging.info("Presto Server is ready...")
    return True


def execute_presto_sql(  # pylint: disable=unused-argument
    sql: str,
    *args: Any,
    **kwargs: Any,
) -> pd.DataFrame:
    conn = prestodb.dbapi.connect(
        host="localhost",
        port=PRESTO_PORT,
        user="admin",
        catalog="system",
        schema="runtime",
    )
    sql = sql.replace("\n", " ")
    cur = conn.cursor()
    cur.execute(sql)
    data_returned = cur.fetchall()
    colnames = [part[0] for part in cur.description]
    try:
        if data_returned:
            to_return = pd.DataFrame(data_returned)
            to_return.columns = colnames
        else:
            to_return = pd.DataFrame(columns=colnames)

    except Exception as error:  # pylint: disable=broad-except
        logging.error(error)
        to_return = pd.DataFrame()

    cur.cancel()
    conn.close()
    return to_return


def create_presto_schema(catalog: str, schema: str) -> None:
    sql = f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}"
    execute_presto_sql(sql)


def get_all_presto_table_data(
    catalog: str,
    schema: str,
    table_name: str,
) -> pd.DataFrame:
    sql_query = f"""SELECT *
                    FROM {catalog}.{schema}.{table_name}
    """
    return execute_presto_sql(sql_query)


def wipe_presto_schema(catalog: str, schema: str) -> None:
    all_schemas = execute_presto_sql(f'SHOW SCHEMAS FROM "{catalog}"')["Schema"]
    if schema.replace('"', "") not in list(all_schemas):
        return

    all_tables = execute_presto_sql(f"SHOW TABLES FROM {catalog}.{schema}")["Table"]
    for table_name in list(all_tables):
        truncate_presto_table(catalog, schema, table_name)


def truncate_presto_table(catalog: str, schema: str, table_name: str) -> None:
    create_temp_table_query = f"""CREATE TABLE {catalog}.{schema}.temp AS
                (SELECT * FROM {catalog}.{schema}.{table_name}
                    WHERE 1 = 0
                )
        """  # noqa: WPS221
    drop_table_query = f"DROP TABLE IF EXISTS {catalog}.{schema}.{table_name}"

    rename_table_query = f"""ALTER TABLE {catalog}.{schema}.temp
                             RENAME TO {catalog}.{schema}.{table_name}
                          """  # noqa: WPS221

    execute_presto_sql(create_temp_table_query)
    execute_presto_sql(drop_table_query)
    execute_presto_sql(rename_table_query)
