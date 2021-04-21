import csv
import os

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
    sql = "SELECT p.id, nama_pesawat, j.nama_jenis_pesawat, a.spesifik as jenis_sayap, b.spesifik as jenis_penempatan_sayap, d.spesifik as arah_sayap, e.spesifik as jenis_mesin, h.spesifik as badan_pesawat, m.spesifik as persenjataan, n.spesifik as warna, r.name FROM tbl_pesawat as p INNER JOIN tbl_jenis_pesawat as j ON p.id_jenis_pesawat=j.id_jenis_pesawat INNER JOIN tbl_spesifik as a ON a.id_spesifik=p.id_jenis_sayap INNER JOIN tbl_spesifik as b ON b.id_spesifik=p.id_jenis_penempatan_sayap INNER JOIN tbl_spesifik as d ON d.id_spesifik=p.id_arah_sayap INNER JOIN tbl_spesifik as e ON e.id_spesifik=p.id_jenis_mesin INNER JOIN tbl_spesifik as h ON h.id_spesifik=p.id_badan_pesawat INNER JOIN tbl_spesifik as m ON m.id_spesifik=p.id_persenjataan INNER JOIN tbl_spesifik as n ON n.id_spesifik=p.id_warna INNER JOIN tbl_karakteristik as r ON r.id=a.id_karakteristik"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:
        res.append({"id" : row[0], "nama_pesawat" : row[1], "nama_jenis_pesawat" : row[2],
                    "jenis_sayap" : row[3], "jenis_penempatan_sayap" : row[4], "arah_sayap" : row[5],
                    "jenis_mesin" : row[6], "badan_pesawat" : row[7],
                    "persenjataan" : row[8], "warna" : row[9]})

    data = {}
    data["data"] = res
    return jsonify(data)

# ================================================
#permission file upload
ALLOWED_EXTENSION=set(['csv','json','xml'])
app.config['UPLOAD_FOLDER'] = 'app/uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION

# ================================================
# fungsi untuk import dataset
@app.route('/importData', methods=['GET','POST'])
def importData():
    if request.method == 'POST':
        file = request.files['file']

    if 'file' not in request.files:
        return redirect(request.url)

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        ext = str(file.filename)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = mysql.connect()
        cursor = conn.cursor()
        data = []
        if ext.rsplit('.', 1)[1] == 'csv':
            csv_data = csv.reader(open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            csv_data = iter(csv_data)
            next(csv_data, None)
            for row in csv_data:
                print(row)
                t = str(row).strip('[]').strip("'")
                b = t.rsplit(";")
                res = []
                count = len(b)
                print(count)
                for line in b:
                    cek = "SELECT id_spesifik FROM tbl_spesifik WHERE spesifik=%s"
                    text = (line)
                    cursor.execute(cek, text)
                    id_spesifik = cursor.fetchone()
                    if id_spesifik == None:
                        cek = "SELECT id_jenis_pesawat FROM tbl_jenis_pesawat WHERE nama_jenis_pesawat=%s"
                        text = (line)
                        cursor.execute(cek, text)
                        id_spesifik = cursor.fetchone()
                    id_spesifik = str(id_spesifik).replace("(", "").replace(")", "").replace(",", "")
                    count-=1
                    if count == 0:
                        res.append(line)
                    else:
                        res.append(id_spesifik)
                data.append(res)
            for row in data:
                sql = "INSERT INTO tbl_pesawat (nama_pesawat, id_jenis_pesawat, id_jenis_sayap, id_jenis_penempatan_sayap, id_arah_sayap, id_jenis_mesin, id_badan_pesawat, id_persenjataan, id_warna) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                t = (row[9], row[8], row[1], row[2], row[3], row[6], row[4], row[5], row[7])
                cursor.execute(sql, t)
        conn.commit()
        cursor.close()
    return redirect(url_for('dataset'))

# ================================================
#proses perhitungan fusi normalisasi dan naivebayes
@app.route('/processData')
def processData():
    return render_template('process.html')

@app.route('/getpPocessData')
def getProcessData():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT p.id, nama_pesawat, j.nama_jenis_pesawat, a.bit_spesifik as jenis_sayap, b.bit_spesifik as jenis_penempatan_sayap, d.bit_spesifik as arah_sayap, e.bit_spesifik as jenis_mesin, h.bit_spesifik as badan_pesawat, m.bit_spesifik as persenjataan, n.bit_spesifik as warna, r.name FROM tbl_pesawat as p INNER JOIN tbl_jenis_pesawat as j ON p.id_jenis_pesawat=j.id_jenis_pesawat INNER JOIN tbl_spesifik as a ON a.id_spesifik=p.id_jenis_sayap INNER JOIN tbl_spesifik as b ON b.id_spesifik=p.id_jenis_penempatan_sayap INNER JOIN tbl_spesifik as d ON d.id_spesifik=p.id_arah_sayap INNER JOIN tbl_spesifik as e ON e.id_spesifik=p.id_jenis_mesin INNER JOIN tbl_spesifik as h ON h.id_spesifik=p.id_badan_pesawat INNER JOIN tbl_spesifik as m ON m.id_spesifik=p.id_persenjataan INNER JOIN tbl_spesifik as n ON n.id_spesifik=p.id_warna INNER JOIN tbl_karakteristik as r ON r.id=a.id_karakteristik"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:
        res.append({"id": row[0], "nama_pesawat": row[1], "nama_jenis_pesawat": row[2],
                    "jenis_sayap": row[3], "jenis_penempatan_sayap": row[4], "arah_sayap": row[5],
                    "jenis_mesin": row[6], "badan_pesawat": row[7],
                    "persenjataan": row[8], "warna": row[9]})

    data = {}
    data["data"] = res
    return jsonify(data)