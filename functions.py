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

def insertListing(conn, bnumber, street1, street2, city, state, zipcode, country, maxguest, start, end):
    '''Inserts a listing and the corresponding availability'''
    curs = dbi.cursor(conn)
    curs.execute('''insert into place(bnumber, city, country, street1, street2,
                    state, maxguest, postalcode) values(%s, %s, %s, %s, %s, %s, %s, %s)''',
                [bnumber, city, country, street1, street2, state, maxguest, zipcode])
    pid = curs.lastrowid
    curs.execute('''insert into availability(pid, start, end) values(%s, %s, %s)''',
                [pid, start, end])
                
def allListings(conn):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place''')
    return curs.fetchall()

def allRequests(conn):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from request where isfilled=0''')
    return curs.fetchall()

def getUserListings(conn, bnumber):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place where bnumber=%s''', [bnumber])
    return curs.fetchall()

def getUserRequests(conn, bnumber):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from request where bnumber=%s''', [bnumber])
    return curs.fetchall()

def getPlace(conn, pid):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place where pid=%s''', [pid])
    return curs.fetchone()

def searchPlace(conn, search):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place where city like %s''', ['%'+search+'%'])
    return curs.fetchall()

def searchRequest(conn, search):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from request where city like %s and isfilled=0''', ['%'+search+'%'])
    return curs.fetchall()

def insertUser(conn,bnumber,email,name,phonenum):
    curs = dbi.cursor(conn)
    curs.execute('''insert into user(bnumber,email,name,phonenum)
                    values (%s,%s,%s,%s)''',
                    [bnumber,email,name,phonenum])

def updateUser(conn,new_bnum,email,name,phonenum,bnumber):
    curs = dbi.cursor(conn)
    curs.execute('''update user
                    set bnumber=%s, email=%s, name=%s, phonenum=%s
                    where bnumber = %s''',
                    [new_bnum,email,name,phonenum,bnumber])

def deleteUser(conn,bnumber):
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
    '''Inserts a request'''
    curs = dbi.cursor(conn)
    curs.execute('''insert into request(bnumber, guestnum, city, country,
                start,end) values(%s, %s, %s, %s, %s, %s)''',
                [bnumber, guestnum, city, country, start, end])
def getRequest(conn, rid):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from request where rid=%s''', [rid])
    return curs.fetchone()
