from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/listing/')
def listing():
    pass

@app.route('/insert/', methods=["GET", "POST"])
def insert():
    conn = lookup.getConn("nli2_db")
    message=''
    if request.method == 'POST':
        bnumber = request.form['bnumber']
        exists = profile.checkUser(conn,bnumber)
        if exists:
            message = 'error: user exists; User with bnumber: %s is already in database' %bnumber
        else:
            email = request.form['email']
            name = request.form['name']
            phonenum = request.form['phonenum']
            profile.insertUser(conn,bnumber,email,name,phonenum)
            message = 'User %s inserted.' %name
        flash(message)
        return redirect( url_for('update', bnumber=bnumber) )
    else:
        return render_template('insert.html', title='Insert A User')

@app.route('/update/<tt>', methods=["GET", "POST"])
def update(tt):
    conn = lookup.getConn("wmdb")
    if request.method == 'GET':
        movie = lookup.getMovie(conn,tt)
        director = ''
        if movie[3] is None:
            director = 'None Specified'
        else:
            director = lookup.getDirector(conn,movie[3])
        return render_template('update.html', movie=movie, director=director)
    else:
        if request.form['submit'] == 'update':
            new_tt = request.form['movie-tt']
            exist = lookup.checkMovie(conn,new_tt)
            director_id = request.form['movie-director']
            valid_nm = lookup.checkDirector(conn,director_id)
            if exist and new_tt != tt:
                flash('Movie already exists')
                return redirect( url_for('update', tt=tt) )
            else:
                if valid_nm or director_id is None:
                    lookup.updateMovie(conn,new_tt,request.form['movie-title'],
                        request.form['movie-release'],request.form['movie-director'],tt)
                    flash('Movie (%s) was successfully updated' %request.form['movie-title'])
                    return redirect( url_for('update', tt=new_tt) )
                else:
                    flash('Director ID is invalid: %s' %director_id)
                    return redirect( url_for('update', tt=tt) )
        else:
            lookup.deleteMovie(conn,tt)
            flash('Movie (%s) was deleted successfully' %tt)
            return redirect(url_for('index'))

@app.route('/form/', methods=["GET", "POST"])
def form():
    if request.method == 'GET':
        return render_template('form.html', page_title='FORM')
    else:
        try:
            return render_template('form.html', page_title='FORM')

        except Exception as err:
            flash('form submission error'+str(err))
            return redirect( url_for('index') )

@app.route('/formecho/', methods=['GET','POST'])
def formecho():
    if request.method == 'GET':
        return render_template('form_data.html',
                               method=request.method,
                               form_data=request.args,
                               page_title='ECHO')
    elif request.method == 'POST':
        return render_template('form_data.html',
                               method=request.method,
                               form_data=request.form,
                               page_title='ECHO')
    else:
        return render_template('form_data.html',
                               method=request.method,
                               form_data={},
                               page_title='ECHO')

if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
