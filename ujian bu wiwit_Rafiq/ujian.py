from tkinter import *
from tkinter import messagebox, ttk
import sqlite3

# Koneksi ke database SQLite
conn = sqlite3.connect('library_attendance.db')
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    purpose TEXT NOT NULL)''')
conn.commit()

# Fungsi CRUD
def add_data():
    name = entry_name.get()
    date = entry_date.get()
    purpose = entry_purpose.get()

    if name and date and purpose:
        cursor.execute("INSERT INTO attendance (name, date, purpose) VALUES (?, ?, ?)", (name, date, purpose))
        conn.commit()
        fetch_data()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
    else:
        messagebox.showerror("Error", "Semua field harus diisi!")

def update_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih data yang ingin diubah!")
        return

    item = tree.item(selected_item)
    record_id = item["values"][0]
    name = entry_name.get()
    date = entry_date.get()
    purpose = entry_purpose.get()

    if name and date and purpose:
        cursor.execute("UPDATE attendance SET name = ?, date = ?, purpose = ? WHERE id = ?", (name, date, purpose, record_id))
        conn.commit()
        fetch_data()
        messagebox.showinfo("Sukses", "Data berhasil diubah!")
    else:
        messagebox.showerror("Error", "Semua field harus diisi!")

def delete_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih data yang ingin dihapus!")
        return

    item = tree.item(selected_item)
    record_id = item["values"][0]

    cursor.execute("DELETE FROM attendance WHERE id = ?", (record_id,))
    conn.commit()
    fetch_data()
    messagebox.showinfo("Sukses", "Data berhasil dihapus!")

def search_data():
    name = entry_search.get()
    if name:
        cursor.execute("SELECT * FROM attendance WHERE name LIKE ?", ('%' + name + '%',))
        rows = cursor.fetchall()
        update_treeview(rows)
    else:
        fetch_data()

def fetch_data():
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    update_treeview(rows)

def update_treeview(rows):
    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        tag = 'odd' if i % 2 == 0 else 'even'
        tree.insert("", "end", values=row, tags=(tag,))

# GUI utama
root = Tk()
root.title("Aplikasi Daftar Hadir Perpustakaan")
root.state('zoomed')

# Styling Treeview untuk Dark Mode
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E")
style.map("Treeview", background=[("selected", "#4caf50")])
style.configure("Treeview.Heading", background="#424242", foreground="white", font=("Arial", 12))

# Frame utama
frame_main = Frame(root, bg="#2E2E2E")
frame_main.pack(fill="both", expand=True, padx=20, pady=20)

# Frame Input
frame_input = Frame(frame_main, bg="#424242", pady=10)
frame_input.pack(fill="x", pady=5)

Label(frame_input, text="Nama:", bg="#424242", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky=W)
entry_name = Entry(frame_input, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=10, pady=5)

Label(frame_input, text="Tanggal:", bg="#424242", fg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky=W)
entry_date = Entry(frame_input, font=("Arial", 12))
entry_date.grid(row=1, column=1, padx=10, pady=5)

Label(frame_input, text="Keperluan:", bg="#424242", fg="white", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky=W)
entry_purpose = Entry(frame_input, font=("Arial", 12))
entry_purpose.grid(row=2, column=1, padx=10, pady=5)

# Frame Tombol
frame_buttons = Frame(frame_main, bg="#2E2E2E", pady=10)
frame_buttons.pack(fill="x", pady=5)

Button(frame_buttons, text="Tambah Data", command=add_data, bg="#4caf50", fg="white", font=("Arial", 12), width=15).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Ubah Data", command=update_data, bg="#2196f3", fg="white", font=("Arial", 12), width=15).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Hapus Data", command=delete_data, bg="#f44336", fg="white", font=("Arial", 12), width=15).pack(side=LEFT, padx=10)

# Frame Pencarian
frame_search = Frame(frame_main, bg="#2E2E2E", pady=10)
frame_search.pack(fill="x", pady=5)

Label(frame_search, text="Cari Nama:", bg="#2E2E2E", fg="white", font=("Arial", 12)).pack(side=LEFT, padx=10)
entry_search = Entry(frame_search, font=("Arial", 12), width=30)
entry_search.pack(side=LEFT, padx=10)
Button(frame_search, text="Cari", command=search_data, bg="#ff9800", fg="white", font=("Arial", 12)).pack(side=LEFT, padx=10)

# Frame Tabel Data
frame_table = Frame(frame_main, bg="#2E2E2E")
frame_table.pack(fill="both", expand=True, pady=5)

tree = ttk.Treeview(frame_table, columns=("ID", "Nama", "Tanggal", "Keperluan"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama")
tree.heading("Tanggal", text="Tanggal")
tree.heading("Keperluan", text="Keperluan")

tree.column("ID", width=50, anchor=CENTER)
tree.column("Nama", width=200)
tree.column("Tanggal", width=150, anchor=CENTER)
tree.column("Keperluan", width=200)

tree.tag_configure('odd', background="#333333", foreground="white")
tree.tag_configure('even', background="#424242", foreground="white")
tree.pack(fill="both", expand=True)

# Load data awal
fetch_data()

# Jalankan aplikasi
root.mainloop()
