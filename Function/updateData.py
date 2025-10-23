from Databases.connect import db
import pandas as pd

from Function.hapusData import deleteKaryawan
from Function.loadData import getDataKaryawan, getInsentifById

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

def updateGaji(value, column, id):
    cur = db.cursor()
    cur.execute("UPDATE karyawan SET "+column+" = '"+value+"' WHERE nik = '"+id+"'")
    db.commit()


def updateLembur(value, column, id):
    cur = db.cursor()
    cur.execute("UPDATE lembur SET "+column+" = '"+value+"' WHERE kode_lembur = '"+id+"'")
    db.commit()

def updateDataPinjamanPajak(value, column, id):
    cur = db.cursor()
    cur.execute("UPDATE pinjaman_pajak SET "+column+"= '"+value+"' WHERE kode_potongan_lain = '"+id+"'")
    db.commit()

def updateKomplain(value, column, id):
    cur = db.cursor()
    cur.execute("UPDATE komplain SET "+column+"= '"+value+"' WHERE kode_komplain = '"+id+"'")
    db.commit()

def updateDataKaryawanBatch(data):
    d_excel = pd.read_excel(data['file-karyawan'], dtype="str_", usecols="A:C")
    lst = d_excel.values.tolist()
    dataKaryawanBaru = []
    namakaryawanTerbaru = []
    karyawanTerhapus = []
    nikBaru = []

    data = getDataKaryawan()
    for dn in lst:
        namakaryawanTerbaru.append(dn[2])
        dataKaryawanBaru.append([dn[1], dn[2]])

    # Deleting data karyawan
    for k in data:
        if k[2] not in namakaryawanTerbaru:
            karyawanTerhapus.append(k[1])
    for kh in karyawanTerhapus:
        deleteKaryawan(kh)

    data = getDataKaryawan()
    # Updating NIK
    for k in data:
        for dk in dataKaryawanBaru:
            if dk[1] == k[2]:
                if k[1] != dk[0]:            
                    nikBaru.append([k[1], dk[0], k[2]])

    for nb in nikBaru:
        cur = db.cursor()
        
        cur.execute("UPDATE komplain SET id_karyawan = '"+str(nb[1])+"' WHERE id_karyawan = '"+str(nb[0])+"'")
        cur.execute("UPDATE pinjaman_pajak SET id_karyawan = '"+str(nb[1])+"' WHERE id_karyawan = '"+str(nb[0])+"'")
        cur.execute("UPDATE lembur SET id_karyawan = '"+str(nb[1])+"' WHERE id_karyawan = '"+str(nb[0])+"'")
        cur.execute("UPDATE izin SET id_karyawan = '"+str(nb[1])+"' WHERE id_karyawan = '"+str(nb[0])+"'")
        cur.execute("UPDATE izin_jam SET id_karyawan = '"+str(nb[1])+"' WHERE id_karyawan = '"+str(nb[0])+"'")
        cur.execute("UPDATE insentif SET id_karyawan = '"+str(nb[1])+"' WHERE id_karyawan = '"+str(nb[0])+"'")
        cur.execute("UPDATE absensi SET id_karyawan = '"+str(nb[1])+"' WHERE id_karyawan = '"+str(nb[0])+"'")
        cur.execute("UPDATE karyawan SET nik='"+str(nb[1])+"' WHERE nik = '"+str(nb[0])+"'")
        db.commit()    

def updateInsentif(data, id):
    dataInsentif = getInsentifById(id)
    cur = db.cursor()
    if data['no_karyawan'] != "":
        id_karyawan = data['no_karyawan'].split('-')
        if len(id_karyawan) > 1:
            if dataInsentif[1] != id_karyawan[0]:
                cur.execute("UPDATE insentif SET id_karyawan = '"+str(id_karyawan[0])+"' WHERE kode_insentif = '"+str(id)+"'")    
    if data['tanggal'] != "":
        if dataInsentif[3] != data['tanggal']:
            cur.execute("UPDATE insentif SET tanggal = '"+str(data['tanggal'])+"' WHERE kode_insentif = '"+str(id)+"'")
    if data['tujuan'] != "":
        if dataInsentif[4] != data['tujuan']:
            cur.execute("UPDATE insentif SET tujuan = '"+str(data['tujuan'])+"' WHERE kode_insentif = '"+str(id)+"'")
    if data['jumlah_hari'] != "":
        if dataInsentif[6] != data['jumlah_hari']:
            cur.execute("UPDATE insentif SET jumlah_hari = '"+str(data['jumlah_hari'])+"' WHERE kode_insentif = '"+str(id)+"'")
    if data['insentif'] != "":
        if dataInsentif[7] != data['insentif']:
            cur.execute("UPDATE insentif SET insentif = '"+str(data['insentif'])+"' WHERE kode_insentif = '"+str(id)+"'")
