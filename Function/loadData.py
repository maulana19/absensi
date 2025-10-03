from Databases.connect import db
from datetime import datetime, date
import pandas as pd
from dateutil.relativedelta import relativedelta
from collections import defaultdict

def getDataAbsen():
    
    data_default = defaultdict(list)

    # Parse into datetime object
    date_obj = date.today()

    # Move to next month and set day to 10
    start_period = datetime.strftime((date_obj - relativedelta(months=1)).replace(day=26), "%Y-%m-%d")
    # start_period = "01/07/2025"
    end_period = datetime.strftime((date_obj + relativedelta(months=1)).replace(day=25), "%Y-%m-%d")
    # end_period = "10/07/2025"
    
    cursor = db.cursor()
    cursor.execute("SELECT absensi.*, karyawan.nama FROM absensi JOIN karyawan ON absensi.id_karyawan = karyawan.id WHERE tanggal BETWEEN '"+str(start_period)+"' AND '"+str(end_period)+"' ORDER BY karyawan.nama ASC")
    res = cursor.fetchall()
    
    for item in res:
        name = item[-1]
        date_obj = datetime.strptime(str(item[1]), "%Y-%m-%d").strftime("%A")
        day_extra = list(item) + [date_obj]
        data_default[name].append(day_extra)
    
    data = list(data_default.values())
    return data


def searchDataAbsen(key):

    data_default = defaultdict(list)

    # Parse into datetime object
    date_obj = date.today()

    # Move to next month and set day to 10
    start_period = datetime.strftime((date_obj - relativedelta(months=1)).replace(day=26), "%Y-%m-%d")
    # start_period = "01/07/2025"
    end_period = datetime.strftime((date_obj + relativedelta(months=1)).replace(day=25), "%Y-%m-%d")
    # end_period = "10/07/2025"    
    
    cursor = db.cursor()
    cursor.execute("SELECT absensi.*, karyawan.nama FROM absensi JOIN karyawan ON absensi.id_karyawan = karyawan.id WHERE karyawan.nama LIKE '%"+key+"%' AND tanggal BETWEEN '"+str(start_period)+"' AND '"+str(end_period)+"' ORDER BY karyawan.nama ASC")
    res = cursor.fetchall()

    for item in res:

        name = item[-1]
        date_obj = datetime.strptime(str(item[1]), "%Y-%m-%d").strftime("%A")
        day_extra = list(item) + [date_obj]
        data_default[name].append(day_extra)
    
    data = list(data_default.values())
    return data

def getDataKaryawan():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM karyawan")
    res = cursor.fetchall()
    data = []
    for item in res:
        dt = list(item)
        data.append(dt)
    return data

def searchDataKaryawan(key):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM karyawan WHERE nama LIKE '%"+str(key)+"%'")
    res = cursor.fetchall()
    data = []
    for item in res:
        dt = list(item)
        data.append(dt)
    return data

def searchDataKaryawanID(key):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM karyawan WHERE nik = '"+str(key)+"'")
    res = cursor.fetchone()

    return res

def getDataJadwal(key):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM jadwal_shift WHERE id_karyawan = '"+str(key)+"'")
    res = cursor.fetchall()
    data = []
    for item in res:
        print(item)
    return res

def getHeaderAbsen():
    tanggal_sekarang = pd.Timestamp('today').normalize()
    bulan_lalu = tanggal_sekarang - pd.DateOffset(months=1)
    start_absen = pd.Timestamp(
        year=bulan_lalu.year,
        month=bulan_lalu.month,
        day= 26
    )
    tanggal = pd.date_range(start_absen,tanggal_sekarang)
    return tanggal.date

def getDataAbsenTable(tanggal):
    data_absen = []
    data = []
    cursor = db.cursor()
    cursor.execute("SELECT * FROM karyawan")
    res = cursor.fetchall()
    for i in res:
        data.append([i[0], i[2], i[1]])
    cursor.execute("SELECT tanggal FROM libur")
    libur_res = cursor.fetchall()
    tanggal_libur = []
    for tl in libur_res:
        tanggal_libur.append(tl[0])
    for d in data:
        for t in tanggal:
            if str(t) in tanggal_libur:
                d.append('L')
            else:
                cursor2 = db.cursor()
                cursor2.execute("SELECT * FROM izin WHERE id_karyawan = '"+str(d[2])+"' AND tanggal = '"+str(t)+"'")
                res2 = cursor2.fetchone()
                if res2:
                    d.append(res2[2])
                else:
                    cursor3 = db.cursor()
                    cursor3.execute("SELECT * FROM absensi WHERE id_karyawan = '"+str(d[0])+"' AND tanggal = '"+str(t)+"'")
                    res3 = cursor3.fetchone()
                    if res3:
                        d.append('1')
                    else:
                        d.append('0')
        data_absen.append(d)
    return(data_absen)

def getDataLibur():
    cursor = db.cursor()
    cursor.execute('SELECT* FROM libur')
    res = cursor.fetchall()
    return res

def getDataLiburById(key):
    cursor = db.cursor()
    cursor.execute("SELECT* FROM libur WHERE kode_libur = '"+key+"'")
    res = cursor.fetchone()
    return res

def searchDataLibur(key):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM libur WHERE keterangan LIKE '%"+str(key)+"%' OR tanggal LIKE '%"+str(key)+"%'")
    res = cursor.fetchall()
    data = []
    for item in res:
        dt = list(item)
        data.append(dt)
    return data

def getDataIzin():
    cur = db.cursor()
    cur.execute("SELECT * FROM izin")
    res = cur.fetchall()
    
    data = []

    for d in res:
        cur2 = db.cursor()
        cur2.execute("SELECT nama FROM karyawan WHERE nik = '"+d[4]+"' LIMIT 1")
        res2 = cur2.fetchone()
        data.append([res2[0], d[1], d[2], d[3], d[4], d[5]])
    return data

def getDataIzinByIDAndTanggal(id):
    data = []
    cur = db.cursor()
    cur.execute("SELECT * FROM izin WHERE  kode_izin = '"+str(id)+"'")
    res = cur.fetchone()

    cur2 = db.cursor()
    cur2.execute("SELECT nama FROM karyawan WHERE nik = '"+str(res[4])+"' LIMIT 1")
    res2 = cur2.fetchone()
    data.append(res2[0])
    data.append(res[1])
    data.append(res[2])
    data.append(res[3])
    data.append(res[4])
    
    return data

def searchDataIzin(key):
    cursor = db.cursor()
    cursor.execute("SELECT izin.*, karyawan.nama as nama FROM IZIN JOIN karyawan ON karyawan.nik = izin.id_karyawan WHERE nama LIKE '%"+str(key)+"%'")
    res = cursor.fetchall()
    data = []
    for item in res:
        dt = list(item)
        dt[0] = dt[6]
        data.append(dt)
    return data

def searchDataAbsenTable(key, tanggal):
    data_absen = []
    data = []

    cursor = db.cursor()
    cursor.execute("SELECT * FROM karyawan WHERE nama LIKE '%"+str(key)+"%'")
    res = cursor.fetchall()
    for i in res:
        data.append([i[0], i[2], i[1]])
    
    cursor.execute("SELECT tanggal FROM libur")
    libur_res = cursor.fetchall()
    tanggal_libur = []
    for tl in libur_res:
        tanggal_libur.append(tl[0])
    for d in data:
        for t in tanggal:
            if str(t) in tanggal_libur:
                d.append('L')
            else:
                cursor2 = db.cursor()
                cursor2.execute("SELECT * FROM izin WHERE id_karyawan = '"+str(d[2])+"' AND tanggal = '"+str(t)+"'")
                res2 = cursor2.fetchone()
                if res2:
                    d.append(res2[2])
                else:
                    cursor3 = db.cursor()
                    cursor3.execute("SELECT * FROM absensi WHERE id_karyawan = '"+str(d[0])+"' AND tanggal = '"+str(t)+"'")
                    res3 = cursor3.fetchone()
                    if res3:
                        d.append('1')
                    else:
                        d.append('0')
        data_absen.append(d)
    return(data_absen)

def getDataIzinJam():
    cur = db.cursor()
    cur.execute("SELECT izin_jam.tanggal,izin_jam.jam_mulai,izin_jam.jam_akhir,izin_jam.status,izin_jam.keterangan,izin_jam.kode_izin_jam,izin_jam.tanggal, karyawan.nama FROM izin_jam JOIN karyawan ON izin_jam.id_karyawan = karyawan.nik")
    data = cur.fetchall()
    return data

def getDataIziJamById(id):
    cur = db.cursor()
    cur.execute("SELECT izin_jam.tanggal,izin_jam.jam_mulai,izin_jam.jam_akhir,izin_jam.status,izin_jam.keterangan,izin_jam.kode_izin_jam,izin_jam.total_izin, karyawan.nik, karyawan.nama FROM izin_jam JOIN karyawan ON izin_jam.id_karyawan = karyawan.nik WHERE kode_izin_jam = '"+id+"' limit 1")
    data = cur.fetchone()
    return data

def searchDataIzinJam(id):
    cur = db.cursor()
    cur.execute("SELECT izin_jam.tanggal,izin_jam.jam_mulai,izin_jam.jam_akhir,izin_jam.status,izin_jam.keterangan,izin_jam.kode_izin_jam,izin_jam.tanggal, karyawan.nama FROM izin_jam JOIN karyawan ON izin_jam.id_karyawan = karyawan.nik WHERE nama LIKE '%"+id+"%'")
    data = cur.fetchall()
    return data

def getDataLembur():
    cur = db.cursor()
    cur.execute("SELECT lembur.*, karyawan.nama FROM lembur JOIN karyawan on lembur.id_karyawan = karyawan.nik")
    data = cur.fetchall()
    return data

def searchDataAbsenByDateAndNIK(nik, tanggal):
    cur = db.cursor()
    cur.execute("SELECT karyawan.id FROM karyawan where nik = '"+nik+"' limit 1")
    id_karyawan = cur.fetchone()[0]

    cur.execute("SELECT * FROM absensi JOIN karyawan ON absensi.id_karyawan = karyawan.id where id_karyawan = "+str(id_karyawan)+" AND absensi.tanggal = '"+tanggal+"'")
    data_karyawan = cur.fetchall()
    return data_karyawan

def hitungHariKerja(karyawan):
    tanggal = getHeaderAbsen()
    data_libur = getDataLibur()
    tanggal_libur = []
    for l in data_libur:
        tanggal_libur.append(l[1])

    harikerja = 0
    for t in tanggal:
        cur = db.cursor()
        cur.execute("SELECT * FROM absensi WHERE tanggal = '"+t.strftime('%Y-%m-%d')+"' AND id_karyawan = "+ str(karyawan) +" LIMIT 1")
        res = cur.fetchone()
        if res:
            if res[1] not in tanggal_libur:
                harikerja+=1
    return harikerja

def hitungHariTidakKerja(id, izin):
    tanggal = getHeaderAbsen()

    totalizin = 0
    for t in tanggal:
        cur = db.cursor()
        cur.execute("SELECT * FROM IZIN WHERE tanggal = '"+t.strftime('%Y-%m-%d')+"' AND id_karyawan = '"+ str(id) +"' AND status = '"+str(izin)+"' LIMIT 1")
        res = cur.fetchone()
        if res and res[2] == izin:
            totalizin += 1
    return totalizin

def hitungIzinJam(id):
    tanggal = getHeaderAbsen()
    izinjam = 0
    for t in tanggal:
        cur = db.cursor()
        print("SELECT * FROM izin_jam where tanggal = '"+t.strftime('%Y-%m-%d')+"' AND id_karyawan = '"+ str(id) +"'")
        cur.execute("SELECT * FROM izin_jam where tanggal = '"+t.strftime('%Y-%m-%d')+"' AND id_karyawan = '"+ str(id) +"'")
        res = cur.fetchone()
        if res:
            print(res[8])
            izinjam += int(res[8])
    return izinjam
            