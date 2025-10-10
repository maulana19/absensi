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
    cursor.execute("DELETE FROM lembur where kode_lembur = '"+str(id)+"'")
    db.commit()

def deletePinjamanPajak(id):
    cur = db.cursor()
    cur.execute("DELETE FROM pinjaman_pajak WHERE kode_potongan_lain = '"+str(id)+"'")
    db.commit()

def deleteKomplain(id):
    cur = db.cursor()
    cur.execute("DELETE FROM komplain WHERE kode_komplain = '"+str(id)+"'")
    db.commit()
def deleteKaryawan(id):
    cur = db.cursor()
    cur.execute("DELETE FROM komplain WHERE id_karyawan = '"+str(id)+"'")
    cur.execute("DELETE FROM jadwal_shift WHERE id_karyawan = '"+str(id)+"'")
    cur.execute("DELETE FROM pinjaman_pajak WHERE id_karyawan = '"+str(id)+"'")
    cur.execute("DELETE FROM lembur WHERE id_karyawan = '"+str(id)+"'")
    cur.execute("DELETE FROM izin WHERE id_karyawan = '"+str(id)+"'")
    cur.execute("DELETE FROM izin_jam WHERE id_karyawan = '"+str(id)+"'")
    cur.execute("DELETE FROM insentif WHERE id_karyawan = '"+str(id)+"'")
    cur.execute("DELETE FROM absensi WHERE id_karyawan = '"+str(id)+"'")
    cur.execute("DELETE FROM karyawan WHERE nik = '"+str(id)+"'")
    db.commit()