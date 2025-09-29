from Databases.connect import db

def updateLibur(value, column, uid):
    cur = db.cursor()
    cur.execute("UPDATE libur SET "+column+" = '"+value+"' WHERE kode_libur = '"+uid+"'")
    db.commit()


def updateIzin(value,column,  id):
    cur = db.cursor()
    cur.execute("UPDATE izin SET "+column+" = '"+value+"' WHERE kode_izin = '"+id+"'")
    db.commit()

def updateIzinJam(value,column,  id):
    cur = db.cursor()
    cur.execute("UPDATE izin_jam SET "+column+" = '"+value+"' WHERE kode_izin_jam = '"+id+"'")
    db.commit()

