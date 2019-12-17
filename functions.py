import dbi

DSN = None

def getConn(db):
    '''returns a database connection to the given database'''
    global DSN
    if DSN is None:
        DSN = dbi.read_cnf()
    conn = dbi.connect(DSN)
    conn.select_db(db)
    return conn

def getUser(conn, bnumber):
    '''Returns the user given their bnumber'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from user where bnumber=%s''', [bnumber])
    return curs.fetchone()

def insertAvailability(conn, pid, start, end):
    '''Inserts an availability for the place with the given pid'''
    curs=dbi.cursor(conn)
    curs.execute('''insert into availability(pid, start, end) values(%s, %s, %s)''',
                [pid, start, end])

def insertListing(conn, bnumber, street1, street2, city, state, zipcode, country, maxguest, start, end):
    '''Inserts a listing and the corresponding availability'''
    curs = dbi.cursor(conn)
    curs.execute('''insert into place(bnumber, city, country, street1, street2,
                    state, maxguest, postalcode) values(%s, %s, %s, %s, %s, %s, %s, %s)''',
                [bnumber, city, country, street1, street2, state, maxguest, zipcode])
    pid = curs.lastrowid
    insertAvailability(conn, pid, start, end)
    return pid

def editListing(conn, pid, newListing):
    '''Updates a listing with the new information provided in dictionary form'''
    curs = dbi.cursor(conn)
    curs.execute('''update place set city=%s, country=%s, street1=%s, street2=%s,
                    state=%s, maxguest=%s, postalcode=%s where pid=%s''', 
                    [newListing['city'], newListing['country'], newListing['street1'],
                    newListing['street2'], newListing['state'], newListing['maxguest'],
                    newListing['zip'], pid])  
                
def allListings(conn):
    '''returns all the listings in the database'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place''')
    return curs.fetchall()

def allRequests(conn):
    '''returns all the unfilled requests in the database'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from request where isfilled=0''')
    return curs.fetchall()

def getUserListings(conn, bnumber):
    '''returns all the listings that belong to the specific user identified by the bnumber'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place where bnumber=%s''', [bnumber])
    return curs.fetchall()

def getUserRequests(conn, bnumber):
    '''returns all the requests that that belong to the specific user identified by the bnumber'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from request where bnumber=%s''', [bnumber])
    return curs.fetchall()

def getPlace(conn, pid):
    '''returns the place that responds to the given pid'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place where pid=%s''', [pid])
    return curs.fetchone()

def searchPlace(conn, search, guest):
    '''returns all the places whos city contains search and maxguest is greater than or equal to guest'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place where city like %s and maxguest>=%s''', ['%'+search+'%', guest])
    return curs.fetchall()

def searchRequest(conn, search):
    '''returns all the unfilled requests whos city contains search'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from request where city like %s and isfilled=0''', ['%'+search+'%'])
    return curs.fetchall()

def insertUser(conn,bnumber,email,name,phonenum):
    '''inserts a user into the database'''
    curs = dbi.cursor(conn)
    curs.execute('''insert into user(bnumber,email,name,phonenum)
                    values (%s,%s,%s,%s)''',
                    [bnumber,email,name,phonenum])

def updateUser(conn,new_bnum,email,name,phonenum,bnumber):
    '''update the user with the given bnumbers information in the database'''
    curs = dbi.cursor(conn)
    curs.execute('''update user
                    set bnumber=%s, email=%s, name=%s, phonenum=%s
                    where bnumber = %s''',
                    [new_bnum,email,name,phonenum,bnumber])

def deleteUser(conn,bnumber):
    '''delete the user with the given bnumber from the database'''
    curs = dbi.cursor(conn)
    curs.execute('''delete from user
                    where bnumber = %s''',
                    [bnumber])

def deleteListing(conn,pid):
    curs = dbi.cursor(conn)
    curs.execute('''delete from place
                    where pid = %s''',
                    [pid])

def deleteRequest(conn,rid):
    curs = dbi.cursor(conn)
    curs.execute('''delete from request
                    where rid = %s''',
                    [rid])

def insertRequest(conn, bnumber, city, country, guestnum, start, end):
    '''Inserts a request into the database'''
    curs = dbi.cursor(conn)
    curs.execute('''insert into request(bnumber, guestnum, city, country,
                start,end) values(%s, %s, %s, %s, %s, %s)''',
                [bnumber, guestnum, city, country, start, end])
                
def getRequest(conn, rid):
    '''return the request with the given rid'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from request where rid=%s''', [rid])
    return curs.fetchone()

def editRequest(conn, rid, newRequest):
    '''updates the request with the new information stored in dict'''
    curs = dbi.dictCursor(conn)
    curs.execute('''update request set guestnum=%s, city=%s , country=%s,
                    start=%s, end=%s where rid=%s''', 
                    [newRequest['guestnum'], newRequest['city'], 
                    newRequest['country'], newRequest['start'], 
                    newRequest['end'], rid])

def getAvailabilityForPlace(conn, pid):
    '''return all the availabilities for a place with the given pid'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from availability where pid=%s''', [pid])
    return curs.fetchall()

def deleteAvailability(conn,aid):
    '''delete the availability with the given aid'''
    curs = dbi.cursor(conn)
    curs.execute('''delete from availability
                    where aid = %s''',
                    [aid])

def getAvailability(conn,aid):
    '''return the avialability with the given aid'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from availability where aid=%s''', [aid])
    return curs.fetchone()

def editAvailability(conn, aid, newAvailability):
    '''updates the availability with the new information stored in dict'''
    curs = dbi.dictCursor(conn)
    curs.execute('''update availability set start=%s, end=%s where aid=%s''', 
                    [newAvailability['start'], newAvailability['end'], aid])
    curs.execute('''select pid from availability where aid=%s''', [aid])
    return curs.fetchone()

def insertPic(conn, pid, filename):
    '''inserts a photo into the database paired with the id of the place the image is of'''
    curs = dbi.dictCursor(conn)
    curs.execute('''insert into pic(pid, filename) values (%s, %s)
                    on duplicate key update filename = %s''',
                    [pid, filename, filename])

def findPic(conn, pid):
    '''finds the filename of the picture of a place given the pid'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select filename from pic where pid=%s''',
                    [pid])
    return curs.fetchone()