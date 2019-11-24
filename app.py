from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random
import profile
import functions

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

@app.route('/insert/', methods=["GET", "POST"])
def insert():
    conn = profile.getConn("wstays_db")
    message=''
    if request.method == 'POST':
        bnumber = request.form['bnumber']
        if len(bnumber) != 9:
            message = 'BNUMBER must be valid'
            flash(message)
            return redirect(request.referrer)
        exists = profile.checkUser(conn,bnumber)
        if exists:
            message = 'error: user exists; User with bnumber: %s is already in database' %bnumber
        else:
            email = request.form['email']
            name = request.form['user_name']
            phonenum = request.form['phonenum']
            profile.insertUser(conn,bnumber,email,name,phonenum)
            message = 'User %s inserted.' %name
        flash(message)
        return redirect( url_for('update', bnumber=bnumber) )
    else:
        return render_template('form.html')

@app.route('/update/<bnumber>', methods=["GET", "POST"])
def update(bnumber):
    conn = profile.getConn("wstays_db")
    if request.method == 'GET':
        user = profile.getUser(conn,bnumber)
        return render_template('update.html', user=user)
    else:
        if request.form['submit'] == 'update':
            new_bnum = request.form['bnumber']
            exist = profile.checkUser(conn,new_bnum)
            if exist and new_bnum != bnumber:
                flash('User already exists')
                return redirect( url_for('update', bnumber=bnumber) )
            else:
                profile.updateUser(conn,new_bnum,request.form['email'],
                    request.form['user_name'],request.form['phonenum'],bnumber)
                flash('User (%s) was successfully updated' %request.form['user_name'])
                return redirect( url_for('update', bnumber=new_bnum) )
        else:
            profile.deleteUser(conn,bnumber)
            flash('User (%s) was deleted successfully' %bnumber)
            return redirect(url_for('index'))

<<<<<<< HEAD
@app.route('/form/', methods=["GET", "POST"])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        try:
            return render_template('form.html')

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

=======
>>>>>>> c062e5996d22878163715edfc49de2c5205156e4
@app.route('/listing/', methods=["GET"])
def listing():
    conn = functions.getConn('wstays_db')

    # if 'bnumber' in session:
    # uncomment out code once login is implemented
    # bnumber = session['bnumber']
    bnumber = "B20856852"   
    user = functions.getUser(conn, bnumber)
    return render_template('listingform.html', user=user)

    # else:
    #     flash('you are not logged in. Please login or join')
    #     return redirect(url_for('index'))

@app.route('/listingecho/', methods=['POST'])
def listingecho():
    conn = functions.getConn('wstays_db')
    form = request.form
    functions.insertListing(conn, form.get("user"), form.get("street1"),
    form.get("street2"), form.get("city"), form.get("state"),
    form.get("zip"), form.get("country"), form.get("maxguest"), 
    form.get("start"), form.get("end"))

    return render_template('listingconfirmation.html', form=form)
    
@app.route('/search/' ,methods=["GET","POST"])
def searchListing():
    conn = functions.getConn("wstays_db")
    listings = functions.allListings(conn)
    return render_template('search.html', listings=listings)

@app.route('/search/<query>', methods=['GET','POST'])
def search(query):
    conn = read.getConn('achan_db')
  
    places = functions.searchPlace(conn, request.form['searchterm'],request.form['guests'])
    return render_template('search.html',
                               query = request.form['searchterm'], data=places)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
