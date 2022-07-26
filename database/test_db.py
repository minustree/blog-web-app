"""
Author: Mia Tran
Description: This program tests database functionality.
"""
import sqlite3
import pytest
import db
db.initialize()
db.execute('DELETE FROM users WHERE username = ?', ('admin',))


def test_user_blank():
    """
    Test for blank users table.
    """
    users = db.select('SELECT * FROM users', (), False)
    assert users == []


def test_post_blank():
    """
    Test for blank posts table.
    """
    posts = db.select('SELECT * FROM posts', (), False)
    assert posts == []


def test_user_insert():
    """
    Test for user insert.
    """
    db.execute('INSERT INTO users (username, email, password) '
               'VALUES (?, ?, ?)',
               ('Izzy', 'izzyli@gmail.com',
                'experiment'))
    user = db.select('SELECT * FROM users', (), True)
    assert user is not None
    assert user['username'] == 'Izzy'
    assert user['email'] == 'izzyli@gmail.com'
    assert user['password'] == 'experiment'


def test_post_insert():
    """
    Test for post insert.
    """
    db.execute('INSERT INTO posts (username, created, title, content) '
               'VALUES (?, ?, ?, ?)',
               ('Izzy', 'January 1, 1999',
                'Hello World', 'I come from an alien planet.'))
    post = db.select('SELECT * FROM posts', (), True)
    assert post is not None
    assert post['username'] == 'Izzy'
    assert post['created'] == 'January 1, 1999'
    assert post['title'] == 'Hello World'
    assert post['content'] == 'I come from an alien planet.'


def test_user_update():
    """
    Test for user update.
    """
    db.execute('UPDATE users SET email = ?, password = ?'
               ' WHERE id = ?',
               ('izzy@chess.com', 'experiment2', 1))
    user = db.select('SELECT * FROM users', (), True)
    assert user is not None
    assert user['email'] == 'izzy@chess.com'
    assert user['password'] == 'experiment2'


def test_post_update():
    """
    Test for post update.
    """
    db.execute('UPDATE posts SET title = ?, content = ?'
               ' WHERE id = ?',
               ('Bye World', 'I am leaving now.', 1))
    post = db.select('SELECT * FROM posts', (), True)
    assert post is not None
    assert post['title'] == 'Bye World'
    assert post['content'] == 'I am leaving now.'


def test_user_unique():
    """
    Test for user unique.
    """
    with pytest.raises(sqlite3.IntegrityError):
        db.execute('INSERT INTO users (username, email) '
                   'VALUES (?, ?)',
                   ('Izzy', 'izzy@chess.com'))


def test_user_delete():
    """
    Test for user delete.
    """
    db.execute('DELETE FROM users WHERE id = ?', (1,))
    users = db.select('SELECT * FROM users', (), False)
    assert users == []


def test_post_delete():
    """
    Test for post delete.
    """
    db.execute('DELETE FROM posts WHERE id = ?', (1,))
    posts = db.select('SELECT * FROM posts', (), False)
    assert posts == []
