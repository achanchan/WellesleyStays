import dbi
DSN = None

def getConn(db):
    global DSN
    if DSN is None:
        DSN = dbi.read_cnf()
    conn = dbi.connect(DSN)
    conn.select_db(db)
    return conn

def checkUser(conn,bnumber):
    curs = dbi.cursor(conn)
    curs.execute('''select *
                    from user
                    where bnumber = %s''',
                    [bnumber])
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

def getUser(conn,bnumber):
    curs = dbi.cursor(conn)
    curs.execute('''select *
                    from user
                    where bnumber = %s''',
                    [bnumber])
    return curs.fetchone()