"""
Author: Mia Tran
Description: This program runs a Flask blog site using an SQL database.
"""
import sqlite3
from datetime import date
from flask import flash, Flask, redirect, url_for, request, session, make_response, render_template
from database import db
from forms import PostForm, RegisterForm, LoginForm

app = Flask(__name__)
app.run(host='0.0.0.0', port=81)
app.secret_key = b'_0#y=!"AWDp*2\n\xec]/'


@app.route("/")
def home():
    """
    Displays the home page.
    :return: Main page with current posts.
    """
    posts = db.select('SELECT * FROM posts', (), False)
    return render_template('home.html', posts=posts)


@app.route("/userlist")
def userlist():
    """
    Displays the userlist.
    :return: Page with table of all registered users.
    """
    if session.get('username') != 'admin':
        return redirect(url_for('home'))
    users = db.select('SELECT * FROM users', (), False)
    return render_template('userlist.html', users=users)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Displays the registration page and allows the user to register and account.
    :return: Page to register user, or redirect to registration success.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            db.execute('INSERT INTO users (username, email, password) '
                       'VALUES (?, ?, ?)',
                       (form.username.data, form.email.data, form.password.data))
        except sqlite3.IntegrityError:
            flash("User already exists.")
            return render_template('register.html', form=form)
        return redirect(url_for('register_success'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Displays the login page.
    :return: Page with login fields, or a redirect to the home page.
    """
    if 'username' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():

        # get user and check if they exist
        user = db.select('SELECT * FROM users WHERE email = (?) AND password = (?)',
                         (form.email.data, form.password.data), True)
        if user is None:
            flash('Password is incorrect or user does not exist.')
            return render_template('login.html', form=form)

        # set session
        session['username'] = user['username']

        # if session is admin, redirect to userlist
        if session.get('username') == 'admin':
            return redirect(url_for('userlist'))

        return redirect(url_for('login_success'))
    return render_template('login.html', form=form)


@app.route("/register/success")
def register_success():
    """
    Displays the registration success page.
    :return: Page confirming registration was successful.
    """
    return render_template('success.html', message="You have successfully registered.")


@app.route("/login/success")
def login_success():
    """
    Displays the Login success page.
    :return: Page confirming login was successful.
    """
    return render_template('success.html', message="You have successfully logged in.")


@app.route("/logout")
def logout():
    """
    Displays the logout page.
    :return: Page confirming logout was successful.
    """
    session.pop('username', None)
    return render_template('success.html', message="You have successfully logged out.")


@app.route("/about")
def about():
    """
    Displays the about page.
    :return: Page with information about the site.
    """
    # counts number of times page has been accessed
    count = request.cookies.get('count')
    if count is None:
        count = 0
    count = int(count) + 1

    resp = make_response(render_template('about.html', count=count))
    resp.set_cookie('count', str(count))
    return resp


@app.route("/delete/<int:post_id>", methods=('GET', 'POST'))
def delete(post_id):
    """
    Deletes a post with the given post id.
    :param post_id: ID of post to delete.
    :return: Page confirming deletion was successful.
    """
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    return render_template('success.html', message="Post successfully deleted.")


@app.route("/edit/<int:post_id>", methods=('GET', 'POST'))
def edit(post_id):
    """
    Allows user to edit a post with the given post id.
    :param post_id: ID of post to edit.
    :return: Page to allow user to edit post or redirect to the home page.
    """
    form = PostForm()
    post = db.select('SELECT * FROM posts WHERE id = ?', (post_id,), True)
    if post is None:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        db.execute('UPDATE posts SET title = ?, content = ?'
                   ' WHERE id = ?',
                   (form.title.data, form.content.data, post_id))
        return redirect(url_for('home'))
    form.title.data = post['title']
    form.content.data = post['content']

    return render_template('edit.html', form=form)


@app.route("/new", methods=('GET', 'POST'))
def new():
    """
    Allows user to write a new a post.
    :return: Page to write post or redirect to the home page.
    """
    form = PostForm()
    if form.validate_on_submit():
        today = date.today()
        db.execute('INSERT INTO posts (username, created, title, content) '
                   'VALUES (?, ?, ?, ?)',
                   (session.get('username'), today.strftime("%B %d, %Y"),
                    form.title.data, form.content.data))
        return redirect(url_for('home'))
    return render_template('new.html', form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
