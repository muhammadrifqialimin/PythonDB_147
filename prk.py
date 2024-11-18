import sqlite3
from tkinter import Tk, Label, Button, StringVar, Entry, messagebox,ttk

 #fungsi untuk membuat database dan tabel
def create_database() :
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute ('''
               CREATE TABLE IF NOT EXISTS nilai_siswa(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_siswa TEXT,
                biologi INTEGER,
                fisika INTEGER,
                inggris INTEGER,
                prediksi_fakultas TEXT

             )
        ''')
    conn.commit()
    conn.close()
#fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_siswa')
    rows = cursor.fetchall()
    conn.close()
    return rows
#fungsi untuk memperbarui data di datanase
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
                 VALUES (?, ?, ?, ?, ?)
''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

#fingsi untuk menghapus data dari database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''  
        UPDATE nilai_siswa SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ? WHERE id = ?
 ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()
#fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()
#fungsi untuk menghitung prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris :
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris :
        return "Teknik"
    elif inggris > biologi and inggris > fisika :
        return "Bahasa"
    else :
        return "Tidak diketahui"
#fungsi untuk menangani tombol submit
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama :
            raise Exception("Nama Siswa tidak boleh kosong")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)
        messagebox.showinfo("sukses", f"Data berhasil disimpan\nPrediksi_fakultas :{prediksi}")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Nilai tidak valid: {e}")
#fungsi untuk menangani tombol update
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data yang ingin diupdate")
        
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama Siswa tidak boleh kosong")
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("sukses", "data Berhasil Diperbaharui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan : {e}")
#fungsi untuk menangani tombol delete
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data tabel yang ingin dihapus!")
        
        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("sukses", "data Berhasil Dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan : {e}")
#fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")
#fungsi untuk mengisi tabel
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)
#fungsi untuk mengisi input dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")
#inisialisasi database
create_database()
#membuat GUI dengan Tkinter
root = Tk()
root.title("Prediksi Fakultas siswa")
#variabel Tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar() #untuk menyimpan id record yang dipilih

#element GUI
Label(root, text="Nama_Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

#Tabel untuk menampilkan data
columns = ("ID", "Nama_Siswa", "Biologi", "Fisika", "Inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

#menyesuaikan posisi teks di setiap kolom ke tengah
#mengatur posisi isi tabel ke tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

#event untuk memilih data di tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)
#mengisi tabel dengan data
populate_table()
#menjalankan aplikasi
root.mainloop()