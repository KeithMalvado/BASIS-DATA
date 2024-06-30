import psycopg2
from tabulate import tabulate
import time, os

def connect():
    conn = psycopg2.connect(
        host='localhost',
        database='masjid',
        user='postgres',
        password='ipan',
        port=5432
    )
    return conn
# ======================================================================== Pemanis ================================================================================

    
def loading():
    print('\033[32m')
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║ Loading ..............                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    time.sleep(1)
    os.system("cls")


# =========================================================================View=====================================================================================

def add_kegiatan():
    while True:
        nama_kegiatan = input("Masukkan nama kegiatan: ")
        penanggung_jawab = input("Masukkan nama penanggung jawab: ")
        proposal = input("Masukkan nama file proposal: ")
        tanggal_kegiatan = input("Masukkan tanggal kegiatan (YYYY-MM-DD): ")
        status = input("Masukkan status kegiatan: ")
        
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO daftar_kegiatan (nama_kegiatan, penanggung_jawab, proposal, tanggal_kegiatan, status) VALUES (%s, %s, %s, %s, %s)",
                        (nama_kegiatan, penanggung_jawab, proposal, tanggal_kegiatan, status))
            conn.commit()
            print("Data kegiatan berhasil ditambahkan.")
            break
        except psycopg2.Error as e:
            print("Gagal menambahkan data kegiatan:", e)
        finally:
            cur.close()
            conn.close()

def view_kegiatan():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM daftar_kegiatan")
        rows = cur.fetchall()
        headers = ["ID", "Nama Kegiatan", "Penanggung Jawab", "Proposal", "Tanggal Kegiatan", "Status"]
        print(tabulate(rows, headers, tablefmt="orgtbl"))
    except psycopg2.Error as e:
        print("Gagal membaca data kegiatan:", e)
    finally:
        cur.close()
        conn.close()

def update_kegiatan():
    while True:
        view_kegiatan()
        id_kegiatan = int(input("Masukkan ID kegiatan yang ingin diperbarui: "))
        nama_kegiatan = input("Masukkan nama kegiatan baru: ")
        penanggung_jawab = input("Masukkan nama penanggung jawab baru: ")
        proposal = input("Masukkan nama file proposal baru: ")
        tanggal_kegiatan = input("Masukkan tanggal kegiatan baru (YYYY-MM-DD): ")
        status = input("Masukkan status kegiatan baru: ")
        
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE daftar_kegiatan SET nama_kegiatan=%s, penanggung_jawab=%s, proposal=%s, tanggal_kegiatan=%s, status=%s WHERE id_kegiatan=%s",
                        (nama_kegiatan, penanggung_jawab, proposal, tanggal_kegiatan, status, id_kegiatan))
            conn.commit()
            print("Data kegiatan berhasil diperbarui.")
            break
        except psycopg2.Error as e:
            print("Gagal memperbarui data kegiatan:", e)
        finally:
            cur.close()
            conn.close()

def delete_kegiatan():
    while True:
        view_kegiatan()
        id_kegiatan = int(input("Masukkan ID kegiatan yang ingin dihapus: "))
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM daftar_kegiatan WHERE id_kegiatan=%s", (id_kegiatan,))
            conn.commit()
            print("Data kegiatan berhasil dihapus.")
            break
        except psycopg2.Error as e:
            print("Gagal menghapus data kegiatan:", e)
        finally:
            cur.close()
            conn.close()

#  ================================================================================================== INVENTARIS ================================================

def view_inventaris():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM inventaris")
        rows = cur.fetchall()
        headers = ["ID", "Nama Inventaris", "Jumlah", "Kategori", "Kondisi"]
        print(tabulate(rows, headers, tablefmt="orgtbl"))
    except psycopg2.Error as e:
        print("Gagal membaca data inventaris:", e)
    finally:
        cur.close()
        conn.close()

def add_inventaris():
    while True:
        nama_inventaris = input("Masukkan nama inventaris: ")
        jumlah = int(input("Masukkan jumlah inventaris: "))
        kategori = input("Masukkan kategori inventaris: ")
        kondisi = input("Masukkan kondisi inventaris: ")
        
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO inventaris (nama_inventaris, jumlah, kategori, kondisi) VALUES (%s, %s, %s, %s)",
                        (nama_inventaris, jumlah, kategori, kondisi))
            conn.commit()
            print("Data inventaris berhasil ditambahkan.")
            break
        except psycopg2.Error as e:
            print("Gagal menambahkan data inventaris:", e)
        finally:
            cur.close()
            conn.close()

def update_inventaris():
    while True:
        view_inventaris()
        id_inventaris = int(input("Masukkan ID inventaris yang ingin diperbarui: "))
        nama_inventaris = input("Masukkan nama inventaris baru: ")
        jumlah = int(input("Masukkan jumlah inventaris baru: "))
        kategori = input("Masukkan kategori inventaris baru: ")
        kondisi = input("Masukkan kondisi inventaris baru: ")
        
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE inventaris SET nama_inventaris=%s, jumlah=%s, kategori=%s, kondisi=%s WHERE id_inventaris=%s",
                        (nama_inventaris, jumlah, kategori, kondisi, id_inventaris))
            conn.commit()
            print("Data inventaris berhasil diperbarui.")
            break
        except psycopg2.Error as e:
            print("Gagal memperbarui data inventaris:", e)
        finally:
            cur.close()
            conn.close()

def delete_inventaris():
    while True:
        view_inventaris()
        id_inventaris = int(input("Masukkan ID inventaris yang ingin dihapus: "))
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM inventaris WHERE id_inventaris=%s", (id_inventaris,))
            conn.commit()
            print("Data inventaris berhasil dihapus.")
            break
        except psycopg2.Error as e:
            print("Gagal menghapus data inventaris:", e)
        finally:
            cur.close()
            conn.close()

# ================================================================================= ADMIN ===============================================================================================

def add_admin():
        view_admin()
        nama_takmir = input("Masukkan nama admin: ")
        email_takmir = input("Masukkan nama_admin admin: ")
        sandi_takmir = input("Masukkan password admin: ")
        loading()
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO admin (nama_takmir, email_takmir, sandi_takmir) VALUES (%s, %s, %s)",
                        (nama_takmir, email_takmir, sandi_takmir))
            conn.commit()
            print("Data admin berhasil ditambahkan.")
        except psycopg2.Error as e:
            print("Gagal menambahkan data admin:", e)
        finally:
            cur.close()
            conn.close()
            
def view_admin():
    loading()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM admin")
        rows = cur.fetchall()
        if rows:
            headers = ["Nama Takmir", "Email Takmir", "Password"]
            print(tabulate(rows, headers, tablefmt="orgtbl"))
        else:
            print("Tidak ada data admin yang tersedia.")
    except psycopg2.Error:
        print("Gagal membaca data admin. Mohon coba lagi.")
    finally:
        cur.close()
        conn.close()


def update_admin():
    while True:
        view_admin()
        nama_takmir = input("Masukkan nama_admin baru: ")
        email_takmir = input("Masukkan email baru: ")
        sandi_takmir = input("Masukkan sandi: ")
        
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE admin SET nama_takmir=%s, email_takmir=%s, sandi_takmir=%s",
                        (nama_takmir, email_takmir, sandi_takmir))
            conn.commit()
            print("Data user berhasil diperbarui.")
            break
        except psycopg2.Error as e:
            print("Gagal memperbarui data user:", e)
        finally:
            cur.close()
            conn.close()

def delete_admin():
    while True:
        view_admin()
        id_user = int(input("Masukkan ID user yang ingin dihapus: "))
        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM daftar_user WHERE id_user=%s", (id_user,))
            conn.commit()
            print("Data user berhasil dihapus.")
            break
        except psycopg2.Error as e:
            print("Gagal menghapus data user:", e)
        finally:
            cur.close()
            conn.close()

# ===================================================================================== JADWAL ===============================================================================================

def add_jadwal_muadin():
    nama_muadin = input("Masukkan nama muadzin: ")
    tanggal = input("Masukkan tanggal (YYYY-MM-DD): ")
    waktu_shubuh = input("Masukkan waktu Shubuh: ")
    imam_shubuh = input("Masukkan nama Imam Shubuh: ")
    waktu_dzuhur = input("Masukkan waktu Dzuhur: ")
    imam_dzuhur = input("Masukkan nama Imam Dzuhur: ")
    waktu_ashar = input("Masukkan waktu Ashar: ")
    imam_ashar = input("Masukkan nama Imam Ashar: ")
    waktu_magrib = input("Masukkan waktu Magrib: ")
    imam_magrib = input("Masukkan nama Imam Magrib: ")
    waktu_isya = input("Masukkan waktu Isya: ")
    imam_isya = input("Masukkan nama Imam Isya: ")

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO jadwal_muadin (nama_muadin, tanggal, waktu_shubuh, imam_shubuh, waktu_dzuhur, imam_dzuhur, waktu_ashar, imam_ashar, waktu_magrib, imam_magrib, waktu_isya, imam_isya) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (nama_muadin, tanggal, waktu_shubuh, imam_shubuh, waktu_dzuhur, imam_dzuhur, waktu_ashar, imam_ashar, waktu_magrib, imam_magrib, waktu_isya, imam_isya))
        conn.commit()
        print("Data jadwal muadin berhasil ditambahkan.")
    except psycopg2.Error as e:
        print("Gagal menambahkan data jadwal muadin:", e)
    finally:
        cur.close()
        conn.close()


def view_jadwal_muadin():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM jadwal_muadin")
        rows = cur.fetchall()
        headers = ["ID", "Nama Muadzin", "Tanggal", "Waktu Shubuh", "Imam Shubuh", "Waktu Dzuhur", "Imam Dzuhur", "Waktu Ashar", "Imam Ashar", "Waktu Magrib", "Imam Magrib", "Waktu Isya", "Imam Isya"]
        print(tabulate(rows, headers, tablefmt="orgtbl"))
    except psycopg2.Error as e:
        print("Gagal membaca data jadwal muadin:", e)
    finally:
        cur.close()
        conn.close()
        
def update_jadwal_muadin():
    view_jadwal_muadin()
    id_muadin = int(input("Masukkan ID jadwal muadin yang ingin diperbarui: "))
    nama_muadin = input("Masukkan nama muadzin baru: ")
    tanggal = input("Masukkan tanggal baru (YYYY-MM-DD): ")
    waktu_shubuh = input("Masukkan waktu Shubuh baru: ")
    imam_shubuh = input("Masukkan nama Imam Shubuh baru: ")
    waktu_dzuhur = input("Masukkan waktu Dzuhur baru: ")
    imam_dzuhur = input("Masukkan nama Imam Dzuhur baru: ")
    waktu_ashar = input("Masukkan waktu Ashar baru: ")
    imam_ashar = input("Masukkan nama Imam Ashar baru: ")
    waktu_magrib = input("Masukkan waktu Magrib baru: ")
    imam_magrib = input("Masukkan nama Imam Magrib baru: ")
    waktu_isya = input("Masukkan waktu Isya baru: ")
    imam_isya = input("Masukkan nama Imam Isya baru: ")
    
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE jadwal_muadin SET nama_muadin=%s, tanggal=%s, waktu_shubuh=%s, imam_shubuh=%s, waktu_dzuhur=%s, imam_dzuhur=%s, waktu_ashar=%s, imam_ashar=%s, waktu_magrib=%s, imam_magrib=%s, waktu_isya=%s, imam_isya=%s WHERE id_muadin=%s",
                    (nama_muadin, tanggal, waktu_shubuh, imam_shubuh, waktu_dzuhur, imam_dzuhur, waktu_ashar, imam_ashar, waktu_magrib, imam_magrib, waktu_isya, imam_isya, id_muadin))
        conn.commit()
        print("Data jadwal muadin berhasil diperbarui.")
    except psycopg2.Error as e:
        print("Gagal memperbarui data jadwal muadin:", e)
    finally:
        cur.close()
        conn.close()

def delete_jadwal_muadin():
    view_jadwal_muadin()
    id_muadin = int(input("Masukkan ID jadwal muadin yang ingin dihapus: "))
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM jadwal_muadin WHERE id_muadin=%s", (id_muadin,))
        conn.commit()
        print("Data jadwal muadin berhasil dihapus.")
    except psycopg2.Error as e:
        print("Gagal menghapus data jadwal muadin:", e)
    finally:
        cur.close()
        conn.close()

def view_jadwal_muadin():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM jadwal_muadin")
        rows = cur.fetchall()
        headers = ["ID", "Nama Muadzin", "Tanggal", "Waktu Shubuh", "Imam Shubuh", "Waktu Dzuhur", "Imam Dzuhur", "Waktu Ashar", "Imam Ashar", "Waktu Magrib", "Imam Magrib", "Waktu Isya", "Imam Isya"]
        print(tabulate(rows, headers, tablefmt="orgtbl"))
    except psycopg2.Error as e:
        print("Gagal membaca data jadwal muadin:", e)
    finally:
        cur.close()
        conn.close()

def login():
    loading()
    conn = connect()
    cur = conn.cursor()

    try:
        print("1. Login sebagai Founder")
        print("2. Login sebagai Takmir")
        role = input("masukan inputan: ")
        loading()

        if role == "1":
            nama_admin = input("Masukkan nama pengguna: ")
            password = input("Masukkan kata sandi: ")
            
            if nama_admin == "bos" and password == "bos":
                print("Anda login sebagai bos")
                loading()
                return "bos"
                
            else:
                print("Login gagal. Cek nama pengguna dan kata sandi Anda.")
                return None
        elif role == "2":
            nama_takmir = input("Masukkan nama takmir: ")
            password_takmir = input("Masukkan kata sandi takmir: ")
            loading()

            cur.execute("SELECT * FROM admin WHERE nama_takmir = %s AND sandi_takmir = %s", (nama_takmir, password_takmir))
            takmir = cur.fetchone()

            if takmir:
                print("Login berhasil. Selamat datang,", nama_takmir)
                return "takmir"
            else:
                print("Login gagal. Cek nama takmir dan kata sandi Anda.")
                return None
        else:
            print("Peran tidak valid. Silakan masukkan 'bos' atau 'takmir'.")
            return None
    except psycopg2.Error as e:
        print("Gagal melakukan login:", e)
    finally:
        cur.close()
        conn.close()            
        
# ======================================== TAKMIR ========================================

def main_takmir():
        print("\n===== SISTEM MANAJEMEN MASJID (TAKMIR) =====")
        print("1. Kegiatan")
        print("2. Inventaris")
        print("3. Muadzin")
        print("4. Keluar")
            
        pilihan = input("Masukkan pilihan Anda: ")
        loading()
        if pilihan == '1':
            takmir_kegiatan()
        elif pilihan == '2':
            takmir_inventaris()
        elif pilihan == '3':
            takmir_muadin()
        elif pilihan == '4':
            login()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def takmir_muadin():
    while True:
        print("\n===== Jadwal =====")
        print("1. Tambah Jadwal Muadin")
        print("2. Ubah jadwal muadin")
        print("3. Hapus jadwal muadin")
        print("4. Lihat Jadwal muadin")
        print("0. Keluar")
        
        pilihan = input("Masukan pilihan anda: ")
        loading()
        if pilihan == '1':
            add_jadwal_muadin()
        elif pilihan == '2':
            update_jadwal_muadin()
        elif pilihan == '3':
            delete_jadwal_muadin()
        elif pilihan == '4':
            view_jadwal_muadin()
        elif pilihan == '0':
            main_takmir()
        else:
            print("pilihan tidak valid")

def takmir_kegiatan():
    while True:
        print("\n===== Kegiatan =====")
        print("1. Tambah Kegiatan")
        print("2. Lihat Kegiatan")
        print("3. hapus kegiatan")
        print("4. Update Kegiatan")
        print("5. Keluar")
        pilihan = input("Masukan pilihan anda: ")
        loading()
        if pilihan == '1':
            add_kegiatan()
        elif pilihan == '2':
            view_kegiatan()
        elif pilihan == '3':
            delete_kegiatan()
        elif pilihan == '4':
            update_kegiatan()
        elif pilihan == '5':
            main_takmir
        else:
            print("pilihan tidak valid")
                
def takmir_inventaris():
    while True:
        print("\n===== Inventaris =====")
        print("1. Tambah Inventaris")
        print("2. Lihat Inventaris")
        print("3. Ubah Inventaris")
        print("4. Hapus Inventaris")
        print("5. Keluar")
        
        pilihan = input("Masukan pilihan anda: ")
        loading()
        if pilihan == '1':
            add_inventaris()
        elif pilihan == '2':
            view_inventaris()
        elif pilihan == '3':
            update_inventaris()
        elif pilihan == '4':
            delete_inventaris()
        elif pilihan == '5':
            main_takmir()
        else:
            print("pilihan tidak valid")
        
# ====================================================== Founder =================================================


def main_founder():
        print("\n===== SISTEM MANAJEMEN MASJID (TAKMIR) =====")
        print("1. Kegiatan")
        print("2. Inventaris")
        print("3. Muadzin")
        print("4. Takmir")
        print("5. Keluar")
            
        pilihan = input("Masukkan pilihan Anda: ")
        loading()
        if pilihan == '1':
            founder_kegiatan()
        elif pilihan == '2':
            founder_inventaris()
        elif pilihan == '3':
            founder_muadin()
        elif pilihan == '4':
            founder_takmir()
        elif pilihan == '5':
            print("Terima kasih! Program selesai.")
            login()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
                
def founder_muadin():
    while True:
        print("\n===== Jadwal =====")
        print("1. Tambah Jadwal muadin")
        print("2. Ubah jadwal muadin")
        print("3. Hapus jadwal muadin")
        print("4. Lihat Jadwal muadin")
        print("5. Keluar")
        
        pilihan = input("Masukan pilihan anda: ")
        loading()
        if pilihan == '1':
            add_jadwal_muadin()
        elif pilihan == '2':
            update_jadwal_muadin()
        elif pilihan == '3':
            delete_jadwal_muadin()
        elif pilihan == '4':
            view_jadwal_muadin()
        elif pilihan == '5':
            main_founder()
        else:
            print("pilihan tidak valid")

def founder_takmir():
    while True:
        print("\n===== Takmir =====")
        print("1. Tambah Takmir")
        print("2. Lihat Takmir")
        print("3. Hapus Takmir")
        print("4. Ubah Takmir")
        print("5. Keluar")
        
        pilihan = input("Masukan pilihan anda: ")
        loading()
        if pilihan == '1':
            add_admin()
        elif pilihan == '2':
            view_admin()
        elif pilihan == '3':
            delete_admin()
        elif pilihan == '4':
            update_admin()
        elif pilihan == '5':
            main_founder
        else:
            print("pilihan tidak valid")

def founder_kegiatan():
    while True:
        print("\n===== Kegiatan =====")
        print("1. Tambah Kegiatan")
        print("2. Lihat Kegiatan")
        print("3. hapus kegiatan")
        print("4. Ubah kegiatan")
        print("5. Keluar")
        
        pilihan = input("Masukan pilihan anda: ")
        loading()
        if pilihan == '1':
            add_kegiatan()
        elif pilihan == '2':
            view_kegiatan()
        elif pilihan == '3':
            delete_kegiatan()
        elif pilihan == '4':
            update_kegiatan()
        elif pilihan == '5':
            main_founder()
        else:
            print("pilihan tidak valid")
                
def founder_inventaris():
    while True:
        print("\n===== Inventaris =====")
        print("1. Tambah Inventaris")
        print("2. Lihat Inventaris")
        print("3. Ubah Inventaris")
        print("4. Hapus Inventaris")
        print("5. Keluar")
        
        pilihan = input("Masukan pilihan anda: ")
        loading()
        if pilihan == '1':
            add_inventaris()
        elif pilihan == '2':
            view_inventaris()
        elif pilihan == '3':
            update_inventaris()
        elif pilihan == '4':
            delete_inventaris()
        elif pilihan == '5':
            main_founder()
        else:
            print("pilihan tidak valid")
 
def main():
    role = login()
    if role == "bos":
        main_founder()
    elif role == "takmir":
        main_takmir()
    else:
        print("Aplikasi akan ditutup karena login gagal.")

main()