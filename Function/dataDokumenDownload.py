
import numpy as np
import pandas as pd
from Function.loadData import getDataBPJSDocument, getDataAbsenDocument, getDataGajiDocument, getDataInsentifDocument, getDataIzinDocument, getDataIzinJamDocument, getDataKaryawan, getDataLemburByDate, getDataLemburDocument, getDataPinjamanPajakDocument, getDatakomplainDocument, getDateRange
from Databases.connect import db

def komplainDownloadData(dt):    
    data = getDatakomplainDocument(dt)
    if data == []:
        data_array = np.array([['-','-','-','-','-','-','-','-']], dtype="str_")
    else:
        data_array = np.array(data, dtype="str_")
    dataframe = pd.DataFrame(data_array, columns=["No", "Jenis Komplain", "Jumlah Komplain", "Keterangan", "Kode Komplain", "Kode Karyawan", "Tanggal", "Nama"])
    column_fixed = dataframe[["No", "Tanggal", "Kode Karyawan", "Nama", "Jenis Komplain", "Jumlah Komplain", "Keterangan"]]
    return column_fixed

def pinjamanPajakDownloadData(dt):
    data = getDataPinjamanPajakDocument(dt)
    
    if data == []:
        data_array = np.array([['-','-','-','-','-','-','-']], dtype="str_")
    else:
        data_array = np.array(data, dtype="str_")
    
    dataframe = pd.DataFrame(data_array, columns=["No", "Jenis Potongan", "Jumlah Potongan", "Masa Berlaku", "Kode Karyawan", "Kode Pinjaman", "Nama"])
    column_fixed = dataframe[["No", "Kode Karyawan", "Nama", "Jenis Potongan", "Jumlah Potongan", "Masa Berlaku"]]
    return column_fixed

def insentifDownloadData(dt):
    data = getDataInsentifDocument(dt) 
    if data == []:
        data_array = np.array([['-','-','-','-','-','-','-','-','-']], dtype="str_")
    else:
        data_array = np.array(data, dtype="str_")
    dataframe = pd.DataFrame(data_array, columns=["No", "Tanggal", "Tujuan", "Lama Tugas", "Insentif Perhari", "Kode Karyawan", "Kode Insentif", "Nama", "Total Didapat"])
    column_fixed = dataframe[["No", "Tanggal", "Nama", "Tujuan", "Lama Tugas", "Insentif Perhari", "Total Didapat"]]
    return column_fixed

def lemburDownloadData(dt):
    data = []
    tanggal = getDateRange(dt["mulai"], dt["akhir"])
    dt_karyawan = getDataKaryawan()
    idx = 1
    for dk in dt_karyawan:
        inner_dt = [idx,dk[1], dk[2]]
        idx+=1
        for t in tanggal:
            cur = db.cursor()
            cur.execute("SELECT * FROM lembur WHERE tanggal = '"+t+"' AND id_karyawan='"+dk[1]+"' LIMIT 1")
            res = cur.fetchone()
            if res:
                inner_dt.append(res[2])
            else:
                inner_dt.append("")
        data.append(inner_dt)
    if data == []:
        data_array = np.array([['-','-','-','-','-','-']], dtype="str_")
    else:
        data_array = np.array(data, dtype="str_")
    dataframe = pd.DataFrame(data_array, columns=["No", "NIK", "NAMA"]+tanggal)
    return dataframe

def izinJamDownloadData(dt):
    data = getDataIzinJamDocument(dt)
    if data == []:
        data_array = np.array([['-','-','-','-','-','-','-','-','-','-']], dtype="str_")
    else:
        data_array = np.array(data, dtype="str_")
    
    dataframe = pd.DataFrame(data_array, columns=["No", "Tanggal", "Jam Mulai Izin", "Jam Akhir Izin", "Status", "Keterangan Izin", "Kode Karyawan", "Kode Izin Jam", "Total Jam Izin", "Nama"])
    column_fixed = dataframe[["No", "Tanggal", "Nama", "Status", "Total Jam Izin", "Jam Mulai Izin", "Jam Akhir Izin", "Keterangan Izin"]]
    return column_fixed

def izinDownloadData(dt):
    data =  getDataIzinDocument(dt)    
    if data == []:
        data_array = np.array([['-','-','-','-','-','-','-']], dtype="str_")
    else:
        data_array = np.array(data, dtype="str_")
    
    dataframe = pd.DataFrame(data_array, columns=["No", "Tanggal", "Status", "Keterangan", "Kode Karyawan", "Kode Izin", "Nama"])
    column_fixed = dataframe[["No", "Tanggal", "Nama", "Status", "Keterangan"]]
    return column_fixed

def presensiDownloadData(dt):
    data = getDataAbsenDocument(dt)

    dt_length = len(data[0])
    empty_value = []
    i = 0
    while i < dt_length:
        empty_value.append('-')
        i+=1
    
    if data == []:
        data_array = np.array(empty_value, dtype="str_")
    else:
        data_array = np.array(data, dtype="str_")
    
    df = pd.DataFrame(data_array)
    df.columns = df.iloc[0].values
    df = df.drop(index=0, axis=0 )
    df = df.reset_index(drop=True)
    return df

def gajiDownloadData(dt):
    data = getDataGajiDocument(dt)
    if data == []:
        data_array = np.array([['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-']], dtype="str_")
    else:
        data_array = np.array(data, dtype="str_") 
    dataframe = pd.DataFrame(data_array, columns=["No", "NIK", "NAMA", "JML HARI KERJA", "IZIN", "CUTI", "SAKIT", "IZIN KHUSUS", "ALPHA", "IZIN BERJAM", "UPAH POKOK", "TUNJANGAN JABATAN", "TUNJANGAN KEAHLIAN", "TUNJANGAN LAIN", "UPAH TOTAL", "LEMBUR", "INSENTIF", "GAJI KOTOR", "POT. BPJS KESEHATAN", "POT. BPJS KETENAGAKERJAAN",  "POT. IZIN", "POT. IZIN PERJAM", "POT. PAJAK", "POT. PINJAMAN", "KOMPLAIN", "GAJI BERSIH"])
    print(dataframe)
    return dataframe

def bpjsDownloadData(dt): 
    data = getDataBPJSDocument(dt)
    if data == []:
        data_array = np.array([['-', '-', '-', '-', '-', '-']])
    else:
        data_array = np.array(data, dtype="str_")
    print(data_array)
    dataframe = pd.DataFrame(data_array, columns=["NIK", "Nama", "Nomor BPJS Kesehatan", "Potongan BPJS Kesehatan", "Nomor BPJS Ketenagakerjaan", "Potongan BPJS Ketenagakerjaan"])
    return dataframe

def slipDownloadData(dt):
    return 'ok'