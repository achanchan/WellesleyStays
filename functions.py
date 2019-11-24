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
    curs.execute('''insert into places(bnumber, city, country, street1, street2,
                    state, maxguest, postalcode) values(%s, %s, %s, %s, %s, %s)''',
                [bnumber, street1, street2, city, state, zipcode, country, maxguest])
    pid = curs.lastrowid
    curs.execute('''insert into availablity(pid, start, end) values(%s, %s, %s)''',
                [pid, start, end])
                
def allListings(conn):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place''')
    return curs.fetchall()

def searchPlace(conn, search, guests):
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from place where city like %s and maxguest=%s''', [search,guest])
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
