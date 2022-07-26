"""
Author: Mia Tran
Description: This program manages a database using a schema.
"""
import sqlite3
NAME = 'database'


def initialize():
    """
    Initializes the database.
    """
    connection = sqlite3.connect(NAME + '.db')
    with open('schema.sql') as file:
        connection.executescript(file.read())
    connection.commit()


def get_connection():
    """
    Returns a connection to the database.
    :return: Connection to messages database.
    """
    conn = sqlite3.connect(NAME + '.db')
    try:
        conn.execute('SELECT * from posts').fetchall()
    except sqlite3.OperationalError:
        initialize()
    conn.row_factory = sqlite3.Row
    return conn


def select(query, args, one):
    """
    Returns selection result given a query, arguments (if any).
    :param query: Query string.
    :param args: Tuple of arguments.
    :param one: Boolean of whether to fetch one or all.
    :return: Selection result.
    """
    conn = get_connection()
    if one:
        result = conn.execute(query, args).fetchone()
    else:
        result = conn.execute(query, args).fetchall()
    conn.close()
    return result


def execute(statement, args):
    """
    Executes statement given a statement and arguments (if any).
    :param statement: Statement string to execute.
    :param args: Tuple of arguments.
    """
    conn = get_connection()
    conn.execute(statement, args)
    conn.commit()
    conn.close()
