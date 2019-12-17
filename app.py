from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random
import functions
# new for CAS
from flask_cas import CAS

from flask_mail import Mail, Message
app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='localhost',    # default; works on Tempest
    MAIL_PORT=25,               # default
    MAIL_USE_SSL=False,         # default
    MAIL_USERNAME='wstays@wellesley.edu'
)
mail = Mail(app)

app.secret_key = '123wst4ys321'

CAS(app)

app.config['CAS_SERVER'] = 'https://login.wellesley.edu:443'
app.config['CAS_LOGIN_ROUTE'] = '/module.php/casserver/cas.php/login'
app.config['CAS_LOGOUT_ROUTE'] = '/module.php/casserver/cas.php/logout'
app.config['CAS_VALIDATE_ROUTE'] = '/module.php/casserver/serviceValidate.php'
app.config['CAS_AFTER_LOGIN'] = 'index'
# the following doesn't work :-(
# app.config['CAS_AFTER_LOGOUT'] = 'after_logout'

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
db = "achan_db"

@app.route('/')
def index():
    if ('CAS_USERNAME' in session):
        attributes = session['CAS_ATTRIBUTES']
        bnumber = attributes['cas:id']
        
        conn = functions.getConn(db)
        user = functions.getUser(conn,bnumber)
        if not user:
            return redirect("insertUser")

    return render_template('home.html')

@app.route('/profile/<bnumber>', methods=["GET"])
def profile(bnumber):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    user = functions.getUser(conn,bnumber)
    listings = functions.getUserListings(conn,bnumber)
    userRequests = functions.getUserRequests(conn,bnumber)
    if userRequests:
        for r in userRequests: 
            if r['isfilled']:
                r['isfilled'] = 'Y'
            else:
                r['isfilled']='N'
    if user:
        return render_template('profile.html', user=user, listings=listings, requests=userRequests)
    else:
        flash('User does not exist.')
        return redirect(request.referrer)

@app.route('/place/<pid>', methods=["GET"])
def place(pid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    place = functions.getPlace(conn,pid)
    host = functions.getUser(conn,place['bnumber'])
    availability = functions.getAvailabilityForPlace(conn, pid)

    if place:
        return render_template('place.html', place=place, host=host, availability=availability)
    else:
        flash('Listing does not exist.')
        return redirect(request.referrer)

@app.route('/insertUser/', methods=["GET", "POST"])
def insertUser():
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    message=''
    if request.method == 'POST':
        bnumber = request.form['bnumber']
        if len(bnumber) != 9:
            message = 'BNUMBER must be valid'
            flash(message)
            return redirect(request.referrer)
        exists = functions.getUser(conn,bnumber)
        if exists:
            message = 'error: user exists; User with bnumber: %s is already in database' %bnumber
        else:
            email = request.form['email']
            name = request.form['user_name']
            phonenum = request.form['phonenum']
            functions.insertUser(conn,bnumber,email,name,phonenum)
            message = 'User %s inserted.' %name
        flash(message)
        return redirect( url_for('index') )
    else:
        attributes = session['CAS_ATTRIBUTES']
        return render_template('insertUser.html', attributes=attributes)

@app.route('/updateUser/<bnumber>', methods=["GET", "POST"])
def updateUser(bnumber):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    if request.method == 'GET':
        user = functions.getUser(conn,bnumber)
        return render_template('updateUser.html', user=user)
    else:
        if request.form['submit'] == 'update':
            new_bnum = request.form['bnumber']
            exist = functions.getUser(conn,new_bnum)
            if exist and new_bnum != bnumber:
                flash('User already exists')
                return redirect( url_for('updateUser', bnumber=bnumber) )
            else:
                functions.updateUser(conn,new_bnum,request.form['email'],
                    request.form['user_name'],request.form['phonenum'],bnumber)
                flash('User (%s) was successfully updated' %request.form['user_name'])
                return redirect( url_for('updateUser', bnumber=new_bnum) )
        else:
            functions.deleteUser(conn,bnumber)
            flash('User (%s) was deleted successfully' %bnumber)
            return redirect(url_for('index'))

@app.route('/listing/', methods=["GET"])
def listing():
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))
    
    attributes = session['CAS_ATTRIBUTES']
    bnumber = attributes['cas:id']
    conn = functions.getConn(db)
    user = functions.getUser(conn, bnumber)
    return render_template('listingform.html', user=user)

    # else:
    #     flash('you are not logged in. Please login or join')
    #     return redirect(url_for('index'))

@app.route('/listingecho/', methods=['POST'])
def listingecho():
    conn = functions.getConn(db)
    form = request.form
    functions.insertListing(conn, form.get("user"), form.get("street1"),
    form.get("street2"), form.get("city"), form.get("state"),
    form.get("zip"), form.get("country"), form.get("maxguest"), 
    form.get("start"), form.get("end"))

    return render_template('listingconfirmation.html', form=form)

@app.route('/deleteListing/<pid>', methods=['POST'])
def deleteListing(pid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    functions.deleteListing(conn, pid)

    return redirect(url_for('profile', bnumber=session['CAS_ATTRIBUTES']['cas:id']))

@app.route('/deleteAvailability/<aid>', methods=['POST'])
def deleteAvailability(aid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    availability = functions.getAvailability(conn,aid)
    functions.deleteAvailability(conn, aid)

    return redirect(url_for('place', pid=availability['pid']))

@app.route('/editListing/<pid>', methods=['POST', 'GET'])
def editListing(pid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    if (request.method ==  'GET'):
        guestRequest = functions.getPlace(conn, pid)
        return render_template('editListing.html', request=guestRequest)
    else:
        form = request.form
        functions.editListing(conn, pid, form)
        flash("Updated successfully!")
        return redirect(url_for('profile', bnumber=session['CAS_ATTRIBUTES']['cas:id']))

@app.route('/editAvailability/<aid>', methods=['POST', 'GET'])
def editAvailability(aid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    if (request.method ==  'GET'):
        availability = functions.getAvailability(conn, aid)
        return render_template('editAvailability.html', availability=availability)
    else:
        form = request.form
        pid = functions.editAvailability(conn, aid, form)['pid']
        flash("Updated successfully!")
        return redirect(url_for('place', pid=pid))

@app.route('/editRequest/<rid>', methods=['POST', 'GET'])
def editRequest(rid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    if (request.method ==  'GET'):
        userRequest = functions.getRequest(conn, rid)
        return render_template('editRequest.html', request=userRequest)
    else:
        form = request.form
        functions.editRequest(conn, rid, form)
        flash("Updated successfully!")
        return redirect(url_for('profile', bnumber=session['CAS_ATTRIBUTES']['cas:id']))

@app.route('/deleteRequest/<rid>', methods=['POST'])
def deleteRequest(rid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    functions.deleteRequest(conn, rid)

    return redirect(url_for('profile', bnumber=session['CAS_ATTRIBUTES']['cas:id']))

@app.route('/search/listing' ,methods=["GET","POST"])
def searchListing():
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))
    
    conn = functions.getConn(db)
    if request.method == "GET":
        listings = functions.allListings(conn)
        return render_template('search.html', listings=listings)
    if request.method == "POST": 
        arg = request.form.get('searchterm')
        guest=request.form.get('guests')
        if arg == "":
            listings = functions.allListings(conn)
            return render_template('search.html', listings=listings)
        return redirect(url_for('search', query=arg, guest=guest))

@app.route('/search/listing/<query>/<guest>', methods=['GET','POST'])
def search(query,guest):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    
    places = functions.searchPlace(conn, query, guest)
    return render_template('search.html', listings=places, guest=guest, query=query)

@app.route('/search/request' ,methods=["GET","POST"])
def searchRequest():
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    if request.method == "GET":
        aRequest = functions.allRequests(conn)
        return render_template('searchrequest.html', requests=aRequest)
    if request.method == "POST": 
        arg =request.form.get('searchterm')
        guest=request.form.get('guests')
        if arg == "":
            aRequest = functions.allRequests(conn)
            return render_template('searchrequest.html', requests=aRequest)
        return redirect(url_for('searchR', query=arg, guest=guest))


@app.route('/search/request/<query>/<guest>' ,methods=["GET","POST"])
def searchR(query,guest):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    aRequest = functions.searchRequest(conn,query)
    return render_template('searchrequest.html', requests=aRequest)


@app.route('/requestform/', methods=["GET"])
def requesting():
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    attributes = session['CAS_ATTRIBUTES']
    bnumber = attributes['cas:id']

    conn = functions.getConn(db)
    user = functions.getUser(conn, bnumber)
    return render_template('requestform.html', user=user)

@app.route('/requestecho/', methods=['POST'])
def requestecho():
    conn = functions.getConn(db)
    form = request.form
    functions.insertRequest(conn, form.get("user"), form.get("city"),
    form.get("country"), form.get("guestnum"), 
    form.get("start"), form.get("end"))

    return render_template('requestconfirmation.html', form=form)

@app.route('/request/<rid>', methods=["GET"])
def requestPage(rid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    aRequest = functions.getRequest(conn,rid)
    guest = functions.getUser(conn,aRequest['bnumber'])
    if aRequest:
        if aRequest['isfilled']:
            aRequest['isfilled'] = 'Y'
        else:
            aRequest['isfilled']='N'
        return render_template('request.html', aRequest=aRequest, guest=guest)
    else:
        flash('Request does not exist.')
        return redirect(request.referrer)

@app.route('/report/<bnumber>', methods=["GET", "POST"])
def report(bnumber):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))
    
    conn = functions.getConn(db)
    if request.method == "GET":
        return render_template('report.html')
    if request.method == "POST": 
        try:
             # throw error if there's trouble
            sender = session['CAS_ATTRIBUTES']['cas:mail']
            recipient = "wstays@cs.wellesley.edu"
            subject = bnumber + ": " + request.form['issues']
            body = request.form['report']
            # print(['form',sender,recipient,subject,body])
            msg = Message(subject=subject,
                          sender=sender,
                          recipients=[recipient],
                          body=body)
            # print(['msg',msg])
            mail.send(msg)
            flash('email sent successfully')
            return render_template('reportconfirmation.html')

        except Exception as err:
            print(['err',err])
            flash('form submission error'+str(err))
            return redirect( url_for('index') )

@app.route('/addAvailability/<pid>', methods=['POST'])
def addAvailability(pid):
    if ('CAS_USERNAME' not in session):
        return redirect(url_for("index"))

    conn = functions.getConn(db)
    form = request.form
    start = form.get('start')
    end = form.get('end')
    functions.insertAvailability(conn, pid, start,end)

    return redirect(url_for('place', pid=pid))



if __name__ == '__main__':
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
