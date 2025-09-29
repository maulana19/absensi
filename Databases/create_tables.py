from connect import db


cursor = db.cursor()

# sql to create tables

KaryawanTable = "CREATE TABLE karyawan (id INT AUTO_INCREMENT PRIMARY KEY, nik VARCHAR(50), nama VARCHAR(255), jam_kerja_normal VARCHAR(1))"
absenTable = "CREATE TABLE absensi (id INT AUTO_INCREMENT PRIMARY KEY, tanggal VARCHAR(100), jam_masuk VARCHAR(30), jam_keluar VARCHAR(30), id_karyawan INT, FOREIGN KEY (id_karyawan) REFERENCES karyawan(id))"
liburTable = "CREATE TABLE libur (id INT AUTO_INCREMENT PRIMARY KEY, tanggal VARCHAR(25), keterangan TEXT, kode_libur VARCHAR(255))"
izinTable = "CREATE TABLE izin (id INT AUTO_INCREMENT PRIMARY KEY, tanggal VARCHAR(25), status VARCHAR(20), keterangan TEXT, id_karyawan VARCHAR(255), kode_izin VARCHAR(255))"


def create_table(table):
    cursor.execute(table)
# create_table(KaryawanTable)
# create_table(absenTable)

print("Table Karyawan Telah dibuat !")