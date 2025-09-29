import pandas as pd
from Databases.connect import db
from datetime import datetime



def insertDataAbsen(file):
    data = pd.read_csv(file,delimiter=';', usecols=[0,3,4,6])
    data_karyawan = data.values.tolist()
    for data in data_karyawan:
        if data[0] not in [57,17,24,29,87,192,20]:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM absensi WHERE id_karyawan = '+str(data[0])+' AND tanggal = "' + str(datetime.strptime(data[1], '%d/%m/%Y')) +'"')

            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO absensi VALUES ("","'+str(datetime.strptime(data[1], '%d/%m/%Y'))+'", "","", '+str(data[0])+')')
                db.commit()

            if data[3] == "Scan Masuk":
                cursor.execute('UPDATE absensi SET jam_masuk = "'+str(data[2])+'" WHERE id_karyawan = '+str(data[0])+' AND tanggal = "'+str(datetime.strptime(data[1], '%d/%m/%Y'))+'"')
                db.commit()
            if data[3] == "Scan Keluar":
                cursor.execute('UPDATE absensi SET jam_keluar = "'+str(data[2])+'" WHERE id_karyawan = '+str(data[0])+' AND tanggal = "'+str(datetime.strptime(data[1], '%d/%m/%Y'))+'"')
                db.commit()

