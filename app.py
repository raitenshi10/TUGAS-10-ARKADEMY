from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'arkademy'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM produk")
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Berhasil Dimasukan")
        namaProduk = request.form['nama_produk']
        keterangan = request.form['keterangan']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO produk (nama_produk, keterangan, harga, jumlah) VALUES (%s, %s, %s, %s)", (namaProduk, keterangan, harga, jumlah))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM produk WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        namaProduk = request.form['nama_produk']
        keterangan = request.form['keterangan']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE produk
               SET nama_produk=%s, keterangan=%s, harga=%s, jumlah=%s
               WHERE id=%s
            """, (namaProduk, keterangan, harga, jumlah, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))



if __name__ == "__main__":
    app.run(debug=True)
