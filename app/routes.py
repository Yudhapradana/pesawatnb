import csv
import os
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flaskext.mysql import MySQL
import hashlib

# setting database ke mysql
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'pesawat'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# route untuk halaman login


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    # variable error untuk menyimpan pesan saat login
    error = None
    # cek method POST (sama seperti jika diklik submit)
    if request.method == 'POST':
        # ambil data username dari form
        username = str(request.form['username'])
        # ambil data password dari form
        password = str(request.form['password'])
        cek = cek_login(username, password)
        if cek:
            session['logged_in'] = True  # set session true saat berhasil login
            session['username'] = username  # get data username pada saat login
            session['name'] = str(cek[0][1])  # get data nama pada saat login
            return redirect(url_for('index'))  # refresh/masuk ke halaman index
        else:
            error = "Ada Kesalahan. Coba Lagi!"  # pesan gagal login
    return render_template('login.html', error=error)


def cek_login(username, password):
    conn = mysql.connect()
    cursor = conn.cursor()
    # query sql untuk ambil data dari db
    sql = "SELECT * FROM tbl_user WHERE username=%s AND password=md5(%s)"
    t = (username, password)  # parameter
    cursor.execute(sql, t)  # eksekusi sql
    result = cursor.fetchall()  # menyimpan hasil ekseskusi sql
    conn.close()
    return result


@app.route('/logout')
def logout():
    session.pop('username', None)  # menghapus session username
    session['logged_in'] = False  # ganti status login jadi false
    msg = "Anda Berhasil Log Out!"
    return render_template('login.html', msg=msg)

# ================================================
# route untuk halaman dashboard


@app.route('/index', methods=["GET", "POST"])
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_jenis_pesawat"
    cursor.execute(sql)
    jenispesawat = cursor.fetchall()
    # ambil data jenisayap untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Jenis Sayap'"
    cursor.execute(sql)
    jenis = cursor.fetchall()
    # ambil data penempatan sayap untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Penempatan Sayap'"
    cursor.execute(sql)
    letak = cursor.fetchall()
    # ambil data badan pesawat untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Badan Pesawat'"
    cursor.execute(sql)
    badan = cursor.fetchall()
    # ambil data arah sayap untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Arah Sayap'"
    cursor.execute(sql)
    arah = cursor.fetchall()
    # ambil data persenjataan untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Persenjataan'"
    cursor.execute(sql)
    persenjataan = cursor.fetchall()
    # ambil data jenismesin untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Jenis Mesin'"
    cursor.execute(sql)
    mesin = cursor.fetchall()
    # ambil data warna untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Warna'"
    cursor.execute(sql)
    warna = cursor.fetchall()
    # ambil data jenis ekor untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Bentuk Ekor Pesawat'"
    cursor.execute(sql)
    ekor = cursor.fetchall()
    # ambil data posisi mesin untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Posisi Mesin'"
    cursor.execute(sql)
    posisi = cursor.fetchall()

    a = None
    datapxp = []  # array untuk menyimpan data P(X|CI) * P(CI)
    datapesawat = []  # array untuk menyimpan data pesawat yang teridentifikasi
    if request.method == 'POST':
        jenis_sayap = request.form['jenis_sayap']  # ambil data dari form
        letak_sayap = request.form['letak_sayap']  # ambil data dari form
        arah_sayap = request.form['arah_sayap']  # ambil data dari form
        jenis_mesin = request.form['jenis_mesin']  # ambil data dari form
        posisi_mesin = request.form['posisi_mesin']  # ambil data dari form
        badan_pesawat = request.form['badan_pesawat']  # ambil data dari form
        persenjataan = request.form['persenjataan']  # ambil data dari form
        warna_pesawat = request.form['warna_pesawat']  # ambil data dari form
        jenis_ekor = request.form['jenis_ekor']  # ambil data dari form
        dataArray = [jenis_sayap, letak_sayap, arah_sayap, jenis_mesin, posisi_mesin, badan_pesawat, persenjataan,
                     warna_pesawat, jenis_ekor]  # menyimpan data dari form input dijadikan dalam bentuk array
        bitArray = []
        for row in dataArray:  # perulangan array yang menyimpan inputan dari form
            # ambil data bit spesifik sesuai inputan
            sql = "SELECT bit_spesifik FROM tbl_spesifik WHERE id_spesifik=%s"
            t = (str(row))  # parameter untuk ambil data bit satu satu
            cursor.execute(sql, t)
            result = cursor.fetchone()
            bit = str(result).replace("'", "").replace("(", "").replace(")", "").replace(
                ",", "")  # convert bentuk data bit dari ('00101010100',) ke 00101010100
            bitArray.append(bit)  # ditambahkan ke array baru
        arr = np.array(bitArray)
        # mengubah bentuk array dari 9 array jadi 1 array
        newarr = arr.reshape(-1)
        count = len(newarr[0])
        # proses menghitung fusi informasi/xor
        a = xor(newarr[0], newarr[1], count)
        a = xor(a, newarr[2], count)
        a = xor(a, newarr[3], count)
        a = xor(a, newarr[4], count)
        a = xor(a, newarr[5], count)
        a = xor(a, newarr[6], count)
        a = xor(a, newarr[7], count)
        a = xor(a, newarr[8], count)
        sql = "SELECT * FROM tbl_jenis_pesawat"
        cursor.execute(sql)
        jenispesawat = cursor.fetchall()
        arraypx = []
        for row in jenispesawat:
            sql = "SELECT jumlah_fusi FROM tbl_process INNER JOIN tbl_pesawat ON tbl_pesawat.id=tbl_process.id_pesawat INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat WHERE fusi_informasi=%s AND tbl_jenis_pesawat.nama_jenis_pesawat=%s"
            t = (str(a), row[1])
            cursor.execute(sql, t)
            # disini proses untuk mencari jumlah fusi yang sama disetiap jenis
            countfusi = cursor.fetchone()
            countfusi = str(countfusi).replace(
                "(", "").replace(")", "").replace(",", "")
            # menyimpan nama jenis pesawat dan jumlah fusi yang sama
            arraypx.append((row[1], countfusi))
        sql = "SELECT tbl_jenis_pesawat.nama_jenis_pesawat, COUNT(tbl_pesawat.id_jenis_pesawat) FROM `tbl_pesawat` " \
              "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat GROUP BY tbl_pesawat.id_jenis_pesawat"  # ambil jumlah data masing" dataset setiap jenis
        cursor.execute(sql)
        countjenis = cursor.fetchall()
        valpx = []
        # mencari p fusi informasi
        for row in arraypx:  # perulangan untuk jenis pesawat dan jumlah fusi yang sama
            for rows in countjenis:  # perulangan ambil jumlah data masing" dataset setiap jenis
                if row[0] == rows[0]:  # jika nama jenis pesawat sama
                    if row[1] == 'None':  # jika nilainya none maka diset 0
                        value = 0
                        # dimasukkan ke dalam array
                        valpx.append((row[0], value))
                    else:  # jika tidak dilakukan perhitungan, jumlah fusi yang sama dibagi jumlah dataset setiap jenis pesawat
                        value = float(int(row[1]) / int(rows[1]))
                        # dimasukkan ke dalam array
                        valpx.append((row[0], value))
        sql = "SELECT * FROM tbl_pesawat"
        cursor.execute(sql)
        pesawat = cursor.fetchall()  # ambil dataset
        countdataset = len(pesawat)  # menghitung jumlah dataset
        valtopxp = []
        for row in valpx:  # perulangan hasil perhitungan px
            for rows in countjenis:  # perulangan ambil jumlah data masing" dataset setiap jenis
                if row[0] == rows[0]:  # jika nama jenis pesawat sama
                    # dilakukan perhitungan hasil P(X|CI) * P(CI)
                    value = float(row[1] * (float(rows[1] / countdataset)))
                    if value != 0:  # jika hasilnya tidak sama dengan nol, disimpan didalam array
                        valtopxp.append((row[0], value))
        if valtopxp:
            datapxp.append(max(valtopxp))  # dicari nilai tertingginya
        sql = "SELECT nama_pesawat FROM tbl_pesawat INNER JOIN tbl_process ON tbl_process.id_pesawat=tbl_pesawat.id WHERE tbl_process.fusi_informasi=%s"
        t = (a)
        cursor.execute(sql, t)
        datapesawat = cursor.fetchall()
        # mencari data pesawat sesuai fusi informasinya
    conn.close()
    return render_template('index.html', jenis=jenis, letak=letak, arah=arah, badan=badan, persenjataan=persenjataan, mesin=mesin, warna=warna, ekor=ekor, posisi=posisi, data=datapxp, datapesawat=datapesawat, fusi=a)

# ================================================
# route untuk halaman jenis pesawat


@app.route('/testing', methods=["GET", "POST"])
def testing():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_jenis_pesawat"
    cursor.execute(sql)
    jenispesawat = cursor.fetchall()
    # ambil data jenisayap untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Jenis Sayap'"
    cursor.execute(sql)
    jenis = cursor.fetchall()
    # ambil data penempatan sayap untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Penempatan Sayap'"
    cursor.execute(sql)
    letak = cursor.fetchall()
    # ambil data badan pesawat untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Badan Pesawat'"
    cursor.execute(sql)
    badan = cursor.fetchall()
    # ambil data arah sayap untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Arah Sayap'"
    cursor.execute(sql)
    arah = cursor.fetchall()
    # ambil data persenjataan untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Persenjataan'"
    cursor.execute(sql)
    persenjataan = cursor.fetchall()
    # ambil data jenismesin untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Jenis Mesin'"
    cursor.execute(sql)
    mesin = cursor.fetchall()
    # ambil data warna untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Warna'"
    cursor.execute(sql)
    warna = cursor.fetchall()
    # ambil data jenis ekor untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Bentuk Ekor Pesawat'"
    cursor.execute(sql)
    ekor = cursor.fetchall()
    # ambil data posisi mesin untuk select option
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Posisi Mesin'"
    cursor.execute(sql)
    posisi = cursor.fetchall()

    # a = None
    # datapxp = []  # array untuk menyimpan data P(X|CI) * P(CI)
    # datapesawat = []  # array untuk menyimpan data pesawat yang teridentifikasi
    # # =========================================================================
    # sql = "SELECT id_jenis_sayap, id_jenis_penempatan_sayap, id_arah_sayap, id_jenis_mesin, id_posisi_mesin, id_badan_pesawat, id_persenjataan, id_warna, id_jenis_ekor, nama_jenis_pesawat FROM tbl_pesawat " \
    #       "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat WHERE id <=20"
    # cursor.execute(sql)
    # getDataTesting = cursor.fetchall()
    # bitArray = []
    # # ===================================================== testing
    # counttrue= 0
    # for i in getDataTesting:  # perulangan array yang menyimpan inputan dari form
    #     for row in i:
    #         sql = "SELECT bit_spesifik FROM tbl_spesifik WHERE id_spesifik=%s"  # ambil data bit spesifik sesuai inputan
    #         t = (str(row))  # parameter untuk ambil data bit satu satu
    #         cursor.execute(sql, t)
    #         result = cursor.fetchone()
    #         bit = str(result).replace("'", "").replace("(", "").replace(")", "").replace(",","")  # convert bentuk data bit dari ('00101010100',) ke 00101010100
    #         bitArray.append(bit)  # ditambahkan ke array baru
    #     arr = np.array(bitArray)
    #     newarr = arr.reshape(-1)  # mengubah bentuk array dari 9 array jadi 1 array
    #     count = len(newarr[0])
    #     # proses menghitung fusi informasi/xor
    #     a = xor(newarr[0], newarr[1], count)
    #     a = xor(a, newarr[2], count)
    #     a = xor(a, newarr[3], count)
    #     a = xor(a, newarr[4], count)
    #     a = xor(a, newarr[5], count)
    #     a = xor(a, newarr[6], count)
    #     a = xor(a, newarr[7], count)
    #     a = xor(a, newarr[8], count)
    #     sql = "SELECT * FROM tbl_jenis_pesawat"
    #     cursor.execute(sql)
    #     jenispesawat = cursor.fetchall()
    #     arraypx = []
    #     for row in jenispesawat:
    #         sql = "SELECT jumlah_fusi FROM tbl_process INNER JOIN tbl_pesawat ON tbl_pesawat.id=tbl_process.id_pesawat INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat WHERE fusi_informasi=%s AND tbl_jenis_pesawat.nama_jenis_pesawat=%s"
    #         t = (str(a), row[1])
    #         cursor.execute(sql, t)
    #         # disini proses untuk mencari jumlah fusi yang sama disetiap jenis
    #         countfusi = cursor.fetchone()
    #         countfusi = str(countfusi).replace("(", "").replace(")", "").replace(",", "")
    #         arraypx.append((row[1], countfusi))  # menyimpan nama jenis pesawat dan jumlah fusi yang sama
    #     sql = "SELECT tbl_jenis_pesawat.nama_jenis_pesawat, COUNT(tbl_pesawat.id_jenis_pesawat) FROM `tbl_pesawat` " \
    #           "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat GROUP BY tbl_pesawat.id_jenis_pesawat"  # ambil jumlah data masing" dataset setiap jenis
    #     cursor.execute(sql)
    #     countjenis = cursor.fetchall()
    #     valpx = []
    #     # mencari p fusi informasi
    #     for row in arraypx:  # perulangan untuk jenis pesawat dan jumlah fusi yang sama
    #         for rows in countjenis:  # perulangan ambil jumlah data masing" dataset setiap jenis
    #             if row[0] == rows[0]:  # jika nama jenis pesawat sama
    #                 if row[1] == 'None':  # jika nilainya none maka diset 0
    #                     value = 0
    #                     valpx.append((row[0], value))  # dimasukkan ke dalam array
    #                 else:  # jika tidak dilakukan perhitungan, jumlah fusi yang sama dibagi jumlah dataset setiap jenis pesawat
    #                     value = float(int(row[1]) / int(rows[1]))
    #                     valpx.append((row[0], value))  # dimasukkan ke dalam array
    #     sql = "SELECT * FROM tbl_pesawat"
    #     cursor.execute(sql)
    #     pesawat = cursor.fetchall()  # ambil dataset
    #     countdataset = len(pesawat)  # menghitung jumlah dataset
    #     valtopxp = []
    #     for row in valpx:  # perulangan hasil perhitungan px
    #         for rows in countjenis:  # perulangan ambil jumlah data masing" dataset setiap jenis
    #             if row[0] == rows[0]:  # jika nama jenis pesawat sama
    #                 value = float(row[1] * (float(rows[1] / countdataset)))  # dilakukan perhitungan hasil P(X|CI) * P(CI)
    #                 if value != 0:  # jika hasilnya tidak sama dengan nol, disimpan didalam array
    #                     valtopxp.append((row[0], value))
    #     # print(valtopxp)
    #     if valtopxp:
    #         datapxp.append(max(valtopxp))  # dicari nilai tertingginya
    #         # print(datapxp[0][0])
    #         # print(i[9])
    #         if datapxp[0][0] == i[9]:
    #             counttrue+=1
    #             print(counttrue)
    # precission = float(counttrue/len(getDataTesting))
    # print(precission)
    # # =========================================================================

    a = None
    datapxp = []  # array untuk menyimpan data P(X|CI) * P(CI)
    datapesawat = []  # array untuk menyimpan data pesawat yang teridentifikasi
    if request.method == 'POST':
        namapesawat = request.form['nama_pesawat']  # ambil data dari form
        jenis_pesawat = request.form['jenis_pesawat']  # ambil data dari form
        jenis_sayap = request.form['jenis_sayap']  # ambil data dari form
        letak_sayap = request.form['letak_sayap']  # ambil data dari form
        arah_sayap = request.form['arah_sayap']  # ambil data dari form
        jenis_mesin = request.form['jenis_mesin']  # ambil data dari form
        posisi_mesin = request.form['posisi_mesin']  # ambil data dari form
        badan_pesawat = request.form['badan_pesawat']  # ambil data dari form
        persenjataan = request.form['persenjataan']  # ambil data dari form
        warna_pesawat = request.form['warna_pesawat']  # ambil data dari form
        jenis_ekor = request.form['jenis_ekor']  # ambil data dari form
        dataArray = [jenis_sayap, letak_sayap, arah_sayap, jenis_mesin, posisi_mesin, badan_pesawat, persenjataan,
                     warna_pesawat, jenis_ekor]  # menyimpan data dari form input dijadikan dalam bentuk array
        bitArray = []
        for row in dataArray:  # perulangan array yang menyimpan inputan dari form
            # ambil data bit spesifik sesuai inputan
            sql = "SELECT bit_spesifik FROM tbl_spesifik WHERE id_spesifik=%s"
            t = (str(row))  # parameter untuk ambil data bit satu satu
            cursor.execute(sql, t)
            result = cursor.fetchone()
            bit = str(result).replace("'", "").replace("(", "").replace(")", "").replace(
                ",", "")  # convert bentuk data bit dari ('00101010100',) ke 00101010100
            bitArray.append(bit)  # ditambahkan ke array baru
        arr = np.array(bitArray)
        # mengubah bentuk array dari 9 array jadi 1 array
        newarr = arr.reshape(-1)
        count = len(newarr[0])
        # proses menghitung fusi informasi/xor
        a = xor(newarr[0], newarr[1], count)
        a = xor(a, newarr[2], count)
        a = xor(a, newarr[3], count)
        a = xor(a, newarr[4], count)
        a = xor(a, newarr[5], count)
        a = xor(a, newarr[6], count)
        a = xor(a, newarr[7], count)
        a = xor(a, newarr[8], count)
        sql = "SELECT * FROM tbl_jenis_pesawat"
        cursor.execute(sql)
        jenispesawat = cursor.fetchall()
        arraypx = []
        for row in jenispesawat:
            sql = "SELECT jumlah_fusi FROM tbl_process INNER JOIN tbl_pesawat ON tbl_pesawat.id=tbl_process.id_pesawat INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat WHERE fusi_informasi=%s AND tbl_jenis_pesawat.nama_jenis_pesawat=%s"
            t = (str(a), row[1])
            cursor.execute(sql, t)
            # disini proses untuk mencari jumlah fusi yang sama disetiap jenis
            countfusi = cursor.fetchone()
            countfusi = str(countfusi).replace(
                "(", "").replace(")", "").replace(",", "")
            # menyimpan nama jenis pesawat dan jumlah fusi yang sama
            arraypx.append((row[1], countfusi))
        sql = "SELECT tbl_jenis_pesawat.nama_jenis_pesawat, COUNT(tbl_pesawat.id_jenis_pesawat) FROM `tbl_pesawat` " \
              "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat GROUP BY tbl_pesawat.id_jenis_pesawat"  # ambil jumlah data masing" dataset setiap jenis
        cursor.execute(sql)
        countjenis = cursor.fetchall()
        valpx = []
        # mencari p fusi informasi
        for row in arraypx:  # perulangan untuk jenis pesawat dan jumlah fusi yang sama
            for rows in countjenis:  # perulangan ambil jumlah data masing" dataset setiap jenis
                if row[0] == rows[0]:  # jika nama jenis pesawat sama
                    if row[1] == 'None':  # jika nilainya none maka diset 0
                        value = 0
                        # dimasukkan ke dalam array
                        valpx.append((row[0], value))
                    else:  # jika tidak dilakukan perhitungan, jumlah fusi yang sama dibagi jumlah dataset setiap jenis pesawat
                        value = float(int(row[1]) / int(rows[1]))
                        # dimasukkan ke dalam array
                        valpx.append((row[0], value))
        sql = "SELECT * FROM tbl_pesawat"
        cursor.execute(sql)
        pesawat = cursor.fetchall()  # ambil dataset
        countdataset = len(pesawat)  # menghitung jumlah dataset
        valtopxp = []
        for row in valpx:  # perulangan hasil perhitungan px
            for rows in countjenis:  # perulangan ambil jumlah data masing" dataset setiap jenis
                if row[0] == rows[0]:  # jika nama jenis pesawat sama
                    # dilakukan perhitungan hasil P(X|CI) * P(CI)
                    value = float(row[1] * (float(rows[1] / countdataset)))
                    if value != 0:  # jika hasilnya tidak sama dengan nol, disimpan didalam array
                        valtopxp.append((row[0], value))
        if valtopxp:
            datapxp.append(max(valtopxp))  # dicari nilai tertingginya
        sql = "SELECT nama_pesawat FROM tbl_pesawat INNER JOIN tbl_process ON tbl_process.id_pesawat=tbl_pesawat.id WHERE tbl_process.fusi_informasi=%s"
        t = (a)
        cursor.execute(sql, t)
        datapesawat = cursor.fetchall()
        # mencari data pesawat sesuai fusi informasinya

        if not datapxp:
            resultmetode = "Objek tidak dikenal atau belum ada di dalam basis data"
        else:
            resultmetode = datapxp[0][0]
        sql = "INSERT INTO tbl_testing(nama_pesawat, id_jenis_pesawat, id_jenis_sayap, id_jenis_penempatan_sayap, id_arah_sayap, id_jenis_mesin, id_badan_pesawat, id_persenjataan, id_warna, id_posisi_mesin, id_jenis_ekor, result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        t = (namapesawat, int(jenis_pesawat), int(jenis_sayap), int(letak_sayap), int(arah_sayap), int(jenis_mesin), int(
            badan_pesawat), int(persenjataan), int(warna_pesawat), int(posisi_mesin), int(jenis_ekor), resultmetode)
        cursor.execute(sql, t)
        conn.commit()
    conn.close()
    return render_template('testing.html', jenis=jenis, letak=letak, arah=arah, badan=badan, persenjataan=persenjataan, mesin=mesin, warna=warna, ekor=ekor, posisi=posisi, data=datapxp, datapesawat=datapesawat, fusi=a, jenispesawat=jenispesawat)

    # a = None
    # datapxp = []  # array untuk menyimpan data P(X|CI) * P(CI)
    # datapesawat = []  # array untuk menyimpan data pesawat yang teridentifikasi
    # if request.method == 'POST':
    #     jenis_sayap = request.form['jenis_sayap']  # ambil data dari form
    #     letak_sayap = request.form['letak_sayap']  # ambil data dari form
    #     arah_sayap = request.form['arah_sayap']  # ambil data dari form
    #     jenis_mesin = request.form['jenis_mesin']  # ambil data dari form
    #     posisi_mesin = request.form['posisi_mesin']  # ambil data dari form
    #     badan_pesawat = request.form['badan_pesawat']  # ambil data dari form
    #     persenjataan = request.form['persenjataan']  # ambil data dari form
    #     warna_pesawat = request.form['warna_pesawat']  # ambil data dari form
    #     jenis_ekor = request.form['jenis_ekor']  # ambil data dari form
    #     dataArray = [jenis_sayap, letak_sayap, arah_sayap, jenis_mesin, posisi_mesin, badan_pesawat, persenjataan,
    #                  warna_pesawat, jenis_ekor]  # menyimpan data dari form input dijadikan dalam bentuk array
    #     bitArray = []
    #     for row in dataArray:  # perulangan array yang menyimpan inputan dari form
    #         # ambil data bit spesifik sesuai inputan
    #         sql = "SELECT bit_spesifik FROM tbl_spesifik WHERE id_spesifik=%s"
    #         t = (str(row))  # parameter untuk ambil data bit satu satu
    #         cursor.execute(sql, t)
    #         result = cursor.fetchone()
    #         bit = str(result).replace("'", "").replace("(", "").replace(")", "").replace(
    #             ",", "")  # convert bentuk data bit dari ('00101010100',) ke 00101010100
    #         bitArray.append(bit)  # ditambahkan ke array baru
    #     arr = np.array(bitArray)
    #     # mengubah bentuk array dari 9 array jadi 1 array
    #     newarr = arr.reshape(-1)
    #     count = len(newarr[0])
    #     # proses menghitung fusi informasi/xor
    #     a = xor(newarr[0], newarr[1], count)
    #     a = xor(a, newarr[2], count)
    #     a = xor(a, newarr[3], count)
    #     a = xor(a, newarr[4], count)
    #     a = xor(a, newarr[5], count)
    #     a = xor(a, newarr[6], count)
    #     a = xor(a, newarr[7], count)
    #     a = xor(a, newarr[8], count)
    #     sql = "SELECT * FROM tbl_jenis_pesawat"
    #     cursor.execute(sql)
    #     jenispesawat = cursor.fetchall()
    #     arraypx = []
    #     for row in jenispesawat:
    #         sql = "SELECT jumlah_fusi FROM tbl_process INNER JOIN tbl_pesawat ON tbl_pesawat.id=tbl_process.id_pesawat INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat WHERE fusi_informasi=%s AND tbl_jenis_pesawat.nama_jenis_pesawat=%s"
    #         t = (str(a), row[1])
    #         cursor.execute(sql, t)
    #         # disini proses untuk mencari jumlah fusi yang sama disetiap jenis
    #         countfusi = cursor.fetchone()
    #         countfusi = str(countfusi).replace(
    #             "(", "").replace(")", "").replace(",", "")
    #         # menyimpan nama jenis pesawat dan jumlah fusi yang sama
    #         arraypx.append((row[1], countfusi))
    #     sql = "SELECT tbl_jenis_pesawat.nama_jenis_pesawat, COUNT(tbl_pesawat.id_jenis_pesawat) FROM `tbl_pesawat` " \
    #           "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat GROUP BY tbl_pesawat.id_jenis_pesawat"  # ambil jumlah data masing" dataset setiap jenis
    #     cursor.execute(sql)
    #     countjenis = cursor.fetchall()
    #     valpx = []
    #     # mencari p fusi informasi
    #     for row in arraypx:  # perulangan untuk jenis pesawat dan jumlah fusi yang sama
    #         for rows in countjenis:  # perulangan ambil jumlah data masing" dataset setiap jenis
    #             if row[0] == rows[0]:  # jika nama jenis pesawat sama
    #                 if row[1] == 'None':  # jika nilainya none maka diset 0
    #                     value = 0
    #                     # dimasukkan ke dalam array
    #                     valpx.append((row[0], value))
    #                 else:  # jika tidak dilakukan perhitungan, jumlah fusi yang sama dibagi jumlah dataset setiap jenis pesawat
    #                     value = float(int(row[1]) / int(rows[1]))
    #                     # dimasukkan ke dalam array
    #                     valpx.append((row[0], value))
    #     sql = "SELECT * FROM tbl_pesawat"
    #     cursor.execute(sql)
    #     pesawat = cursor.fetchall()  # ambil dataset
    #     countdataset = len(pesawat)  # menghitung jumlah dataset
    #     valtopxp = []
    #     for row in valpx:  # perulangan hasil perhitungan px
    #         for rows in countjenis:  # perulangan ambil jumlah data masing" dataset setiap jenis
    #             if row[0] == rows[0]:  # jika nama jenis pesawat sama
    #                 # dilakukan perhitungan hasil P(X|CI) * P(CI)
    #                 value = float(row[1] * (float(rows[1] / countdataset)))
    #                 if value != 0:  # jika hasilnya tidak sama dengan nol, disimpan didalam array
    #                     valtopxp.append((row[0], value))
    #     if valtopxp:
    #         datapxp.append(max(valtopxp))  # dicari nilai tertingginya
    #     sql = "SELECT nama_pesawat FROM tbl_pesawat INNER JOIN tbl_process ON tbl_process.id_pesawat=tbl_pesawat.id WHERE tbl_process.fusi_informasi=%s"
    #     t = (a)
    #     cursor.execute(sql, t)
    #     datapesawat = cursor.fetchall()
    #     # mencari data pesawat sesuai fusi informasinya
    # conn.close()
    # return render_template('index.html', jenis=jenis, letak=letak, arah=arah, badan=badan, persenjataan=persenjataan, mesin=mesin, warna=warna, ekor=ekor, posisi=posisi, data=datapxp, datapesawat=datapesawat, fusi=a)

# ================================================
# route untuk halaman jenis pesawat


@app.route('/jenis')
def jenis():
    return render_template('jenis.html')

# fungsi untuk ambil data jenis pesawat


@app.route('/getJenis')
def getJenis():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_jenis_pesawat"  # ambil data jenis pesawat
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:  # dilakukan perulangan untuk dimasukkan kedalam array dan diberi index
        res.append({"id": row[0], "jenis": row[1]})

    data = {}
    data["data"] = res  # menyimpan hasil select ke variable data
    return jsonify(data)  # kirim data ke html dalam bentuk json


@app.route('/insertJenis', methods=["POST"])
def insertJenis():
    name = request.form['jenis_pesawat']  # ambil inputan jenis pesawat
    conn = mysql.connect()
    cursor = conn.cursor()
    # sql untuk insert data
    sql = "INSERT INTO tbl_jenis_pesawat (nama_jenis_pesawat) VALUES (%s)"
    t = (name)  # parameter yang di inputkan
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('jenis'))


@app.route('/updateJenis', methods=["POST"])
def updateJenis():
    jenis = request.form['ujenis_pesawat']  # ambil inputan jenis pesawat
    id = request.form['uid']  # ambil inputan id jenis pesawat
    conn = mysql.connect()
    cursor = conn.cursor()
    # sql untuk update
    sql = "UPDATE tbl_jenis_pesawat SET nama_jenis_pesawat=%s WHERE id_jenis_pesawat=%s"
    t = (jenis, id)  # parameter untuk update
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('jenis'))


@app.route('/deleteJenis', methods=["POST"])
def deleteJenis():
    id = request.form['did']  # ambil id jenis pesawat
    conn = mysql.connect()
    cursor = conn.cursor()
    # sql untuk menghapus data
    sql = "DELETE FROM tbl_jenis_pesawat WHERE id_jenis_pesawat=%s"
    t = (id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('jenis'))
# ================================================
# route untuk halaman karakteristik pesawat


@app.route('/karakteristik')
def karakteristik():
    return render_template('karakteristik.html')

# fungsi untuk ambil data karakteristik pesawat


@app.route('/getKarakteristik')
def getKarakteristik():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_karakteristik"  # ambil data karakteristik
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:  # dilakukan perulangan untuk dimasukkan kedalam array dan diberi index
        res.append({"id": row[0], "name": row[1]})  # di inputkan ke array res

    data = {}
    data["data"] = res  # menyimpan res ke variable data
    return jsonify(data)  # kirim data ke html


@app.route('/insertKarakteristik', methods=["POST"])
def insertKarakteristik():
    name = request.form['name']  # ambil inputan nama karakteristik dari form
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO tbl_karakteristik(name) VALUES (%s)"  # sql untuk insert
    t = (name)  # parameter yang mau di insert
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('karakteristik'))


@app.route('/updateKarakteristik', methods=["POST"])
def updateKarakteristik():
    name = request.form['uname']  # ambil inputan nama karakteristik dari form
    id = request.form['uid']  # ambil inputan id dari form
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "UPDATE tbl_karakteristik SET name=%s WHERE id=%s"  # sql untuk update
    t = (name, id)  # parameter untuk update
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('karakteristik'))


@app.route('/deleteKarakteristik', methods=["POST"])
def deleteKarakteristik():
    id = request.form['did']  # ambil data id dari form
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "DELETE FROM tbl_karakteristik WHERE id=%s"  # sql untuk proses delete
    t = (id)  # parameter untuk delete berdasarkan id
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('karakteristik'))
# ================================================
# route untuk halaman spesifik pesawat


@app.route('/spesifik')
def spesifik():
    conn = mysql.connect()
    cursor = conn.cursor()
    # ambil data karakteristik untuk form select option
    sql = "SELECT * FROM tbl_karakteristik"
    cursor.execute(sql)
    karakteristik = cursor.fetchall()
    conn.close()
    # lempar data ke file html
    return render_template('spesifik.html', karakteristik=karakteristik)

# fungsi untuk ambil data spesifik pesawat


@app.route('/getSpesifik')
def getSpesifik():
    conn = mysql.connect()
    cursor = conn.cursor()
    # sql untuk mengambil data dari database
    sql = "SELECT s.id_spesifik, k.name, s.kode_spesifik, s.spesifik, s.bit_spesifik, s.id_karakteristik FROM tbl_spesifik as s INNER JOIN tbl_karakteristik as k ON k.id=s.id_karakteristik"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:  # dilakukan perulangan untuk dimasukkan kedalam array dan diberi index
        res.append({"id": row[0], "name_karakteristik": row[1], "kode_spesifik": row[2], "spesifik": row[3],
                    "bit_spesifik": row[4], "id_karakteristik": row[5]})  # di input ke variable res

    data = {}
    data["data"] = res  # array res disimpan ke variable data
    return jsonify(data)


@app.route('/insertSpesifik', methods=["POST"])
def insertSpesifik():
    # ambil inputan tipe karakteristik
    karakteristik = request.form['karakteristik']
    kode = request.form['kode_spesifik']  # ambil inputan data kode spesifik
    spesifik = request.form['spesifik']  # ambil inputan nama spesifik
    bit = request.form['bit_spesifik']  # ambil inputan bit spesifik
    conn = mysql.connect()
    cursor = conn.cursor()
    # sql untuk input
    sql = "INSERT INTO tbl_spesifik(id_karakteristik, kode_spesifik, spesifik, bit_spesifik) VALUES (%s, %s, %s, %s)"
    t = (karakteristik, kode, spesifik, bit)  # parameter untuk input data
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('spesifik'))


@app.route('/updateSpesifik', methods=["POST"])
def updateSpesifik():
    id = request.form['uid']  # ambil id spesifik
    # ambil inputan tipe karakteristik
    karakteristik = request.form['ukarakteristik']
    kode = request.form['ukode_spesifik']  # ambil inputan tipe spesifik
    spesifik = request.form['uspesifik']  # ambil inputan nama spesifik
    bit = request.form['ubit_spesifik']  # ambil inputan bit spesifik
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "UPDATE tbl_spesifik SET id_karakteristik=%s, kode_spesifik=%s, spesifik=%s, bit_spesifik=%s WHERE id_spesifik=%s"  # sql update
    t = (karakteristik, kode, spesifik, bit, id)  # parameter inputan
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('spesifik'))


@app.route('/deleteSpesifik', methods=["POST"])
def deleteSpesifik():
    id = request.form['did']  # ambil id dari form untuk proses delete
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "DELETE FROM tbl_spesifik WHERE id_spesifik=%s"  # sql untuk delete
    t = (id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('spesifik'))

# ================================================
# route untuk halaman dataset


@app.route('/dataset')
def dataset():
    conn = mysql.connect()
    cursor = conn.cursor()
    # ambil data untuk select option jenis pesawat
    sql = "SELECT * FROM tbl_jenis_pesawat"
    cursor.execute(sql)
    jenis = cursor.fetchall()
    # ambil data untuk select option jenis sayap
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Jenis Sayap'"
    cursor.execute(sql)
    js = cursor.fetchall()
    # ambil data untuk select option penempatan sayap
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Penempatan Sayap'"
    cursor.execute(sql)
    jp = cursor.fetchall()
    # ambil data untuk select option arah sayap
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Arah Sayap'"
    cursor.execute(sql)
    rs = cursor.fetchall()
    # ambil data untuk select option jenis mesin
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Jenis Mesin'"
    cursor.execute(sql)
    jm = cursor.fetchall()
    # ambil data untuk select option badan pesawat
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Badan Pesawat'"
    cursor.execute(sql)
    bp = cursor.fetchall()
    # ambil data untuk select option persenjataan
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Persenjataan'"
    cursor.execute(sql)
    ps = cursor.fetchall()
    # ambil data untuk select option jenis pesawat
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Warna'"
    cursor.execute(sql)
    wn = cursor.fetchall()
    # ambil data untuk select option posisi mesin
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Posisi Mesin'"
    cursor.execute(sql)
    pm = cursor.fetchall()
    # ambil data untuk select option jenis ekor
    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Bentuk Ekor Pesawat'"
    cursor.execute(sql)
    je = cursor.fetchall()

    conn.close()
    return render_template('dataset.html', jenis=jenis, js=js, jp=jp, rs=rs, jm=jm, bp=bp, ps=ps, wn=wn, pm=pm, je=je)

# fungsi untuk ambil data dataset pesawat


@app.route('/getDataset')
def getDataset():
    conn = mysql.connect()
    cursor = conn.cursor()
    # sql untuk menampilkan dataset ke halaman html
    sql = "SELECT p.id, nama_pesawat, j.nama_jenis_pesawat, a.spesifik as jenis_sayap, b.spesifik as jenis_penempatan_sayap, " \
          "d.spesifik as arah_sayap, e.spesifik as jenis_mesin, h.spesifik as badan_pesawat, m.spesifik as persenjataan, " \
          "n.spesifik as warna, o.spesifik as posisi_mesin, q.spesifik as jenis_ekor, j.id_jenis_pesawat, a.id_spesifik as id_jenis_sayap, " \
          "b.id_spesifik as id_jenis_penempatan_sayap, d.id_spesifik as id_arah_sayap, e.id_spesifik as id_jenis_mesin, h.id_spesifik as id_badan_pesawat, " \
          "m.id_spesifik as id_persenjataan, " \
          "n.id_spesifik as id_warna, o.id_spesifik as id_posisi_mesin, q.id_spesifik as id_jenis_ekor FROM tbl_pesawat as p " \
          "INNER JOIN tbl_jenis_pesawat as j ON p.id_jenis_pesawat=j.id_jenis_pesawat " \
          "INNER JOIN tbl_spesifik as a ON a.id_spesifik=p.id_jenis_sayap " \
          "INNER JOIN tbl_spesifik as b ON b.id_spesifik=p.id_jenis_penempatan_sayap " \
          "INNER JOIN tbl_spesifik as d ON d.id_spesifik=p.id_arah_sayap " \
          "INNER JOIN tbl_spesifik as e ON e.id_spesifik=p.id_jenis_mesin " \
          "INNER JOIN tbl_spesifik as h ON h.id_spesifik=p.id_badan_pesawat " \
          "INNER JOIN tbl_spesifik as m ON m.id_spesifik=p.id_persenjataan " \
          "INNER JOIN tbl_spesifik as n ON n.id_spesifik=p.id_warna " \
          "INNER JOIN tbl_spesifik as o ON o.id_spesifik=p.id_posisi_mesin " \
          "INNER JOIN tbl_spesifik as q ON q.id_spesifik=p.id_jenis_ekor " \
          "INNER JOIN tbl_karakteristik as r ON r.id=a.id_karakteristik"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    res = []
    for row in result:  # dilakukan perulangan untuk dimasukkan kedalam array dan diberi index
        # lalu di input ke array res
        res.append({"id": row[0], "nama_pesawat": row[1], "nama_jenis_pesawat": row[2],
                    "jenis_sayap": row[3], "jenis_penempatan_sayap": row[4], "arah_sayap": row[5],
                    "jenis_mesin": row[6], "badan_pesawat": row[7],
                    "persenjataan": row[8], "warna": row[9], "posisi_mesin": row[10], "jenis_ekor": row[11],
                    "id_jenis_pesawat": row[12], 'id_jenis_sayap': row[13], 'id_penempatan_sayap': row[14],
                    "id_arah_sayap": row[15], "id_jenis_mesin": row[16], "id_badan_pesawat": row[17],
                    "id_persenjataan": row[18], "id_warna": row[19], "id_posisi_mesin": row[20], "id_jenis_ekor": row[21]})

    data = {}
    # menyimpan data dari array res ke array data dengan index data
    data["data"] = res
    return jsonify(data)


# ================================================
# permission file upload
ALLOWED_EXTENSION = set(['csv', 'json', 'xml', 'xlsx'])
app.config['UPLOAD_FOLDER'] = 'app/uploads'
# cek ekstensi file


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

# ================================================
# fungsi untuk import dataset


@app.route('/importData', methods=['GET', 'POST'])
def importData():
    if request.method == 'POST':  # cek request method
        file = request.files['file']  # ambil data file import

    if 'file' not in request.files:  # jika tidak terbaca file importnya
        return redirect(request.url)

    if file.filename == '':
        return redirect(request.url)

    # jika file importnya ada dan sesuai dengan ekstensi yang diperbolehkan
    if file and allowed_file(file.filename):
        ext = str(file.filename)  # menyimpan nama file
        filename = secure_filename(file.filename)
        # menyimpan file kelokasi yang telah ditentukan diconfig diatas
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = mysql.connect()
        cursor = conn.cursor()
        data = []
        if ext.rsplit('.', 1)[1] == 'csv':  # jika ektensi csv
            csv_data = csv.reader(
                open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))  # membaca file
            csv_data = iter(csv_data)
            # skip 1 perulangan, karena perulangan pertama judul kolom
            next(csv_data, None)
            for row in csv_data:  # melakukan perulangan hasil ambil data nya
                t = str(row).strip('[]').strip("'")  # menghapus karakter
                b = t.rsplit(";")  # memisah karakter
                res = []
                count = len(b)  # menghitung data hasil pemisahan
                for line in b:
                    # mengambil id spsifik berdasarkan inputan
                    cek = "SELECT id_spesifik FROM tbl_spesifik WHERE spesifik=%s"
                    text = (line)
                    cursor.execute(cek, text)
                    id_spesifik = cursor.fetchone()
                    if id_spesifik == None:  # jika id_spesifik none
                        # mengambil id jenis pesawat berdasarkan inputan
                        cek = "SELECT id_jenis_pesawat FROM tbl_jenis_pesawat WHERE nama_jenis_pesawat=%s"
                        text = (line)
                        cursor.execute(cek, text)
                        id_spesifik = cursor.fetchone()
                    id_spesifik = str(id_spesifik).replace("(", "").replace(
                        ")", "").replace(",", "")  # convert/menghapus karakter
                    count -= 1
                    if count == 0:
                        res.append(line)
                    else:
                        res.append(id_spesifik)
                data.append(res)

        if ext.rsplit('.', 1)[1] == 'xlsx':  # jika ektensi xlsx
            # membaca data excel
            df = pd.read_excel(app.config['UPLOAD_FOLDER']+'/'+filename)
            for index, row in df.iterrows():  # perulangan data inputan untuk dicari id nya
                res = []
                count = len(row)
                for line in row:
                    # ambil id setiap inputan
                    cek = "SELECT id_spesifik FROM tbl_spesifik WHERE spesifik=%s"
                    text = (line)
                    cursor.execute(cek, text)
                    id_spesifik = cursor.fetchone()
                    if id_spesifik == None:  # jika id_spesifik none
                        # mengambil id jenis pesawat berdasarkan inputan
                        cek = "SELECT id_jenis_pesawat FROM tbl_jenis_pesawat WHERE nama_jenis_pesawat=%s"
                        text = (line)
                        cursor.execute(cek, text)
                        id_spesifik = cursor.fetchone()
                    id_spesifik = str(id_spesifik).replace("(", "").replace(
                        ")", "").replace(",", "")  # convert/menghapus karakter
                    count -= 1
                    if count == 0:
                        res.append(line)
                    else:
                        res.append(id_spesifik)
                data.append(res)
        print(data)
        for row in data:
            # input ke database
            sql = "INSERT INTO tbl_pesawat (nama_pesawat, id_jenis_pesawat, id_jenis_sayap, id_jenis_penempatan_sayap, id_arah_sayap, id_jenis_mesin, id_badan_pesawat, id_persenjataan, id_warna, id_posisi_mesin, id_jenis_ekor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            t = (row[11], row[10], row[1], row[2], row[3],
                 row[4], row[6], row[8], row[9], row[5], row[7])
            cursor.execute(sql, t)
        conn.commit()
        cursor.close()
    return redirect(url_for('dataset'))


@app.route('/insertDataset', methods=["POST"])
def insertDataset():
    nama_pesawat = request.form['nama_pesawat']
    jenis_pesawat = request.form['jenis_pesawat']
    jenis_sayap = request.form['jenis_sayap']
    penempatan_sayap = request.form['jenis_penempatan_sayap']
    arah_sayap = request.form['arah_sayap']
    jenis_mesin = request.form['jenis_mesin']
    posisi_mesin = request.form['posisi_mesin']
    badan_pesawat = request.form['badan_pesawat']
    jenis_ekor = request.form['jenis_ekor']
    persenjataan = request.form['persenjataan']
    warna = request.form['warna']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO tbl_pesawat(nama_pesawat, id_jenis_pesawat, id_jenis_sayap, id_jenis_penempatan_sayap, id_arah_sayap, id_jenis_mesin, id_badan_pesawat, id_persenjataan, id_warna, id_posisi_mesin, id_jenis_ekor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    t = (nama_pesawat, jenis_pesawat, jenis_sayap, penempatan_sayap, arah_sayap,
         jenis_mesin, badan_pesawat, persenjataan, warna, posisi_mesin, jenis_ekor)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('dataset'))


@app.route('/updateDataset', methods=["POST"])
def updateDataset():
    id = request.form['uid']
    nama_pesawat = request.form['unama_pesawat']
    jenis_pesawat = request.form['ujenis_pesawat']
    jenis_sayap = request.form['ujenis_sayap']
    penempatan_sayap = request.form['ujenis_penempatan_sayap']
    arah_sayap = request.form['uarah_sayap']
    jenis_mesin = request.form['ujenis_mesin']
    posisi_mesin = request.form['uposisi_mesin']
    badan_pesawat = request.form['ubadan_pesawat']
    jenis_ekor = request.form['ujenis_ekor']
    persenjataan = request.form['upersenjataan']
    warna = request.form['uwarna']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "UPDATE tbl_pesawat SET nama_pesawat=%s, id_jenis_pesawat=%s, id_jenis_sayap=%s, id_jenis_penempatan_sayap=%s, id_arah_sayap=%s, id_jenis_mesin=%s, id_badan_pesawat=%s, id_persenjataan=%s, id_warna=%s, id_posisi_mesin=%s, id_jenis_ekor=%s WHERE id=%s"
    t = (nama_pesawat, jenis_pesawat, jenis_sayap, penempatan_sayap, arah_sayap,
         jenis_mesin, badan_pesawat, persenjataan, warna, posisi_mesin, jenis_ekor, id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('dataset'))


@app.route('/deleteDataset', methods=["POST"])
def deleteDataset():
    id = request.form['did']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "DELETE FROM tbl_pesawat WHERE id=%s"
    t = (id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('dataset'))

# ================================================
# proses perhitungan fusi normalisasi dan naivebayes


@app.route('/processData')
def processData():
    return render_template('process.html')


def xor(a, b, n):
    val = ""
    for i in range(n):
        if (a[i] == b[i]):
            val += "0"
        else:
            val += "1"
    return val


@app.route('/getpPocessData')
def getProcessData():
    conn = mysql.connect()
    cursor = conn.cursor()
    # ambil data di tbl_process
    sql = "SELECT tbl_process.id_pesawat, tbl_jenis_pesawat.nama_jenis_pesawat, tbl_process.fusi_informasi, tbl_process.jumlah_fusi, tbl_process.naive_bayes, tbl_pesawat.nama_pesawat " \
          "FROM tbl_process INNER JOIN tbl_pesawat ON tbl_pesawat.id=tbl_process.id_pesawat " \
          "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat"
    cursor.execute(sql)
    tblprocess = cursor.fetchall()
    # ambil data pesawat
    sql = "SELECT * FROM tbl_pesawat"
    cursor.execute(sql)
    tblpesawat = cursor.fetchall()
    arrayres = []
    # validasi jika jumlah data pesawat dan jumlah data di tbl_process tidak sama, akah diproses, jika tidak, tidak akan diproses lagi
    if len(tblprocess) != len(tblpesawat):
        # ambil data bit setiap ciri-ciri
        sql = "SELECT p.id, p.nama_pesawat, j.nama_jenis_pesawat, a.bit_spesifik as jenis_sayap, b.bit_spesifik as jenis_penempatan_sayap, " \
              "d.bit_spesifik as arah_sayap, e.bit_spesifik as jenis_mesin, x.bit_spesifik as posisi_mesin, h.bit_spesifik as badan_pesawat, y.bit_spesifik as jenis_ekor, " \
              "m.bit_spesifik as persenjataan, " \
              "n.bit_spesifik as warna, r.name FROM tbl_pesawat as p INNER JOIN tbl_jenis_pesawat as j ON p.id_jenis_pesawat=j.id_jenis_pesawat " \
              "INNER JOIN tbl_spesifik as a ON a.id_spesifik=p.id_jenis_sayap INNER JOIN tbl_spesifik as b ON b.id_spesifik=p.id_jenis_penempatan_sayap " \
              "INNER JOIN tbl_spesifik as d ON d.id_spesifik=p.id_arah_sayap INNER JOIN tbl_spesifik as e ON e.id_spesifik=p.id_jenis_mesin " \
              "INNER JOIN tbl_spesifik as h ON h.id_spesifik=p.id_badan_pesawat INNER JOIN tbl_spesifik as m ON m.id_spesifik=p.id_persenjataan " \
              "INNER JOIN tbl_spesifik as x ON x.id_spesifik=p.id_posisi_mesin INNER JOIN tbl_spesifik as y ON y.id_spesifik=p.id_jenis_ekor "\
              "INNER JOIN tbl_spesifik as n ON n.id_spesifik=p.id_warna INNER JOIN tbl_karakteristik as r ON r.id=a.id_karakteristik"
        cursor.execute(sql)
        result = cursor.fetchall()
        res = []
        # proses perhitungan fusi informasi/xor
        for row in result:
            count = len(row[3])
            a = xor(row[3], row[4], count)
            a = xor(a, row[5], count)
            a = xor(a, row[6], count)
            a = xor(a, row[7], count)
            a = xor(a, row[8], count)
            a = xor(a, row[9], count)
            a = xor(a, row[10], count)
            a = xor(a, row[11], count)
            # res.append((row[0], row[2], a))
            res.append((row[0], row[2], a, row[1]))
        listfusi = []
        # membuat list fusi yang berbeda
        for row in res:
            if row[2] not in listfusi:
                listfusi.append(row[2])
        # membuat dictionary dari list fusi
        dictset = dict.fromkeys(listfusi, 0)
        # menghitung fusi yang sama
        for row in res:
            if row[2] in dictset:
                dictset[row[2]] += 1
        dataarray = []
        # menyimpan data ke dalam array sebelum dilakukan input kedatabase
        for row in res:
            id = row[0]
            jenispesawat = row[1]
            fusi = row[2]
            namapesawat = row[3]
            for datafusi, val in dictset.items():
                if fusi == datafusi:
                    countfusi = val
            dataarray.append((id, jenispesawat, fusi, countfusi, namapesawat))
        # ambil jumlah data masing" dataset setiap jenis
        sql = "SELECT tbl_jenis_pesawat.nama_jenis_pesawat, COUNT(tbl_pesawat.id_jenis_pesawat) FROM `tbl_pesawat` " \
              "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat GROUP BY tbl_pesawat.id_jenis_pesawat"
        cursor.execute(sql)
        countjenis = cursor.fetchall()
        # perulangan untuk proses perhitungan P(X|CI)
        for row in dataarray:
            for jenis in countjenis:
                if row[1] == jenis[0]:
                    nb = float(row[3]/jenis[1])
            arrayres.append({"id_pesawat": row[0], "jenis_pesawat": row[1], "fusi": row[2],
                             "jumlah_fusi": row[3], "naive_bayes": nb, "nama_pesawat": row[4]})
            sql = "INSERT INTO tbl_process(id_pesawat, fusi_informasi, jumlah_fusi, naive_bayes) VALUES(%s, %s, %s, %s)"
            t = (row[0], row[2], row[3], nb)
            cursor.execute(sql, t)
            conn.commit()
    # if not tblprocess:
    for row in tblprocess:
        arrayres.append({"id_pesawat": row[0], "nama_pesawat": row[1], "fusi": row[2],
                         "jumlah_fusi": row[3], "naive_bayes": row[4], "jenis_pesawat": row[5]})

    data = {}
    data["data"] = arrayres
    return jsonify(data)

# ================================================
# route untuk halaman spesifik pesawat


@app.route('/confusionmatrix')
def confusionmatrix():
    conn = mysql.connect()
    cursor = conn.cursor()
    # ambil data karakteristik untuk form select option
    sql = "SELECT * FROM tbl_testing"
    cursor.execute(sql)
    testing = cursor.fetchall()

    sql = "SELECT nama_pesawat, nama_jenis_pesawat, result FROM tbl_testing INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_testing.id_jenis_pesawat"
    cursor.execute(sql)
    gettesting = cursor.fetchall()
    count = 0
    for row in gettesting:
        if row[1] == row[2]:
            count += 1
    try:
        precission = float((count / len(testing)) * 100)
    except ZeroDivisionError:
        precission = 0
    conn.close()
    # lempar data ke file html
    return render_template('confusionmatrix.html', testing=testing, precission=precission)

# fungsi untuk ambil data spesifik pesawat


@app.route('/getTesting')
def getTesting():
    conn = mysql.connect()
    cursor = conn.cursor()
    # sql untuk mengambil data dari database
    sql = "SELECT nama_pesawat, tbl_jenis_pesawat.nama_jenis_pesawat, result FROM tbl_testing INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_testing.id_jenis_pesawat"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:  # dilakukan perulangan untuk dimasukkan kedalam array dan diberi index
        # di input ke variable res
        res.append(
            {"namapesawat": row[0], "jenispesawatreal": row[1], "result": row[2]})

    data = {}
    data["data"] = res  # array res disimpan ke variable data
    return jsonify(data)
