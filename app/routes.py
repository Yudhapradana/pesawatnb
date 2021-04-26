import csv, os, pandas as pd
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

@app.route('/insertJenis', methods=["POST"])
def insertJenis():
    name = request.form['jenis_pesawat']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO tbl_jenis_pesawat (nama_jenis_pesawat) VALUES (%s)"
    t = (name)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('jenis'))

@app.route('/updateJenis', methods=["POST"])
def updateJenis():
    jenis = request.form['ujenis_pesawat']
    id = request.form['uid']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "UPDATE tbl_jenis_pesawat SET nama_jenis_pesawat=%s WHERE id_jenis_pesawat=%s"
    t = (jenis, id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('jenis'))

@app.route('/deleteJenis', methods=["POST"])
def deleteJenis():
    id = request.form['did']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "DELETE FROM tbl_jenis_pesawat WHERE id_jenis_pesawat=%s"
    t = (id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('jenis'))
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

@app.route('/insertKarakteristik', methods=["POST"])
def insertKarakteristik():
    name = request.form['name']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO tbl_karakteristik(name) VALUES (%s)"
    t = (name)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('karakteristik'))

@app.route('/updateKarakteristik', methods=["POST"])
def updateKarakteristik():
    name = request.form['uname']
    id = request.form['uid']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "UPDATE tbl_karakteristik SET name=%s WHERE id=%s"
    t = (name, id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('karakteristik'))

@app.route('/deleteKarakteristik', methods=["POST"])
def deleteKarakteristik():
    id = request.form['did']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "DELETE FROM tbl_karakteristik WHERE id=%s"
    t = (id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('karakteristik'))
# ================================================
#route untuk halaman spesifik pesawat
@app.route('/spesifik')
def spesifik():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM tbl_karakteristik"
    cursor.execute(sql)
    karakteristik = cursor.fetchall()
    conn.close()
    return render_template('spesifik.html', karakteristik=karakteristik)

#fungsi untuk ambil data spesifik pesawat
@app.route('/getSpesifik')
def getSpesifik():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT s.id_spesifik, k.name, s.kode_spesifik, s.spesifik, s.bit_spesifik, s.id_karakteristik FROM tbl_spesifik as s INNER JOIN tbl_karakteristik as k ON k.id=s.id_karakteristik"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    res = []
    for row in result:
        res.append({"id" : row[0], "name_karakteristik" : row[1], "kode_spesifik" : row[2], "spesifik" : row[3], "bit_spesifik" : row[4], "id_karakteristik" : row[5]})

    data = {}
    data["data"] = res
    return jsonify(data)

@app.route('/insertSpesifik', methods=["POST"])
def insertSpesifik():
    karakteristik = request.form['karakteristik']
    kode = request.form['kode_spesifik']
    spesifik = request.form['spesifik']
    bit = request.form['bit_spesifik']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO tbl_spesifik(id_karakteristik, kode_spesifik, spesifik, bit_spesifik) VALUES (%s, %s, %s, %s)"
    t = (karakteristik, kode, spesifik, bit)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('spesifik'))

@app.route('/updateSpesifik', methods=["POST"])
def updateSpesifik():
    id = request.form['uid']
    karakteristik = request.form['ukarakteristik']
    kode = request.form['ukode_spesifik']
    spesifik = request.form['uspesifik']
    bit = request.form['ubit_spesifik']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "UPDATE tbl_spesifik SET id_karakteristik=%s, kode_spesifik=%s, spesifik=%s, bit_spesifik=%s WHERE id_spesifik=%s"
    t = (karakteristik, kode, spesifik, bit, id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('spesifik'))

@app.route('/deleteSpesifik', methods=["POST"])
def deleteSpesifik():
    id = request.form['did']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "DELETE FROM tbl_spesifik WHERE id_spesifik=%s"
    t = (id)
    cursor.execute(sql, t)
    conn.commit()
    return redirect(url_for('spesifik'))

# ================================================
#route untuk halaman dataset
@app.route('/dataset')
def dataset():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM tbl_jenis_pesawat"
    cursor.execute(sql)
    jenis = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Jenis Sayap'"
    cursor.execute(sql)
    js = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Penempatan Sayap'"
    cursor.execute(sql)
    jp = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Arah Sayap'"
    cursor.execute(sql)
    rs = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Jenis Mesin'"
    cursor.execute(sql)
    jm = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Badan Pesawat'"
    cursor.execute(sql)
    bp = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Persenjataan'"
    cursor.execute(sql)
    ps = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Warna'"
    cursor.execute(sql)
    wn = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Posisi Mesin'"
    cursor.execute(sql)
    pm = cursor.fetchall()

    sql = "SELECT * FROM tbl_spesifik INNER JOIN tbl_karakteristik ON tbl_karakteristik.id=tbl_spesifik.id_karakteristik WHERE name='Bentuk Ekor Pesawat'"
    cursor.execute(sql)
    je = cursor.fetchall()

    conn.close()
    return render_template('dataset.html', jenis=jenis, js=js, jp=jp, rs=rs, jm=jm, bp=bp, ps=ps, wn=wn, pm=pm, je=je)

#fungsi untuk ambil data dataset pesawat
@app.route('/getDataset')
def getDataset():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT p.id, nama_pesawat, j.nama_jenis_pesawat, a.spesifik as jenis_sayap, b.spesifik as jenis_penempatan_sayap, " \
          "d.spesifik as arah_sayap, e.spesifik as jenis_mesin, h.spesifik as badan_pesawat, m.spesifik as persenjataan, " \
          "n.spesifik as warna, o.spesifik as posisi_mesin, q.spesifik as jenis_ekor, j.id_jenis_pesawat, a.id_spesifik as id_jenis_sayap, " \
          "b.id_spesifik as id_jenis_penempatan_sayap, d.id_spesifik as id_arah_sayap, e.id_spesifik as id_jenis_mesin, h.id_spesifik as id_badan_pesawat, m.id_spesifik as id_persenjataan, " \
          "n.id_spesifik as id_warna, o.id_spesifik as id_posisi_mesin, q.id_spesifik as id_jenis_ekor FROM tbl_pesawat as p INNER JOIN tbl_jenis_pesawat as j ON p.id_jenis_pesawat=j.id_jenis_pesawat " \
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
    print(result)
    conn.close()
    res = []
    for row in result:
        res.append({"id" : row[0], "nama_pesawat" : row[1], "nama_jenis_pesawat" : row[2],
                    "jenis_sayap" : row[3], "jenis_penempatan_sayap" : row[4], "arah_sayap" : row[5],
                    "jenis_mesin" : row[6], "badan_pesawat" : row[7],
                    "persenjataan" : row[8], "warna" : row[9], "posisi_mesin" : row[10], "jenis_ekor" : row[11],
                    "id_jenis_pesawat" : row[12], 'id_jenis_sayap' : row[13], 'id_penempatan_sayap': row[14],
                    "id_arah_sayap" : row[15], "id_jenis_mesin" : row[16], "id_badan_pesawat" : row[17],
                    "id_persenjataan" : row[18], "id_warna" : row[19], "id_posisi_mesin" : row[20], "id_jenis_ekor" : row[21]})

    data = {}
    data["data"] = res
    return jsonify(data)

# ================================================
#permission file upload
ALLOWED_EXTENSION=set(['csv','json','xml', 'xlsx'])
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
                t = str(row).strip('[]').strip("'")
                b = t.rsplit(";")
                res = []
                count = len(b)
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

        if ext.rsplit('.', 1)[1] == 'xlsx':
            df = pd.read_excel(app.config['UPLOAD_FOLDER']+'/'+filename)
            for index, row in df.iterrows():
                res = []
                count = len(row)
                for line in row:
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
                    count -= 1
                    if count == 0:
                        res.append(line)
                    else:
                        res.append(id_spesifik)
                data.append(res)
        print(data)
        for row in data:
            sql = "INSERT INTO tbl_pesawat (nama_pesawat, id_jenis_pesawat, id_jenis_sayap, id_jenis_penempatan_sayap, id_arah_sayap, id_jenis_mesin, id_badan_pesawat, id_persenjataan, id_warna, id_posisi_mesin, id_jenis_ekor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            t = (row[11], row[10], row[1], row[2], row[3], row[4], row[6], row[8], row[9], row[5], row[7])
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
    t = (nama_pesawat, jenis_pesawat, jenis_sayap ,penempatan_sayap, arah_sayap, jenis_mesin, badan_pesawat, persenjataan, warna, posisi_mesin, jenis_ekor)
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
    t = (nama_pesawat, jenis_pesawat, jenis_sayap, penempatan_sayap, arah_sayap, jenis_mesin, badan_pesawat, persenjataan,warna, posisi_mesin, jenis_ekor, id)
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
#proses perhitungan fusi normalisasi dan naivebayes
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
    sql = "SELECT tbl_process.id_pesawat, tbl_jenis_pesawat.nama_jenis_pesawat, tbl_process.fusi_informasi, tbl_process.jumlah_fusi, tbl_process.naive_bayes " \
          "FROM tbl_process INNER JOIN tbl_pesawat ON tbl_pesawat.id=tbl_process.id_pesawat " \
          "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat"
    cursor.execute(sql)
    tblprocess = cursor.fetchall()
    sql = "SELECT * FROM tbl_pesawat"
    cursor.execute(sql)
    tblpesawat = cursor.fetchall()
    arrayres = []
    if len(tblprocess) != len(tblpesawat):
        sql = "SELECT p.id, nama_pesawat, j.nama_jenis_pesawat, a.bit_spesifik as jenis_sayap, b.bit_spesifik as jenis_penempatan_sayap, " \
              "d.bit_spesifik as arah_sayap, e.bit_spesifik as jenis_mesin, h.bit_spesifik as badan_pesawat, m.bit_spesifik as persenjataan, " \
              "n.bit_spesifik as warna, r.name FROM tbl_pesawat as p INNER JOIN tbl_jenis_pesawat as j ON p.id_jenis_pesawat=j.id_jenis_pesawat " \
              "INNER JOIN tbl_spesifik as a ON a.id_spesifik=p.id_jenis_sayap INNER JOIN tbl_spesifik as b ON b.id_spesifik=p.id_jenis_penempatan_sayap " \
              "INNER JOIN tbl_spesifik as d ON d.id_spesifik=p.id_arah_sayap INNER JOIN tbl_spesifik as e ON e.id_spesifik=p.id_jenis_mesin " \
              "INNER JOIN tbl_spesifik as h ON h.id_spesifik=p.id_badan_pesawat INNER JOIN tbl_spesifik as m ON m.id_spesifik=p.id_persenjataan " \
              "INNER JOIN tbl_spesifik as n ON n.id_spesifik=p.id_warna INNER JOIN tbl_karakteristik as r ON r.id=a.id_karakteristik"
        cursor.execute(sql)
        result = cursor.fetchall()
        res = []
        for row in result:
            count = len(row[3])
            a = xor(row[3], row[4], count)
            a = xor(a, row[5], count)
            a = xor(a, row[6], count)
            a = xor(a, row[7], count)
            a = xor(a, row[8], count)
            a = xor(a, row[9], count)
            res.append((row[0], row[2], a))
        listfusi = []
        for row in res:
            if row[2] not in listfusi:
                listfusi.append(row[2])
        dictset = dict.fromkeys(listfusi, 0)
        for row in res:
            if row[2] in dictset:
                dictset[row[2]] +=1
        dataarray = []
        for row in res:
            id = row[0]
            jenispesawat = row[1]
            fusi = row[2]
            for datafusi, val in dictset.items():
                if fusi == datafusi:
                    countfusi = val
            dataarray.append((id, jenispesawat, fusi, countfusi))
        sql = "SELECT tbl_jenis_pesawat.nama_jenis_pesawat, COUNT(tbl_pesawat.id_jenis_pesawat) FROM `tbl_pesawat` " \
              "INNER JOIN tbl_jenis_pesawat ON tbl_jenis_pesawat.id_jenis_pesawat=tbl_pesawat.id_jenis_pesawat GROUP BY tbl_pesawat.id_jenis_pesawat"
        cursor.execute(sql)
        countjenis = cursor.fetchall()
        for row in dataarray:
            for jenis in countjenis:
                if row[1] == jenis[0]:
                    nb = float(row[3]/jenis[1])
            arrayres.append({"id_pesawat" : row[0], "nama_pesawat" : row[1], "fusi" : row[2], "jumlah_fusi" : row[3], "naive_bayes" : nb})
            sql = "INSERT INTO tbl_process(id_pesawat, fusi_informasi, jumlah_fusi, naive_bayes) VALUES(%s, %s, %s, %s)"
            t = (row[0], row[2], row[3], nb)
            cursor.execute(sql, t)
            conn.commit()
    for row in tblprocess:
        arrayres.append({"id_pesawat": row[0], "nama_pesawat": row[1], "fusi": row[2], "jumlah_fusi": row[3], "naive_bayes": row[4]})

    data = {}
    data["data"] = arrayres
    return jsonify(data)