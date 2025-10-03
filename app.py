from flask import Flask, jsonify, request, render_template,redirect
import pandas as pd
import os

from Databases.connect import db
from Function.loadData import *
from Function.DataKaryawan import getNamaKaryawan, insertJadwal, updateKaryawan
import locale
from Function.tambahData import insertLibur, insertIzinJam, insertDataAbsen, insertIzinKaryawan, insertLembur
from Function.hapusData import deleteLibur,deleteIzin, deleteIzinJam, deleteLembur
from Function.convertData import changeFormatDate
from Function.updateData import updateIzin, updateLibur, updateIzinJam

# from Function.tambahAbsensiKaryawanShift import insertDataKaryawanShift

app = Flask(__name__)
locale.setlocale(locale.LC_TIME, "id_ID.utf8")

@app.route('/')
def home():
    data = getDataAbsen()
    return render_template("Pages/index.html", data=data)

@app.route('/tambah-absen', methods=["GET", "POST"])
def tambah_absen():
    if request.method == 'GET':
        return render_template("Pages/absen/add.html")
    if request.method == 'POST':
        file =  request.files['file-absen']
        if file.filename == "":
            return 'Tidak Ada File yang Terpilih', 400
        
        file_xls = pd.read_excel(file)
        file_path = os.path.join('data',file.filename)
        file_xls.to_csv(file_path,sep=";", index= None, header= True)
        
        # getNamaKaryawan(file_path)
        insertDataAbsen(file_path)
        return redirect('/')

@app.route('/cari-jam_absen', methods = ["GET"])
def cari_jam_absen():
    if request.method == "GET":
        search_key = request.args.get('key')
        if search_key == "":
            return redirect('/')
        data_search = searchDataAbsen(search_key)
        return render_template("Pages/absen/search.html",data = data_search)

@app.route('/daftar-karyawan')
def karyawan():
    data = getDataKaryawan()
    return render_template("Pages/karyawan/list.html", data = data)

@app.route('/cari-karyawan')
def cari_karyawan():
    search_key = request.args.get('key')
    if search_key == "":
        return redirect('/daftar-karyawan')
    data_search = searchDataKaryawan(search_key)
    return render_template("Pages/karyawan/list.html", data = data_search)

@app.route('/absensi')
def daftar_absensi():
    headerTable = getHeaderAbsen()
    absen = getDataAbsenTable(headerTable)
    return render_template("Pages/absen/list.html", header = headerTable, data = absen)

@app.route('/libur')
def daftar_libur():
    dt_libur = getDataLibur()
    return render_template('Pages/absen/libur/list.html', data= dt_libur)

@app.route('/tambah-libur', methods=['GET', 'POST'])
def tambah_libur():
    if request.method == 'GET':
        return render_template('Pages/absen/libur/tambah.html')
    elif request.method == 'POST':
        insertLibur(request.form)
        return redirect('/libur')

@app.route('/hapus-libur/<kode_id>', methods=['GET'])
def hapus_libur(kode_id):
    deleteLibur(kode_id)
    return redirect('/libur')

@app.route('/update-libur/<kode_id>', methods=['GET', 'POST'])
def update_libur(kode_id):
    if request.method == 'GET':
        data_libur = list(getDataLiburById(kode_id))
        new_date = changeFormatDate(data_libur[1])
        data_libur[1] = new_date
        return render_template('Pages/absen/libur/edit.html', data = data_libur)
    if request.method == 'POST':
        data = {
            'tanggal' : '',
            'keterangan' : '',
        }
        if request.form['tanggal'] != '':
            data['tanggal'] = request.form['tanggal']
        if request.form['keterangan'] != '':
            data['keterangan'] = request.form['keterangan']

        if data['tanggal'] != '':
            updateLibur(data['tanggal'], 'tanggal', kode_id)

        if data['keterangan'] != '':
            updateLibur(data['keterangan'], 'keterangan', kode_id)
        return redirect('/libur')

@app.route('/cari-libur')
def cari_libur():
    search_key = request.args.get('key')
    if search_key == "":
        return redirect('/libur')
    
    data_search = searchDataLibur(search_key)
    return render_template("Pages/absen/libur/list.html", data = data_search)

# @app.route('/ubah-shift/<key>')
# def ubah_shift(key):
#     if key == "":
#         return redirect('/daftar-karyawan')
#     updateKaryawan(key)
#     return redirect("/daftar-karyawan")

# @app.route('/jadwal-shift/<key>', methods=["GET", "POST"])
# def jadwal_shift(key):
#     if key == "":
#         return redirect('/daftar-karyawan')

#     data_karyawan = searchDataKaryawanID(key)
#     if request.method == "GET":
#         data_jadwal = getDataJadwal(data_karyawan[0])
#         data = []
#         for item in data_jadwal:
#             lsdata = list(item)
#             lsdata.append(item[2].strftime("%A"))
#             data.append(lsdata)
            
#         return render_template('Pages/karyawan/shift.html', data = data_karyawan, jadwal = data)
#     if request.method == "POST":
#         data = [
#             data_karyawan[0],
#             request.form.get('tanggal'),
#             request.form.get('jadwal'),
#         ]
#         insertJadwal(data)
#         return redirect('/jadwal-shift/'+key)




@app.route('/izin', methods=['GET'])
def daftar_izin():
    data_izin = getDataIzin()
    return render_template('Pages/absen/izin/list.html', data = data_izin)

@app.route('/tambah-izin', methods=['GET', 'POST'])
def tambah_izin():
    if request.method == 'GET':
        data_karyawan = getDataKaryawan()
        return render_template('Pages/absen/izin/add.html', data = data_karyawan)
    elif request.method == 'POST':
        insertIzinKaryawan(request.form)
        return redirect('/izin')

@app.route('/hapus-izin/<id>', methods=['GET','post'])
def hapusIzin(id):
    if request.method == 'GET':
        deleteIzin(id)
        return redirect('/izin')

@app.route('/update-izin/<id>', methods=['GET','POST'])
def ubahIzin(id):
    if request.method == 'GET':
        data_izin = getDataIzinByIDAndTanggal(id)
        data_karyawan = getDataKaryawan()
        return render_template('Pages/absen/izin/edit.html', data = data_izin,data_karyawan = data_karyawan, url_params = [id])
    
    if request.method == 'POST':
        if request.form['keterangan'] != '':
            updateIzin(request.form['keterangan'], 'keterangan', id)

        if request.form['izin'] != '':
            izin = id.split('_')
            kode_izin = request.form['izin']+"_"+izin[1]
            updateIzin(request.form['izin'], 'status', id)
            updateIzin(kode_izin, 'kode_izin', id)

        if request.form['no_karyawan'] != '':
            split_karyawan = request.form['no_karyawan'].split('-')
            id_karyawan = split_karyawan[0]
            updateIzin(id_karyawan, 'id_karyawan', id)

        if request.form['tanggal'] != '':
            updateIzin(request.form['tanggal'], 'tanggal', id)

        return redirect('/izin')

@app.route('/cari-izin')
def cari_izin():
    search_key = request.args.get('key')
    if search_key == "":
        return redirect('/izin')
    data_search = searchDataIzin(search_key)
    return render_template("Pages/absen/izin/list.html", data = data_search)


@app.route('/cari-absen')
def cari_absen():
    if(request.args.get('key') != ""):
        headerTable = getHeaderAbsen()
        absen = searchDataAbsenTable(request.args.get('key'),headerTable)
        return render_template("Pages/absen/list.html", header = headerTable, data = absen)
    else:
        return redirect('/absensi')


@app.route('/izin-jam')
def daftar_izin_jam():
    data_izin = getDataIzinJam()
    return render_template('Pages/absen/izin-jam/list.html', data= data_izin)

@app.route('/tambah-izin-jam', methods=['GET', 'POST'])
def tambah_izin_jam():
    if request.method == 'GET':
        data_karyawan = getDataKaryawan()
        return render_template('Pages/absen/izin-jam/add.html',data = data_karyawan)
    elif request.method == 'POST':
        insertIzinJam(request.form)
        return redirect('/izin-jam')

@app.route('/hapus-izin-jam/<id>', methods=['GET'])
def hapusIzinJam(id):
    if request.method == 'GET':
        deleteIzinJam(id)
        return redirect('/izin-jam')
    
@app.route('/update-izin-jam/<id>', methods=['GET', 'POST'])
def ubahJamIzin(id):
    if request.method == 'GET':
        data_izin = getDataIziJamById(id)
        data_karyawan = getDataKaryawan()
        return render_template('Pages/absen/izin-jam/edit.html', data = data_izin, data_karyawan = data_karyawan, url_params =[id])
    elif request.method == 'POST':
        if request.form['no_karyawan'] != '':
            split_karyawan = request.form['no_karyawan'].split('-')
            id_karyawan = split_karyawan[0]

            updateIzinJam(id_karyawan,'id_karyawan',id)
        if request.form['tanggal'] != '':
            updateIzinJam(request.form['tanggal'],'tanggal',id)
        if request.form['izin'] != '':
            izin = id.split('_')
            kode_izin_jam = request.form['izin']+"_"+izin[1]
            
            updateIzinJam(request.form['izin'], 'status', id)
            updateIzinJam(kode_izin_jam, 'kode_izin_jam', id)
        if request.form['jam_mulai'] != '':
            updateIzinJam(request.form['jam_mulai'],'jam_mulai',id)
        if request.form['jam_akhir'] != '':
            updateIzinJam(request.form['jam_akhir'],'jam_akhir',id)
        if request.form['total_jam'] != '':
            updateIzinJam(request.form['total_jam'],'total_izin',id)
        if request.form['keterangan'] != '':
            updateIzinJam(request.form['keterangan'],'keterangan',id)
    return redirect('/izin-jam')

@app.route('/cari-izin-jam')
def cariIzinJam():
    search_key = request.args.get('key')
    if search_key == "":
        return redirect('/izin-jam')
    data_search = searchDataIzinJam(search_key)
    return render_template("Pages/absen/izin-jam/list.html", data = data_search)

@app.route('/lembur')
def daftarLembur():
    data_lembur = getDataLembur()
    data_karyawan = getDataKaryawan()
    print(data_lembur)
    return render_template("Pages/absen/lembur/list.html", data = data_lembur, karyawan = data_karyawan)

@app.route('/tambah-lembur', methods =['GET', 'POST'])
def tambahLembur():
    if request.method == 'GET':
        split_karyawan = request.args.get('no_karyawan').split('-')
        id_karyawan = split_karyawan[0]
        data = searchDataAbsenByDateAndNIK(id_karyawan, request.args.get('tanggal'))
        return render_template('Pages/absen/lembur/add.html', data_absen = data, data_karyawan =[request.args.get('no_karyawan'), request.args.get('tanggal')])
    if request.method == 'POST':
        insertLembur(request.form)
        return redirect('/lembur')

@app.route('/hapus-lembur/<id>', methods=["GET"])
def hapusLembur(id):
    deleteLembur(id)
    return redirect('/lembur')


@app.route('/gaji-karyawan', methods=['GET'])
def gajikaryawan():
    data = []
    data_karyawan = getDataKaryawan()
    
    tanggal = getHeaderAbsen()
    if data_karyawan:
        for d in data_karyawan:
            totalharikerja = hitungHariKerja(d[0])
            totalhariizin = hitungHariTidakKerja(d[1], "I")
            totalharicuti = hitungHariTidakKerja(d[1], "C")
            totalharisakit = hitungHariTidakKerja(d[1], "S")
            totalhariizinkhusus = hitungHariTidakKerja(d[1], "IK")
            totalharialpha = len(tanggal) - totalharikerja - totalhariizin - totalharicuti - totalharisakit - totalhariizinkhusus


            totalizinperjam = hitungIzinJam(d[1])
            data.append([d[0],d[1], d[2], totalharikerja, totalizinperjam, totalhariizin, totalharicuti, totalharisakit, totalhariizinkhusus, totalharialpha])
    return render_template('Pages/karyawan/gaji/list.html', data = data)

@app.route('/ubah-gaji/<id>')
def ubahGaji(id):
    return render_template('Pages/karyawan/gaji/edit.html')


app.run(port=5000, debug=True)