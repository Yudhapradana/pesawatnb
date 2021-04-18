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

#route untuk halaman login
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        cek = cek_login(username, password)
        print(cek)
        if cek:
            session['logged_in'] = True
            session['username'] = username
            session['name'] = str(cek[0][1])
            return redirect(url_for('index'))
        else:
            error = "Ada Kesalahan. Coba Lagi!"
    return render_template('login.html', error=error)

def cek_login(username, password):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_user WHERE username=%s AND password=md5(%s)"
    t = (username, password)
    cursor.execute(sql, t)
    result = cursor.fetchall()
    conn.close
    return result

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    msg = "Anda Berhasil Log Out!"
    return render_template('login.html', msg=msg)

# ================================================
# route untuk halaman dashboard
@app.route('/index')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Jenis Sayap'"
    cursor.execute(sql)
    jenis = cursor.fetchall()

    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Penempatan Sayap'"
    cursor.execute(sql)
    letak = cursor.fetchall()

    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Badan Pesawat'"
    cursor.execute(sql)
    badan = cursor.fetchall()

    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Arah Sayap'"
    cursor.execute(sql)
    arah = cursor.fetchall()

    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Persenjataan'"
    cursor.execute(sql)
    persenjataan = cursor.fetchall()

    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Jenis Mesin'"
    cursor.execute(sql)
    mesin = cursor.fetchall()

    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Warna'"
    cursor.execute(sql)
    warna = cursor.fetchall()

    sql = "SELECT tbl_spesifik.id_spesifik, tbl_spesifik.spesifik FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE tbl_karakteristik.name='Bentuk Ekor Pesawat'"
    cursor.execute(sql)
    ekor = cursor.fetchall()

    conn.close()
    return render_template('index.html', jenis=jenis, letak=letak, arah=arah, badan=badan, persenjataan=persenjataan, mesin=mesin, warna=warna, ekor=ekor)

# ================================================
#route untuk halaman jenis pesawat
@app.route('/jenis')
def jenis():
    return render_template('jenis.html')

#fungsi untuk ambil data jenis pesawat
@app.route('/getJenis')
def getJenis():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_jenis_pesawat"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:
        res.append({"id" : row[0], "jenis" : row[1]})

    data = {}
    data["data"] = res
    return jsonify(data)

# ================================================
#route untuk halaman karakter pesawat
@app.route('/karakter')
def karakter():
    return render_template('karakter.html')

#fungsi untuk ambil data karakter pesawat
@app.route('/getKarakter')
def getKarakter():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_karakter_pesawat"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:
        res.append({"id" : row[0], "name" : row[1]})

    data = {}
    data["data"] = res
    return jsonify(data)

# ================================================
#route untuk halaman karakteristik pesawat
@app.route('/karakteristik')
def karakteristik():
    return render_template('karakteristik.html')

#fungsi untuk ambil data karakteristik pesawat
@app.route('/getKarakteristik')
def getKarakteristik():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_karakteristik"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:
        res.append({"id" : row[0], "name" : row[1]})

    data = {}
    data["data"] = res
    return jsonify(data)

# ================================================
#route untuk halaman spesifik pesawat
@app.route('/spesifik')
def spesifik():
    return render_template('spesifik.html')

#fungsi untuk ambil data spesifik pesawat
@app.route('/getSpesifik')
def getSpesifik():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT s.id_spesifik, k.name, s.kode_spesifik, s.spesifik, s.bit_spesifik FROM tbl_spesifik as s INNER JOIN tbl_karakteristik as k ON k.id=s.id_karakteristik"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:
        res.append({"id" : row[0], "name_karakteristik" : row[1], "kode_spesifik" : row[2], "spesifik" : row[3], "bit_spesifik" : row[4]})

    data = {}
    data["data"] = res
    return jsonify(data)

# ================================================
#route untuk halaman dataset
@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

#fungsi untuk ambil data dataset pesawat
@app.route('/getDataset')
def getDataset():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT p.id, nama_pesawat, j.nama_jenis_pesawat, k.nama_karakter_pesawat, a.spesifik as jenis_sayap, b.spesifik as jenis_penempatan_sayap, c.spesifik as jumlah_sayap, d.spesifik as arah_sayap, e.spesifik as jenis_mesin, f.spesifik as jumlah_mesin, g.spesifik as posisi_mesin, h.spesifik as badan_pesawat, i.spesifik as jenis_ekor, l.spesifik as jenis_landing_gear, m.spesifik as persenjataan, n.spesifik as warna, r.name FROM tbl_pesawat as p INNER JOIN tbl_jenis_pesawat as j ON p.id_jenis_pesawat=j.id_jenis_pesawat INNER JOIN tbl_karakter_pesawat as k ON k.id_karakter_pesawat=p.id_karakter_pesawat INNER JOIN tbl_spesifik as a ON a.id_spesifik=p.id_jenis_sayap INNER JOIN tbl_spesifik as b ON b.id_spesifik=p.id_jenis_penempatan_sayap INNER JOIN tbl_spesifik as c ON c.id_spesifik=p.id_jumlah_sayap INNER JOIN tbl_spesifik as d ON d.id_spesifik=p.id_arah_sayap INNER JOIN tbl_spesifik as e ON e.id_spesifik=p.id_jenis_mesin INNER JOIN tbl_spesifik as f ON f.id_spesifik=p.id_jumlah_mesin INNER JOIN tbl_spesifik as g ON g.id_spesifik=p.id_posisi_mesin INNER JOIN tbl_spesifik as h ON h.id_spesifik=p.id_badan_pesawat INNER JOIN tbl_spesifik as i ON i.id_spesifik=p.id_jenis_ekor INNER JOIN tbl_spesifik as l ON l.id_spesifik=p.id_jenis_landing_gear INNER JOIN tbl_spesifik as m ON m.id_spesifik=p.id_persenjataan INNER JOIN tbl_spesifik as n ON n.id_spesifik=p.id_warna INNER JOIN tbl_karakteristik as r ON r.id=a.id_karakteristik"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:
        res.append({"id" : row[0], "nama_pesawat" : row[1], "nama_jenis_pesawat" : row[2], "nama_karakter_pesawat" : row[3],
                    "jenis_sayap" : row[4], "jenis_penempatan_sayap" : row[5], "jumlah_sayap" : row[6], "arah_sayap" : row[7],
                    "jenis_mesin" : row[8], "jumlah_mesin" : row[9], "posisi_mesin" : row[10], "badan_pesawat" : row[11],
                    "jenis_ekor" : row[12], "jenis_landing_gear" : row[13], "persenjataan" : row[14], "warna" : row[15], "name_karakteristik" : row[16],})

    data = {}
    data["data"] = res
    return jsonify(data)