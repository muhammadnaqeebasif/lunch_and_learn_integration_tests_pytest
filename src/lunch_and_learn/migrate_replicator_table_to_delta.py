import logging


def execute_presto_sql(sql: str) -> None:
    logging.info(sql)


def create_table_replicator_delta() -> None:
    sql = """CREATE TABLE IF NOT EXISTS delta.replicatormanager.replicator (
            id INT,
            replicator VARCHAR(128),
            active BOOLEAN
        )
        """
    execute_presto_sql(sql)


def migrate_replicator_table_to_presto() -> None:
    create_table_replicator_delta()
    sql = """INSERT INTO delta.replicatormanager.replicator
                SELECT id,
                    name,
                    CAST(active AS BOOLEAN)
                FROM replicatormanager.replicatormanager.replicator
                WHERE id NOT IN (SELECT id FROM delta.replicatormanager.replicator)
        """
    execute_presto_sql(sql)
