from Databases.connect import db

def deleteLibur(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM libur where kode_libur = '"+str(id)+"'")
    db.commit()

def deleteIzin(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM izin where kode_izin = '"+str(id)+"'")
    db.commit()

def deleteIzinJam(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM izin_jam where kode_izin_jam = '"+str(id)+"'")
    db.commit()

def deleteLembur(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM lembur where id = '"+str(id)+"'")
    db.commit()