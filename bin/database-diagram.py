#!/usr/bin/env python3

"""Create a database diagram of Cylc's database, reading its schema, and adding
relationships manually. The output contains a dot file, and a PNG image."""

import logging
import sqlite3
import tempfile
from contextlib import closing

from cylc.flow.rundb import CylcSuiteDAO
from eralchemy import render_er, main as eralchemy_main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_relationships():
    """These are the database relationships. * means 0..N, and ? {0, 1}.

    Ideally we would have these relationships in the database model, but doing
    that would require further tests to prevent regressions for users
    after they update Cylc. So we are hard-coding the relationships here
    for now.

    Returns:
        list: with relationships in the eralchemy markdown syntax.
    """
    # TODO: remove this once the relationships are in the DB, and then automate
    return [
        "task_states *--? task_events",
        "task_states *--? task_jobs",
        "broadcast_states *--? broadcast_states_checkpoints",
        "checkpoint_id *--? broadcast_states_checkpoints",
        "checkpoint_id *--? suite_params_checkpoints",
        "checkpoint_id *--? task_pool_checkpoints",
        "suite_params *--? suite_params_checkpoints",
        "task_pool *--? task_pool_checkpoints",
        "task_pool *--? task_action_timers",
        "task_pool ?--? task_late_flags",
        "task_pool *--? task_outputs",
        "task_pool ?--? task_timeout_timers"
    ]


def get_columns_metadata(table_name, conn):
    """Return the metadata for the columns in a table.

    Args:
        table_name (str): name of the DB table to retrieve the columns.
        conn (sqlite3.Connection): SQLite connection.
    Returns:
        list: an array with the cid, name, type, notnull, default_value,
        and pk value (0=not, 1=yes).
    """
    with closing(conn.cursor()) as cursor:
        cursor.execute(f'PRAGMA table_info({table_name})')
        return cursor.fetchall()


def schema_to_markdown(db_name):
    """Return the database markdown schema.

    Args:
        db_name (str): database name
    Returns:
        list: lines of a markdown file
    :return: array with markdown lines
    """
    lines = []
    with closing(sqlite3.connect(db_name)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            for row in cursor:
                lines.append(f"[{row[0]}]")
                for column in get_columns_metadata(row[0], conn):
                    pk = "*" if column[5] > 0 else ""  # 1 is normally PK
                    label = f"{{label: {column[2].upper()}}}"
                    line = f"\t{pk}{column[1]} {label}"
                    lines.append(line)
            # in the eralchemy example, relationships go at the end of the file
            lines.extend(get_relationships())
    return lines

def main():
    """Create Cylc public database, run diagram creation tool, and
    then finally adjust the generated dot file for better display layout."""

    # temporary file to hold the Cylc database to be passed to eralchemy
    with tempfile.NamedTemporaryFile() as tf_db:
        # is_public=False triggers the creation of tables
        CylcSuiteDAO(db_file_name=tf_db.name, is_public=False)
        logger.info(f"Cylc database created in {tf_db.name}!")
        schema = schema_to_markdown(db_name=tf_db.name)

        # eralchemy needs a file that ends with .er to parse markdown
        with tempfile.NamedTemporaryFile(suffix=".er") as tf_md:
            markdown = "\n".join(schema)
            logger.info(f"Markdown generated: ")
            logger.info(markdown)
            tf_md.write(markdown.encode("utf-8"))
            tf_md.flush()

            with tempfile.NamedTemporaryFile(suffix=".dot") as tf_dot:
                # TODO: monkey-patching not really elegant, but here we need
                #       to change the graph beginning in the dot output, and
                #       there is no way of doing that in eralchemy
                eralchemy_main.GRAPH_BEGINNING = (
                    '  graph {\n'
                    '      node [label = "\\N", shape = plaintext];\n'
                    '      edge [color = gray50, minlen = 2, style = dashed];\n'
                    '      rankdir = "TB";\n'
                    '      newrank="true"\n'
                )

                render_er(input=tf_md.name, output=tf_dot.name, mode="dot")
                logger.info("")


if __name__ == '__main__':
    main()
