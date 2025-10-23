import io
from flask import Flask, request, render_template,redirect, send_file
import numpy as np
import pandas as pd
import os
import waitress

from Databases.connect import db
from Function.dataDokumenDownload import gajiDownloadData, insentifDownloadData, izinDownloadData, izinJamDownloadData, komplainDownloadData, lemburDownloadData, pinjamanPajakDownloadData, presensiDownloadData
from Function.loadData import *
from Function.DataKaryawan import getNamaKaryawan, insertJadwal, updateKaryawan
import locale
from Function.tambahData import insertLibur, insertIzinJam, insertDataAbsen, insertInsentif, insertIzinKaryawan, insertLembur, insertPotonganLain, insertDataKomplain, insertGajiKaryawan
from Function.hapusData import deleteInsentif, deleteLibur,deleteIzin, deleteIzinJam, deleteLembur, deletePinjamanPajak, deleteKomplain
from Function.convertData import changeFormatDate
from Function.updateData import updateIzin, updateLibur, updateIzinJam, updateDataPinjamanPajak, updateGaji, updateLembur, updateKomplain, updateDataKaryawanBatch,updateInsentif

# from Function.tambahAbsensiKaryawanShift import insertDataKaryawanShift

app = Flask(__name__)
locale.setlocale(locale.LC_ALL, "id_ID.UTF-8")

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

@app.route('/ubah-lembur/<id>', methods = ["GET", "POST"])
def ubahLembur(id):
    if request.method == "GET":
        data = searchDataLemburById(id)
        return render_template('Pages/absen/lembur/edit.html', data_karyawan = data)
    elif request.method == "POST":
        if request.form['total_jam'] != "":
            updateLembur(request.form['total_jam'],'total_jam', id)
        return redirect('/lembur')

@app.route('/cari-lembur')
def cari_lembur():
    search_key = request.args.get('key')
    if search_key == "":
        return redirect('/lembur')
    
    data_search = searchDataLembur(search_key)
    return render_template("Pages/absen/lembur/list.html", data = data_search)
@app.route('/gaji-karyawan', methods=['GET'])
def gajikaryawan():
    data = []
    data_karyawan = getDataKaryawan()
    tanggal_header = getHeaderAbsen()
    tanggal = []
    for t in tanggal_header:
        tanggal.append(datetime.strftime(t, "%Y-%m-%d"))
    totalharilibur = hitungHariLibur(tanggal)
    if data_karyawan:
        for d in data_karyawan:
            totalharikerja = hitungHariKerja(d[1])
            totalhariizin = hitungHariTidakKerja(d[1], "I")
            totalharicuti = hitungHariTidakKerja(d[1], "C")
            totalharisakit = hitungHariTidakKerja(d[1], "S")
            totalhariizinkhusus = hitungHariTidakKerja(d[1], "IK")
            totalharialpha = len(tanggal) - totalharikerja - totalhariizin - totalharicuti - totalharisakit - totalhariizinkhusus - totalharilibur
            dataGajiKaryawan = getGajiKaryawan(d[1])

            gaji_pokok = dataGajiKaryawan[0] if dataGajiKaryawan[0] != None else 0
            tunjangan_jabatan = dataGajiKaryawan[1] if dataGajiKaryawan[1] != None else 0
            tunjangan_keahlian = dataGajiKaryawan[2] if dataGajiKaryawan[2] != None else 0
            tunjangan_lain = dataGajiKaryawan[3] if dataGajiKaryawan[3] != None else 0
            upah_total = gaji_pokok+tunjangan_jabatan+tunjangan_keahlian+tunjangan_lain

            lembur = getJamLembur(d[1])*15897
            insentif = getTotalnsentif(d[1])

            gajiKotor= upah_total+lembur+insentif

            totalizinperjam = hitungIzinJam(d[1])
            potonganIzin = (int(upah_total)/25) * (int(totalhariizin) + int(totalharialpha))
            potonganIzinJam = (int(upah_total)/25)/7 * (int(totalizinperjam))
            potonganPajak = int(getPajak(d[1])[0])
            potonganPinjaman = int(getPinjaman(d[1], tanggal)[0])

            komplain = getDataKomplainByName(d[1], tanggal)
            
            gaji_bersih = int(gajiKotor) - int(potonganIzin) - int(potonganIzinJam) - int(potonganPajak) - int(potonganPinjaman) + komplain
            data.append(
                [
                    d[0],d[1], d[2], 
                    totalharikerja, totalizinperjam, totalhariizin, totalharicuti, 
                    totalharisakit, totalhariizinkhusus, totalharialpha,
                    locale.currency(gaji_pokok, grouping=True), 
                    locale.currency(tunjangan_jabatan, grouping=True),
                    locale.currency(tunjangan_keahlian, grouping=True),
                    locale.currency(tunjangan_lain, grouping=True),
                    locale.currency(upah_total, grouping=True),
                    locale.currency(lembur, grouping=True),
                    locale.currency(insentif, grouping=True),
                    locale.currency(gajiKotor, grouping=True),
                    locale.currency(potonganIzin, grouping=True),
                    locale.currency(potonganIzinJam, grouping=True),
                    locale.currency(potonganPajak, grouping=True),
                    locale.currency(potonganPinjaman, grouping=True),
                    locale.currency(komplain, grouping=True),
                    locale.currency(gaji_bersih, grouping=True),
                ])
    return render_template('Pages/karyawan/gaji/list.html', data = data)

@app.route('/cari-gaji')
def searchGaji():
    data  = []    
    data_karyawan = searchDataKaryawan(request.args.get('key'))
    tanggal_header = getHeaderAbsen()
    tanggal = []
    for t in tanggal_header:
        tanggal.append(datetime.strftime(t, "%Y-%m-%d"))
    tanggal_sekarang = datetime.now()
    totalharilibur = hitungHariLibur(tanggal)

    if request.args.get('key') != "":
        if data_karyawan:
            for d in data_karyawan:
                totalharikerja = hitungHariKerja(d[1])
                totalhariizin = hitungHariTidakKerja(d[1], "I")
                totalharicuti = hitungHariTidakKerja(d[1], "C")
                totalharisakit = hitungHariTidakKerja(d[1], "S")
                totalhariizinkhusus = hitungHariTidakKerja(d[1], "IK")
                totalharialpha = len(tanggal) - totalharikerja - totalhariizin - totalharicuti - totalharisakit - totalhariizinkhusus - totalharilibur
                dataGajiKaryawan = getGajiKaryawan(d[1])

                gaji_pokok = dataGajiKaryawan[0] if dataGajiKaryawan[0] != None else 0
                tunjangan_jabatan = dataGajiKaryawan[1] if dataGajiKaryawan[1] != None else 0
                tunjangan_keahlian = dataGajiKaryawan[2] if dataGajiKaryawan[2] != None else 0
                tunjangan_lain = dataGajiKaryawan[3] if dataGajiKaryawan[3] != None else 0
                upah_total = gaji_pokok+tunjangan_jabatan+tunjangan_keahlian+tunjangan_lain

                lembur = getJamLembur(d[1])
                insentif = getTotalnsentif(d[1])

                gajiKotor= upah_total+lembur+insentif

                totalizinperjam = hitungIzinJam(d[1])
                potonganIzin = (int(upah_total)/25) * (int(totalhariizin) + int(totalharialpha))
                potonganIzinJam = (int(upah_total)/25)/7 * (int(totalizinperjam))

                potonganPajak = int(getPajak(d[1])[0])
                potonganPinjaman = int(getPinjaman(d[1], tanggal_sekarang)[0])

                komplain = getDataKomplainByName(d[1], tanggal_sekarang)
                
                gaji_bersih = int(gajiKotor) - int(potonganIzin) - int(potonganIzinJam) - int(potonganPajak) - int(potonganPinjaman) + komplain
                data.append(
                    [
                        d[0],d[1], d[2], 
                        totalharikerja, totalizinperjam, totalhariizin, totalharicuti, 
                        totalharisakit, totalhariizinkhusus, totalharialpha,
                        locale.currency(gaji_pokok, grouping=True), 
                        locale.currency(tunjangan_jabatan, grouping=True),
                        locale.currency(tunjangan_keahlian, grouping=True),
                        locale.currency(tunjangan_lain, grouping=True),
                        locale.currency(upah_total, grouping=True),
                        locale.currency(lembur*15897, grouping=True),
                        locale.currency(insentif, grouping=True),
                        locale.currency(gajiKotor, grouping=True),
                        locale.currency(potonganIzin, grouping=True),
                        locale.currency(potonganIzinJam, grouping=True),
                        locale.currency(potonganPajak, grouping=True),
                        locale.currency(potonganPinjaman, grouping=True),
                        locale.currency(komplain, grouping=True),
                        locale.currency(gaji_bersih, grouping=True),
                    ])
        return render_template('Pages/karyawan/gaji/list.html', data = data)
    else:
        return redirect('/gaji-karyawan')

@app.route('/tambah-gaji', methods=['GET', 'POST'])
def tambahGaji():
    if request.method == "GET":
        return render_template('Pages/karyawan/gaji/tambah.html')
    if request.method == "POST":
        updateDataKaryawanBatch(request.files)
        insertGajiKaryawan(request.files)
        return redirect('/gaji-karyawan')

@app.route('/ubah-gaji/<id>', methods=['GET', 'POST'])
def ubahGaji(id):
    if request.method == "GET":
        data_karyawan = searchDataKaryawanID(id)
        return render_template('Pages/karyawan/gaji/edit.html', data = data_karyawan, kode = id)
    if request.method == "POST":
        if request.form['gaji_pokok'] != "":
            updateGaji(request.form['gaji_pokok'], 'u_pokok', id)
        if request.form['t_keahlian'] != "":
            updateGaji(request.form['t_keahlian'], 't_keahlian', id)
        if request.form['t_jabatan'] != "":
            updateGaji(request.form['t_jabatan'], 't_jabatan', id)
        if request.form['t_lain'] != "":
            updateGaji(request.form['t_lain'], 't_lain', id)
        return redirect('/daftar-karyawan')

@app.route('/insentif')
def insentif():
    dataInsentif = getInsentif()
    data = []
    for i in dataInsentif:
        insentif = list(i)
        insentif.append(locale.currency(int(int(i[5]) * int(i[6])), grouping=True))
        insentif[6] = locale.currency(int(i[6]), grouping=True)
        data.append(insentif)
    return render_template('Pages/karyawan/insentif/list.html', data = data)

@app.route('/tambah-insentif', methods=["GET", "POST"])
def tambahInsentif():
    if request.method == "GET":
        data_karyawan = getDataKaryawan()
        return render_template('Pages/karyawan/insentif/add.html', data=data_karyawan)
    elif request.method == "POST":
        insertInsentif(request.form)
        return redirect('/insentif')
@app.route('/cari-insentif')
def cariInsentif():
    if request.args.get('key') != "":
        data = searchInsentif(request.args.get('key'))
        return render_template('Pages/karyawan/insentif/list.html', data = data)
    else:
        return redirect('/insentif')

@app.route('/ubah-insentif/<id>', methods =['GET', 'POST'])
def ubahInsentif(id):
    if request.method == "GET":
        data_karyawan = getDataKaryawan()
        data = getInsentifById(id)
        return render_template('Pages/karyawan/insentif/edit.html', data = data_karyawan, di = data)
    if request.method == "POST":
        updateInsentif(request.form, id)
        return redirect('/insentif')

@app.route('/hapus-insentif/<id>', methods=['GET'])
def hapusInsentif(id):
    deleteInsentif(id)
    return redirect('/insentif')

@app.route('/pinjaman-pajak')
def pinjamanPajak():
    dataPinjaman = getPinjamanPajak()
    return render_template('Pages/karyawan/pinjaman_pajak/list.html', data = dataPinjaman)

@app.route('/pinjaman-pajak/tambah-baru', methods=["get", "post"])
def tambahPinjamanPajak():
    if request.method == "GET":
        data_karyawan = getDataKaryawan()
        return render_template("Pages/karyawan/pinjaman_pajak/add.html" ,data = data_karyawan)
    elif request.method == "POST":
        insertPotonganLain(request.form)
        return redirect('/pinjaman-pajak')
    
@app.route('/update-pinjaman-pajak/<id>', methods=['GET', 'POST'])
def updatePinjamanPajak(id):
    if request.method == "GET":
        data_karyawan = getDataKaryawan()
        data_pinjaman_pajak = getDataPinjamanPajakById(id)
        return render_template('Pages/karyawan/pinjaman_pajak/edit.html', karyawan = data_karyawan, data = data_pinjaman_pajak)
    elif request.method == "POST":
        if request.form['no_karyawan'] != "":
            id_karyawan = request.form['no_karyawan'].split('-')[0]
            updateDataPinjamanPajak(id_karyawan,"id_karyawan", id)
        if request.form['jenis_pot']:
            updateDataPinjamanPajak(request.form['jenis_pot'],"jenis_pot", id)
            if request.form['jenis_pot'] == 'pjk':
                updateDataPinjamanPajak('',"berlaku", id)
            if request.form['jenis_pot'] == 'pnj':
                updateDataPinjamanPajak(request.form['berlaku'],"berlaku", id)
        if request.form['jumlah'] != "":
            updateDataPinjamanPajak(request.form['jumlah'], "jumlah", id)

        return redirect('/pinjaman-pajak')
    
@app.route('/hapus-pinjaman-pajak/<id>', methods=['GET'])
def hapusPinjamanPajak(id):
    deletePinjamanPajak(id)
    return redirect('/pinjaman-pajak')

@app.route('/cari-pinjaman-pajak')
def cariPinjamPajak():
    dataPinjaman = searchPinjamanPajak(request.args.get('key'))
    return render_template('Pages/karyawan/pinjaman_pajak/list.html', data = dataPinjaman)


@app.route('/komplain', methods=["GET", "POST"])
def daftarKomplain():
    data = []
    data_komplain = getDataKomplain()
    for d in data_komplain:
        dt = list(d)
        dt[2] = locale.currency(int(dt[2]), grouping=True)
        data.append(dt)
    return render_template('Pages/karyawan/komplain/list.html', data = data)

@app.route('/komplain/tambah-baru', methods=["GET", "POST"])
def tambahKomplain():
    if request.method == "GET":
        data_karyawan = getDataKaryawan()
        return render_template('Pages/karyawan/komplain/add.html', data= data_karyawan)
    elif request.method == "POST":
        insertDataKomplain(request.form)
        return redirect('/komplain')

@app.route('/update-komplain/<id>', methods=["GET", "POST"])
def editKomplain(id):
    if request.method == "GET":
        data_karyawan = getDataKaryawan()
        data_komplain = getDataKomplainById(id)
        return render_template('Pages/karyawan/komplain/edit.html', data = data_karyawan, komplain = data_komplain)
    if request.method == "POST":
        if request.form['no_karyawan'] != "":
            id_karyawan = request.form['no_karyawan'].split('-')[0]
            updateKomplain(id_karyawan, 'id_karyawan', id)
        if request.form['jenis'] != "":
            updateKomplain(request.form['jenis'], 'jenis', id)
        if request.form['berlaku'] != "":
            updateKomplain(request.form['berlaku'], 'berlaku', id)
        if request.form['jumlah'] != "":
            updateKomplain(request.form['jumlah'], 'jumlah', id)
        if request.form['keterangan'] != "":
            updateKomplain(request.form['keterangan'], 'keterangan', id)
        
        return redirect('/komplain')

@app.route('/hapus-komplain/<id>')
def hapusKomplain(id):
    deleteKomplain(id)
    return redirect('/komplain')

@app.route('/cari-komplain')
def cariKomplain():
    if request.args.get('key') != "":
        data = searchKomplain(request.args.get('key'))
        return render_template('Pages/karyawan/komplain/list.html', data = data)
    else:
        return redirect('/komplain')

@app.route('/data/gaji-karyawan/download')
def downloadGajiKaryawan():
    data = getDataKaryawan()
    arr = np.array(data, dtype="str_")
    dataFrame = pd.DataFrame(arr, columns=["NOMOR", "NIK", "NAMA KARYAWAN", "JAM KERJA", "UPAH POKOK", "TUNJANGAN JABATAN", "TUNJANGAN KEAHLIAN", "TUNJAGAN LAIN"])
    filename = "DataKaryawan.xlsx"
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataFrame.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-komplain', methods = ['GET', 'POST'])
def downloadKomplain():
    if request.method == "GET":
        data = getDataKaryawan()
        return render_template('Pages/download/komplain.html', data = data)
    if request.method == "POST":
        dt = komplainDownloadData(request.form)
        filename = getNamaDokumen('Data Komplain Periode', request.form)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-pinjaman-pajak', methods=['GET', 'POST'])
def downloadPinjamanPajak():
    if request.method == "GET":
        data = getDataKaryawan()
        return render_template('Pages/download/pinjaman-pajak.html', data = data)
    if request.method == "POST":
        filename = getNamaDokumen("Data Pinjaman dan Pajak Periode", request.form) 
        dt = pinjamanPajakDownloadData(request.form)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-insentif', methods=['GET', 'POST'])
def downloadInsentif():
    if request.method == "GET":
        data = getDataKaryawan()
        return render_template('Pages/download/insentif.html', data = data)
    if request.method == "POST":
        dt = insentifDownloadData(request.form)
        filename = getNamaDokumen("Data Insentif Periode", request.form) 
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt.to_excel(writer, index=False, sheet_name='BONUS & INSENTIF')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-lembur', methods =['GET', 'POST'])
def downloadLembur():
    if request.method == "GET": 
        data = getDataKaryawan()
        return render_template('Pages/download/lembur.html', data = data)
    elif request.method == "POST":
        dt = lemburDownloadData(request.form)
        filename = getNamaDokumen("Data Lembur Periode", request.form) 
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt.to_excel(writer, index=False, sheet_name='LEMBUR')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-izin-jam', methods=['GET', 'POST'])
def downloadIzinJam():
    if request.method == "GET":
        data = getDataKaryawan()
        return render_template('Pages/download/izin-jam.html', data = data)
    elif request.method == "POST":
        dt = izinJamDownloadData(request.form)
        filename = getNamaDokumen("Data Izin Jam Karyawan Periode", request.form)  
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt.to_excel(writer, index=False, sheet_name='IZIN JAM')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-izin', methods =['GET', 'POST'])
def downloadIzin():
    if request.method == "GET":
        data = getDataKaryawan()
        return render_template('Pages/download/izin.html', data = data)
    elif request.method == "POST":
        dt = izinDownloadData(request.form)
        filename = getNamaDokumen("Data Izin Karyawan Periode", request.form)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt.to_excel(writer, index=False, sheet_name='IZIN')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-presensi', methods= ['GET', 'POST'])
def downloadPresensi():
    if request.method == "GET":
        data = getDataKaryawan()
        return render_template('Pages/download/presensi.html', data = data)
    elif request.method == "POST":
        dt = presensiDownloadData(request.form)
        filename = getNamaDokumen("Data Presensi Periode", request.form)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt.to_excel(writer, index=False, sheet_name='PRESENSI')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-gaji', methods=['GET', 'POST'])
def downloadGaji():
    if request.method == "GET":
        data = getDataKaryawan()
        return render_template('Pages/download/gaji.html', data = data)
    elif request.method == "POST":
        filename = getNamaDokumen("Data Gaji Karyawan Periode", request.form)
        dt = gajiDownloadData(request.form)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt.to_excel(writer, index=False, sheet_name='GAJI')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download-data-lengkap', methods=['GET', 'POST'])
def downloadDataFull():
    if request.method == "GET":
        data = getDataKaryawan()
        return render_template('Pages/download/full.html', data = data)
    elif request.method == "POST":
        filename = getNamaDokumen("Data LENGKAP Gaji Karyawan Periode", request.form)
        
        dt_gaji = gajiDownloadData(request.form)
        dt_presensi = presensiDownloadData(request.form)
        dt_izin = izinDownloadData(request.form)
        dt_izin_jam = izinJamDownloadData(request.form)
        dt_lembur = lemburDownloadData(request.form)
        dt_komplain = komplainDownloadData(request.form)
        dt_pinjaman_pajak = pinjamanPajakDownloadData(request.form)
        dt_insentif = insentifDownloadData(request.form)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dt_presensi.to_excel(writer, index=False, sheet_name='PRESENSI')
            dt_izin.to_excel(writer, index=False, sheet_name='IZIN')
            dt_izin_jam.to_excel(writer, index=False, sheet_name='IZIN JAM')
            dt_lembur.to_excel(writer, index=False, sheet_name='LEMBUR')
            dt_pinjaman_pajak.to_excel(writer, index=False, sheet_name='PINJAMAN DAN PAJAK')
            dt_insentif.to_excel(writer, index=False, sheet_name='INSENTIF')
            dt_komplain.to_excel(writer, index=False, sheet_name='KOMPLAIN')
            dt_gaji.to_excel(writer, index=False, sheet_name='GAJI')
        output.seek(0)

        return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__": 
    app.run(host="127.0.0.1",port=5000, debug=True)