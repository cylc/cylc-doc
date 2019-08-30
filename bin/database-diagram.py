#!/usr/bin/env python3

# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2019 NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""database-diagram

Create a database diagram of Cylc's database, reading its schema, and adding
relationships manually.

The console output should include the markdown and the dot file used,
and a PNG image with the database diagram will be created in the working
directory, with the name cylc-database.png."""

import logging
import sqlite3
import tempfile
from contextlib import closing

import pygraphviz as pgv
from cylc.flow.rundb import CylcSuiteDAO
from eralchemy import render_er, main as eralchemy_main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ONE_TO_ONE = "?--?"
ONE_TO_MANY = "*--?"


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
        [CylcSuiteDAO.TABLE_TASK_STATES, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_TASK_EVENTS],
        [CylcSuiteDAO.TABLE_TASK_STATES, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_TASK_JOBS],
        [CylcSuiteDAO.TABLE_BROADCAST_STATES, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_BROADCAST_STATES_CHECKPOINTS],
        [CylcSuiteDAO.TABLE_CHECKPOINT_ID, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_BROADCAST_STATES_CHECKPOINTS],
        [CylcSuiteDAO.TABLE_CHECKPOINT_ID, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_SUITE_PARAMS_CHECKPOINTS],
        [CylcSuiteDAO.TABLE_CHECKPOINT_ID, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_TASK_POOL_CHECKPOINTS],
        [CylcSuiteDAO.TABLE_SUITE_PARAMS, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_SUITE_PARAMS_CHECKPOINTS],
        [CylcSuiteDAO.TABLE_TASK_POOL, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_TASK_POOL_CHECKPOINTS],
        [CylcSuiteDAO.TABLE_TASK_POOL, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_TASK_ACTION_TIMERS],
        [CylcSuiteDAO.TABLE_TASK_POOL, ONE_TO_ONE,
         CylcSuiteDAO.TABLE_TASK_LATE_FLAGS],
        [CylcSuiteDAO.TABLE_TASK_POOL, ONE_TO_MANY,
         CylcSuiteDAO.TABLE_TASK_OUTPUTS],
        [CylcSuiteDAO.TABLE_TASK_POOL, ONE_TO_ONE,
         CylcSuiteDAO.TABLE_TASK_TIMEOUT_TIMERS]
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
        tuple: one side with lines of a markdown file, the other with
            the orphan tables
    """
    lines = []
    orphans = []
    relationships = get_relationships()
    with closing(sqlite3.connect(db_name)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            for row in cursor:
                table = row[0]
                lines.append(f"[{table}]")
                for column in get_columns_metadata(table, conn):
                    pk = "*" if column[5] > 0 else ""  # 1 is normally PK
                    label = f"{{label: {column[2].upper()}}}"
                    line = f"\t{pk}{column[1]} {label}"
                    lines.append(line)

                if not any((
                    table in relationship
                    for relationship in relationships
                )):
                    orphans.append(table)
            # in the eralchemy example, relationships go at the end of the file
            lines.extend([" ".join(value) for value in relationships])
    return lines, orphans


def add_orphans_subgraph(file_name, orphans, append=None):
    """Add a subgraph with the orphans tables, so they appear grouped
    at the bottom of the diagram.

    What this function is doing is, basically, to re-organise the current
    content of the file, by separating some portions of the original dot file
    in lists, and then returning them in order, so that they can be rendered.

    Args:
        file_name (str): dot file name
        orphans (list): list of orphan tables
        append (list): list of table names to be appended to the subgraph
    """
    # TODO: rather complicated, some extensibility work around eralchemy
    #       may make it way simpler later
    graph_beginning = []  # dot file graph beginning
    subgraph = ["subgraph orphan {rank = sink\n"]  # subgraph
    subgraph_append = []  # extra tables that must be appended to subgraph too
    graph = []  # normal graph
    relationships = []  # the relationships after the graph
    if not append:
        append = []
    with open(file_name) as dot_file:
        for line in dot_file:
            if line.strip() == "}":
                # we are closing the graph section ourselves later
                continue
            if not line.strip().startswith("\""):
                # only lines in our dot file that start with " are tables
                # and relationships
                graph_beginning.append(line)
            else:
                if "--" in line:
                    # relationships use -- for eralchemy
                    relationships.append(line)
                else:
                    # we got a table line, just need to group orphans
                    # and not orphans
                    quote_left = line.index("\"", 0) + 1
                    quote_right = line.index("\"", quote_left)
                    table = line[quote_left:quote_right]
                    if table in orphans:
                        subgraph.append(line)
                    elif table not in append:
                        graph.append(line)
                    else:
                        subgraph_append.append(line)
        subgraph_append.append("}\n")  # close the subgraph section
        relationships.append("}\n")  # close the main graph section

    # combine again everything creating a new dot file
    return "".join(graph_beginning +
                   subgraph +
                   subgraph_append +
                   graph +
                   relationships)


def render_dot_graph(file_name):
    G = pgv.AGraph(file_name)
    G.draw("cylc-database.png", prog="dot")


def main():
    """Create Cylc public database, run diagram creation tool, and
    then finally adjust the generated dot file for better display layout."""

    # temporary file to hold the Cylc database to be passed to eralchemy
    with tempfile.NamedTemporaryFile() as tf_db:
        # is_public=False triggers the creation of tables
        CylcSuiteDAO(db_file_name=tf_db.name, is_public=False)
        logger.info(f"Cylc database created in {tf_db.name}!")
        schema, orphans = schema_to_markdown(db_name=tf_db.name)

        # eralchemy needs a file that ends with .er to parse markdown
        with tempfile.NamedTemporaryFile(suffix=".er") as tf_md:
            markdown = "\n".join(schema)
            logger.info(f"Markdown generated: ")
            logger.info(markdown)
            tf_md.write(markdown.encode("utf-8"))
            tf_md.flush()

            # this is the output of eralchemy, instead of a PNG, get a DOT file
            with tempfile.NamedTemporaryFile(suffix=".dot") as tf_dot:
                # TODO: monkey-patching not really elegant, but here we need
                #       to change the graph beginning in the dot output, and
                #       there is no way of doing that in eralchemy
                eralchemy_main.GRAPH_BEGINNING = (
                    'graph {\n'
                    '  node [label = "\\N", shape = plaintext];\n'
                    '  edge [color = gray50, minlen = 2, style = dashed];\n'
                    '  rankdir = "TB";\n'
                    '  newrank="true"\n'
                )

                render_er(input=tf_md.name, output=tf_dot.name, mode="dot")
                tf_dot.flush()

                # finally modify a little bit the DOT file, by adding a
                # subgraph with the orphan tables, and one linking table
                # broadcast_states, which is not orphan, but balances the graph
                new_file = add_orphans_subgraph(tf_dot.name, orphans,
                                                ["broadcast_states"])

                logger.info("Final dot file: ")
                logger.info(new_file)

                tf_dot.truncate(0)
                tf_dot.write(new_file.encode("utf-8"))

                render_dot_graph(tf_dot.name)


if __name__ == '__main__':
    main()
