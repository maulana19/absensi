from Databases.connect import db
import pandas as pd
from datetime import date, datetime 
from dateutil.relativedelta import relativedelta
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
    cursor.close()
    

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
    cur.close()
            


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
    cursor.close()
                

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
    cur.close()
    

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
    cur.close()
    


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
    cur.close()
    

    
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
    cur.close()
    


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
    cur.close()
    

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
    cur.close()
    

def insertGajiKaryawan(data):
    d_excel = pd.read_excel(data['file-karyawan'], dtype="str_").fillna('0')
    lst = d_excel.values.tolist()
    cur = db.cursor()
    for g in lst:
        cur.execute("UPDATE karyawan SET u_pokok = "+g[4]+", t_jabatan = "+g[5]+", t_keahlian = "+g[6]+", t_lain = "+g[7]+" WHERE nik = '"+str(g[1])+"'")
    db.commit()
    cur.close()
    
def insertDataBPJS(data):
    cur = db.cursor()
    cur.execute("SELECT * FROM bpjs WHERE id_karyawan = '"+data["no_karyawan"].split('-')[0]+"' and jenis = 'ks'")
    res_ks = cur.fetchone()
    if res_ks == None:
        cur.execute("INSERT INTO bpjs(jenis, nomor, jumlah, id_karyawan) VALUES ('ks', '"+data['nomor_bpjs_kes']+"', '"+data['pot_bpjs_kes']+"', '"+data["no_karyawan"].split('-')[0]+"')")
        db.commit()
    cur.execute("SELECT * FROM bpjs WHERE id_karyawan = '"+data["no_karyawan"].split('-')[0]+"' and jenis = 'kt'")
    res_kt = cur.fetchone()
    if res_kt == None:
        cur.execute("INSERT INTO bpjs(jenis, nomor, jumlah, id_karyawan) VALUES ('kt', '"+data['nomor_bpjs_ket']+"', '"+data['pot_bpjs_ket']+"', '"+data["no_karyawan"].split('-')[0]+"')")
        db.commit()
    cur.close()

def insertIzinBatch(data):
    d_excel = pd.read_excel(data['file-izin'], dtype="str_")
    lst = d_excel.values.tolist()
    cur = db.cursor()
    for d in lst:
        cur.execute("SELECT nik,nama FROM karyawan WHERE nama LIKE '%"+d[0]+"%'")
        res = cur.fetchone()
        if res:
            tanggal = d[1].split(" ")[0]
            cur.execute("SELECT * FROM izin WHERE id_karyawan = '"+res[0]+"' and tanggal = '"+tanggal+"'")
            res2 = cur.fetchone()
            if d[2].lower() == "izin":
                status = 'I'
            elif d[2].lower() == "cuti":
                status = "C"
            elif d[2].lower() == "izin khusus":
                status = "IK"
            else:
                status = d[2]

            merge_tanggal = ''
            for t in tanggal.split('-'):
                merge_tanggal += t
            merge_tanggal += str(random.randrange(1,400))
            str_tanggal = list(merge_tanggal)
            random.shuffle(str_tanggal)
            fixed_random_code = ''.join(str_tanggal)
            kode_izin = status+'_'+str(fixed_random_code)
            if res2 == None:
                cur.execute("INSERT INTO izin(tanggal, status, keterangan, id_karyawan, kode_izin) VALUES ('"+d[1].split(" ")[0]+"', '"+status.capitalize()+"', '"+d[3]+"', '"+res[0]+"', '"+kode_izin+"')")
                db.commit()
    cur.close()
                

def insertLemburBatch(data):
    d_excel = pd.read_excel(data['file-lembur'], dtype="str_")
    lst = d_excel.values.tolist()
    cur = db.cursor()
    for d in lst:
        cur.execute("SELECT nik,nama FROM karyawan WHERE nama LIKE '%"+d[0]+"%'")
        userRes = cur.fetchone()
        if userRes: 
            tanggal = d[1].split(" ")[0]
            cur.execute("SELECT * FROM lembur WHERE id_karyawan = '"+userRes[0]+"' and tanggal = '"+tanggal+"'")
            res = cur.fetchone()
            if res == None: 
                merge_tanggal = ''
                for t in tanggal.split('-'):
                    merge_tanggal += t
                merge_tanggal += str(random.randrange(1,100))
                str_tanggal = list(merge_tanggal)
                random.shuffle(str_tanggal)
                fixed_random_code = ''.join(str_tanggal)
                kode_lembur = 'lm_'+str(fixed_random_code)
                cur.execute("INSERT INTO lembur(tanggal, total_jam, id_karyawan, kode_lembur) VALUES ('"+d[1].split(" ")[0]+"', '"+d[2]+"', '"+userRes[0]+"', '"+kode_lembur+"')")
                db.commit()
    cur.close()

def insertBpjsBatch(data):
    d_excel = pd.read_excel(data['file-bpjs'], dtype="str_")
    lst = d_excel.values.tolist()
    cur = db.cursor()
    for d in lst:
        cur.execute("SELECT nik, nama FROM karyawan WHERE nama LIKE '%"+d[0]+"%' LIMIT 1")
        resUser = cur.fetchone()
        if resUser:
            cur.execute("SELECT * FROM bpjs WHERE id_karyawan = '"+resUser[0]+"' and jenis = 'ks' LIMIT 1")
            resKs = cur.fetchone()
            if resKs == None:
                cur.execute("INSERT INTO bpjs(jenis, nomor, jumlah, id_karyawan) VALUES ('ks', '"+d[1]+"', '"+d[2]+"', '"+resUser[0]+"')")
            else:
                cur.execute('UPDATE bpjs SET nomor = "'+d[1]+'", jumlah = "'+d[2]+'" WHERE id_karyawan = "'+resUser[0]+'" AND jenis = "ks"')
            db.commit()

            cur.execute("SELECT * FROM bpjs WHERE id_karyawan = '"+resUser[0]+"' and jenis = 'kt' LIMIT 1")
            resKt = cur.fetchone()
            if resKt == None:
                cur.execute("INSERT INTO bpjs(jenis, nomor, jumlah, id_karyawan) VALUES ('kt', '"+d[3]+"', '"+d[4]+"', '"+resUser[0]+"')")
            else:
                cur.execute('UPDATE bpjs SET nomor = "'+d[3]+'", jumlah = "'+d[4]+'" WHERE id_karyawan = "'+resUser[0]+'" AND jenis = "kt"')
            db.commit()
    cur.close()


def insertKomplainBatch(data):
    d_excel = pd.read_excel(data['file-komplain'], dtype="str_")
    lst = d_excel.values.tolist()
    cur = db.cursor()

    # Parse into datetime object
    date_obj = date.today()

    # Move to next month and set day to 10
    if int(datetime.strftime(date_obj, "%d"))>=26:
        tanggal = datetime.strftime((date_obj + relativedelta(months=1)).replace(day=25), "%Y-%m-%d")
    else:
        tanggal = datetime.strftime(date_obj.replace(day=25), "%Y-%m-%d")
    for d in lst:
        cur.execute("SELECT nik,nama FROM karyawan WHERE nama LIKE '%"+d[0]+"%'")
        userRes = cur.fetchone()
        if userRes:
            cur.execute("SELECT * FROM komplain WHERE id_karyawan = '"+userRes[0]+"' and berlaku = '"+tanggal+"'")
            res = cur.fetchone()
            if res == None:

                if int(d[1])<0:
                    jenis = 'kr'
                else:
                    jenis = 'tb'
                merge_tanggal = ''
                for t in tanggal.split('-'):
                    merge_tanggal += t
                merge_tanggal += str(random.randrange(1,100))
                str_tanggal = list(merge_tanggal)
                random.shuffle(str_tanggal)
                fixed_random_code = ''.join(str_tanggal)
                kode_komplain = jenis+'_'+str(fixed_random_code)
                cur.execute("INSERT INTO komplain(jenis, jumlah, keterangan, kode_komplain, id_karyawan, berlaku) VALUES ('"+jenis+"', '"+d[1]+"', '"+d[2]+"', '"+kode_komplain+"','"+userRes[0]+"', '"+tanggal+"')")
                db.commit()
    cur.close()
    return 'ok'
                