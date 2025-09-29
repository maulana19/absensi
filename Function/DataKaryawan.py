from datetime import datetime
import chardet
import pandas as pd
from Databases.connect import db

def getNamaKaryawan(file):
    data = pd.read_csv(file, delimiter=';', usecols=[0,1,2])
    data_karyawan = data.values.tolist()
    for item in data_karyawan:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM karyawan WHERE id = "+str(item[0]))
        res = cursor.fetchall()
        if res == []:
            cursor.execute('INSERT INTO karyawan VALUES ('+str(item[0])+',"'+str(item[1])+'", "'+str(item[2])+'","")')
            db.commit()

def updateKaryawan(key):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM karyawan WHERE nik = '"+str(key)+"'")
    res = cursor.fetchone()
    
    if res[3] == "":
        cursor.execute("UPDATE karyawan SET jam_kerja_normal = '2' WHERE nik ='"+str(key)+"'")
        db.commit()
    elif res[3] == "2":
        cursor.execute("DELETE FROM jadwal_shift WHERE id_karyawan = '"+str(res[0])+"'")
        cursor.execute("UPDATE karyawan SET jam_kerja_normal = '' WHERE nik ='"+str(key)+"'")
        db.commit()
    return "success"

def insertJadwal(key):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM jadwal_shift WHERE id_karyawan = '"+str(key[0])+"' AND tanggal = '"+str(datetime.strptime(key[1], '%Y-%m-%d')) + "'")
    res = cursor.fetchone()
    if res == None:
        cursor.execute("INSERT INTO jadwal_shift VALUES ('','"+str(key[0])+"', '"+str(datetime.strptime(key[1], '%Y-%m-%d'))+"','"+key[2]+"')")
        db.commit()
    return "success"
