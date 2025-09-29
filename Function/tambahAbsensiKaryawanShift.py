import pandas as pd
from Databases.connect import db

def insertDataKaryawanShift(file):
    data = pd.read_csv(file,delimiter=';', usecols=[0,1,3,4,6])
    nik_karyawan = []
    id_karyawan = []
    data_karyawan = []
    cursor = db.cursor()
    cursor.execute("SELECT id,nik from karyawan where jam_kerja_normal = 2 ")
    for item in cursor.fetchall():
        nik_karyawan.append(item[1])
        id_karyawan.append(item[0])
    
    for item in data.values.tolist():
        if item[1] in nik_karyawan:
            data_karyawan.append(item)
    datasorted = data_karyawan.sort()
    print(data_karyawan)
    return 'ok'