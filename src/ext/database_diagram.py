#!/usr/bin/env python3

# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2020 NIWA & British Crown (Met Office) & Contributors.
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

"""Create a database diagram of Cylc's database, reading its schema, and adding
relationships manually."""

import sqlite3
import tempfile
from contextlib import closing

import pygraphviz as pgv
from cylc.flow.rundb import CylcSuiteDAO
from eralchemy import render_er, main as eralchemy_main
from eralchemy.main import all_to_intermediary
from docutils.parsers.rst import directives
from sphinx.ext.graphviz import Graphviz

__version__ = '1.0.0'

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
            lines.extend(orphans)
    return lines, orphans


def group_nodes(nodes):
    """Place the provided nodes in a subgraph to keep them together."""
    lines = [
        'subgraph {',
        'rank=same',
        'rankdir=LR'
    ]
    lines.extend([f'"{x}"' for x in nodes])
    return lines + ['}']


class CylcRunDBDirective(Graphviz):
    """Directive which inserts a Cylc run DB graph."""

    option_spec = dict(Graphviz.option_spec)
    required_arguments = 0

    @staticmethod
    def generate_dotcode():
        # get markdown
        with tempfile.NamedTemporaryFile() as tf_db:
            # is_public=False triggers the creation of tables
            CylcSuiteDAO(db_file_name=tf_db.name, is_public=False)
            schema, orphans = schema_to_markdown(db_name=tf_db.name)

        # graph prefix
        dotcode = [
            'graph {',
            'node [label = "\\N", shape = plaintext];',
            'edge [color = gray50, minlen = 2, style = dashed];',
            'rankdir = "LR";'
        ]

        # the database graph
        tables, relationships = all_to_intermediary(schema)
        dotcode.extend([x.to_dot() for x in tables])
        dotcode.extend([x.to_dot() for x in relationships])

        # group orphan nodes to cut down on clutter
        dotcode.extend(group_nodes(orphans))

        # use invisible graph edges to change the graph layout
        dotcode.append(
            f'"task_pool_checkpoints" -- "inheritance"[style=invis];'
        )

        # graph suffix
        dotcode += ['}']

        return dotcode

    def run(self):
        self.content = self.generate_dotcode()
        return Graphviz.run(self)


def setup(app):
    app.add_directive('cylc-db-graph', CylcRunDBDirective)
    return {'version': __version__, 'parallel_read_safe': True}
