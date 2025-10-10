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

def insertDataKaryawan(file):
    karyawanTerdaftar = []
    data = pd.read_csv(file,delimiter=';', usecols=[1,2]).values.tolist()
    cur = db.cursor()
    cur.execute("SELECT karyawan.nama From karyawan")
    res = cur.fetchall()
    
    for r in res:
        if r:
            karyawanTerdaftar.append(r[0])
    for d in data:
        if d[1] not in karyawanTerdaftar:
            karyawanTerdaftar.append(d[1])
            cur.execute('INSERT INTO karyawan(nik,nama) VALUES ("'+str(d[0])+'","'+str(d[1])+'")')
            db.commit()


def insertDataAbsen(file):
    data = pd.read_csv(file,delimiter=';', usecols=[0,1,3,4,6])
    data_karyawan = data.values.tolist()
    insertDataKaryawan(file)
    
    for data in data_karyawan:
        if data[0] not in [57,17,24,29,87,192]:
            tanggal = data[2].split("/")
            tanggal_fix = tanggal[2]+'-'+tanggal[1]+'-'+tanggal[0]

            cursor = db.cursor()
            cursor.execute('SELECT * FROM absensi WHERE id_karyawan = "'+str(data[1])+'" AND tanggal = "' + tanggal_fix +'"')

            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO absensi VALUES ("","'+tanggal_fix+'", "","", "'+str(data[1])+'")')
                db.commit()

            if data[4] == "Scan Masuk":
                cursor.execute('UPDATE absensi SET jam_masuk = "'+str(data[3])+'" WHERE id_karyawan = "'+str(data[1])+'" AND tanggal = "'+tanggal_fix+'"')
                db.commit()
            if data[4] == "Scan Keluar":
                cursor.execute('UPDATE absensi SET jam_keluar = "'+str(data[3])+'" WHERE id_karyawan = "'+str(data[1])+'" AND tanggal = "'+tanggal_fix+'"')
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

    merge_tanggal = ''
    for t in data['tanggal'].split('-'):
        merge_tanggal += t
    merge_tanggal += str(random.randrange(1,100))
    str_tanggal = list(merge_tanggal)
    random.shuffle(str_tanggal)
    fixed_random_code = ''.join(str_tanggal)
    kode_lembur = 'lm_'+str(fixed_random_code)

    cur = db.cursor()
    cur.execute("INSERT INTO lembur(tanggal, total_jam, id_karyawan, kode_lembur) VALUES ('"+str(data["tanggal"])+"','"+str(data["total_jam"])+"','"+str(id_karyawan)+"', '"+kode_lembur+"')")
    db.commit()

    
def insertInsentif(data):
    split_karyawan = data['no_karyawan'].split('-')
    id_karyawan = split_karyawan[0]

    
    merge_tanggal = ''
    for t in data['tanggal'].split('-'):
        merge_tanggal += t
    merge_tanggal += str(random.randrange(1,100))
    str_tanggal = list(merge_tanggal)
    random.shuffle(str_tanggal)
    fixed_random_code = ''.join(str_tanggal)
    kode_insentif = 'ins_'+str(fixed_random_code)

    cur = db.cursor()
    cur.execute("INSERT INTO insentif(tanggal, tujuan, jumlah_hari, insentif, id_karyawan,kode_insentif) VALUES ('"+str(data["tanggal"])+"','"+str(data["tujuan"])+"','"+str(data["jumlah_hari"])+"','"+str(data["insentif"])+"','"+str(id_karyawan)+"', '"+kode_insentif+"')")
    db.commit()


def insertPotonganLain(data):
    column = []
    value = []

    for i in data:
        column.append(i)
    for c in column:
        value.append("'"+data[c]+"'")


    value[0] = value[0].split('-')[0]+"'"
    merge_tanggal = ''
    for t in datetime.now().strftime("%Y-%m-%d").split('-'):
        merge_tanggal += t
    merge_tanggal += str(random.randrange(1,100))
    str_tanggal = list(merge_tanggal)
    random.shuffle(str_tanggal)
    fixed_random_code = ''.join(str_tanggal)
    id_karyawan = value[1].replace("'","")+'_'+str(fixed_random_code)
    
    column.append('kode_potongan_lain')
    value.append("'"+id_karyawan+"'")

    column[0] = 'id_karyawan'

    cur = db.cursor()
    cur.execute("INSERT INTO pinjaman_pajak("+', '.join(column)+") VALUES ("+', '.join(value)+")")
    db.commit()

def insertDataKomplain(data):
    id_karyawan = data['no_karyawan'].split('-')[0]
    merge_tanggal = ''
    keterangan = '-'

    for t in data['berlaku'].split('-'):
        merge_tanggal += t
    merge_tanggal += str(random.randrange(1,100))
    str_tanggal = list(merge_tanggal)
    random.shuffle(str_tanggal)
    fixed_random_code = ''.join(str_tanggal)
    kode_komplain = data['jenis']+'_'+str(fixed_random_code)

    if data['keterangan'] != "":
        keterangan = data['keterangan']

    cur = db.cursor()
    cur.execute("INSERT INTO komplain (jenis, jumlah, keterangan, kode_komplain, id_karyawan, berlaku) VALUE ('"+str(data['jenis'])+"','"+str(data['jumlah'])+"','"+str(keterangan)+"','"+str(kode_komplain)+"','"+str(id_karyawan)+"','"+str(data['berlaku'])+"')")
    db.commit()

def insertGajiKaryawan(data):
    d_excel = pd.read_excel(data['file-karyawan'], dtype="str_").fillna('0')
    lst = d_excel.values.tolist()
    cur = db.cursor()
    for g in lst:
        cur.execute("UPDATE karyawan SET u_pokok = "+g[4]+", t_jabatan = "+g[5]+", t_keahlian = "+g[6]+", t_lain = "+g[7]+" WHERE nik = '"+str(g[1])+"'")
    db.commit()