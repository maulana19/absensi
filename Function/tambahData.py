from Databases.connect import db
import pandas as pd
from datetime import datetime
import random

def insertLibur(data):
    tanggal = data['tanggal'].split('-')
    merge_tanggal = ''
    for t in tanggal:
        merge_tanggal += t
    merge_tanggal += str(random.randrange(1,100))
    str_tanggal = list(merge_tanggal)
    random.shuffle(str_tanggal)
    fixed_random_code = ''.join(str_tanggal)
    kode_libur = 'TL_'+str(fixed_random_code)
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO libur(tanggal,keterangan, kode_libur) VALUES ('"+data['tanggal']+"', '"+data['keterangan']+"', '"+kode_libur+"')")
    db.commit()

def insertDataAbsen(file):
    data = pd.read_csv(file,delimiter=';', usecols=[0,3,4,6])
    data_karyawan = data.values.tolist()
    for data in data_karyawan:
        if data[0] not in [57,17,24,29,87,192,20]:
            tanggal = data[1].split("/")
            tanggal_fix = tanggal[2]+'-'+tanggal[1]+'-'+tanggal[0]

            cursor = db.cursor()
            cursor.execute('SELECT * FROM absensi WHERE id_karyawan = '+str(data[0])+' AND tanggal = "' + tanggal_fix +'"')

            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO absensi VALUES ("","'+tanggal_fix+'", "","", '+str(data[0])+')')
                db.commit()

            if data[3] == "Scan Masuk":
                cursor.execute('UPDATE absensi SET jam_masuk = "'+str(data[2])+'" WHERE id_karyawan = '+str(data[0])+' AND tanggal = "'+tanggal_fix+'"')
                db.commit()
            if data[3] == "Scan Keluar":
                cursor.execute('UPDATE absensi SET jam_keluar = "'+str(data[2])+'" WHERE id_karyawan = '+str(data[0])+' AND tanggal = "'+tanggal_fix+'"')
                db.commit()

def insertIzinKaryawan(data):
    tanggal = data['tanggal']
    status = data['izin']
    keterangan = data['keterangan']
    id_karyawan  = ''

    split_karyawan = data['no_karyawan'].split('-')
    id_karyawan = split_karyawan[0]


    merge_tanggal = ''
    for t in tanggal.split('-'):
        merge_tanggal += t
    merge_tanggal += str(random.randrange(1,100))
    str_tanggal = list(merge_tanggal)
    random.shuffle(str_tanggal)
    fixed_random_code = ''.join(str_tanggal)
    kode_izin = status+'_'+str(fixed_random_code)

    cur = db.cursor()
    cur.execute("SELECT * FROM izin WHERE  tanggal = '"+str(tanggal)+"' AND id_karyawan = '"+str(id_karyawan)+"' LIMIT 1")
    res = cur.fetchone()

    if res:
        print('')
    else:   
        cur = db.cursor()
        cur.execute("INSERT INTO izin(tanggal, status, keterangan, id_karyawan, kode_izin) VALUES ('"+str(tanggal)+"', '"+str(status)+"', '"+str(keterangan)+"', '"+str(id_karyawan)+"', '"+str(kode_izin)+"')")
        db.commit()

def insertIzinJam(data):
    
    split_karyawan = data['no_karyawan'].split('-')
    id_karyawan = split_karyawan[0]

    
    merge_tanggal = ''
    for t in data['tanggal'].split('-'):
        merge_tanggal += t
    merge_tanggal += str(random.randrange(1,100))
    str_tanggal = list(merge_tanggal)
    random.shuffle(str_tanggal)
    fixed_random_code = ''.join(str_tanggal)
    kode_izin = data['izin']+'_'+str(fixed_random_code)


    cur = db.cursor()
    cur.execute("INSERT INTO izin_jam(tanggal, jam_mulai, jam_akhir, status, keterangan, id_karyawan, kode_izin_jam, total_izin) VALUES ('"+str(data['tanggal'])+"', '"+str(data['jam_mulai'])+"', '"+str(data['jam_akhir'])+"', '"+str(data['izin'])+"', '"+str(data['keterangan'])+"', '"+str(id_karyawan)+"', '"+str(kode_izin)+"','"+str(data['total_jam'])+"')")
    db.commit()


def insertLembur(data):
    split_karyawan = data['no_karyawan'].split('-')
    id_karyawan = split_karyawan[0]

    cur = db.cursor()
    cur.execute("INSERT INTO lembur(tanggal, total_jam, id_karyawan) VALUES ('"+str(data["tanggal"])+"','"+str(data["total_jam"])+"','"+str(id_karyawan)+"')")
    db.commit()