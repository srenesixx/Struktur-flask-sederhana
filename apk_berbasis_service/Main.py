from flask import Flask, request, jsonify, render_template, redirect, url_for
from sqlalchemy.orm import Session
from config import engine, SessionLocal, Base
from models import Mahasiswa
import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# Buat tabel jika belum ada
Base.metadata.create_all(bind=engine)

# -------------------------------
# 🌸 ROUTES SERVICE
# -------------------------------

@app.route('/get', methods=['GET'])
def get_data():
    db = SessionLocal()
    data = db.query(Mahasiswa).all()
    db.close()

    result = [
        {
            "nim": m.nim,
            "nama": m.nama,
            "tahun_masuk": m.tahun_masuk,
            "alamat": m.alamat,
            "tanggal_lahir": m.tanggal_lahir.strftime("%Y-%m-%d") if m.tanggal_lahir else None
        }
        for m in data
    ]
    return jsonify(result)


@app.route('/post', methods=['POST'])
def post_data():
    db = SessionLocal()
    data = request.get_json()

    try:
        new_mhs = Mahasiswa(
            nim=data['nim'],
            nama=data['nama'],
            tahun_masuk=data['tahun_masuk'],
            alamat=data.get('alamat', ''),
            tanggal_lahir=datetime.datetime.strptime(data['tanggal_lahir'], "%Y-%m-%d").date()
        )
        db.add(new_mhs)
        db.commit()
        message = {"message": "Data mahasiswa berhasil ditambahkan!"}
    except Exception as e:
        db.rollback()
        message = {"error": str(e)}
    finally:
        db.close()

    return jsonify(message)


@app.route('/detail/<string:nim>', methods=['GET'])
def detail_mahasiswa(nim):
    db = SessionLocal()
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    db.close()

    if not mahasiswa:
        return "Mahasiswa tidak ditemukan", 404

    return render_template("detail.html", mahasiswa=mahasiswa)


@app.route('/delete/<string:nim>', methods=['DELETE'])
def delete_mahasiswa(nim):
    db = SessionLocal()
    m = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()

    if not m:
        db.close()
        return jsonify({"message": "Mahasiswa tidak ditemukan"}), 404

    db.delete(m)
    db.commit()
    db.close()

    return jsonify({"message": "Data berhasil dihapus!"})


# -------------------------------
# 🌸 ROUTES GUI
# -------------------------------
@app.route('/')
def index():
    db = SessionLocal()
    mahasiswa_list = db.query(Mahasiswa).all()
    db.close()
    return render_template('index.html', mahasiswa_list=mahasiswa_list)


@app.route('/form', methods=['GET', 'POST'])
def add_mahasiswa():
    if request.method == 'POST':
        db = SessionLocal()
        nim = request.form['nim']
        nama = request.form['nama']
        tahun_masuk = request.form['tahun_masuk']
        alamat = request.form['alamat']
        tanggal_lahir = datetime.datetime.strptime(request.form['tanggal_lahir'], "%Y-%m-%d").date()

        new_mhs = Mahasiswa(
            nim=nim,
            nama=nama,
            tahun_masuk=tahun_masuk,
            alamat=alamat,
            tanggal_lahir=tanggal_lahir
        )
        db.add(new_mhs)
        db.commit()
        db.close()
        return redirect(url_for('index'))
    return render_template('form.html')


@app.route('/detail/view/<string:nim>')
def detail_view(nim):
    db = SessionLocal()
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    db.close()
    return render_template('detail.html', mahasiswa=mahasiswa)


@app.route('/delete/view/<string:nim>')
def delete_view(nim):
    db = SessionLocal()
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    if mahasiswa:
        db.delete(mahasiswa)
        db.commit()
    db.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
