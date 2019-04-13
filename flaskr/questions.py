from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for
)
import os
import shutil
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('questions', __name__, url_prefix='/questions')

@bp.route('/')
@login_required
def index():
    db = get_db()
    problems = db.execute(
        'SELECT p.id, visible, title, body, author_id, username'
        ' FROM problem p JOIN user u ON p.author_id = u.id'
    ).fetchall()
    return render_template('questions/index.html', problems=problems)

@bp.route('/createAdmin', methods=('GET', 'POST'))
@login_required
def createAdmin():
    if request.method == 'POST':
        email = request.form['email']
        error = None
        if not email:
            error = 'Email is required.'
        db = get_db()
        usr = db.execute(
            'SELECT * FROM user'
            ' WHERE id = ?',
            (g.user['id'],)
        ).fetchone()
        if usr['isAdmin'] != "TRUE" and usr['username'] != "csevirus":
            error = 'You are not Admin, You are not supposed to access this page'
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE user SET isAdmin = "TRUE"'
            )
            db.commit()
            return redirect(url_for('questions.index'))
    return render_template('questions/createAdmin.html')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        db = get_db()
        error = None
        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'
        elif db.execute(
            'SELECT id FROM problem WHERE title = ?', (title,)
        ).fetchone() is not None:
            error = 'Title {} is already registered.'.format(title)
        usr = db.execute(
            'SELECT * FROM user'
            ' WHERE id = ?',
            (g.user['id'],)
        ).fetchone()
        if usr['isAdmin'] != "TRUE":
            error = 'You are not Admin, You are not supposed to access this page'
        if error is not None:
            flash(error)
        else:
            path = current_app.config['INSTANCE_PATH']
            try:
                os.makedirs(path+'/'+title)
            except OSError:
                pass
            db = get_db()
            cur = db.cursor()
            cur.execute(
                'INSERT INTO problem (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('questions.update', id = cur.lastrowid ))
    return render_template('questions/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT * FROM problem'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    if post is None:
        abort(404, "Problem id {0} doesn't exist.".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        input = request.files['in']
        output = request.files['out']
        if input.filename == '' or output.filename == '':
            error = 'No selected file'
        extension = input.filename.rsplit('.', 1)[1].lower()
        if extension != 'txt':
            error = 'file extention not permited by the server'
        extension = output.filename.rsplit('.', 1)[1].lower()
        if extension != 'txt':
            error = 'file extention not permited by the server'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            path = current_app.config['INSTANCE_PATH']
            try:
                os.rename(path+'/'+post['title'],path+'/'+title)
            except OSError:
                pass
            input.save(os.path.join(path+'/'+title,'in.txt'))
            output.save(os.path.join(path+'/'+title,'out.txt'))
            db.execute(
                'UPDATE problem SET title = ?, body = ?, visible = ?'
                ' WHERE id = ?',
                (title, body, "TRUE", id)
            )
            db.commit()
            return redirect(url_for('questions.index'))
    return render_template('questions/update.html', post=post)

@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db = get_db()
    path = current_app.config['INSTANCE_PATH']
    shutil.rmtree(path+'/'+post['title'])
    db.execute('DELETE FROM problem WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('questions.index'))
