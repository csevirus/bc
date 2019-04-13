from flask import (
    Blueprint, flash, current_app, g, redirect, render_template, request, url_for
)
import os
import subprocess
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.questions import get_post

bp = Blueprint('solver', __name__, url_prefix='/solver')
semaphore = 1;

def p():
    global semaphore
    while(semaphore == 0):
        pass;
    semaphore -= 1

def v():
    global semaphore
    semaphore += 1

@bp.route('/<int:id>', methods=('POST','GET'))
@login_required
def index(id):
    post = get_post(id,False)
    if request.method == 'POST':
        p();
        path = current_app.config['INSTANCE_PATH']+'/'+post['title']
        ret = request.get_json()
        lang = ret['lang']
        code = ret['code']
        timetaken = ret['timetaken']
        verdict = ""
        score = 0
        msg = ""
        passed = 0
        write_code(lang,code,path)
        verdict = run_compiler(lang,path)
        if verdict == "Compiled Successfully" :
            passed = int(check_ac(path))
            if passed == 0:
                msg = "Wrong Answer"
            else:
                msg = "Accepted"
                score += int(300-timetaken)/5
                score += 10*passed
            score += 20
        else :
            msg = show_compilation_err(verdict,path)
        db = get_db()
        cur = db.cursor()
        cur.execute(
        'INSERT INTO submission (author_id, problem_id, verdict, score, code, msg, passed)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?)',
        (g.user['id'], id, verdict, score, code, msg, passed)
        )
        db.commit()
        v();
        return str(cur.lastrowid)
    return render_template('solver/index.html', post = post)

@bp.route('/submission/<int:id>', methods=('GET',))
@login_required
def submission(id):
    submission = get_submission(id,False)
    return render_template('solver/submission.html', submission = submission)

def get_submission(id, check_author=True):
    submission = get_db().execute(
        'SELECT verdict, msg, passed, score, code FROM submission'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    if submission is None:
        abort(404, "Submission id {0} doesn't exist.".format(id))
    if check_author and submission['author_id'] != g.user['id']:
        abort(403)
    return submission

def write_code(lang,code,path):
    fin = open(path+'/code.'+lang,"w")
    fin.write(code)
    fin.close()

def run_compiler(lang,path):
    out = open(path+"/output.txt","w")
    err = open(path+"/err.txt","w")
    fin = open(path+"/in.txt","r")
    rerr = open(path+"/rerr.txt","w")
    run_err = ""
    p1 = path + "/code"
    if lang == "py":
        path1 =path+"/code.py"
        subprocess.call(["python",path1],stdout=out,stderr=err,stdin=fin)
    if lang == "cpp":
        path1 =path+"/code.cpp"
        sr = subprocess.call(["g++",path1,"-o",p1],stderr=err)
        err.close()
        err = open(path+"/err.txt","r")
        run_err = err.read()
        if run_err == "" :
            subprocess.call([p1],stdout=out,stderr=rerr,stdin=fin)
    if lang == "java":
        path1 = path+"/code.java"
        subprocess.call(["javac",path1],stderr=err)
        subprocess.call(["java","-cp",p,"code"],stdout=out,stderr=rerr,stdin=fin)
    if lang == "c":
        path1 = path+"/code.c"
        subprocess.call(["g++",path1,"-o",p1],stderr=err)
        err.close()
        err = open(path+"/err.txt","r")
        run_err = err.read()
        if run_err == "" :
            subprocess.call([p1],stdout=out,stderr=rerr,stdin=fin)
    out.close()
    err.close()
    fin.close()
    rerr.close()
    rerr = open(path+"/rerr.txt","r")
    err = open(path+"/err.txt","r")
    compiling_err = ""
    compiling_err = err.read()
    run_err = ""
    run_err = rerr.read()
    if compiling_err == "" and run_err == "":
        return "Compiled Successfully"
    if run_err == "" :
        return "Compilation Error"
    return "Runtime Error"

def check_ac(path):
    f1 = open(path+"/out.txt","r")
    f2 = open(path+"/output.txt","r")
    count = 0
    for line1 in f2 :
        if line1 == f1.readline() :
            count+=1
    return count

def show_compilation_err(compiled,path):
    if compiled == "Compilation Error" :
        err = open(path+"/err.txt","r")
    else :
        err = open(path+"/rerr.txt","r")
    return err.read()
