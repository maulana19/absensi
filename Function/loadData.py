import locale
from Databases.connect import db
from datetime import datetime, date, timedelta
import pandas as pd
from dateutil.relativedelta import relativedelta
from collections import defaultdict

def getDataAbsen():
    
    data_default = defaultdict(list)

    # Parse into datetime object
    date_obj = date.today()

    # Move to next month and set day to 10
    if int(datetime.strftime(date_obj, "%d"))>=26:
        start_period = datetime.strftime(date_obj.replace(day=26), "%Y-%m-%d")
    else:
        start_period = datetime.strftime((date_obj - relativedelta(months=1)).replace(day=26), "%Y-%m-%d")
    
    end_period = datetime.strftime(date_obj.replace(day=25), "%Y-%m-%d")
    
    cursor = db.cursor()
    cursor.execute("SELECT absensi.*, karyawan.nama FROM absensi JOIN karyawan ON absensi.id_karyawan = karyawan.nik WHERE tanggal BETWEEN '"+str(start_period)+"' AND '"+str(end_period)+"' ORDER BY karyawan.nama ASC")
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
    cursor.execute("SELECT absensi.*, karyawan.nama FROM absensi JOIN karyawan ON absensi.id_karyawan = karyawan.nik WHERE karyawan.nama LIKE '%"+key+"%' AND tanggal BETWEEN '"+str(start_period)+"' AND '"+str(end_period)+"' ORDER BY karyawan.nama ASC")
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
                    cursor3.execute("SELECT * FROM absensi WHERE id_karyawan = '"+str(d[2])+"' AND tanggal = '"+str(t)+"'")
                    res3 = cursor3.fetchone()
                    if res3:
                        d.append('')
                    else:
                        d.append('A')
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
                    cursor3.execute("SELECT * FROM absensi WHERE id_karyawan = '"+str(d[2])+"' AND tanggal = '"+str(t)+"'")
                    res3 = cursor3.fetchone()
                    if res3:
                        d.append('')
                    else:
                        d.append('A')
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


def searchDataLembur(key):
    print("SELECT lembur.*, karyawan.nama FROM lembur join karyawan on lembur.id_karyawan = karyawan.nik where karyawan.nama LIKE '%"+str(key)+"%'")
    cur = db.cursor()
    cur.execute("SELECT lembur.*, karyawan.nama FROM lembur join karyawan on lembur.id_karyawan = karyawan.nik where karyawan.nama LIKE '%"+str(key)+"%'")
    data = cur.fetchall()
    return data

def searchDataLemburById(id):
    cur = db.cursor()
    cur.execute("SELECT lembur.*, karyawan.nama, absensi.jam_masuk, absensi.jam_keluar FROM lembur JOIN karyawan on lembur.id_karyawan = karyawan.nik JOIN absensi on lembur.id_karyawan = absensi.id_karyawan where kode_lembur = '"+id+"' and absensi.tanggal = lembur.tanggal limit 1")
    data = cur.fetchone()
    return data

def searchDataAbsenByDateAndNIK(nik, tanggal):
    cur = db.cursor()
    cur.execute("SELECT * FROM absensi JOIN karyawan ON absensi.id_karyawan = karyawan.nik where id_karyawan = '"+str(nik)+"' AND absensi.tanggal = '"+tanggal+"'")
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
        cur.execute("SELECT * FROM absensi WHERE tanggal = '"+t.strftime('%Y-%m-%d')+"' AND id_karyawan = '"+ str(karyawan) +"' LIMIT 1")
        res = cur.fetchone()
        if res:
            if res[1] not in tanggal_libur:
                harikerja+=1
    return harikerja

def hitungHariLibur(tanggal_libur):
    total_libur = 0
    cur = db.cursor()
    for l in tanggal_libur:    
        cur.execute("SELECT * FROM libur WHERE tanggal = '"+l+"' limit 1")
        res = cur.fetchone()
        if res:
            total_libur += 1
    return total_libur

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
        cur.execute("SELECT * FROM izin_jam where tanggal = '"+t.strftime('%Y-%m-%d')+"' AND id_karyawan = '"+ str(id) +"'")
        res = cur.fetchone()
        if res:
            izinjam += int(res[8])
    return izinjam

def getGajiKaryawan(id):
    cur = db.cursor()
    cur.execute("SELECT u_pokok, t_jabatan, t_keahlian, t_lain FROM karyawan WHERE nik = '"+id+"' limit 1")
    res = cur.fetchone()
    return res      

def getJamLembur(id):
    totalLembur = 0
    cur = db.cursor()
    cur.execute("select total_jam from lembur WHERE id_karyawan = '"+id+"'")
    res = cur.fetchall()
    if res:
        for l in res:
            totalLembur+= int(l[0])
    return totalLembur      

def getInsentif():
    cur = db.cursor()
    cur.execute("SELECT karyawan.nama, karyawan.nik, insentif.* FROM insentif JOIN karyawan ON insentif.id_karyawan = karyawan.nik")
    res = cur.fetchall()
    return res
def searchInsentif(key):
    data = []
    cur = db.cursor()
    cur.execute("SELECT karyawan.nama, karyawan.nik, insentif.* FROM insentif JOIN karyawan ON insentif.id_karyawan = karyawan.nik where karyawan.nama LIKE '%"+str(key)+"%'")
    res = cur.fetchall()
    for i in res:
        insentif = list(i)
        insentif.append(locale.currency(int(int(i[5]) * int(i[6])), grouping=True))
        insentif[6] = locale.currency(int(i[6]), grouping=True)
        data.append(insentif)
    return data

def getInsentifById(id):
    cur = db.cursor()
    cur.execute("SELECT karyawan.nama, karyawan.nik, insentif.* FROM insentif JOIN karyawan ON insentif.id_karyawan = karyawan.nik WHERE kode_insentif = '"+str(id)+"' limit 1")
    res = cur.fetchone()
    return res

def getTotalnsentif(id):
    date_obj = date.today()
    totalinsentif = 0
    start_period = datetime.strftime((date_obj - relativedelta(months=1)).replace(day=26), "%Y-%m-%d")
    end_period = datetime.strftime(date_obj.replace(day=25), "%Y-%m-%d")

    cur = db.cursor()
    cur.execute("SELECT * FROM insentif where tanggal between '"+str(start_period)+"' AND '"+str(end_period)+"' AND id_karyawan = '"+id+"'")
    res = cur.fetchall()
    
    for i in res:
        totalinsentif += (int(i[3])*int(i[4]))
    return totalinsentif


def getPinjamanPajak():
    date_obj = datetime.today()
    
    if int(date_obj.strftime("%d")) > 25:
        start = datetime.strftime(date_obj.replace(day=26), "%Y-%m-%d")
    else:
        start = datetime.strftime((date_obj - relativedelta(months=1)).replace(day=26), "%Y-%m-%d")

    data = []

    start_time = datetime.strptime(start, "%Y-%m-%d")

    cur = db.cursor()
    cur.execute("SELECT pinjaman_pajak.*, karyawan.nama FROM pinjaman_pajak JOIN karyawan on karyawan.nik = pinjaman_pajak.id_karyawan")
    res = cur.fetchall()
    for i in res:
        if i[3]:
            tanggal = datetime.strptime(i[3], "%Y-%m-%d")
            if tanggal > start_time and date_obj <= tanggal:
                in_data = []
                for idx, d in enumerate(i):
                    if idx == 2:
                        in_data.append(locale.currency(int(d), grouping=True))
                    else:
                        in_data.append(d)
                data.append(in_data)
        else:
            in_data = []
            for idx, d in enumerate(i):
                if idx == 2:
                    in_data.append(locale.currency(int(d), grouping=True))
                else:
                    in_data.append(d)
            
            data.append(in_data)

    return data

def searchPinjamanPajak(key):
    data = []
    cur = db.cursor()
    cur.execute("SELECT pinjaman_pajak.*, karyawan.nama FROM pinjaman_pajak JOIN karyawan on karyawan.nik = pinjaman_pajak.id_karyawan where karyawan.nama LIKE '%"+str(key)+"%'")
    res = cur.fetchall()
    for d in res:
        dt = list(d)
        dt[2] = locale.currency(int(d[2]), grouping=True)
        data.append(dt)
    return data

def getDataPinjamanPajakById(id):
    cur = db.cursor()
    cur.execute("SELECT pinjaman_pajak.*, karyawan.nama FROM pinjaman_pajak JOIN karyawan ON karyawan.nik = pinjaman_pajak.id_karyawan where kode_potongan_lain = '"+id+"' limit 1")
    res = cur.fetchone()
    data = list(res)
    data.append(str(data[4])+'-'+str(data[6]))
    return data

def getPajak(id):
    cur = db.cursor()
    cur.execute("SELECT pinjaman_pajak.jumlah FROM pinjaman_pajak WHERE id_karyawan = '"+id+"' AND jenis_pot = 'pjk' limit 1")
    res = cur.fetchone()
    if res:
        return res
    else:
        return [0]
    
def getPinjaman(id, now):
    cur = db.cursor()
    cur.execute("SELECT pinjaman_pajak.jumlah, pinjaman_pajak.berlaku FROM pinjaman_pajak WHERE id_karyawan = '"+id+"' AND jenis_pot = 'pnj' limit 1")
    res = cur.fetchone()
    if res:
        tanggal = datetime.strptime(res[1], "%Y-%m-%d")
        if tanggal >= now:
            return res
        else:        
            return [0]
    else:
        return [0]
    
def getDataKomplain():
    cur = db.cursor()
    cur.execute("SELECT komplain.*, karyawan.nama FROM komplain JOIN karyawan ON komplain.id_karyawan = karyawan.nik")
    res = cur.fetchall()
    return res

def getDataKomplainById(id):
    cur = db.cursor()
    cur.execute("SELECT komplain.*, karyawan.nama FROM komplain JOIN karyawan ON komplain.id_karyawan = karyawan.nik WHERE kode_komplain = '"+str(id)+"'")
    res = cur.fetchone()
    return res

def getDataKomplainByName(id, now):
    data = 0
    cur = db.cursor()
    cur.execute("SELECT * FROM komplain where id_karyawan = '"+str(id)+"'")
    res = cur.fetchall()
    for i in res:
        if now <= datetime.strptime(i[6],"%Y-%m-%d"):
            if i[1] == 'kr':
                data = -int(i[2])
            else:
                data = int(i[2])
    return data

def searchKomplain(key):
    cur = db.cursor()
    cur.execute("SELECT komplain.*, karyawan.nama FROM komplain JOIN karyawan ON komplain.id_karyawan = karyawan.nik WHERE karyawan.nama LIKE '%"+str(key)+"%'")
    res = cur.fetchall()
    return res

def getDatakomplainDocument(data):
    tanggal_data = []
    datares = []
    start_period = datetime.strptime(data['mulai'], "%Y-%m-%d")
    end_period = datetime.strptime(data['akhir'], "%Y-%m-%d")

    delta = end_period - start_period
    for d in range(delta.days +1):
        tanggal_data.append(datetime.strftime(start_period + timedelta(days = d), "%Y-%m-%d"))        

    cur = db.cursor()
    if 'semuaData' in data and data['semuaData'] == "on":
        cur.execute('SELECT komplain.*, karyawan.nama FROM komplain JOIN karyawan on komplain.id_karyawan = karyawan.nik')    
    elif 'no_karyawan' in data and data['no_karyawan'] != "":
        cur.execute("SELECT komplain.*, karyawan.nama FROM komplain JOIN karyawan on komplain.id_karyawan = karyawan.nik WHERE komplain.id_karyawan ='"+data['no_karyawan'].split('-')[0]+"'")
    res = cur.fetchall()
    for r in res:
        if r[6] in tanggal_data:
            lst = list(r)
            if r[1] == 'tb':
                lst[1] = 'Penambahan Gaji'
            if r[1] == 'kr':
                lst[1] = 'Pengurangan Gaji'
            datares.append(lst)
    return datares

def getDataPinjamanPajakDocument(data):
    
    tanggal_data = []
    datares = []
    start_period = datetime.strptime(data['mulai'], "%Y-%m-%d")
    end_period = datetime.strptime(data['akhir'], "%Y-%m-%d")

    delta = end_period - start_period
    for d in range(delta.days +1):
        tanggal_data.append(datetime.strftime(start_period + timedelta(days = d), "%Y-%m-%d"))        

    cur = db.cursor()
    if 'semuaData' in data and data['semuaData'] == "on":
        cur.execute('SELECT pinjaman_pajak.*, karyawan.nama FROM pinjaman_pajak JOIN karyawan on pinjaman_pajak.id_karyawan = karyawan.nik')    
    elif 'no_karyawan' in data and data['no_karyawan'] != "":
        cur.execute("SELECT pinjaman_pajak.*, karyawan.nama FROM pinjaman_pajak JOIN karyawan on pinjaman_pajak.id_karyawan = karyawan.nik WHERE pinjaman_pajak.id_karyawan ='"+data['no_karyawan'].split('-')[0]+"'")
    res = cur.fetchall()
    for r in res:
        lst = list(r)
        if r[3] in tanggal_data:
            if r[1] == 'pnj':
                lst[1] = 'Pinjaman'
            if r[1] == 'kr':
                lst[1] = 'Pajak'
        if r[3] == '':
            lst[3] = '-'
        
        datares.append(lst)
    return datares

def getDataInsentifDocument(data):
    tanggal_data = getDateRange(data['mulai'], data['akhir'])
    datares = []
    cur = db.cursor()
    if 'semuaData' in data and data['semuaData'] == "on":
        cur.execute('SELECT insentif.*, karyawan.nama FROM insentif JOIN karyawan on insentif.id_karyawan = karyawan.nik')    
    elif 'no_karyawan' in data and data['no_karyawan'] != "":
        cur.execute("SELECT insentif.*, karyawan.nama FROM insentif JOIN karyawan on insentif.id_karyawan = karyawan.nik WHERE insentif.id_karyawan ='"+data['no_karyawan'].split('-')[0]+"'")
    res = cur.fetchall()
    for r in res:
        lst = list(r)
        if lst[1] in tanggal_data:
            ttl_insenif = locale.currency(int(lst[3]) * int(lst[4]), grouping=True)
            if 'Rp' in ttl_insenif:
                ttl_insenif = ttl_insenif.replace('Rp', 'Rp ')
            lst.append(ttl_insenif)
            if lst[4] != '':
                cr = locale.currency(int(lst[4]), grouping=True)
                if 'Rp' in cr:
                    cr = cr.replace('Rp', 'Rp ')
                lst[4] = cr
            datares.append(lst)
    return datares

def getDataLemburDocument(data):
    tanggal_data = getDateRange(data['mulai'], data['akhir'])
    datares = []

    cur = db.cursor()
    if 'semuaData' in data and data['semuaData'] == "on":
        cur.execute('SELECT lembur.*, karyawan.nama FROM lembur JOIN karyawan on lembur.id_karyawan = karyawan.nik')    
    elif 'no_karyawan' in data and data['no_karyawan'] != "":
        cur.execute("SELECT lembur.*, karyawan.nama FROM lembur JOIN karyawan on lembur.id_karyawan = karyawan.nik WHERE lembur.id_karyawan ='"+data['no_karyawan'].split('-')[0]+"'")
    res = cur.fetchall()
    for r in res:
        lst = list(r)
        if lst[1] in tanggal_data:        
            datares.append(lst)
    return datares

def getDataIzinJamDocument(data):
    tanggal_data = getDateRange(data['mulai'], data['akhir'])
    datares = []

    cur = db.cursor()
    if 'semuaData' in data and data['semuaData'] == "on":
        cur.execute('SELECT izin_jam.*, karyawan.nama FROM izin_jam JOIN karyawan on izin_jam.id_karyawan = karyawan.nik')    
    elif 'no_karyawan' in data and data['no_karyawan'] != "":
        cur.execute("SELECT izin_jam.*, karyawan.nama FROM izin_jam JOIN karyawan on izin_jam.id_karyawan = karyawan.nik WHERE izin_jam.id_karyawan ='"+data['no_karyawan'].split('-')[0]+"'")
    res = cur.fetchall()
    for r in res:
        lst = list(r)
        if lst[1] in tanggal_data: 
            if lst[4] == "T":
                lst[4] = "Terlambat"
            elif lst[4] == "PA":
                lst[4] = "Pulang Awal"
            elif lst[4] == "MP":
                lst[4] = "Meninggalkan Pekerjaan"
            datares.append(lst)
    return datares

def getDataIzinDocument(data):
    tanggal_data = getDateRange(data['mulai'], data['akhir'])
    datares = []

    cur = db.cursor()
    if 'semuaData' in data and data['semuaData'] == "on":
        cur.execute('SELECT izin.*, karyawan.nama FROM izin JOIN karyawan on izin.id_karyawan = karyawan.nik')    
    elif 'no_karyawan' in data and data['no_karyawan'] != "":
        cur.execute("SELECT izin.*, karyawan.nama FROM izin JOIN karyawan on izin.id_karyawan = karyawan.nik WHERE izin.id_karyawan ='"+data['no_karyawan'].split('-')[0]+"'")
    res = cur.fetchall()
    for r in res:
        if r[1] in tanggal_data:
            lst = list(r)
            if lst[2] == "C":
                lst[2] = "Cuti"
            if lst[2] == "I":
                lst[2] = "Izin"
            if lst[2] == "IK":
                lst[2] = "Izin Khusus"
            if lst[2] == "S":
                lst[2] = "Sakit"
            datares.append(lst)

    return datares

def getDataAbsenDocument(data):
    tanggal_data = getDateRange(data['mulai'], data['akhir'])
    if 'semuaData' in data and data['semuaData'] == "on":
        dataAbsen = getDataAbsenTable(tanggal_data)
    elif 'no_karyawan' in data and data['no_karyawan'] != "":
        dataAbsen = searchDataAbsenTable(data['no_karyawan'].split('-')[1] , tanggal_data)

    header = ['No', 'Nama', 'Kode Karyawan'] + tanggal_data
    dataAbsen.insert(0,header)
    return dataAbsen

def getDataGajiDocument(data): 
    tanggal = getDateRange(data['mulai'], data['akhir'])
    totalhariLibur = hitungHariLibur(tanggal)
    if 'semuaData' in data and data['semuaData'] == "on":
        data_karyawan = getDataKaryawan()
        for d in data_karyawan:
            totalhariKerja = hitungHariKerja(d[1])
            totalhariizin = hitungHariTidakKerja(d[1], "I")
            totalharicuti = hitungHariTidakKerja(d[1], "C")
            totalharisakit = hitungHariTidakKerja(d[1], "S")
            totalhariizinkhusus = hitungHariTidakKerja(d[1], "IK")
            totalharialpha = len(tanggal) - totalhariKerja - totalhariizin - totalharicuti - totalharisakit - totalhariizinkhusus - totalhariLibur
            
            dataGajiKaryawan = getGajiKaryawan(d[1])
            gaji_pokok = dataGajiKaryawan[0] if dataGajiKaryawan[0] != None else 0
            tunjangan_jabatan = dataGajiKaryawan[1] if dataGajiKaryawan[1] != None else 0
            tunjangan_keahlian = dataGajiKaryawan[2] if dataGajiKaryawan[2] != None else 0
            tunjangan_lain = dataGajiKaryawan[3] if dataGajiKaryawan[3] != None else 0
            upah_total = gaji_pokok+tunjangan_jabatan+tunjangan_keahlian+tunjangan_lain

            lembur = getJamLembur(d[1])
            insentif = getTotalnsentif(d[1])
            
            gajiKotor= upah_total+lembur+insentif
            print(gajiKotor)
    return totalhariLibur

def getDateRange(mulai, akhir):
    tanggal_data = []
    start_period = datetime.strptime(mulai, "%Y-%m-%d")
    end_period = datetime.strptime(akhir, "%Y-%m-%d")

    delta = end_period - start_period
    for d in range(delta.days +1):
        tanggal_data.append(datetime.strftime(start_period + timedelta(days = d), "%Y-%m-%d"))        
    return tanggal_data

def getNamaDokumen(nama, data):
    namaFile = str(nama)
    tanggal_mulai = datetime.strftime(datetime.strptime(data['mulai'], '%Y-%m-%d'), '%d %b %Y')
    tanggal_akhir = datetime.strftime(datetime.strptime(data['akhir'], '%Y-%m-%d'), '%d %b %Y')
    namaFile+=' '
    namaFile+=tanggal_mulai
    namaFile+= ' - '
    namaFile+=tanggal_akhir
    namaFile+=" | "
    if 'semuaData' in data and data['semuaData'] == "on":
        namaFile+="Semua Data"
    elif 'no_karyawan' in data and data['no_karyawan'] != "":
        namaFile+=data['no_karyawan'].split('-')[1]
    
    namaFile+=".xlsx"

    return namaFile